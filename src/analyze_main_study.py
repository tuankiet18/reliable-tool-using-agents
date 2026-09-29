#!/usr/bin/env python3
"""Analyze the preregistered deterministic main study without changing its decision rule."""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
N_BOOTSTRAP = 10_000
LAMBDAS = (0.10, 0.25, 0.50)


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    weight = position - low
    return ordered[low] * (1 - weight) + ordered[high] * weight


def paired_bootstrap(
    rows: list[dict[str, Any]],
    regime: str,
    treatment: str,
    control: str,
    metric_name: str,
    metric: Callable[[dict[str, Any]], float],
) -> dict[str, Any]:
    selected = [
        row
        for row in rows
        if row["regime"] == regime and row["policy"] in {treatment, control}
    ]
    pairs: dict[tuple[str, int], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in selected:
        pairs[(row["task_id"], row["seed"])][row["policy"]] = row
    tasks = sorted({task_id for task_id, _ in pairs})
    if any(set(pair) != {treatment, control} for pair in pairs.values()):
        raise ValueError(f"incomplete paired cells for {regime}/{metric_name}")
    task_differences = {
        task_id: mean(
            [
                metric(pair[treatment]) - metric(pair[control])
                for (paired_task, _), pair in pairs.items()
                if paired_task == task_id
            ]
        )
        for task_id in tasks
    }
    estimate = mean(list(task_differences.values()))
    rng = random.Random(
        20260915 + sum(map(ord, regime + treatment + control + metric_name))
    )
    samples = [
        mean([task_differences[rng.choice(tasks)] for _ in tasks])
        for _ in range(N_BOOTSTRAP)
    ]
    return {
        "regime": regime,
        "treatment": treatment,
        "control": control,
        "metric": metric_name,
        "difference": estimate,
        "ci95": [quantile(samples, 0.025), quantile(samples, 0.975)],
        "task_clusters": len(tasks),
        "bootstrap_resamples": N_BOOTSTRAP,
    }


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["regime"], row["policy"])].append(row)
    output = []
    for (regime, policy), group in sorted(groups.items()):
        attempts = [row for row in group if row["refund_attempted"]]
        output.append(
            {
                "regime": regime,
                "policy": policy,
                "episodes": len(group),
                "task_success_rate": mean([float(row["final_state_correct"]) for row in group]),
                "unsafe_refund_rate": mean([float(row["unsafe_refund"]) for row in group]),
                "false_block_rate": mean([float(row["false_block"]) for row in group]),
                "refund_attempt_rate": mean([float(row["refund_attempted"]) for row in group]),
                "conflict_rate": mean([float(row["conflict"]) for row in group]),
                "boundary_attempt_coverage": (
                    sum(row["boundary_check_count"] for row in attempts) / len(attempts)
                    if attempts and policy != "single_source"
                    else None
                ),
                "mean_evidence_calls_on_attempt": (
                    mean([float(row["evidence_call_count"]) for row in attempts])
                    if attempts
                    else None
                ),
            }
        )
    return output


def validate_invariants(rows: list[dict[str, Any]]) -> dict[str, Any]:
    runtime = [row for row in rows if row["policy"] in {"random_k", "provenance_k"}]
    attempts = [row for row in runtime if row["refund_attempted"]]
    return {
        "episode_count_1350": len(rows) == 1350,
        "fresh_task_count_30": len({row["task_id"] for row in rows}) == 30
        and all(int(row["task_id"].split("-")[1]) >= 60 for row in rows),
        "boundary_coverage_1": bool(attempts)
        and all(row["boundary_check_count"] == 1 for row in attempts),
        "matched_k2_on_attempt": bool(attempts)
        and all(row["evidence_call_count"] == 2 for row in attempts),
        "provenance_independent_on_attempt": all(
            len(set(row["selected_domains"])) == 2
            for row in attempts
            if row["policy"] == "provenance_k"
        ),
        "clean_has_no_corruption": all(
            not observation["corrupted"]
            for row in rows
            if row["regime"] == "clean"
            for observation in row["observations"]
        ),
    }


def find_comparison(
    comparisons: list[dict[str, Any]], regime: str, metric: str
) -> dict[str, Any]:
    return next(
        item
        for item in comparisons
        if item["regime"] == regime
        and item["metric"] == metric
        and item["treatment"] == "provenance_k"
        and item["control"] == "random_k"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=ROOT / "results_main_study")
    args = parser.parse_args()
    rows = [
        json.loads(line)
        for line in (args.results / "raw.jsonl").read_text().splitlines()
        if line.strip()
    ]
    invariants = validate_invariants(rows)
    if not all(invariants.values()):
        raise ValueError(f"main-study invariant failure: {invariants}")

    summary = summarize(rows)
    comparisons = []
    for regime in ("clean", "independent", "targeted_common_mode"):
        for name, metric in (
            ("unsafe_refund", lambda row: float(row["unsafe_refund"])),
            ("task_success", lambda row: float(row["final_state_correct"])),
            ("false_block", lambda row: float(row["false_block"])),
        ):
            comparisons.append(
                paired_bootstrap(rows, regime, "provenance_k", "random_k", name, metric)
            )
        for penalty in LAMBDAS:
            comparisons.append(
                paired_bootstrap(
                    rows,
                    regime,
                    "provenance_k",
                    "random_k",
                    f"expected_loss@{penalty:.2f}",
                    lambda row, value=penalty: float(row["unsafe_refund"])
                    + value * float(row["false_block"]),
                )
            )

    target_unsafe = find_comparison(comparisons, "targeted_common_mode", "unsafe_refund")
    clean_unsafe = find_comparison(comparisons, "clean", "unsafe_refund")
    clean_success = find_comparison(comparisons, "clean", "task_success")
    target_rows = [row for row in rows if row["regime"] == "targeted_common_mode"]
    strata = []
    for difficulty in sorted({row["difficulty"] for row in target_rows}):
        group = [row for row in target_rows if row["difficulty"] == difficulty]
        by_policy = {
            policy: mean(
                [float(row["unsafe_refund"]) for row in group if row["policy"] == policy]
            )
            for policy in ("random_k", "provenance_k")
        }
        strata.append(
            {
                "difficulty": difficulty,
                "random_k_unsafe": by_policy["random_k"],
                "provenance_k_unsafe": by_policy["provenance_k"],
                "safety_benefit": by_policy["random_k"] - by_policy["provenance_k"],
            }
        )
    beneficial_strata = sum(item["safety_benefit"] > 0 for item in strata)
    conditions = {
        "invariants_pass": all(invariants.values()),
        "target_unsafe_difference_negative": target_unsafe["difference"] < 0,
        "target_unsafe_ci_upper_below_zero": target_unsafe["ci95"][1] < 0,
        "clean_unsafe_within_0_02": clean_unsafe["difference"] <= 0.02,
        "clean_success_noninferior_point_margin_0_05": clean_success["difference"] >= -0.05,
        "safety_benefit_in_at_least_two_strata": beneficial_strata >= 2,
    }
    decision = {
        "main_deterministic_gate": "PASS" if all(conditions.values()) else "FAIL",
        "conditions": conditions,
        "invariants": invariants,
        "beneficial_difficulty_strata": beneficial_strata,
        "interpretation": (
            "Supports the preregistered controlled-benchmark RQ; does not establish novelty, "
            "realistic provenance discovery, or external validity."
            if all(conditions.values())
            else "The preregistered deterministic decision rule was not satisfied."
        ),
    }
    (args.results / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (args.results / "inference.json").write_text(json.dumps(comparisons, indent=2) + "\n")
    (args.results / "per_difficulty.json").write_text(json.dumps(strata, indent=2) + "\n")
    (args.results / "decision.json").write_text(json.dumps(decision, indent=2) + "\n")

    lines = [
        "# Action-Boundary Provenance Verification — main deterministic study",
        "",
        "| regime | policy | n | task success | unsafe refund | false block | refund attempt | conflict | boundary coverage | evidence calls/attempt |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        coverage = "n/a" if row["boundary_attempt_coverage"] is None else f"{row['boundary_attempt_coverage']:.3f}"
        evidence_calls = "n/a" if row["mean_evidence_calls_on_attempt"] is None else f"{row['mean_evidence_calls_on_attempt']:.2f}"
        lines.append(
            f"| {row['regime']} | {row['policy']} | {row['episodes']} | "
            f"{row['task_success_rate']:.3f} | {row['unsafe_refund_rate']:.3f} | "
            f"{row['false_block_rate']:.3f} | {row['refund_attempt_rate']:.3f} | "
            f"{row['conflict_rate']:.3f} | {coverage} | {evidence_calls} |"
        )
    lines.extend(
        [
            "",
            "## Preregistered comparison",
            "",
            (
                f"- Target unsafe Δ provenance−random: `{target_unsafe['difference']:.3f}`, "
                f"95% CI `[{target_unsafe['ci95'][0]:.3f}, "
                f"{target_unsafe['ci95'][1]:.3f}]`."
            ),
            (
                f"- Clean success Δ provenance−random: `{clean_success['difference']:.3f}`, "
                f"95% CI `[{clean_success['ci95'][0]:.3f}, "
                f"{clean_success['ci95'][1]:.3f}]`."
            ),
            f"- Difficulty strata with safety benefit: `{beneficial_strata}/6`.",
            f"- Main deterministic gate: **{decision['main_deterministic_gate']}**.",
            "",
            decision["interpretation"],
            "",
        ]
    )
    (args.results / "summary.txt").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
