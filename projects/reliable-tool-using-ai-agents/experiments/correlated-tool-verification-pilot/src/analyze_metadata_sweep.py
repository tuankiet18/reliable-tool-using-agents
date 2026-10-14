#!/usr/bin/env python3
"""Exact analysis of provenance-selector safety as failure-domain label noise varies.

POST-HOC / EXPLORATORY. Adds no study episodes and no model calls. It

1. derives the exact probability that `provenance_k` (and `random_k`) selects each
   corroborator, as a function of label-missing rate `m` and label-wrong rate `w`,
   by enumerating all 4**4 observed-label states of the four tools;
2. checks that derivation against the *real* selector code in
   `run_robustness_gate.py` (Monte Carlo over task/seed ids);
3. sweeps (m, w, leakage) on a fine grid and reports where the provenance advantage
   vanishes (break-even) and where it becomes worse than random.

Scope: tasks whose canonical action is escalation but whose primary reads a wrong
`eligible=True` value (the only tasks that can yield an unsafe refund decision under
targeted common-mode faults). Whole-population rates multiply by that task share `pi`.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from fractions import Fraction
from pathlib import Path

import run_robustness_gate as rg
from run_main_study import CORROBORATORS, PRIMARY_TOOL, SOURCE_TOPOLOGY

ROOT = Path(__file__).resolve().parents[1]
TOOLS = tuple(SOURCE_TOPOLOGY)
DOMAINS = tuple(dict.fromkeys(SOURCE_TOPOLOGY.values()))
SAME_DOMAIN_TOOL = "check_eligibility_search"  # shares operational_db with the primary
PI_MAIN = 2 / 3  # share of canonical-escalation tasks in the frozen main set


def label_distribution(true_domain: str, m: float, w: float) -> dict[str | None, float]:
    """Distribution of the observed label for one tool (mirrors observed_topology)."""
    others = [d for d in DOMAINS if d != true_domain]
    dist: dict[str | None, float] = {None: m, true_domain: 1.0 - m - w}
    for other in others:
        dist[other] = dist.get(other, 0.0) + w / len(others)
    return dist


def selection_probabilities(m: float, w: float) -> dict[str, float]:
    """Exact P(provenance_k selects corroborator t) by enumerating label states."""
    probs = {tool: 0.0 for tool in CORROBORATORS}
    per_tool = {tool: label_distribution(SOURCE_TOPOLOGY[tool], m, w) for tool in TOOLS}
    for labels in itertools.product(*(per_tool[tool].items() for tool in TOOLS)):
        observed = {tool: label for tool, (label, _) in zip(TOOLS, labels)}
        weight = 1.0
        for _, (_, p) in zip(TOOLS, labels):
            weight *= p
        if weight == 0.0:
            continue
        primary_label = observed[PRIMARY_TOOL]
        candidates = [
            tool
            for tool in CORROBORATORS
            if primary_label is not None
            and observed[tool] is not None
            and observed[tool] != primary_label
        ]
        if not candidates:  # fallback: random over every corroborator
            candidates = list(CORROBORATORS)
        for tool in candidates:
            probs[tool] += weight / len(candidates)
    return probs


def unsafe_given_escalation_task(probs: dict[str, float], leakage: float) -> float:
    """P(unsafe refund decision | canonical-escalation task, targeted fault).

    The same-domain corroborator is always wrong; independent-domain corroborators
    are wrong with probability `leakage`. A wrong corroborator agrees with the
    (identically corrupted) primary, so the gate authorises the unsafe refund.
    """
    return sum(
        p * (1.0 if tool == SAME_DOMAIN_TOOL else leakage) for tool, p in probs.items()
    )


def random_unsafe(leakage: float) -> float:
    n = len(CORROBORATORS)
    return (1.0 + (n - 1) * leakage) / n


def empirical_selection(m: float, w: float, draws: int) -> dict[str, float]:
    """Selection frequencies produced by the REAL selector code."""
    rg.METADATA_CONDITIONS["__sweep__"] = (m, w)
    counts = {tool: 0 for tool in CORROBORATORS}
    for index in range(draws):
        tool, _, _ = rg.select_provenance(f"SWEEP-{index:06d}", 1000 + index % 7, 0.0, "__sweep__")
        counts[tool] += 1
    return {tool: count / draws for tool, count in counts.items()}


def frange(stop: float, step: float) -> list[float]:
    count = int(round(stop / step))
    return [round(index * step, 10) for index in range(count + 1)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True, help="NEW output directory")
    parser.add_argument("--draws", type=int, default=40000)
    parser.add_argument("--tolerance", type=float, default=0.01)
    args = parser.parse_args()
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {args.out}")
    args.out.mkdir(parents=True, exist_ok=True)

    # 1) Validate the analytic derivation against the real selector code.
    checks = []
    for m, w in [(0.0, 0.0), (0.25, 0.0), (0.0, 0.25), (0.25, 0.25), (0.0, 0.5), (0.0, 1.0), (0.5, 0.25)]:
        exact = selection_probabilities(m, w)
        empirical = empirical_selection(m, w, args.draws)
        gap = max(abs(exact[t] - empirical[t]) for t in CORROBORATORS)
        checks.append({"m": m, "w": w, "max_abs_gap": gap, "exact": exact, "empirical": empirical})
        if gap > args.tolerance:
            raise SystemExit(f"analytic/real mismatch at m={m} w={w}: gap={gap:.4f}")

    # 2) Fine sweep: unsafe rate given an escalation task under a targeted fault.
    rows = []
    for leakage in (0.0, 0.10, 0.25, 0.50):
        baseline = random_unsafe(leakage)
        for m in frange(0.5, 0.125):
            for w in frange(1.0 - m, 0.025):
                probs = selection_probabilities(m, w)
                unsafe = unsafe_given_escalation_task(probs, leakage)
                rows.append(
                    {
                        "leakage": leakage,
                        "missing": m,
                        "wrong": w,
                        "random_unsafe": baseline,
                        "provenance_unsafe": unsafe,
                        "difference": unsafe - baseline,
                        "p_select_same_domain": probs[SAME_DOMAIN_TOOL],
                    }
                )

    # 3) Break-even and worse-than-random thresholds on the w axis (m fixed).
    thresholds = []
    for leakage in (0.0, 0.10, 0.25, 0.50):
        for m in (0.0, 0.25, 0.5):
            subset = [r for r in rows if r["leakage"] == leakage and r["missing"] == m]
            subset.sort(key=lambda r: r["wrong"])
            advantage_gone = next((r["wrong"] for r in subset if r["difference"] >= 0), None)
            thresholds.append(
                {
                    "leakage": leakage,
                    "missing": m,
                    "first_wrong_rate_with_no_advantage": advantage_gone,
                    "difference_at_w0": subset[0]["difference"],
                    "difference_at_max_w": subset[-1]["difference"],
                }
            )

    # Share-of-task scaling for the main frozen set, for context only.
    summary = {
        "scope": "post-hoc exact analysis; escalation-canonical tasks under targeted common-mode fault",
        "pi_main_escalation_share": PI_MAIN,
        "validation_max_gap": max(c["max_abs_gap"] for c in checks),
        "validation": checks,
        "thresholds": thresholds,
        "note": "Whole-population unsafe rate = pi * values here; correct-expected-refund tasks are unaffected because the actor escalates after a false denial.",
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    with (args.out / "sweep.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print("validation max gap:", f"{summary['validation_max_gap']:.4f}")
    print("leakage missing  first_w_with_no_advantage  diff@w=0  diff@max_w")
    for t in thresholds:
        print(
            f"{t['leakage']:<8} {t['missing']:<8} {str(t['first_wrong_rate_with_no_advantage']):<26} "
            f"{t['difference_at_w0']:+.3f}    {t['difference_at_max_w']:+.3f}"
        )


if __name__ == "__main__":
    main()
