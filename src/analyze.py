#!/usr/bin/env python3
"""Cluster-bootstrap paired policy differences from pilot raw results."""

from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_SEED = 20260913
N_BOOTSTRAP = 10_000


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    index = (len(ordered) - 1) * q
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def value(row: dict, metric: str, abstention_cost: float | None = None) -> float:
    if metric == "expected_loss":
        assert abstention_cost is not None
        return float(row["unsafe_accept"]) + abstention_cost * float(row["alarm"])
    return float(row[metric])


def cluster_bootstrap(
    rows: list[dict], regime: str, treatment: str, control: str, metric: str, cost=None
) -> dict:
    selected = [r for r in rows if r["regime"] == regime and r["policy"] in {treatment, control}]
    paired: dict[tuple[str, int], dict[str, dict]] = defaultdict(dict)
    for row in selected:
        paired[(row["task_id"], row["seed"])][row["policy"]] = row
    tasks = sorted({task for task, _ in paired})

    def task_difference(task: str) -> float:
        pairs = [policies for (task_id, _), policies in paired.items() if task_id == task]
        differences = [
            value(item[treatment], metric, cost) - value(item[control], metric, cost)
            for item in pairs
        ]
        return mean(differences)

    task_differences = {task: task_difference(task) for task in tasks}
    estimate = mean(list(task_differences.values()))
    rng = random.Random(BOOTSTRAP_SEED + sum(map(ord, regime + treatment + control + metric)))
    boot = []
    for _ in range(N_BOOTSTRAP):
        sample = [rng.choice(tasks) for _ in tasks]
        boot.append(mean([task_differences[task] for task in sample]))
    return {
        "regime": regime,
        "treatment": treatment,
        "control": control,
        "metric": metric,
        "abstention_cost": cost,
        "estimate": estimate,
        "ci95": [quantile(boot, 0.025), quantile(boot, 0.975)],
        "clusters": len(tasks),
        "bootstrap_resamples": N_BOOTSTRAP,
    }


def main() -> None:
    rows = [json.loads(line) for line in (ROOT / "results" / "raw.jsonl").read_text().splitlines()]
    comparisons = []
    for regime in ("independent", "common_mode"):
        for control in ("fixed_k", "random_k"):
            for metric in ("unsafe_accept", "alarm", "accepted_correct"):
                comparisons.append(
                    cluster_bootstrap(rows, regime, "provenance_aware", control, metric)
                )
            for cost in (0.0, 0.1, 0.25, 0.5, 0.75, 1.0):
                comparisons.append(
                    cluster_bootstrap(
                        rows, regime, "provenance_aware", control, "expected_loss", cost
                    )
                )
    out = ROOT / "results"
    (out / "inference.json").write_text(json.dumps(comparisons, indent=2) + "\n")
    lines = [
        "# Paired cluster-bootstrap analysis",
        "",
        "Differences are `provenance_aware - control`. Negative is better for unsafe acceptance/expected loss; positive is better for correct acceptance. Resampling unit is task (`n=10`), retaining all five seeds.",
        "",
        "| regime | control | metric | abstention cost | difference | 95% cluster-bootstrap CI |",
        "|---|---|---|---:|---:|---:|",
    ]
    for item in comparisons:
        lo, hi = item["ci95"]
        cost = "n/a" if item["abstention_cost"] is None else f"{item['abstention_cost']:.2f}"
        lines.append(
            f"| {item['regime']} | {item['control']} | {item['metric']} | {cost} | "
            f"{item['estimate']:.3f} | [{lo:.3f}, {hi:.3f}] |"
        )
    lines.extend(
        [
            "",
            "CIs quantify uncertainty over these ten synthetic task fixtures only; they do not establish external validity.",
            "",
        ]
    )
    (out / "inference.md").write_text("\n".join(lines))
    print(f"wrote {len(comparisons)} comparisons to {out}")


if __name__ == "__main__":
    main()

