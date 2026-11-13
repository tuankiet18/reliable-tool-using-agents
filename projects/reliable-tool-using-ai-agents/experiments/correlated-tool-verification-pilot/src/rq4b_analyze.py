#!/usr/bin/env python3
"""Analysis for "Protocol - LLM Corroborator Choice Mechanism and Label Inversion" (sec. 4-5).

Unit: choice set (a set's shared-choice rate is the mean over its valid rotations). Per model:
  (Amendment B1, written before any model call, after the self-test showed that the original C4 - C0 contrast
   on the shared-choice rate has a tiny expected effect, +0.17, even for a perfect label-follower.)
  H-B1  main prompt:         d < 0  (sets that have C4)   CI upper bound < 0
  H-B2  neutral prompt:      d > 0  (sets that have C4)   CI lower bound > 0
        where d = P(choose the candidate labelled with the primary's provider | C4)
                - P(choose that same candidate in the same position | C0), averaged per set over rotations.
        The C0 term is position- and text-matched, so position bias cancels.
  The original contrast C4 - C0 on the shared-choice rate is reported as secondary (no Holm).
  H-B3  consistency prompt:  C1 - C0 > 0  (all 56 sets)            CI lower bound > 0
  H-B4  (gpt-4.1 only)       main prompt: H-A1 (C1 - C0 < 0) and H-A2 (C1 rate < 1/3), as in RQ4
One-sided bootstrap p (share of resamples on the wrong side of the boundary), 10,000 resamples, seed 20261112,
Holm over all tests of the family at alpha 0.025.

Usage: python3 rq4b_analyze.py --results r1.jsonl [r2.jsonl ...] --out <new dir>
       python3 rq4b_analyze.py --selftest
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS_B = ROOT / "data" / "rq4_agent_choice" / "runner" / "items_b.jsonl"
SEED, B, ALPHA = 20261112, 10000, 0.025
THIRD = 1 / 3
LARGE_MODEL_PREFIX = "gpt-4.1-2"  # the larger model; gpt-4.1-mini starts with "gpt-4.1-m"


def boot_mean(values: list[float], rng: random.Random) -> list[float]:
    n = len(values)
    return sorted(sum(values[rng.randrange(n)] for _ in range(n)) / n for _ in range(B))


def ci95(dist: list[float]) -> list[float]:
    return [dist[int(0.025 * B)], dist[int(0.975 * B) - 1]]


def holm(pvals: dict[str, float]) -> dict[str, float]:
    order = sorted(pvals, key=pvals.get)
    adj, running = {}, 0.0
    for i, k in enumerate(order):
        running = max(running, min(1.0, (len(order) - i) * pvals[k]))
        adj[k] = running
    return adj


def set_rates(rows: list[dict], condition: str, prompt: str, field: str = "chose_shared",
              only: set | None = None) -> dict[str, float]:
    acc = defaultdict(list)
    for r in rows:
        if r["condition"] == condition and r["prompt"] == prompt and r["valid"] and r.get(field) is not None:
            if only is None or r["set_id"] in only:
                acc[r["set_id"]].append(1.0 if r[field] else 0.0)
    return {k: sum(v) / len(v) for k, v in acc.items()}


def mimic_d(rows: list[dict], prompt: str, only: set) -> list[float]:
    """Per-set mean of [chose mimic letter in C4] - [chose that letter in C0], matched by (set, rotation)."""
    c4 = {(r["set_id"], r["rotation"]): r for r in rows
          if r["condition"] == "C4" and r["prompt"] == prompt and r["valid"] and r["set_id"] in only}
    c0 = {(r["set_id"], r["rotation"]): r for r in rows
          if r["condition"] == "C0" and r["prompt"] == prompt and r["valid"]}
    acc = defaultdict(list)
    for key, r4 in c4.items():
        r0 = c0.get(key)
        if r0 is None:
            continue
        letter = r4["labelled_same_letter"]
        acc[key[0]].append((1.0 if r4["choice"] == letter else 0.0) - (1.0 if r0["choice"] == letter else 0.0))
    return [sum(v) / len(v) for _, v in sorted(acc.items())]


def paired(a: dict, b: dict) -> list[float]:
    return [a[k] - b[k] for k in sorted(a) if k in b]


def test(values: list[float], boundary: float, direction: str, rng: random.Random) -> dict:
    """direction 'gt': H says mean > boundary; 'lt': mean < boundary."""
    dist = boot_mean(values, rng)
    wrong = sum(1 for x in dist if (x <= boundary if direction == "gt" else x >= boundary)) / B
    lo, hi = ci95(dist)
    ok_ci = lo > boundary if direction == "gt" else hi < boundary
    return {"sets": len(values), "estimate": sum(values) / len(values), "ci95": [lo, hi],
            "p_one_sided": wrong, "ci_condition_met": ok_ci}


def analyze(rows_by_model: dict[str, list[dict]]) -> dict:
    out = {"seed": SEED, "bootstrap": B, "alpha": ALPHA, "models": {}}
    pvals, tests = {}, {}
    for model, rows in rows_by_model.items():
        rng = random.Random(SEED)
        c4_sets = {r["set_id"] for r in rows if r["condition"] == "C4"}
        res = {"n_rows": len(rows), "c4_sets": len(c4_sets)}
        main_rows = [r for r in rows if r["prompt"] == "main"]
        res["invalid_rate_main"] = (sum(1 for r in main_rows if not r["valid"]) / len(main_rows)) if main_rows else None
        desc = {}
        for prompt in ("main", "neutral", "consistency"):
            for cond in ("C0", "C1", "C4"):
                if not any(r["prompt"] == prompt and r["condition"] == cond for r in rows):
                    continue
                only = c4_sets if cond == "C4" else None
                rates = set_rates(rows, cond, prompt, only=only)
                same = set_rates(rows, cond, prompt, "chose_labelled_same", only=only)
                if not rates:
                    continue
                v = list(rates.values())
                entry = {"sets": len(v), "shared_choice_rate": sum(v) / len(v),
                         "ci95": ci95(boot_mean(v, rng))}
                if same:
                    entry["labelled_same_choice_rate"] = sum(same.values()) / len(same)
                desc[f"{prompt}/{cond}"] = entry
        res["descriptive"] = desc

        def contrast(prompt, a, b, only=None):
            return paired(set_rates(rows, a, prompt, only=only), set_rates(rows, b, prompt, only=only))

        v = mimic_d(rows, "main", c4_sets)
        if v:
            tests[f"{model}|H-B1"] = test(v, 0.0, "lt", rng)
        v = mimic_d(rows, "neutral", c4_sets)
        if v:
            tests[f"{model}|H-B2"] = test(v, 0.0, "gt", rng)
        sec = {}
        for prompt in ("main", "neutral"):
            v = contrast(prompt, "C4", "C0", c4_sets)
            if v:
                dist = boot_mean(v, rng)
                sec[f"{prompt}: shared-choice C4-C0"] = {"sets": len(v), "estimate": sum(v) / len(v), "ci95": ci95(dist)}
        res["secondary_contrasts"] = sec
        key = f"{model}|H-B3"
        v = contrast("consistency", "C1", "C0")
        if v:
            tests[key] = test(v, 0.0, "gt", rng)
        if model.startswith(LARGE_MODEL_PREFIX):
            v = contrast("main", "C1", "C0")
            if v:
                tests[f"{model}|H-A1"] = test(v, 0.0, "lt", rng)
            rates = list(set_rates(rows, "C1", "main").values())
            if rates:
                tests[f"{model}|H-A2"] = test(rates, THIRD, "lt", rng)
        out["models"][model] = res
    pvals = {k: t["p_one_sided"] for k, t in tests.items()}
    adj = holm(pvals) if pvals else {}
    for k, t in tests.items():
        t["p_holm"] = adj[k]
        t["supported"] = bool(t["ci_condition_met"] and adj[k] < ALPHA)
    out["tests"] = tests
    return out


def load_rows(paths: list[Path]) -> dict[str, list[dict]]:
    items = {}
    for line in ITEMS_B.open(encoding="utf-8"):
        it = json.loads(line)
        items[it["item_id"]] = it
    by_model: dict[str, dict[str, dict]] = defaultdict(dict)
    for p in paths:
        for line in p.open(encoding="utf-8"):
            r = json.loads(line)
            if "item_id" not in r or r["item_id"] not in items:
                continue  # headers, and RQ4 cells (C2) that are not part of this study
            by_model[r["model"]].setdefault(r["item_id"], {**items[r["item_id"]], **r})
    return {m: list(d.values()) for m, d in by_model.items()}


def selftest() -> None:
    items = [json.loads(l) for l in ITEMS_B.open(encoding="utf-8")]
    letters = "ABC"

    def synth(policy: str) -> list[dict]:
        rng = random.Random(7)
        rows = []
        for it in items:
            same = it["labelled_same_letter"]
            if policy == "random" or (policy == "avoider" and not same) or (policy == "consistent" and not same):
                choice = rng.choice(letters)
            elif policy == "avoider":  # avoids the candidate labelled with the primary's provider
                choice = rng.choice([x for x in letters if x != same])
            else:  # "consistent": seeks the candidate labelled like the primary, except when told to be independent
                choice = rng.choice([x for x in letters if x != same]) if it["prompt"] == "main" else same
            rows.append({**it, "model": f"synthetic-{policy}", "choice": choice, "valid": True,
                         "chose_shared": choice == it["shared_letter"],
                         "chose_labelled_same": (choice == same) if same else None})
        return rows
    res = analyze({"synthetic-random": synth("random"), "synthetic-avoider": synth("avoider"),
                   "synthetic-consistent": synth("consistent"),
                   "gpt-4.1-2025-04-14": synth("consistent")})
    for k, t in sorted(res["tests"].items()):
        print(f"{k:42s} est {t['estimate']:+.3f} ci [{t['ci95'][0]:+.3f},{t['ci95'][1]:+.3f}] holm {t['p_holm']:.4f} supported={t['supported']}")
    want = {"synthetic-random|H-B1": False, "synthetic-random|H-B2": False, "synthetic-random|H-B3": False,
            "synthetic-avoider|H-B1": True, "synthetic-avoider|H-B2": False, "synthetic-avoider|H-B3": False,
            "synthetic-consistent|H-B1": True, "synthetic-consistent|H-B2": True, "synthetic-consistent|H-B3": True}
    bad = {k: (res["tests"][k]["supported"], v) for k, v in want.items() if res["tests"][k]["supported"] != v}
    print("SELFTEST", "FAILED " + str(bad) if bad else "PASSED")
    raise SystemExit(1 if bad else 0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", nargs="+", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    args.out.mkdir(parents=True, exist_ok=False)
    res = analyze(load_rows(args.results))
    (args.out / "analysis_b.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(res["tests"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
