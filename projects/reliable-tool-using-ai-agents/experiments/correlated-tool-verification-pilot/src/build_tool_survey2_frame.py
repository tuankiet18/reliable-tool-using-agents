#!/usr/bin/env python3
"""Build the frozen sampling frame for survey 2 (protocol §3).

For each of 12 information types: run "<keyword> mcp server" sorted by stars, top 50.
If it returns fewer than 30 results, run exactly one pre-specified alternate query and
append its results (duplicates dropped). Repositories already considered in survey 1
are kept in the record but flagged `excluded_survey1` so screening skips them.
Written and run before any survey-2 repository code is read.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = "fullName,url,description,stargazersCount,isFork,isArchived,updatedAt,defaultBranch,language"
LIMIT = 50
THIN = 30
CATEGORIES = {  # category: (primary keyword, alternate query)
    "weather": ("weather", "weather mcp"),
    "currency_exchange": ("currency exchange", "exchange rate mcp"),
    "stock_quotes": ("stock", "stock price mcp"),
    "crypto_prices": ("crypto", "crypto price mcp"),
    "geocoding": ("geocoding", "geocode mcp"),
    "web_search": ("web search", "search engine mcp"),
    "news": ("news", "news api mcp"),
    "translation": ("translation", "translate mcp"),
    "ip_geolocation": ("ip geolocation", "ip lookup mcp"),
    "movies": ("movie", "tmdb mcp"),
    "books": ("books", "book search mcp"),
    "air_quality": ("air quality", "aqi mcp"),
}


def search(query: str) -> list[dict]:
    out = subprocess.run(
        ["gh", "search", "repos", query, "--sort", "stars", "--order", "desc",
         "--limit", str(LIMIT), "--json", FIELDS],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--survey1-screening", type=Path, default=ROOT / "data" / "tool_survey" / "screening.csv")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit(f"refusing to overwrite existing frame: {args.out}")

    survey1 = {row["repo_url"].rstrip("/").split("github.com/")[1].lower()
               for row in csv.DictReader(args.survey1_screening.open(encoding="utf-8"))}
    frame = {
        "protocol": "synthesis/Protocol: Expanded Real-Tool Metadata Survey.md v1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "search": {"tool": "gh search repos", "sort": "stars", "order": "desc", "limit": LIMIT, "thin_threshold": THIN},
        "server_id_rule": "<category>/<owner>/<repo>",
        "survey1_repos_excluded": len(survey1),
        "human_subset_rule": "at least 20 included servers with the smallest sha256(server_id) hex",
        "categories": {},
    }
    for category, (keyword, alternate) in CATEGORIES.items():
        primary_query = f"{keyword} mcp server"
        results = search(primary_query)
        queries = [primary_query]
        if len(results) < THIN:
            seen = {r["fullName"].lower() for r in results}
            for item in search(alternate):
                if item["fullName"].lower() not in seen:
                    seen.add(item["fullName"].lower())
                    results.append(item)
            queries.append(alternate)
        records = []
        for rank, item in enumerate(results, start=1):
            records.append({"rank": rank, "server_id": f"{category}/{item['fullName']}",
                            "excluded_survey1": item["fullName"].lower() in survey1, **item})
        frame["categories"][category] = {"queries": queries, "results": records}
        n_ex = sum(r["excluded_survey1"] for r in records)
        print(f"{category:<18} {len(records):>3} results ({n_ex} from survey 1)  queries={queries}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(frame, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {args.out}\nsha256 {hashlib.sha256(args.out.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
