#!/usr/bin/env python3
"""Numerically check the closed form proved in `paper/proof-j-condition.md`.

Theorem (class-conditional labels, uniform selection with uniform fallback):
    P(select shared) - s/n = -(s(n-s)/n) * (b - a) * E[1 / (1 + K)]
with a = P(shared tool is a candidate), b = P(independent tool is a candidate),
K ~ Binomial(s-1, a) + Binomial(n-s-1, b). Without missing labels a = 1-r, b = 1-phi,
so b - a = r - phi = J.

With labels present w.p. k (missing labels are never candidates) and the primary's
label missing w.p. 1 - k_primary (then uniform fallback):
    a = k(1-r), b = k(1-phi), and the gap is multiplied by k_primary.
"""

from __future__ import annotations

from math import comb

from analyze_hidden_dependency import p_select_shared_exact
from analyze_tool_survey import p_select_shared_with_missing


def expected_inverse(s: int, n: int, a: float, b: float) -> float:
    total = 0.0
    for i in range(s):
        pi = comb(s - 1, i) * a**i * (1 - a) ** (s - 1 - i)
        for j in range(n - s):
            pj = comb(n - s - 1, j) * b**j * (1 - b) ** (n - s - 1 - j)
            total += pi * pj / (1 + i + j)
    return total


def closed_form(n: int, s: int, r: float, phi: float, k: float = 1.0, k_primary: float = 1.0) -> float:
    a, b = k * (1 - r), k * (1 - phi)
    gap = -(s * (n - s) / n) * (b - a) * expected_inverse(s, n, a, b)
    return s / n + k_primary * gap


def main() -> None:
    grid = [i / 20 for i in range(21)]
    topologies = [(2, 1), (3, 1), (4, 2), (5, 1), (6, 2), (10, 3), (10, 7)]
    worst = 0.0
    for n, s in topologies:
        for r in grid:
            for phi in grid:
                worst = max(worst, abs(closed_form(n, s, r, phi) - p_select_shared_exact(n, s, r, phi)))
    print(f"no missing labels: {len(topologies) * 21 * 21} points, max |closed form - enumeration| = {worst:.2e}")

    worst_m = 0.0
    for n, s in topologies:
        if n > 8:
            continue  # enumeration helper is exponential in n
        for r in grid[::2]:
            for phi in grid[::2]:
                for k in (0.0, 0.3, 0.55, 0.8, 1.0):
                    ref = p_select_shared_with_missing(n, s, r, phi, k)  # primary label missing w.p. 1-k
                    worst_m = max(worst_m, abs(closed_form(n, s, r, phi, k=k, k_primary=k) - ref))
    print(f"with missing labels: max |closed form - enumeration| = {worst_m:.2e}")


if __name__ == "__main__":
    main()
