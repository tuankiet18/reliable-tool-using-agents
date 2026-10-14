#!/usr/bin/env python3
"""Inter-rater agreement between coder A (AI) and coder B (human) for survey 1.

Reports exact-string agreement and agreement after a name-normalisation table. The table
only merges spelling/naming variants of the SAME organisation or service; it never merges
different constructs (e.g. a CDN host vs the dataset owner, or 'ambiguous' vs a name).
For survey 1 this table was written after seeing both files (survey 1's protocol did not
pre-specify one) and is therefore reported alongside the exact-string result.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME_MAP = {  # variant (lower-case) -> canonical (lower-case)
    "openstreetmap": "openstreetmap nominatim",
    "sina": "sina finance",
    "tencent": "tencent finance",
    "searxng": "searxng (self-hosted)",
    "microsoft": "bing",          # Bing is operated by Microsoft
    "brave": "brave search",
    "fawazahmed0/exchange-api": "fawazahmed0 exchange-api",
}


def labels(value: str, normalise: bool) -> str:
    parts = [p.strip() for p in value.split(";") if p.strip()]
    if normalise:
        parts = [NAME_MAP.get(p.lower(), p.lower()) for p in parts]
    return "|".join(sorted(parts)) or "unknown"


def kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", type=Path, default=ROOT / "data" / "tool_survey" / "coding.csv")
    parser.add_argument("--b", type=Path, default=ROOT / "data" / "tool_survey" / "coder_b_labels.csv")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    a = {r["server_id"]: r for r in csv.DictReader(args.a.open(encoding="utf-8"))}
    b = [r for r in csv.DictReader(args.b.open(encoding="utf-8")) if r["upstream_providers"].strip()]
    out = {"servers": len(b), "name_map": NAME_MAP, "fields": {}, "disagreements": []}
    for field, key in (("upstream", "upstream_providers"), ("l1", "l1_declared_provider"), ("l2", "l2_declared_provider")):
        res = {}
        for mode, norm in (("exact", False), ("normalised", True)):
            xa = [labels(a[r["server_id"]][key], norm) for r in b]
            xb = [labels(r[key], norm) for r in b]
            res[mode] = {"agreement": sum(x == y for x, y in zip(xa, xb)) / len(b), "kappa": kappa(xa, xb)}
            if mode == "normalised":
                for r, x, y in zip(b, xa, xb):
                    if x != y:
                        out["disagreements"].append({"server_id": r["server_id"], "field": field, "A": x, "B": y})
        out["fields"][field] = res
    # L1 presence (known vs unknown) is what the selector model uses
    pa = ["known" if labels(a[r["server_id"]]["l1_declared_provider"], True) != "unknown" else "unknown" for r in b]
    pb = ["known" if labels(r["l1_declared_provider"], True) != "unknown" else "unknown" for r in b]
    out["fields"]["l1_presence"] = {"agreement": sum(x == y for x, y in zip(pa, pb)) / len(b), "kappa": kappa(pa, pb)}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "agreement.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    for f, r in out["fields"].items():
        if "exact" in r:
            print(f"{f:<9} exact {r['exact']['agreement']:.2f} (κ={r['exact']['kappa']:.2f})   normalised {r['normalised']['agreement']:.2f} (κ={r['normalised']['kappa']:.2f})")
        else:
            k = "n/a" if r["kappa"] is None else f"{r['kappa']:.2f}"
            print(f"{f:<9} agreement {r['agreement']:.2f} (κ={k})")
    for d in out["disagreements"]:
        print("DISAGREE", d)


if __name__ == "__main__":
    main()
