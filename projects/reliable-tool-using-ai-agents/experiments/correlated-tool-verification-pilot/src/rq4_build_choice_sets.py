#!/usr/bin/env python3
"""RQ4 step 1: build the choice sets (protocol "Agent Corroborator Choice with Real Tool Metadata" §3).

For every usable primary (same survey and information type; >=1 server sharing an operator-level
provider and >=2 independent servers; AMBIGUOUS servers and servers without a resolved upstream
excluded) draw one shared and two independent candidates with seed 20261018.
"""

from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "rq4_agent_choice"
SEED = 20261018
SOURCES = (("s1", ROOT / "data" / "tool_survey" / "coding.csv"), ("s2", ROOT / "data" / "tool_survey_2" / "coding.csv"))
REPORT_ONLY_S2 = {"geocoding", "ip_geolocation"}


def providers(value: str) -> frozenset[str]:
    return frozenset(p.strip() for p in value.split(";") if p.strip() and p.strip().lower() not in ("unknown", "ambiguous"))


def main() -> None:
    rows = []
    for survey, path in SOURCES:
        for r in csv.DictReader(path.open(encoding="utf-8")):
            if survey == "s2" and r["category"] in REPORT_ONLY_S2:
                continue
            if "AMBIGUOUS" in r["notes"] or not providers(r["upstream_providers"]):
                continue
            rows.append({"survey": survey, "server_id": r["server_id"], "category": r["category"],
                         "repo_url": r["repo_url"], "commit_sha": r["commit_sha"],
                         "providers": sorted(providers(r["upstream_providers"]))})
    groups = defaultdict(list)
    for r in rows:
        groups[(r["survey"], r["category"])].append(r)
    rng = random.Random(SEED)
    sets = []
    for key in sorted(groups):
        members = sorted(groups[key], key=lambda r: r["server_id"])
        for primary in members:
            p = set(primary["providers"])
            shared = [m for m in members if m is not primary and p & set(m["providers"])]
            indep = [m for m in members if m is not primary and not p & set(m["providers"])]
            if not shared or len(indep) < 2:
                continue
            s = rng.choice(shared)
            i1, i2 = rng.sample(indep, 2)
            sets.append({"set_id": f"{key[0]}-{len(sets) + 1:02d}", "survey": key[0], "category": key[1],
                         "primary": primary["server_id"], "shared": s["server_id"],
                         "independent": [i1["server_id"], i2["server_id"]]})
    servers = {r["server_id"]: r for r in rows}
    needed = sorted({sid for st in sets for sid in [st["primary"], st["shared"], *st["independent"]]})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "choice_sets.json").write_text(json.dumps({"seed": SEED, "sets": sets}, indent=2) + "\n")
    (OUT / "servers_needed.json").write_text(json.dumps([servers[s] for s in needed], indent=2) + "\n")
    print(f"{len(sets)} choice sets; {len(needed)} servers need tool text")


if __name__ == "__main__":
    main()
