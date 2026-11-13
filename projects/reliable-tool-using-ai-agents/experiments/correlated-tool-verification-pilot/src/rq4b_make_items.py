#!/usr/bin/env python3
"""RQ4-ext step: render the model inputs of "Protocol - LLM Corroborator Choice Mechanism and Label Inversion"
into runner/items_b.jsonl.

Cells (prompt x condition), each 56 sets x 3 rotations = 168 items:
  main, neutral:  C0, C1 (identical text to items.jsonl; flagged new=false), C4 (new)
  consistency:    C0, C1, C4 (all new)
C4 = inverted labels: the truly shared candidate gets a decoy provider (taken from another set of the same
category, never a provider of any tool in this set); exactly one truly independent candidate (chosen by seed)
gets the primary's provider; the other independent candidate and the primary keep their true provider.
Sets without a usable decoy are excluded from C4 (listed in items_b_report.json).
"""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

from rq4_make_items import DIR, FORMAT, INSTRUCTION, LETTERS, RUNNER, SYSTEM, block

SEED = 20261112
INSTRUCTION = {**INSTRUCTION,
               "consistency": ("Choose ONE candidate tool whose result is most likely to be consistent with the "
                               "primary tool's result.")}


def render(tool: dict, condition: str, providers: list[str] | None) -> str:
    if condition == "C4":
        server, name = tool["server"], tool["tool"]
        desc = tool["description"] or "(no description)"
        return "\n".join([f"Server: {server}", f"Tool: {name}", f"Description: {desc}",
                          "Upstream provider: " + ", ".join(providers)])
    return block(tool, condition)


def decoy_for(st: dict, tools: dict) -> list[str] | None:
    own = {p.lower() for sid in [st["primary"], st["shared"], *st["independent"]] for p in tools[sid]["providers"]}
    members = {st["primary"], st["shared"], *st["independent"]}
    pool = []
    for sid, t in sorted(tools.items()):
        if sid.split("/")[0] != st["category"] or sid in members:
            continue
        if any(p.lower() in own for p in t["providers"]):
            continue
        pool.append(t["providers"])
    if not pool:
        return None
    return random.Random(f"{SEED}|{st['set_id']}|decoy").choice(pool)


def main() -> None:
    sets = json.loads((DIR / "choice_sets.json").read_text(encoding="utf-8"))["sets"]
    tools = json.loads((DIR / "tool_texts.json").read_text(encoding="utf-8"))
    old = {}
    for line in (RUNNER / "items.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        old[r["item_id"]] = r
    cells = [("main", "C0", False), ("main", "C1", False), ("main", "C4", True),
             ("neutral", "C0", False), ("neutral", "C1", False), ("neutral", "C4", True),
             ("consistency", "C0", True), ("consistency", "C1", True), ("consistency", "C4", True)]
    items, report = [], {"seed": SEED, "no_decoy_sets": [], "c4_sets": 0}
    for st in sets:
        decoy = decoy_for(st, tools)
        if decoy is None:
            report["no_decoy_sets"].append(st["set_id"])
        else:
            report["c4_sets"] += 1
        mimic = random.Random(f"{SEED}|{st['set_id']}|mimic").choice(st["independent"])
        label = {st["primary"]: tools[st["primary"]]["providers"], st["shared"]: decoy or [],
                 mimic: tools[st["primary"]]["providers"]}
        for sid in st["independent"]:
            label.setdefault(sid, tools[sid]["providers"])
        for prompt, condition, new in cells:
            if condition == "C4" and decoy is None:
                continue
            for rot in range(3):
                order = list(st["independent"])
                order.insert(rot, st["shared"])
                cands = "\n\n".join(f"{LETTERS[i]})\n{render(tools[sid], condition, label.get(sid))}"
                                    for i, sid in enumerate(order))
                user = (f"A primary tool has returned a result that you must verify before acting.\n\n"
                        f"PRIMARY TOOL\n{render(tools[st['primary']], condition, label[st['primary']])}\n\n"
                        f"CANDIDATE TOOLS\n{cands}\n\n{INSTRUCTION[prompt]}\n{FORMAT}")
                item_id = f"{st['set_id']}|{condition}|{prompt}|r{rot}"
                same_label = {"C0": None, "C1": LETTERS[rot], "C4": LETTERS[order.index(mimic)]}[condition]
                item = {"item_id": item_id, "set_id": st["set_id"], "category": st["category"],
                        "condition": condition, "prompt": prompt, "rotation": rot, "shared_letter": LETTERS[rot],
                        "labelled_same_letter": same_label, "new": new,
                        "candidates": dict(zip(LETTERS, order)),
                        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}
                if not new:  # must be byte-identical to the already-run RQ4 item
                    assert old[item_id]["messages"] == item["messages"], item_id
                items.append(item)
    path = RUNNER / "items_b.jsonl"
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    report["items"] = len(items)
    report["new_items"] = sum(1 for i in items if i["new"])
    report["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    (RUNNER / "items_b_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
