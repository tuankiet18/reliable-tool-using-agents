#!/usr/bin/env python3
"""Freeze a case-specific varied schedule before the secondary runtime replication."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "data" / "secondary_schema_contract_v1.json"
SEEDS = [1901, 1993, 2017, 2081, 2143, 2213, 2281, 2347, 2411, 2477, 2551, 2617]
REGIMES = ["clean", "independent_single_source", "targeted_common_mode_0", "targeted_common_mode_25"]
POLICIES = ["random_k", "provenance_k"]
SCHEDULE_VERSION = "secondary-varied-v1"


def digest(case_id: str, seed: int, purpose: str) -> str:
    key = f"{SCHEDULE_VERSION}|{case_id}|{seed}|{purpose}".encode("utf-8")
    return hashlib.sha256(key).hexdigest()


def ranked_seeds(case_id: str, purpose: str) -> list[int]:
    return sorted(SEEDS, key=lambda seed: (digest(case_id, seed, purpose), seed))


def hash_rows(rows: list[dict[str, Any]]) -> str:
    encoded = "\n".join(
        json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        for row in rows
    ) + "\n"
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def varied_matrix(contract: dict[str, Any]) -> list[dict[str, Any]]:
    shared = contract["shared_contract"]
    if shared["policies"] != POLICIES:
        raise ValueError(f"unexpected policies: {shared['policies']}")
    cases = [case for case in contract["cases"] if case["matrix_regimes"] == "ALL"]
    rows: list[dict[str, Any]] = []

    for case in cases:
        case_id = case["id"]
        selector_s = set(ranked_seeds(case_id, "selector")[:6])
        leakage_seeds = set(ranked_seeds(case_id, "leakage")[:3])
        ranked_faults = ranked_seeds(case_id, "single_fault")
        independent_faults = {
            seed: ("P" if index < 4 else "S" if index < 8 else "I")
            for index, seed in enumerate(ranked_faults)
        }
        p_ref = case["shared_context"]["fairness_invariant"]["p_observation_ref"] if "shared_context" in case else f"{case_id.lower()}_primary_obs"
        ctx_ref = case["shared_context"]["fairness_invariant"]["shared_context_ref"] if "shared_context" in case else None
        p_hash = case["shared_context"]["p_observation_sha256"] if "shared_context" in case else None
        ctx_hash = case["shared_context"]["shared_context_sha256"] if "shared_context" in case else None

        for seed in SEEDS:
            for regime in REGIMES:
                if regime == "clean":
                    faults: list[str] = []
                elif regime == "independent_single_source":
                    faults = [independent_faults[seed]]
                elif regime == "targeted_common_mode_0":
                    faults = ["P", "S"]
                elif regime == "targeted_common_mode_25":
                    faults = ["P", "S", "I"] if seed in leakage_seeds else ["P", "S"]
                else:  # pragma: no cover - regime list is frozen above
                    raise ValueError(f"unexpected regime: {regime}")

                proposal_is_clean = case["eligibility"] == "UTILITY_ONLY" or "P" not in faults
                proposal = case["clean_action"] if proposal_is_clean else case["fault_action"]
                proposal_typed = case["clean_action_typed"] if proposal_is_clean else case["fault_action_typed"]
                for policy in POLICIES:
                    selected = "S" if policy == "random_k" and seed in selector_s else "I"
                    rows.append({
                        "case_id": case_id,
                        "seed": seed,
                        "regime": regime,
                        "policy": policy,
                        "faulted_sources": faults,
                        "selected_corroborator": selected,
                        "proposed_action": proposal,
                        "proposed_action_typed": proposal_typed,
                        "p_observation_ref": p_ref,
                        "shared_context_ref": ctx_ref,
                        "p_observation_sha256": p_hash,
                        "shared_context_sha256": ctx_hash,
                        "eligibility": case["eligibility"],
                        "schedule_version": SCHEDULE_VERSION,
                        "selector_digest": digest(case_id, seed, "selector"),
                        "leakage_digest": digest(case_id, seed, "leakage"),
                        "single_fault_digest": digest(case_id, seed, "single_fault"),
                    })
    return rows


def validate_schedule(rows: list[dict[str, Any]], cases: list[dict[str, Any]]) -> dict[str, Any]:
    runnable = [case for case in cases if case["matrix_regimes"] == "ALL"]
    expected_rows = len(runnable) * len(SEEDS) * len(REGIMES) * len(POLICIES)
    if len(runnable) != 11 or expected_rows != 1056 or len(rows) != expected_rows:
        raise ValueError(f"unexpected matrix size: runnable={len(runnable)}, rows={len(rows)}")

    per_case: dict[str, Any] = {}
    signatures = set()
    grouped: dict[tuple[str, int, str], list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault((row["case_id"], row["seed"], row["regime"]), []).append(row)
    if len(grouped) != 528:
        raise ValueError(f"expected 528 pairs, got {len(grouped)}")

    for case in runnable:
        case_id = case["id"]
        # The source choice is read from the random policy rows, not inferred from outcomes.
        random_rows = [row for row in rows if row["case_id"] == case_id and row["regime"] == "clean" and row["policy"] == "random_k"]
        selector_s = sorted(row["seed"] for row in random_rows if row["selected_corroborator"] == "S")
        leak_rows = [row for row in rows if row["case_id"] == case_id and row["regime"] == "targeted_common_mode_25" and row["seed"] in SEEDS]
        leakage_seeds = sorted(row["seed"] for row in leak_rows if row["policy"] == "provenance_k" and row["faulted_sources"] == ["P", "S", "I"])
        independent = [row for row in rows if row["case_id"] == case_id and row["regime"] == "independent_single_source" and row["policy"] == "provenance_k"]
        fault_counts = {source: sum(row["faulted_sources"] == [source] for row in independent) for source in ("P", "S", "I")}
        if len(selector_s) != 6 or len(leakage_seeds) != 3 or fault_counts != {"P": 4, "S": 4, "I": 4}:
            raise ValueError(f"schedule balance failed for {case_id}: selector={len(selector_s)}, leakage={len(leakage_seeds)}, independent={fault_counts}")
        signatures.add((tuple(selector_s), tuple(leakage_seeds), tuple(row["faulted_sources"][0] for row in independent)))
        per_case[case_id] = {
            "random_k_same_domain_seeds": selector_s,
            "independent_leakage_seeds": leakage_seeds,
            "independent_fault_counts": fault_counts,
            "selector_leakage_overlap": sorted(set(selector_s) & set(leakage_seeds)),
        }

    if len(signatures) < 2:
        raise ValueError("schedule signatures do not vary across cases")

    for key, pair in grouped.items():
        if len(pair) != 2 or {row["policy"] for row in pair} != set(POLICIES):
            raise ValueError(f"incomplete pair: {key}")
        for field in ("faulted_sources", "proposed_action_typed", "p_observation_ref", "p_observation_sha256", "shared_context_ref", "shared_context_sha256", "eligibility"):
            if pair[0][field] != pair[1][field]:
                raise ValueError(f"paired mismatch for {field}: {key}")
        provenance = next(row for row in pair if row["policy"] == "provenance_k")
        random = next(row for row in pair if row["policy"] == "random_k")
        if provenance["selected_corroborator"] != "I":
            raise ValueError(f"provenance selector did not choose I: {key}")
        if random["selected_corroborator"] not in {"S", "I"}:
            raise ValueError(f"random selector invalid: {key}")

    return {
        "runnable_cases": len(runnable),
        "rows": len(rows),
        "pairs": len(grouped),
        "distinct_case_schedule_signatures": len(signatures),
        "per_case_schedule": per_case,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=CONTRACT_PATH)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "data" / "secondary_varied_schedule_v1")
    args = parser.parse_args()

    contract_bytes = args.contract.read_bytes()
    contract = json.loads(contract_bytes)
    if contract["contract_version"] != "1.2-recheck-candidate":
        raise SystemExit("Unexpected contract version; refusing schedule generation.")
    rows = varied_matrix(contract)
    validation = validate_schedule(rows, contract["cases"])
    rows_path = args.out_dir / "schedule.jsonl"
    manifest_path = args.out_dir / "manifest.json"
    if rows_path.exists() or manifest_path.exists():
        raise SystemExit(f"Refusing to overwrite existing frozen schedule at {args.out_dir}")
    args.out_dir.mkdir(parents=True, exist_ok=False)
    rows_bytes = ("\n".join(json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False) for row in rows) + "\n").encode("utf-8")
    rows_path.write_bytes(rows_bytes)
    manifest = {
        "status": "FROZEN_BEFORE_RUNTIME",
        "schedule_version": SCHEDULE_VERSION,
        "contract_version": contract["contract_version"],
        "contract_sha256": hashlib.sha256(contract_bytes).hexdigest(),
        "schedule_sha256": hashlib.sha256(rows_bytes).hexdigest(),
        "algorithm_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "seed_list": SEEDS,
        "regimes": REGIMES,
        "policies": POLICIES,
        "validation": validation,
        "policy_outcome_accessed_during_schedule_generation": False,
        "run_status": "NOT_RUN",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
