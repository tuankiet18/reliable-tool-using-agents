#!/usr/bin/env python3
"""Post-hoc analytic and counterfactual diagnostics; no new policy episodes."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

from run_main_study import PRIMARY_TOOL, SOURCE_TOPOLOGY

ROOT = Path(__file__).resolve().parents[1]
FROZEN_INPUTS = {
    "src/run_main_study.py": "387696644bd707ee63d9c9982a2628a5e93c67b2b23642bdabfdea3e54053523",
    "results_main_study/raw.jsonl": "a51aebcb207f996e7a4d065b2e424fe794346d685d5f37a615d0de6bcb872234",
    "results_secondary_varied/episodes.jsonl": "40a419491011308dcce04db477c4a98dbda2e543d2db531b0a4fb07c08b43c35",
    "results_secondary_varied/analysis-summary.json": "ba8bda32d76c79e0aaf6cb5fe0195899d871f4ad4449ddc71c7f38a50600dd4b",
    "data/secondary_schema_contract_v1.json": "552ef2c689cae93494d68c9114482d1550f5bcfa4653e9bff8902d3b19cfed1a",
    "data/secondary_varied_schedule_v1/schedule.jsonl": "f630cb0a34276c23462d838eb23113ea2e4d6c4270958b292db25d26ce725469",
}


def read_jsonl(relative: str) -> list[dict]:
    return [json.loads(line) for line in (ROOT / relative).read_text(encoding="utf-8").splitlines() if line.strip()]


def rate(numerator: int, denominator: int) -> dict:
    return {"numerator": numerator, "denominator": denominator, "rate": numerator / denominator}


def exact(value: Fraction) -> dict:
    return {"fraction": str(value), "rate": float(value)}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main_diagnostic(rows: list[dict]) -> dict:
    groups = defaultdict(dict)
    for row in rows:
        key = (row["task_id"], row["seed"], row["regime"])
        check(row["policy"] not in groups[key], "duplicate main row")
        groups[key][row["policy"]] = row
    check(len(rows) == 1350 and len(groups) == 450, "unexpected main matrix")
    for pair in groups.values():
        check(set(pair) == {"random_k", "provenance_k", "single_source"}, "incomplete main comparison")
        reference = pair["random_k"]
        for row in pair.values():
            check(row["expected_action"] == reference["expected_action"], "main oracle mismatch")
            check(row["expected_amount_eur"] == reference["expected_amount_eur"], "main amount mismatch")
            check(row["observations"][0] == reference["observations"][0], "main primary mismatch")

    corroborators = [tool for tool in SOURCE_TOPOLOGY if tool != PRIMARY_TOOL]
    shared = [tool for tool in corroborators if SOURCE_TOPOLOGY[tool] == SOURCE_TOPOLOGY[PRIMARY_TOOL]]
    targeted = [row for row in rows if row["regime"] == "targeted_common_mode" and row["policy"] == "random_k"]
    check(len(targeted) == 150, "unexpected main targeted rows")
    for row in targeted:
        primary = row["observations"][0]
        check(primary["corrupted"] and primary["eligible"] == (row["expected_action"] == "escalate"), "targeted flip assumption fails")
    pi = Fraction(sum(row["expected_action"] == "escalate" for row in targeted), len(targeted))
    q = Fraction(len(shared), len(corroborators))
    observed = {}
    counterfactual = {}
    losses = {}
    for regime in ("clean", "independent", "targeted_common_mode"):
        reference = [row for row in rows if row["regime"] == regime and row["policy"] == "random_k"]
        n = len(reference)
        eligible_n = sum(row["expected_action"] == "refund" for row in reference)
        counterfactual[regime] = {
            "unsafe_decisions": rate(0, n),
            "action_oracle_correctness": rate(n - eligible_n, n),
            "correct_expected_refund_decisions": rate(0, eligible_n),
            "missed_authorized_refunds": rate(eligible_n, n),
            "budget_status": "COUNTERFACTUAL; not a matched-K=2 measured policy",
        }
        observed[regime] = {}
        for policy in ("random_k", "provenance_k", "single_source"):
            subset = [row for row in rows if row["regime"] == regime and row["policy"] == policy]
            observed[regime][policy] = {
                "unsafe_decisions": rate(sum(row["unsafe_refund"] for row in subset), len(subset)),
                "action_oracle_correctness": rate(sum(row["final_state_correct"] for row in subset), len(subset)),
                "correct_expected_refund_decisions": rate(sum(row["expected_action"] == "refund" and row["final_state_correct"] for row in subset), eligible_n),
                "missed_authorized_refunds": rate(sum(row["false_block"] for row in subset), len(subset)),
            }
        losses[regime] = {}
        for penalty in (Fraction(1, 10), Fraction(1, 4), Fraction(1, 2)):
            losses[regime][str(penalty)] = {
                policy: metrics["unsafe_decisions"]["rate"] + float(penalty) * metrics["missed_authorized_refunds"]["rate"]
                for policy, metrics in {**observed[regime], "always_escalate_counterfactual": counterfactual[regime]}.items()
            }
    thresholds = {}
    for policy in ("random_k", "provenance_k"):
        metrics = observed["independent"][policy]
        missed = metrics["missed_authorized_refunds"]["numerator"]
        always_missed = counterfactual["independent"]["missed_authorized_refunds"]["numerator"]
        thresholds[policy] = exact(Fraction(metrics["unsafe_decisions"]["numerator"], always_missed - missed))
    return {
        "uniform_selector_model": {
            "canonical_escalation_fraction_pi": exact(pi),
            "random_same_domain_probability_q": exact(q),
            "random_expected_unsafe_decision_rate_pi_q": exact(pi * q),
            "provenance_expected_unsafe_decision_rate": exact(Fraction(0)),
            "random_expected_action_correctness": exact(pi * (1 - q)),
            "provenance_expected_action_correctness": exact(pi),
            "expected_refund_correctness_under_targeted_fault": exact(Fraction(0)),
            "scope": "Expectation over uniform corroborator choice; observed fixed seeds are a finite realization. Independent corroborators retain truth in this targeted model.",
        },
        "observed_main": observed,
        "always_escalate_counterfactual": counterfactual,
        "posthoc_loss_sensitivity": {
            "definition": "unsafe decision rate + lambda * missed authorized refund rate; no human/call/latency cost measured",
            "point_values": losses,
            "independent_break_even_lambda": thresholds,
            "interpretation": "Observed policy has lower proxy loss than always escalation only above its break-even lambda; no CI or real cost justification.",
        },
    }


def secondary_diagnostic(rows: list[dict], schedule: list[dict], contract: dict, old_summary: dict) -> dict:
    cases = {case["id"]: case for case in contract["cases"]}
    safety = {case_id for case_id, case in cases.items() if case["eligibility"] == "SAFETY_CURRENT"}
    utility = {case_id for case_id, case in cases.items() if case["eligibility"] == "UTILITY_ONLY"}
    check(len(safety) == 8 and len(utility) == 2 and len(rows) == 1056, "unexpected secondary cohort")
    grouped = defaultdict(dict)
    for row in rows:
        key = (row["case_id"], row["seed"], row["regime"])
        check(row["policy"] not in grouped[key], "duplicate secondary row")
        grouped[key][row["policy"]] = row
    check(len(grouped) == 528, "unexpected secondary pairs")
    for pair in grouped.values():
        check(set(pair) == {"random_k", "provenance_k"}, "incomplete secondary pair")
        for field in ("proposed_action_typed", "faulted_sources", "p_claim"):
            check(pair["random_k"][field] == pair["provenance_k"][field], "secondary proposal/fault mismatch")

    normalized = {}
    comparisons = {}
    for regime in sorted({row["regime"] for row in rows}):
        unique = [pair["random_k"] for key, pair in grouped.items() if key[2] == regime]
        clean = [row for row in unique if row["proposed_action_typed"] == cases[row["case_id"]]["clean_action_typed"]]
        wrong_safety = [row for row in unique if row["case_id"] in safety and row not in clean]
        utility_clean = [row for row in clean if row["case_id"] in utility]
        pooled = old_summary["always_block_diagnostic"][regime]
        check(pooled["clean_proposals_blocked_false_block"] == 2 * len(clean), "pooled clean diagnostic mismatch")
        check(pooled["utility_only_false_blocks"] == 2 * len(utility_clean), "pooled utility diagnostic mismatch")
        check(pooled["wrong_safety_proposals_blocked"] == 2 * len(wrong_safety), "pooled safety diagnostic mismatch")
        normalized[regime] = {
            "unique_scenario_keys": len(unique),
            "clean_proposals_blocked": rate(len(clean), len(clean)),
            "wrong_safety_proposals_blocked": len(wrong_safety),
            "utility_false_blocks": rate(len(utility_clean), sum(row["case_id"] in utility for row in unique)),
            "safety_unsafe_accepted": rate(0, sum(row["case_id"] in safety for row in unique)),
            "note": "Deduplicated (case_id, seed, regime), excluding WB-295 from safety/utility denominators. Counterfactual always-block; no new episodes or measured matched budget.",
        }
        comparisons[regime] = {
            policy: old_summary["regime_metrics"][regime][policy]
            for policy in ("random_k", "provenance_k")
        }
    reconstruction = []
    for case_id in sorted(safety):
        sub = [row for row in schedule if row["case_id"] == case_id and row["regime"] == "targeted_common_mode_25"]
        s_seeds = {row["seed"] for row in sub if row["policy"] == "random_k" and row["selected_corroborator"] == "S"}
        leaked = {row["seed"] for row in sub if "I" in row["faulted_sources"]}
        overlap = len(s_seeds & leaked)
        check(len(s_seeds) == 6 and len(leaked) == 3, "secondary quota mismatch")
        predicted = {"random_k": 9 - overlap, "provenance_k": 3}
        for policy, count in predicted.items():
            actual = sum(row["unsafe_wrong_action_accepted"] for row in rows if row["case_id"] == case_id and row["regime"] == "targeted_common_mode_25" and row["policy"] == policy)
            check(actual == count, f"schedule reconstruction mismatch for {case_id}/{policy}")
        reconstruction.append({"case_id": case_id, "overlap_r": overlap, "unsafe_counts_reconstructed": predicted, "difference": exact(Fraction(overlap - 6, 12))})
    return {"always_block_normalized": normalized, "observed_policy_metrics": comparisons, "targeted_schedule_reconstruction": reconstruction}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "results_topology_diagnostics_20261003" / "analysis.json")
    args = parser.parse_args()
    for relative, expected in FROZEN_INPUTS.items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        check(actual == expected, f"frozen source hash mismatch: {relative}")
    main_rows = read_jsonl("results_main_study/raw.jsonl")
    secondary_rows = read_jsonl("results_secondary_varied/episodes.jsonl")
    schedule = read_jsonl("data/secondary_varied_schedule_v1/schedule.jsonl")
    contract = json.loads((ROOT / "data/secondary_schema_contract_v1.json").read_text(encoding="utf-8"))
    old_summary = json.loads((ROOT / "results_secondary_varied/analysis-summary.json").read_text(encoding="utf-8"))
    result = {
        "status": "POST_HOC_ANALYTICAL_COUNTERFACTUAL_DIAGNOSTIC_ONLY",
        "new_episodes": 0,
        "inputs_sha256": FROZEN_INPUTS,
        "main": main_diagnostic(main_rows),
        "secondary": secondary_diagnostic(secondary_rows, schedule, contract, old_summary),
        "scope": "No new experiment, CI, causal effect estimate, policy execution or live-agent validation. Formulas explain the frozen model; counterfactuals use its existing oracles and proposals.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": result["status"], "output": str(args.output), "source_hashes_verified": len(FROZEN_INPUTS), "secondary_cases_reconstructed": 8, "new_episodes": 0}))


if __name__ == "__main__":
    main()
