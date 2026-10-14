#!/usr/bin/env python3
"""Apply author-approved screening corrections and merge coder A's partial labels (survey 2).

1. Rewrites `data/tool_survey_2/screening.csv` with the corrections in
   `coding_partial/screening_corrections.json` (protocol §4: errors found while coding are fixed
   in rank order). The pre-correction file is in git history; its SHA-256 is in protocol §9.
2. Merges `coding_partial/<category>.json` into `coding.csv` (every `include` server, used for
   estimates) and `coding_agreement_only.csv` (servers excluded after the human-coder subset was
   frozen; coded only so agreement covers the full subset, never used in estimates).

Computes no metric. Refuses to run twice.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tool_survey_2"
CODER = "A (Claude, AI-assisted)"
COLUMNS = ["server_id", "category", "repo_url", "commit_sha", "upstream_providers", "upstream_evidence",
           "configurable_upstream", "l1_declared_provider", "l1_evidence", "l2_declared_provider",
           "l2_evidence", "origin_a", "origin_a_evidence", "coder", "notes"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def apply_corrections(screening: list[dict], corrections: list[dict]) -> list[dict]:
    by_id = {row["server_id"]: row for row in screening}
    order = list(dict.fromkeys(row["category"] for row in screening))
    for c in corrections:
        row = by_id[c["server_id"]]
        if row["decision"] != c["old_decision"]:
            raise SystemExit(f"already applied or unexpected decision: {c['server_id']}")
        row["decision"] = c["new_decision"]
        row["reason"] = f"screening correction during coding (protocol §4): {c['reason']}"
        new = [dict(n, reason=n["reason"]) for n in c.get("newly_screened", [])]
        rep = c["replacement"]
        new.append({**rep, "decision": "include", "reason": f"replacement for {c['server_id']}: {rep['reason']}"})
        for n in new:
            if n["server_id"] in by_id:
                raise SystemExit(f"already screened: {n['server_id']}")
            owner_repo = n["server_id"].split("/", 1)[1]
            by_id[n["server_id"]] = {
                "category": c["category"], "rank": str(n["rank"]), "server_id": n["server_id"],
                "repo_url": n.get("repo_url", f"https://github.com/{owner_repo}"),
                "commit_sha": n["commit_sha"], "decision": n["decision"], "reason": n["reason"],
            }
    return sorted(by_id.values(), key=lambda r: (order.index(r["category"]), int(r["rank"])))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DATA)
    args = parser.parse_args()
    screening_path = args.data / "screening.csv"
    partial = args.data / "coding_partial"
    corrections = json.loads((partial / "screening_corrections.json").read_text())
    for out in ("coding.csv", "coding_agreement_only.csv"):
        if (args.data / out).exists():
            raise SystemExit(f"refusing to overwrite {out}")

    print(f"screening before: sha256 {sha(screening_path)}")
    screening = list(csv.DictReader(screening_path.open(encoding="utf-8")))
    fields = list(screening[0])
    screening = apply_corrections(screening, corrections)
    with screening_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(screening)
    print(f"screening after:  sha256 {sha(screening_path)}  ({len(screening)} rows)")

    meta = {row["server_id"]: row for row in screening}
    include = {sid for sid, row in meta.items() if row["decision"] == "include"}
    agreement_only = {c["server_id"] for c in corrections if c.get("human_subset_affected")}
    human = {row["server_id"] for row in csv.DictReader((args.data / "human_coder_template.csv").open(encoding="utf-8"))}

    coded = {}
    for path in sorted(partial.glob("*.json")):
        if path.name == "screening_corrections.json":
            continue
        for row in json.loads(path.read_text()):
            if row["server_id"] in coded:
                raise SystemExit(f"duplicate label: {row['server_id']}")
            coded[row["server_id"]] = row
    if set(coded) != include | agreement_only:
        raise SystemExit(f"label set mismatch: missing {sorted(include - set(coded))}, "
                         f"extra {sorted(set(coded) - include - agreement_only)}")
    if not human <= set(coded):
        raise SystemExit(f"human subset not fully coded: {sorted(human - set(coded))}")

    for name, ids in (("coding.csv", include), ("coding_agreement_only.csv", agreement_only)):
        path = args.data / name
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS)
            writer.writeheader()
            for sid in sorted(ids, key=lambda s: (meta[s]["category"], int(meta[s]["rank"]))):
                row = coded[sid]
                writer.writerow({**{k: row.get(k, "") for k in COLUMNS}, "category": meta[sid]["category"],
                                 "repo_url": meta[sid]["repo_url"], "commit_sha": meta[sid]["commit_sha"],
                                 "configurable_upstream": str(row["configurable_upstream"]), "coder": CODER})
        print(f"{name}: {len(ids)} servers  sha256 {sha(path)}")
    print(f"human subset: {len(human)} servers, all coded ({len(human & agreement_only)} agreement-only)")


if __name__ == "__main__":
    main()
