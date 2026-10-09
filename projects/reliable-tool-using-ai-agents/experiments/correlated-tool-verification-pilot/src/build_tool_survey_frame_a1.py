#!/usr/bin/env python3
"""Amendment A1 to the tool-survey sampling frame.

For every category whose original query returned fewer than 30 results, run exactly
one pre-specified alternate query (same sort/limit) and append its results after the
original list, dropping repositories already present. The original frame file is not
modified; this writes a separate amendment file. Decided before any repository code
was read (see the protocol's lock log).
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from build_tool_survey_frame import LIMIT, search

ALTERNATE_QUERIES = {
    "currency_exchange": "exchange rate mcp",
    "geocoding": "geocode mcp",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frame", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit(f"refusing to overwrite existing amendment: {args.out}")

    frame_bytes = args.frame.read_bytes()
    frame = json.loads(frame_bytes)
    thin = [c for c, v in frame["categories"].items() if len(v["results"]) < LIMIT]
    if sorted(thin) != sorted(ALTERNATE_QUERIES):
        raise SystemExit(f"thin categories {thin} do not match pre-specified {list(ALTERNATE_QUERIES)}")

    amendment = {
        "amendment": "A1",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_frame_sha256": hashlib.sha256(frame_bytes).hexdigest(),
        "rule": "categories with < 30 original results get one alternate query; results appended after the original list, duplicates dropped",
        "categories": {},
    }
    for category, query in ALTERNATE_QUERIES.items():
        original = frame["categories"][category]["results"]
        seen = {item["fullName"].lower() for item in original}
        added, duplicates = [], []
        for item in search(query):
            if item["fullName"].lower() in seen:
                duplicates.append(item["fullName"])
                continue
            seen.add(item["fullName"].lower())
            added.append(item)
        start = len(original) + 1
        amendment["categories"][category] = {
            "query": query,
            "duplicates_dropped": duplicates,
            "appended_results": [
                {"rank": start + i, "server_id": f"{category}/{item['fullName']}", **item}
                for i, item in enumerate(added)
            ],
        }
        print(f"{category:<18} query={query!r}: appended {len(added)}, duplicates {len(duplicates)}")

    args.out.write_text(json.dumps(amendment, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {args.out}\nsha256 {hashlib.sha256(args.out.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
