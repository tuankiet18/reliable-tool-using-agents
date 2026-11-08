#!/usr/bin/env python3
"""RQ4 secondary breakdowns promised by protocol sec. 2 and 7 (descriptive only, no hypothesis tests):

1. shared-choice rate by information type (category), per model, prompt and condition;
2. share of `reason` strings that mention the data source, by prompt and condition, and for
   the neutral-prompt C1 cells split by whether the model chose the shared candidate.

The keyword rule for (2) was fixed in this script AFTER the main RQ4 results were known (2026-11-08);
it is a crude lexical rule, not a human or model judgement of the reasoning.

Usage: python3 rq4_breakdowns.py --results r1.jsonl [r2.jsonl ...] --out <new dir>
"""

from __future__ import annotations

import argparse
import json
import random
import re
from collections import defaultdict
from pathlib import Path

from rq4_analyze import B, ITEMS, SEED, boot, ci, load, set_rates  # reuse the locked loader

SOURCE_RE = re.compile(r"\b(provider|upstream|data ?source|underlying|same (?:api|source|provider|data|backend)|"
                       r"different (?:api|source|provider|data|backend)|sources?)\b", re.I)
PROVIDER_RE = re.compile(r"\b(provider|upstream)\b", re.I)
INDEP_RE = re.compile(r"\b(independent|independence|different|distinct|diversif\w*)\b", re.I)


def mean(v):
    return sum(v) / len(v) if v else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", nargs="+", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    items = {json.loads(l)["item_id"]: json.loads(l) for l in ITEMS.open(encoding="utf-8")}
    out = {"seed": SEED, "bootstrap": B, "note": "descriptive; keyword rule set after main results"}
    for path in args.results:
        model, _, rows = load(path, items)
        res = {}
        # 1. by category
        cats = sorted({r["category"] for r in rows})
        by_cat = {}
        for cat in cats:
            sub = [r for r in rows if r["category"] == cat]
            sets = sorted({r["set_id"] for r in sub})
            entry = {"sets": len(sets)}
            rng = random.Random(SEED)
            for prompt in ("main", "neutral"):
                for cond in ("C0", "C1", "C2"):
                    rates = set_rates(sub, cond, prompt)
                    vals = list(rates.values())
                    key = f"{prompt}/{cond}"
                    entry[key] = {"rate": mean(vals)}
                    if len(vals) >= 3:
                        entry[key]["ci95"] = ci(boot(vals, rng))
            by_cat[cat] = entry
        res["by_category"] = by_cat
        # 2. reasons
        reasons = {}
        for prompt in ("main", "neutral"):
            for cond in ("C0", "C1", "C2"):
                sub = [r for r in rows if r["prompt"] == prompt and r["condition"] == cond and r["valid"]]
                texts = [r["attempts"][-1]["raw"] for r in sub]
                parsed = []
                for t in texts:
                    try:
                        parsed.append(str(json.loads(t).get("reason", "")))
                    except (json.JSONDecodeError, AttributeError):
                        parsed.append("")
                reasons[f"{prompt}/{cond}"] = {
                    "n": len(sub),
                    "mentions_source": mean([1.0 if SOURCE_RE.search(x) else 0.0 for x in parsed]),
                    "mentions_provider_word": mean([1.0 if PROVIDER_RE.search(x) else 0.0 for x in parsed]),
                    "mentions_independence": mean([1.0 if INDEP_RE.search(x) else 0.0 for x in parsed]),
                }
        res["reason_keywords"] = reasons
        split = {}
        for prompt in ("main", "neutral"):
            for chose_shared in (True, False):
                sub = [r for r in rows if r["prompt"] == prompt and r["condition"] == "C1" and r["valid"]
                       and r["chose_shared"] is chose_shared]
                parsed = []
                for r in sub:
                    try:
                        parsed.append(str(json.loads(r["attempts"][-1]["raw"]).get("reason", "")))
                    except (json.JSONDecodeError, AttributeError):
                        parsed.append("")
                split[f"{prompt}/C1/chose_shared={chose_shared}"] = {
                    "n": len(sub),
                    "mentions_source": mean([1.0 if SOURCE_RE.search(x) else 0.0 for x in parsed]),
                    "mentions_provider_word": mean([1.0 if PROVIDER_RE.search(x) else 0.0 for x in parsed]),
                }
        res["C1_reason_by_choice"] = split
        out[model] = res
    (args.out / "breakdowns.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
