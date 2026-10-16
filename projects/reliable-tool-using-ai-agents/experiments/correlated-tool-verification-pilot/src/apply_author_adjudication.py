#!/usr/bin/env python3
"""Apply the author's adjudication (protocol Amendment A3) to coder A's survey-2 labels.

Author decisions (author_adjudication.xlsx): R1 count data-origin names behind an API (= coder A);
R2 do NOT count providers that are not used by default (coder A had counted them); R3 WSJ and
MarketWatch are two providers (= coder A); R4 brand names count (= coder A); cases C1-C4 all
= coder A. Only R2 changes labels: the names below were checked by reading each server's notes
and are optional or disabled by default. Following the author's stated reason ("a source that is
not used is not a source"), R2 is applied to L1 as well as L2.

Writes data/tool_survey_2/coding_adjudicated.csv (sensitivity input; the main analysis is
unchanged) and a post-hoc agreement with the AI-made organisation-level name merges.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tool_survey_2"
R2_REMOVE = {  # server_id: names that are not called by default
    "news/wudalu/mcp-hot-news-server": {"Kuaishou"},  # README table only; not in the default platform map
    "stock_quotes/yadinae/stock-mcp-server": {"Eastmoney", "Tongdaxin (TDX)"},  # selectable source / optional mootdx fallback
    "translation/kunalchhabra/translation-mcp-server": {"Ollama (local)"},  # alternative to default OpenAI
    "web_search/MemoryClear/claude-web-search-mcp": {"Bing", "SerpAPI"},  # disabled in default config
    "web_search/hpuhsp/web-search-mcp-server": {"Bing", "Brave Search"},  # "Optional: Bing, Brave"
}
MERGE = {  # AI-made organisation-level merges (sheet 3, all "Có"); post-hoc, agreement only
    "google maps platform": "google", "google books": "google",
    "amazon location service": "amazon web services", "eastmoney": "east money",
    "hacker news (y combinator)": "hacker news", "360 search": "qihoo 360",
    "grokipedia (xai)": "spacexai", "wikipedia": "wikimedia foundation",
    "fawazahmed0 exchange-api": "fawazahmed0", "baidu translate": "baidu",
    # survey-1 table (pre-specified)
    "openstreetmap": "openstreetmap nominatim", "sina": "sina finance", "tencent": "tencent finance",
    "searxng": "searxng (self-hosted)", "microsoft": "bing", "brave": "brave search",
    "fawazahmed0/exchange-api": "fawazahmed0 exchange-api",
}


def names(value: str) -> list[str]:
    return [p.strip() for p in value.split(";") if p.strip() and p.strip().lower() != "unknown"]


def norm(value: str) -> str:
    parts = sorted({MERGE.get(p.lower(), p.lower()) for p in names(value)})
    return "|".join(parts) or "unknown"


def kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def main() -> None:
    rows = list(csv.DictReader((DATA / "coding.csv").open(encoding="utf-8")))
    fields = list(rows[0])
    changed = []
    for r in rows:
        drop = R2_REMOVE.get(r["server_id"], set())
        for level in ("l1_declared_provider", "l2_declared_provider"):
            kept = [p for p in names(r[level]) if p not in drop]
            new = ";".join(kept) or "unknown"
            if new != (r[level] or "unknown") and names(r[level]) != kept:
                changed.append({"server_id": r["server_id"], "field": level, "before": r[level], "after": new})
                r[level] = new
    missing = set(R2_REMOVE) - {c["server_id"] for c in changed}
    if missing:
        raise SystemExit(f"R2 removal had no effect for {missing}")
    out = DATA / "coding_adjudicated.csv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    a = {r["server_id"]: r for f in ("coding.csv", "coding_agreement_only.csv")
         for r in csv.DictReader((DATA / f).open(encoding="utf-8"))}
    b = list(csv.DictReader((DATA / "coder_2_labels.csv").open(encoding="utf-8-sig")))
    agreement = {}
    for key in ("upstream_providers", "l1_declared_provider", "l2_declared_provider"):
        xa = [norm(a[r["server_id"]][key]) for r in b]
        xb = [norm(r[key]) for r in b]
        agreement[key] = {"agreement": sum(x == y for x, y in zip(xa, xb)) / len(b), "kappa": kappa(xa, xb),
                          "disagreements": [r["server_id"] for r, x, y in zip(b, xa, xb) if x != y]}
    summary = {"changed_labels": changed,
               "post_hoc_org_level_agreement_A_vs_coder2": agreement,
               "note": "post-hoc: organisation-level merges were made by Claude (AI), not approved by the author"}
    (DATA / "adjudication" / "adjudication_applied.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out} ({len(changed)} label changes)")
    for c in changed:
        print(f"  {c['server_id']} {c['field']}: {c['before']}  ->  {c['after']}")
    for k, v in agreement.items():
        print(f"agreement (org-level merges) {k}: {v['agreement']:.2f} (κ={v['kappa']:.2f})  disagree: {len(v['disagreements'])}")


if __name__ == "__main__":
    main()
