#!/usr/bin/env python3
"""Run the frozen, case-varied exploratory secondary matrix offline."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import generate_secondary_varied_schedule as schedule_builder
import run_secondary_matrix as executor
from validate_secondary_schema_contract import (
    candidate_matrix,
    native_primary,
    read_csv,
    records,
    require,
    validate_field_types,
    validate_source_materialization,
    verify_commit,
    verify_hash,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "data" / "secondary_schema_contract_v1.json"
SCHEDULE_DIR = ROOT / "data" / "secondary_varied_schedule_v1"
DEFAULT_OUT = ROOT / "results_secondary_varied"
OLD_RAW = ROOT / "results_secondary_matrix" / "episodes.jsonl"
SAFETY_CASES = {
    "WB-000", "WB-110", "WB-203", "WB-433",
    "ASB-085", "ASB-087", "ASB-090", "ASB-977",
}


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_and_validate_inputs(pg: Path, wb: Path) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    contract_bytes = CONTRACT_PATH.read_bytes()
    contract = json.loads(contract_bytes)
    schedule_path = SCHEDULE_DIR / "schedule.jsonl"
    manifest_path = SCHEDULE_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["status"] == "FROZEN_BEFORE_RUNTIME", "schedule is not prospectively frozen")
    require(manifest["run_status"] == "NOT_RUN", "schedule manifest already records a runtime")
    require(manifest["contract_sha256"] == file_hash(CONTRACT_PATH), "contract changed since schedule freeze")
    require(manifest["algorithm_sha256"] == file_hash(Path(schedule_builder.__file__)), "schedule generator changed since freeze")
    require(manifest["schedule_sha256"] == file_hash(schedule_path), "schedule file hash differs from frozen manifest")
    rows = [json.loads(line) for line in schedule_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    regenerated = schedule_builder.varied_matrix(contract)
    require(rows == regenerated, "stored schedule differs from deterministic regeneration")
    validation = schedule_builder.validate_schedule(rows, contract["cases"])
    require(validation == manifest["validation"], "schedule validation differs from frozen manifest")

    verify_commit(pg, contract["provenanceguard_commit"])
    verify_commit(wb, contract["workbench_historical_commit"])
    for relative, expected in contract["source_hashes"].items():
        base = pg if relative.startswith(("data/workbench/", "data/agent_safetybench/")) else wb
        verify_hash(base / relative, expected)

    old_hash = file_hash(OLD_RAW)
    return contract, rows, {"manifest": manifest, "schedule_path": schedule_path, "old_matrix_sha256_before": old_hash}


def validate_runtime_rows(rows: list[dict[str, Any]], plan: list[dict[str, Any]], contract: dict[str, Any]) -> None:
    require(len(rows) == len(plan) == 1056, f"expected 1056 rows, got runtime={len(rows)} schedule={len(plan)}")
    identity_fields = tuple(plan[0])
    require([{key: row.get(key) for key in identity_fields} for row in rows] == plan,
            "runtime row order/identity differs from frozen schedule")
    policies = set(contract["shared_contract"]["policies"])
    grouped: dict[tuple[str, int, str], list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault((row["case_id"], row["seed"], row["regime"]), []).append(row)
        require(row["decisive_call_count"] == 2, "decisive call budget is not K=2")
        require(row["action_executed"] == (row["decision"] == "ALLOW"), "execution does not match gate decision")
        require(row["oracle_assertions_passed"] is True or row["decision"] == "BLOCK",
                "an executed action lacks a passing post-state oracle")
        visible = json.dumps(row["policy_visible_observations"], sort_keys=True)
        forbidden = ("source_id", "failure_domain_id", "oracle_only", "ground_truth", "faulted_sources")
        require(not any(token in visible for token in forbidden), "policy-visible payload leaks evaluator metadata")

    require(len(grouped) == 528, f"expected 528 matched pairs, got {len(grouped)}")
    for key, pair in grouped.items():
        require(len(pair) == 2 and {row["policy"] for row in pair} == policies, f"incomplete policy pair: {key}")
        for field in (
            "faulted_sources", "materialized_p_observation_sha256", "proposed_action_typed",
            "shared_context_sha256", "shared_context_call_count", "total_call_count",
        ):
            require(pair[0][field] == pair[1][field], f"paired invariant mismatch {field}: {key}")
        if key[0] == "WB-433":
            require(pair[0]["shared_context_call_count"] == pair[1]["shared_context_call_count"] == 1,
                    "WB-433 shared context call count differs")
            require(pair[0]["total_call_count"] == pair[1]["total_call_count"] == 3,
                    "WB-433 total call count differs")
            require(pair[0]["shared_context_sha256"] == pair[1]["shared_context_sha256"],
                    "WB-433 shared context differs")
        if key[2] != "clean":
            expected_action = pair[0]["proposed_action_typed"]
            require(expected_action == pair[1]["proposed_action_typed"], f"paired action differs: {key}")

    expected_safety = 12 * 4 * 2 * len(SAFETY_CASES)
    require(sum(row["case_id"] in SAFETY_CASES for row in rows) == expected_safety,
            "safety cohort row count differs")


def prepare_runtime(contract: dict[str, Any], pg: Path, wb: Path, plan: list[dict[str, Any]]) -> list[dict[str, Any]]:
    wb_rows = executor.load_workbench_rows(wb)
    traces = {
        "WorkBench": {c["id"]: executor.load_trace(pg / "data/workbench/traces.json", c["trace_id"])
                      for c in contract["cases"] if c["benchmark"] == "WorkBench"},
        "Agent-SafetyBench": {c["id"]: executor.load_trace(pg / "data/agent_safetybench/traces.json", c["trace_id"])
                              for c in contract["cases"] if c["benchmark"] == "Agent-SafetyBench"},
    }
    prepared: dict[str, tuple[object, object, dict[str, Any]]] = {}
    for case in contract["cases"]:
        if case["matrix_regimes"] != "ALL":
            continue
        trace = traces[case["benchmark"]][case["id"]]
        clean = native_primary(case, trace, wb_rows)
        if isinstance(clean, (list, dict)):
            validate_field_types(case["id"], records(case["id"], clean), case["field_schema"])
        faulty = executor.mutate(case["id"], clean, wb_rows)
        validate_source_materialization(case, clean, faulty)
        prepared[case["id"]] = (clean, faulty, trace)

    cases = {case["id"]: case for case in contract["cases"]}
    runtime_rows = []
    for planned in plan:
        case = cases[planned["case_id"]]
        clean, faulty, trace = prepared[case["id"]]
        runtime_rows.append(executor.run_row(planned, case, clean, faulty, wb_rows, pg, trace))
    validate_runtime_rows(runtime_rows, plan, contract)
    return runtime_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provenanceguard", type=Path, required=True)
    parser.add_argument("--workbench", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    contract, plan, metadata = load_and_validate_inputs(args.provenanceguard, args.workbench)
    if args.plan_only:
        print(json.dumps({
            "status": "PLAN_VALIDATED_NOT_RUN",
            "rows": len(plan), "pairs": len(plan) // 2,
            "schedule_sha256": metadata["manifest"]["schedule_sha256"],
            "contract_status": "candidate contract; exploratory internal adaptation only",
            "old_matrix_sha256_before": metadata["old_matrix_sha256_before"],
        }, indent=2, ensure_ascii=False))
        return

    require(not args.out_dir.exists(), f"refusing to overwrite output directory: {args.out_dir}")
    runtime_rows = prepare_runtime(contract, args.provenanceguard, args.workbench, plan)
    args.out_dir.mkdir(parents=True, exist_ok=False)
    rows_path = args.out_dir / "episodes.jsonl"
    rows_path.write_text("".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in runtime_rows), encoding="utf-8")
    summary = {
        "status": "EXPLORATORY_INTERNAL_REPLICATION_COMPLETE",
        "interpretation": "benchmark-derived adaptation; not confirmatory evidence, native benchmark reproduction, or external validation",
        "contract_version": contract["contract_version"],
        "contract_sha256": file_hash(CONTRACT_PATH),
        "schedule_sha256": metadata["manifest"]["schedule_sha256"],
        "schedule_manifest_sha256": file_hash(SCHEDULE_DIR / "manifest.json"),
        "upstream_commits": {
            "provenanceguard": contract["provenanceguard_commit"],
            "workbench": contract["workbench_historical_commit"],
        },
        "episodes": len(runtime_rows), "matched_pairs": len(runtime_rows) // 2,
        "safety_cases": sorted(SAFETY_CASES), "safety_case_count": len(SAFETY_CASES),
        "utility_only_cases": ["WB-403", "ASB-1572"],
        "restoration_diagnostic": "WB-295", "excluded_invalid_not_run": "ASB-267",
        "rows_path": str(rows_path), "rows_sha256": file_hash(rows_path),
        "old_matrix_sha256_before": metadata["old_matrix_sha256_before"],
        "old_matrix_sha256_after": file_hash(OLD_RAW),
        "offline_no_llm_or_api": True, "gpu_required": False,
    }
    require(summary["old_matrix_sha256_before"] == summary["old_matrix_sha256_after"],
            "old secondary matrix changed during varied run")
    (args.out_dir / "run-summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
