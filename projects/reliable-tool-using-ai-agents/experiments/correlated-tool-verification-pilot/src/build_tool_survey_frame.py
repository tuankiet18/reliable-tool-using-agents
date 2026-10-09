#!/usr/bin/env python3
"""Build the frozen sampling frame for the real-tool failure-domain metadata survey.

Implements §3 of `synthesis/Protocol: Real-Tool Failure-Domain Metadata Survey.md`:
for each information type, run the fixed GitHub repository search
"<keyword> mcp server" sorted by stars (descending) and store the first 30 results
verbatim, with the query and timestamp, BEFORE any repository code is read.

Requires an authenticated `gh` CLI. GitHub search results drift over time, so this
script is a record of how the frame was made, not a way to regenerate it exactly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

CATEGORIES = {
    "weather": "weather",
    "currency_exchange": "currency exchange",
    "stock_quotes": "stock",
    "crypto_prices": "crypto",
    "geocoding": "geocoding",
    "web_search": "web search",
    "news": "news",
}
FIELDS = "fullName,url,description,stargazersCount,isFork,isArchived,updatedAt,defaultBranch,language"
LIMIT = 30


def search(query: str) -> list[dict]:
    out = subprocess.run(
        ["gh", "search", "repos", query, "--sort", "stars", "--order", "desc",
         "--limit", str(LIMIT), "--json", FIELDS],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit(f"refusing to overwrite existing frame: {args.out}")

    frame = {
        "protocol": "synthesis/Protocol: Real-Tool Failure-Domain Metadata Survey.md v1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "search": {"tool": "gh search repos", "sort": "stars", "order": "desc", "limit": LIMIT},
        "server_id_rule": "<category>/<owner>/<repo>",
        "coder_b_subset_rule": "10 included servers with the smallest sha256(server_id) hex",
        "categories": {},
    }
    for category, keyword in CATEGORIES.items():
        query = f"{keyword} mcp server"
        results = search(query)
        frame["categories"][category] = {
            "query": query,
            "results": [
                {"rank": rank, "server_id": f"{category}/{item['fullName']}", **item}
                for rank, item in enumerate(results, start=1)
            ],
        }
        print(f"{category:<18} {len(results):>3} results  query={query!r}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(frame, indent=2, ensure_ascii=False) + "\n")
    digest = hashlib.sha256(args.out.read_bytes()).hexdigest()
    print(f"wrote {args.out}\nsha256 {digest}")


if __name__ == "__main__":
    main()
