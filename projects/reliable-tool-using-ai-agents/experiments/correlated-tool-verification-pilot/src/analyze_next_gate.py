#!/usr/bin/env python3
"""Summarize and bootstrap the 30-task metadata-robustness gate."""

from __future__ import annotations

import json
import random
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results_next_gate"
N_BOOTSTRAP = 10_000
COSTS = (0.0, 0.1, 0.25, 0.5, 0.75, 1.0)


def label(row: dict[str, Any]) -> str:
    if row["policy"] == "provenance_aware":
        return f"provenance_aware/{row['metadata_condition']}"
    return row["policy"]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def quantile(values: list[float], q: float) -> float:
    values = sorted(values)
    position = (len(values) - 1) * q
    lo = int(position)
    hi = min(lo + 1, len(values) - 1)
    weight = position - lo
    return values[lo] * (1 - weight) + values[hi] * weight


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["regime"], label(row))].append(row)
    summary = []
    for (regime, policy), group in sorted(groups.items()):
        accepted = sum(item["accepted"] for item in group)
        selected_faults = sum(item["selected_fault"] for item in group)
        accuracies = [x["metadata_accuracy"] for x in group if x["metadata_accuracy"] is not None]
        summary.append(
            {
                "regime": regime,
                "policy": policy,
                "episodes": len(group),
                "unsafe_accept_rate": mean([float(x["unsafe_accept"]) for x in group]),
                "correct_accept_rate": mean([float(x["accepted_correct"]) for x in group]),
                "abstention_rate": mean([float(x["alarm"]) for x in group]),
                "selective_accuracy": sum(x["accepted_correct"] for x in group) / accepted,
                "detection_recall": (
                    sum(x["alarm"] and x["selected_fault"] for x in group) / selected_faults
                    if selected_faults
                    else None
                ),
                "true_domain_diversity_rate": mean(
                    [float(x["true_domain_diversity"] == 2) for x in group]
                ),
                "metadata_completeness": mean([x["metadata_completeness"] for x in group]),
                "metadata_accuracy": mean(accuracies),
            }
        )
    return summary


def paired_bootstrap(
    rows: list[dict[str, Any]],
    regime: str,
    treatment: str,
    control: str,
    metric: Callable[[dict[str, Any]], float],
    metric_name: str,
) -> dict[str, Any]:
    selected = [
        row for row in rows if row["regime"] == regime and label(row) in {treatment, control}
    ]
    paired: dict[tuple[str, int], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in selected:
        paired[(row["task_id"], row["seed"])][label(row)] = row
    tasks = sorted({task for task, _ in paired})
    task_differences = {}
    for task in tasks:
        pairs = [value for (task_id, _), value in paired.items() if task_id == task]
        task_differences[task] = mean(
            [metric(pair[treatment]) - metric(pair[control]) for pair in pairs]
        )
    estimate = mean(list(task_differences.values()))
    rng = random.Random(20260914 + sum(map(ord, treatment + control + metric_name + regime)))
    boot = [
        mean([task_differences[rng.choice(tasks)] for _ in tasks])
        for _ in range(N_BOOTSTRAP)
    ]
    return {
        "regime": regime,
        "treatment": treatment,
        "control": control,
        "metric": metric_name,
        "difference": estimate,
        "ci95": [quantile(boot, 0.025), quantile(boot, 0.975)],
        "clusters": len(tasks),
    }


def main() -> None:
    rows = [json.loads(line) for line in (RESULTS / "raw.jsonl").read_text().splitlines()]
    summary = summarize(rows)
    comparisons = []
    treatments = [
        "provenance_aware/accurate",
        "provenance_aware/missing_25",
        "provenance_aware/wrong_25",
        "provenance_aware/mixed_25_each",
        "provenance_aware/wrong_50",
    ]
    for treatment in treatments:
        for control in ("fixed_k", "random_k"):
            regimes = ("common_mode", "independent") if treatment.endswith("/accurate") else ("common_mode",)
            for regime in regimes:
                comparisons.append(
                    paired_bootstrap(
                        rows, regime, treatment, control,
                        lambda x: float(x["unsafe_accept"]), "unsafe_accept"
                    )
                )
                for cost in COSTS:
                    comparisons.append(
                        paired_bootstrap(
                            rows, regime, treatment, control,
                            lambda x, c=cost: float(x["unsafe_accept"]) + c * float(x["alarm"]),
                            f"expected_loss@{cost:.2f}",
                        )
                    )

    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (RESULTS / "inference.json").write_text(json.dumps(comparisons, indent=2) + "\n")

    common = [row for row in summary if row["regime"] == "common_mode"]
    lines = [
        "# 30-task metadata robustness gate",
        "",
        "Holdout: 30 disjoint tasks × 5 seeds. Mọi K=2 policy dùng primary `order_api` và đúng một corroborating call.",
        "",
        "| policy | unsafe accept | correct accept | abstain | selective accuracy | true source diversity | metadata completeness | metadata accuracy |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in common:
        lines.append(
            f"| {row['policy']} | {row['unsafe_accept_rate']:.3f} | {row['correct_accept_rate']:.3f} | "
            f"{row['abstention_rate']:.3f} | {row['selective_accuracy']:.3f} | "
            f"{row['true_domain_diversity_rate']:.3f} | {row['metadata_completeness']:.3f} | "
            f"{row['metadata_accuracy']:.3f} |"
        )
    lines.extend([
        "", "## Expected loss under common-mode faults", "",
        "`L = unsafe_accept + λ × abstain`; wrong-accept cost = 1. Lower is better.", "",
        "| policy | λ=0 | λ=.10 | λ=.25 | λ=.50 | λ=.75 | λ=1 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    for row in common:
        values = [row["unsafe_accept_rate"] + cost * row["abstention_rate"] for cost in COSTS]
        lines.append(f"| {row['policy']} | " + " | ".join(f"{value:.3f}" for value in values) + " |")
    lines.extend([
        "",
        "Cluster-bootstrap dùng task làm resampling unit (`n=30`, 10,000 resamples). Xem `inference.json` cho paired comparisons.",
        "",
    ])
    # Use .txt because generated experiment reports are artifacts, not Obsidian knowledge pages.
    (RESULTS / "summary.txt").write_text("\n".join(lines))
    print(f"wrote summary and {len(comparisons)} comparisons to {RESULTS}")


if __name__ == "__main__":
    main()
