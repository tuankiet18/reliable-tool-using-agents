#!/usr/bin/env python3
"""Exact analysis of provenance selection under SYSTEMATIC failure-domain label errors.

POST-HOC / EXPLORATORY. No study episodes, no model calls.

Model. A primary has `n` candidate corroborators; `s` of them truly share its failure
domain. Metadata acts as a classifier of "shares the primary's domain":
  * recall `r`: P(a truly shared tool is labelled shared); 1 - r = hidden dependency;
  * false-sharing `phi`: P(a truly independent tool is labelled shared).
Labels are drawn independently per tool given its true class. The provenance selector
picks uniformly among tools labelled independent and falls back to a uniform choice
over all `n` tools when none is labelled independent (as in run_robustness_gate.py).
Random-K picks uniformly over all `n` tools.

Under a targeted common-mode fault a truly shared corroborator always agrees with the
wrong primary; an independent one is wrong with probability `leakage`. Hence
  unsafe = P(select shared) + leakage * (1 - P(select shared)).

Claim checked numerically here: provenance beats random iff r > phi, i.e. iff the
metadata's Youden index J = r - phi is positive; it is exactly as unsafe as random at
J = 0 and strictly worse at J < 0.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from math import comb
from pathlib import Path


def p_select_shared_exact(n: int, s: int, r: float, phi: float) -> float:
    total = 0.0
    for j in range(s + 1):  # hidden shared tools (labelled independent)
        pj = comb(s, j) * (1 - r) ** j * r ** (s - j)
        for f in range(n - s + 1):  # independent tools wrongly labelled shared
            pf = comb(n - s, f) * phi**f * (1 - phi) ** (n - s - f)
            candidates = (n - s - f) + j
            p = s / n if candidates == 0 else j / candidates
            total += pj * pf * p
    return total


def p_select_shared_mc(n: int, s: int, r: float, phi: float, draws: int, seed: int) -> float:
    rng = random.Random(seed)
    hits = 0
    for _ in range(draws):
        shared = [True] * s + [False] * (n - s)
        labelled_independent = [
            tool
            for tool, is_shared in enumerate(shared)
            if (is_shared and rng.random() >= r) or (not is_shared and rng.random() >= phi)
        ]
        pool = labelled_independent or list(range(n))
        hits += shared[rng.choice(pool)]
    return hits / draws


def unsafe(p_shared: float, leakage: float) -> float:
    return p_shared + leakage * (1 - p_shared)


def grid(step: float) -> list[float]:
    count = int(round(1 / step))
    return [round(i * step, 10) for i in range(count + 1)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True, help="NEW output directory")
    parser.add_argument("--draws", type=int, default=60000)
    args = parser.parse_args()
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {args.out}")
    args.out.mkdir(parents=True, exist_ok=True)

    # Topologies: the frozen main study (n=3, s=1) plus larger hypothetical registries.
    topologies = [(3, 1), (4, 2), (6, 2), (10, 3), (10, 7)]

    # 1) Exact enumeration vs an independent Monte Carlo implementation.
    validation = []
    for index, ((n, s), r, phi) in enumerate(
        [((3, 1), 1.0, 0.0), ((3, 1), 0.0, 0.0), ((3, 1), 0.0, 0.5), ((4, 2), 0.6, 0.3),
         ((10, 3), 0.5, 0.5), ((10, 7), 0.9, 0.2), ((6, 2), 0.2, 0.7)]
    ):
        exact = p_select_shared_exact(n, s, r, phi)
        mc = p_select_shared_mc(n, s, r, phi, args.draws, 1000 + index)
        validation.append({"n": n, "s": s, "r": r, "phi": phi, "exact": exact, "mc": mc,
                           "abs_gap": abs(exact - mc)})
    max_gap = max(v["abs_gap"] for v in validation)
    if max_gap > 0.01:
        raise SystemExit(f"exact/MC mismatch: {max_gap:.4f}")

    # 2) Sweep r, phi; test the J = r - phi sign rule.
    rows, violations = [], 0
    for n, s in topologies:
        base = s / n
        for r in grid(0.05):
            for phi in grid(0.05):
                ps = p_select_shared_exact(n, s, r, phi)
                diff = ps - base  # leakage scales this by (1 - leakage)
                j = round(r - phi, 10)
                sign_ok = (j > 0 and diff < -1e-12) or (j == 0 and abs(diff) < 1e-12) or (
                    j < 0 and diff > 1e-12
                )
                # Edge case: when no tool can ever be labelled independent the selector
                # always falls back to random, so diff == 0 regardless of J.
                degenerate = (r == 1.0 and phi == 1.0)
                if not sign_ok and not degenerate:
                    violations += 1
                rows.append({"n": n, "s": s, "r": r, "phi": phi, "J": j,
                             "p_select_shared_provenance": ps, "p_select_shared_random": base,
                             "diff_same_domain_selection": diff})

    # 3) Readable slices for the main topology (n=3, s=1) with leakage 0.10.
    main_slices = []
    for r, phi in [(1.0, 0.0), (0.75, 0.0), (0.5, 0.0), (0.0, 0.0), (0.75, 0.25),
                   (0.5, 0.5), (0.25, 0.5), (0.0, 0.5), (0.0, 1.0)]:
        ps = p_select_shared_exact(3, 1, r, phi)
        main_slices.append({"r": r, "phi": phi, "J": round(r - phi, 3),
                            "unsafe_provenance_leak_0.10": unsafe(ps, 0.10),
                            "unsafe_random_leak_0.10": unsafe(1 / 3, 0.10)})

    summary = {
        "scope": "post-hoc exact analysis; systematic (class-conditional) label errors",
        "validation_max_abs_gap": max_gap,
        "validation": validation,
        "sign_rule": "provenance better than random iff r > phi (J > 0); equal iff J = 0; worse iff J < 0",
        "sign_rule_violations_on_grid": violations,
        "grid_points": len(rows),
        "main_topology_slices": main_slices,
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    with (args.out / "sweep.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"validation max gap: {max_gap:.4f}")
    print(f"sign-rule violations: {violations} / {len(rows)} grid points")
    print("main topology n=3,s=1, leakage .10:   r     phi    J     prov   random")
    for item in main_slices:
        print(f"{'':38}{item['r']:<6}{item['phi']:<7}{item['J']:<6}"
              f"{item['unsafe_provenance_leak_0.10']:.3f}  {item['unsafe_random_leak_0.10']:.3f}")


if __name__ == "__main__":
    main()
