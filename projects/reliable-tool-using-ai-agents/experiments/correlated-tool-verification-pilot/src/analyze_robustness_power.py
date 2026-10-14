#!/usr/bin/env python3
"""Power of the robustness-gate criterion (upper 95% CI < 0) for the wrong_25 condition.

POST-HOC / EXPLORATORY. No real study episodes and no model calls: it simulates new
synthetic studies with the REAL episode code (`run_robustness_gate.run_episode`), then
applies a task-cluster percentile bootstrap like the original analyzer.

Synthetic tasks mirror the frozen robustness set's structure: a share `pi` of tasks are
canonical escalations (primary corrupted to eligible=True), the rest canonical refunds.
Five seeds per task, matching the frozen design.
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
from pathlib import Path

import run_robustness_gate as rg

Z_975, Z_80 = 1.959964, 0.841621


def synthetic_case(index: int, escalate: bool, study: int) -> dict:
    amount = 40.0 + index % 17
    return {
        "task_id": f"PWR-{study:04d}-{index:04d}",
        "difficulty": "synthetic",
        "expected_action": "escalate" if escalate else "refund",
        "expected_amount_eur": None if escalate else amount,
        "canonical_eligible": not escalate,
        "canonical_max_refund_eur": 0.0 if escalate else amount,
        "fallback_max_refund_eur": 120.0,
    }


def task_differences(n_tasks: int, pi: float, seeds: list[int], leakage: float,
                     condition: str, study: int) -> list[float]:
    n_escalate = round(pi * n_tasks)
    diffs = []
    for index in range(n_tasks):
        case = synthetic_case(index, index < n_escalate, study)
        prov = rand = 0
        for seed in seeds:
            fault_map = rg.build_fault_map(case, seed, leakage)
            rand += rg.run_episode(case, seed, leakage, "random_k", fault_map, "baseline")["unsafe_refund"]
            prov += rg.run_episode(case, seed, leakage, "provenance_k", fault_map, condition)["unsafe_refund"]
        diffs.append((prov - rand) / len(seeds))
    return diffs


def bootstrap_upper(diffs: list[float], resamples: int, rng: random.Random) -> float:
    n = len(diffs)
    means = sorted(sum(rng.choice(diffs) for _ in range(n)) / n for _ in range(resamples))
    return means[int(0.975 * resamples) - 1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True, help="NEW output directory")
    parser.add_argument("--studies", type=int, default=300)
    parser.add_argument("--resamples", type=int, default=1000)
    parser.add_argument("--observed-sd", type=float, default=0.1988,
                        help="per-task paired-difference SD in frozen wrong_25/leak .10 data")
    args = parser.parse_args()
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {args.out}")
    args.out.mkdir(parents=True, exist_ok=True)

    pi, leakage, condition = 2 / 3, 0.10, "wrong_25"
    seeds = list(rg.DEFAULT_SEEDS)
    rng = random.Random(20261006)

    # Normal-approximation power for two plausible effect sizes.
    analytic = []
    for label, delta in [("predicted_exact_model", -0.088), ("observed_frozen", -0.0667)]:
        n80 = ((Z_975 + Z_80) * args.observed_sd / abs(delta)) ** 2
        se30 = args.observed_sd / 30**0.5
        power30 = statistics.NormalDist().cdf(abs(delta) / se30 - Z_975)
        analytic.append({"effect": label, "delta": delta, "power_at_30_tasks": power30,
                         "tasks_for_80pct_power": n80})

    # Simulation with the real episode code.
    simulated = []
    for n_tasks in (30, 45, 60, 90, 120):
        passes, means, sds = 0, [], []
        for study in range(args.studies):
            diffs = task_differences(n_tasks, pi, seeds, leakage, condition, study * 1000 + n_tasks)
            means.append(statistics.mean(diffs))
            sds.append(statistics.stdev(diffs))
            passes += bootstrap_upper(diffs, args.resamples, rng) < 0
        simulated.append({"tasks": n_tasks, "studies": args.studies,
                          "power_upper_ci_below_zero": passes / args.studies,
                          "mean_effect": statistics.mean(means),
                          "mean_task_sd": statistics.mean(sds)})
        print(f"tasks={n_tasks:<4} power={passes / args.studies:.3f} "
              f"mean_effect={statistics.mean(means):+.4f} task_sd={statistics.mean(sds):.4f}")

    summary = {"scope": "post-hoc power analysis of the wrong_25 / leakage .10 robustness criterion",
               "pi": pi, "seeds": seeds, "analytic_normal_approx": analytic,
               "simulation_real_episode_code": simulated}
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    for item in analytic:
        print(f"{item['effect']}: delta={item['delta']} power@30={item['power_at_30_tasks']:.2f} "
              f"tasks_for_80%={item['tasks_for_80pct_power']:.0f}")


if __name__ == "__main__":
    main()
