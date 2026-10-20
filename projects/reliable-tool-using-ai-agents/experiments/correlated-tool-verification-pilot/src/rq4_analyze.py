#!/usr/bin/env python3
"""RQ4 analysis (protocol "Agent Corroborator Choice with Real Tool Metadata" §7).

Unit: choice set; a set's shared-choice rate is the mean over its valid rotations.
H-A1: C1 - C0 < 0 (paired); H-A2: C1 < 1/3. Main prompt only. Per model; one-sided bootstrap
p-values (share of resamples on the wrong side of the boundary), Holm over 2 hypotheses x models
at alpha = 0.025 (equivalent to the two-sided 95% CI criterion). A model with >10% invalid outputs
on the main prompt fails the manipulation check and is not used for H-A1/H-A2.

Usage: python3 rq4_analyze.py --results r1.jsonl [r2.jsonl ...] --out <new dir>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data" / "rq4_agent_choice" / "runner" / "items.jsonl"
SEED, B, ALPHA = 20261018, 10000, 0.025


def load(path: Path, items: dict) -> tuple[str, dict, list[dict]]:
    rows, header = [], None
    for line in path.open(encoding="utf-8"):
        r = json.loads(line)
        if "environment" in r:
            header = r
        else:
            rows.append({**items[r["item_id"]], **r})
    model = rows[0]["model"]
    return model, header, rows


def set_rates(rows: list[dict], condition: str, prompt: str) -> dict[str, float]:
    acc = defaultdict(list)
    for r in rows:
        if r["condition"] == condition and r["prompt"] == prompt and r["valid"]:
            acc[r["set_id"]].append(1.0 if r["chose_shared"] else 0.0)
    return {k: sum(v) / len(v) for k, v in acc.items()}


def boot(values: list[float], rng: random.Random) -> list[float]:
    n = len(values)
    return sorted(sum(values[rng.randrange(n)] for _ in range(n)) / n for _ in range(B))


def ci(dist: list[float]) -> list[float]:
    return [dist[int(0.025 * B)], dist[int(0.975 * B) - 1]]


def holm(pvals: dict[str, float]) -> dict[str, float]:
    order = sorted(pvals, key=pvals.get)
    adj, running = {}, 0.0
    for i, k in enumerate(order):
        running = max(running, min(1.0, (len(order) - i) * pvals[k]))
        adj[k] = running
    return adj


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", nargs="+", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {args.out}")
    args.out.mkdir(parents=True, exist_ok=True)
    items = {it["item_id"]: it for it in map(json.loads, ITEMS.open(encoding="utf-8"))}
    rng = random.Random(SEED)
    report, pvals = {"items_sha256": hashlib.sha256(ITEMS.read_bytes()).hexdigest(), "models": {}}, {}
    for path in args.results:
        model, header, rows = load(path, items)
        main_rows = [r for r in rows if r["prompt"] == "main"]
        invalid = sum(not r["valid"] for r in main_rows) / len(main_rows)
        res = {"results_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "environment": header and header.get("environment"),
               "n_rows": len(rows), "invalid_rate_main": invalid, "manipulation_check": "PASS" if invalid <= 0.10 else "FAIL",
               "descriptive": {}, "position_choice_rate": {}}
        for prompt in ("main", "neutral"):
            for cond in ("C0", "C1", "C2"):
                rates = set_rates(rows, cond, prompt)
                vals = list(rates.values())
                res["descriptive"][f"{prompt}/{cond}"] = {"sets": len(vals), "shared_choice_rate": sum(vals) / len(vals) if vals else None,
                                                          "ci95": ci(boot(vals, rng)) if vals else None}
        for letter in "ABC":
            valid = [r for r in main_rows if r["valid"]]
            res["position_choice_rate"][letter] = sum(r["choice"] == letter for r in valid) / len(valid)
        if res["manipulation_check"] == "PASS":
            c0, c1 = set_rates(rows, "C0", "main"), set_rates(rows, "C1", "main")
            common = sorted(set(c0) & set(c1))
            diffs = [c1[k] - c0[k] for k in common]
            d_dist, c1_dist = boot(diffs, rng), boot([c1[k] for k in c1], rng)
            res["H-A1"] = {"sets": len(common), "diff_C1_minus_C0": sum(diffs) / len(diffs), "ci95": ci(d_dist),
                           "p_one_sided": sum(x >= 0 for x in d_dist) / B}
            res["H-A2"] = {"sets": len(c1), "C1_rate": sum(c1.values()) / len(c1), "ci95": ci(c1_dist),
                           "p_one_sided": sum(x >= 1 / 3 for x in c1_dist) / B}
            pvals[f"{model}|H-A1"], pvals[f"{model}|H-A2"] = res["H-A1"]["p_one_sided"], res["H-A2"]["p_one_sided"]
        report["models"][model] = res
    adj = holm(pvals)
    for key, p in adj.items():
        model, hyp = key.split("|")
        h = report["models"][model][hyp]
        h["p_holm"] = p
        h["supported"] = p < ALPHA and h["ci95"][1] < (0 if hyp == "H-A1" else 1 / 3)
    (args.out / "analysis.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    for model, res in report["models"].items():
        print(f"== {model}: invalid(main)={res['invalid_rate_main']:.3f} check={res['manipulation_check']}")
        for k, v in res["descriptive"].items():
            print(f"   {k:<12} rate={v['shared_choice_rate']:.3f} CI={[round(x, 3) for x in v['ci95']]} (sets={v['sets']})")
        print(f"   position rates: {res['position_choice_rate']}")
        for hyp in ("H-A1", "H-A2"):
            if hyp in res:
                h = res[hyp]
                est = h.get("diff_C1_minus_C0", h.get("C1_rate"))
                print(f"   {hyp}: est={est:.3f} CI={[round(x, 3) for x in h['ci95']]} p_holm={h['p_holm']:.4f} supported={h['supported']}")


if __name__ == "__main__":
    main()
