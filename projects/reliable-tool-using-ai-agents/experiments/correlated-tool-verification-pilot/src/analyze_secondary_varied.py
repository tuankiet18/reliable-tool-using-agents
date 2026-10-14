#!/usr/bin/env python3
"""Analyze the varied-schedule matrix descriptively at the case level."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROWS = ROOT / "results_secondary_varied" / "episodes.jsonl"
DEFAULT_CONTRACT = ROOT / "data" / "secondary_schema_contract_v1.json"
DEFAULT_SCHEDULE = ROOT / "data" / "secondary_varied_schedule_v1" / "schedule.jsonl"
SAFETY_CASES = {
    "WB-000", "WB-110", "WB-203", "WB-433",
    "ASB-085", "ASB-087", "ASB-090", "ASB-977",
}
POLICIES = ("random_k", "provenance_k")
REGIMES = ("clean", "independent_single_source", "targeted_common_mode_0", "targeted_common_mode_25")
ANALYSIS_SEED = 20260928


def mean_case_cluster_bootstrap(differences: list[float], n_boot: int = 10_000) -> dict[str, Any]:
    rng = random.Random(ANALYSIS_SEED)
    means = sorted(statistics.mean(rng.choices(differences, k=len(differences))) for _ in range(n_boot))
    return {
        "point_estimate": statistics.mean(differences),
        "percentile_95_ci": [means[int(0.025 * n_boot)], means[int(0.975 * n_boot) - 1]],
        "bootstrap_replicates": n_boot,
        "analysis_seed": ANALYSIS_SEED,
        "resampling_unit": "case (8 purposively selected cases)",
    }


def rate(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
    numerator = sum(bool(row[field]) for row in rows)
    return {"numerator": numerator, "denominator": len(rows), "rate": numerator / len(rows) if rows else None}


def analyze(rows: list[dict[str, Any]], contract: dict[str, Any], schedule: list[dict[str, Any]]) -> dict[str, Any]:
    cases = {case["id"]: case for case in contract["cases"]}
    expected_case_ids = {case["id"] for case in contract["cases"] if case["matrix_regimes"] == "ALL"}
    if len(rows) != 1056 or {row["case_id"] for row in rows} != expected_case_ids:
        raise ValueError("expected the frozen 1056-row / 11-case matrix")
    grouped: dict[tuple[str, int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["case_id"], row["seed"], row["regime"])].append(row)
    if len(grouped) != 528 or any(len(pair) != 2 for pair in grouped.values()):
        raise ValueError("matrix has incomplete matched policy pairs")

    summary: dict[str, Any] = {
        "status": "EXPLORATORY_INTERNAL_REPLICATION_DESCRIPTIVE_ONLY",
        "rows": len(rows), "matched_pairs": len(grouped),
        "analysis_unit": "case; seeds are repeated schedule positions, not independent tasks",
        "safety_cases": sorted(SAFETY_CASES),
        "utility_only_cases": ["WB-403", "ASB-1572"],
        "restoration_diagnostic_case": "WB-295",
        "regime_metrics": {},
        "targeted_common_mode_25_by_safety_case": [],
        "primary_exploratory_comparison": {},
        "selector_leakage_overlap": [],
        "always_block_diagnostic": {},
        "execution_errors": 0,
        "interpretation_guardrails": [
            "This is a project-defined benchmark-derived adaptation, not native benchmark reproduction or external validation.",
            "The eight safety cases were purposively selected; the case-cluster bootstrap does not justify broad population claims.",
            "A blocked wrong action is not task completion; report safety and utility separately.",
            "No human case-level review was performed; the candidate contract and project-defined source topology remain limitations.",
        ],
    }

    for regime in REGIMES:
        summary["regime_metrics"][regime] = {}
        for policy in POLICIES:
            subset = [row for row in rows if row["regime"] == regime and row["policy"] == policy]
            safe = [row for row in subset if row["case_id"] in SAFETY_CASES]
            utility = [row for row in subset if cases[row["case_id"]]["eligibility"] == "UTILITY_ONLY"]
            restoration = [row for row in subset if row["case_id"] == "WB-295"]
            summary["regime_metrics"][regime][policy] = {
                "safety_unsafe_accepted": rate(safe, "unsafe_wrong_action_accepted"),
                "safety_false_blocks": rate(safe, "false_block"),
                "safety_task_success": rate(safe, "task_success"),
                "utility_only_task_success": rate(utility, "task_success"),
                "utility_only_false_blocks": rate(utility, "false_block"),
                "restoration_diagnostic_wrong_actions_accepted": rate(restoration, "unsafe_wrong_action_accepted"),
                "all_rows_task_success": rate(subset, "task_success"),
                "mean_decisive_calls_per_row": statistics.mean(row["decisive_call_count"] for row in subset),
                "mean_total_calls_per_row": statistics.mean(row["total_call_count"] for row in subset),
                "rows": len(subset),
            }

    case_diffs: list[float] = []
    for case_id in sorted(SAFETY_CASES):
        case_rows = [row for row in rows if row["case_id"] == case_id and row["regime"] == "targeted_common_mode_25"]
        per_policy = {}
        for policy in POLICIES:
            selected = [row for row in case_rows if row["policy"] == policy]
            per_policy[policy] = rate(selected, "unsafe_wrong_action_accepted")
        difference = per_policy["provenance_k"]["rate"] - per_policy["random_k"]["rate"]
        case_diffs.append(difference)
        summary["targeted_common_mode_25_by_safety_case"].append({
            "case_id": case_id,
            "domain": cases[case_id]["analysis_domain"],
            "random_k_unsafe": per_policy["random_k"],
            "provenance_k_unsafe": per_policy["provenance_k"],
            "difference_provenance_minus_random": difference,
        })

    loo_means = [statistics.mean(case_diffs[:i] + case_diffs[i + 1:]) for i in range(len(case_diffs))]
    ci = mean_case_cluster_bootstrap(case_diffs)
    summary["primary_exploratory_comparison"] = {
        "regime": "targeted_common_mode_25",
        "estimand": "unweighted mean across eight purposively selected cases of provenance_k minus random_k unsafe-accepted-action rate",
        "mean_difference": statistics.mean(case_diffs),
        "median_difference": statistics.median(case_diffs),
        "case_differences": case_diffs,
        "improved_cases": sum(value < 0 for value in case_diffs),
        "unchanged_cases": sum(value == 0 for value in case_diffs),
        "worsened_cases": sum(value > 0 for value in case_diffs),
        "leave_one_case_out_mean_range": [min(loo_means), max(loo_means)],
        "case_cluster_bootstrap": ci,
        "ci_is_degenerate": ci["percentile_95_ci"][0] == ci["percentile_95_ci"][1],
        "interpretation": "Descriptive schedule-sensitivity result only; seeds are not independent tasks and purposive case clustering limits inference.",
    }

    safety_schedule_ids = SAFETY_CASES
    for case_id in sorted(safety_schedule_ids):
        sub = [row for row in schedule if row["case_id"] == case_id and row["regime"] == "targeted_common_mode_25"]
        leakage = {row["seed"] for row in sub if row["faulted_sources"] == ["P", "S", "I"]}
        random_same_domain = {row["seed"] for row in sub if row["policy"] == "random_k" and row["selected_corroborator"] == "S"}
        summary["selector_leakage_overlap"].append({
            "case_id": case_id,
            "random_k_selects_S": len(random_same_domain),
            "I_leakage": len(leakage),
            "overlap_S_and_I_leakage": len(random_same_domain & leakage),
            "random_k_selects_I_while_I_leaks": len(leakage - random_same_domain),
        })

    # Always-block is a diagnostic outside the matched K=2 policy comparison.
    for regime in REGIMES:
        subset = [row for row in rows if row["regime"] == regime]
        clean_proposals = [row for row in subset if row["proposed_action_typed"] == cases[row["case_id"]]["clean_action_typed"]]
        unsafe_proposals = [row for row in subset if row["proposed_action_typed"] != cases[row["case_id"]]["clean_action_typed"] and row["case_id"] in SAFETY_CASES]
        summary["always_block_diagnostic"][regime] = {
            "unsafe_actions_executed": 0,
            "clean_proposals_blocked_false_block": len(clean_proposals),
            "clean_proposal_denominator": len(clean_proposals),
            "utility_only_false_blocks": sum(row["case_id"] in {"WB-403", "ASB-1572"} for row in clean_proposals),
            "wrong_safety_proposals_blocked": len(unsafe_proposals),
            "note": "Diagnostic only; not a matched-K=2 policy and not included in the primary effect.",
        }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--schedule", type=Path, default=DEFAULT_SCHEDULE)
    parser.add_argument("--out", type=Path, default=ROOT / "results_secondary_varied" / "analysis-summary.json")
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.rows.read_text(encoding="utf-8").splitlines() if line.strip()]
    schedule = [json.loads(line) for line in args.schedule.read_text(encoding="utf-8").splitlines() if line.strip()]
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    result = analyze(rows, contract, schedule)
    result["rows_sha256"] = hashlib.sha256(args.rows.read_bytes()).hexdigest()
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
