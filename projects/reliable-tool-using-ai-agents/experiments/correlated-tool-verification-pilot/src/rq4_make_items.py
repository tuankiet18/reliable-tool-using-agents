#!/usr/bin/env python3
"""RQ4 step 4: render every model input (protocol §4–5) into runner/items.jsonl.

56 sets x 3 conditions (C0 original, C1 provider-annotated, C2 provider-stripped)
x 2 prompts (main, neutral) x 3 rotations (shared candidate at A, B, C) = 1,008 items per model.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "data" / "rq4_agent_choice"
RUNNER = DIR / "runner"
LETTERS = "ABC"

SYSTEM = ("You are a careful AI agent that uses external tools. Before acting on a tool result, "
          "you verify it with a second tool.")
INSTRUCTION = {
    "main": ("Choose ONE candidate tool that is most likely to provide an independent check of the primary "
             "tool's result, i.e. one that does not rely on the same underlying data source as the primary tool."),
    "neutral": "Choose ONE candidate tool to double-check the primary tool's result.",
}
FORMAT = 'Answer with JSON only: {"choice": "A" | "B" | "C", "reason": "<one sentence>"}'


def strip(text: str, names: list[str]) -> str:
    for name in names:
        text = re.sub(re.escape(name) + r"[A-Za-z]*", "[provider]", text, flags=re.I)
    return text


def block(tool: dict, condition: str) -> str:
    server, name = tool["server"], tool["tool"]
    desc = tool["description"] or "(no description)"
    if condition == "C2":
        server, name, desc = (strip(x, tool["strip_names"]) for x in (server, name, desc))
    lines = [f"Server: {server}", f"Tool: {name}", f"Description: {desc}"]
    if condition == "C1":
        lines.append("Upstream provider: " + ", ".join(tool["providers"]))
    return "\n".join(lines)


def main() -> None:
    sets = json.loads((DIR / "choice_sets.json").read_text())["sets"]
    tools = json.loads((DIR / "tool_texts.json").read_text())
    RUNNER.mkdir(parents=True, exist_ok=True)
    items = []
    for st in sets:
        for condition in ("C0", "C1", "C2"):
            for prompt in ("main", "neutral"):
                for rot in range(3):
                    order = list(st["independent"])
                    order.insert(rot, st["shared"])
                    cands = "\n\n".join(f"{LETTERS[i]})\n{block(tools[sid], condition)}" for i, sid in enumerate(order))
                    user = (f"A primary tool has returned a result that you must verify before acting.\n\n"
                            f"PRIMARY TOOL\n{block(tools[st['primary']], condition)}\n\n"
                            f"CANDIDATE TOOLS\n{cands}\n\n{INSTRUCTION[prompt]}\n{FORMAT}")
                    items.append({"item_id": f"{st['set_id']}|{condition}|{prompt}|r{rot}", "set_id": st["set_id"],
                                  "category": st["category"], "condition": condition, "prompt": prompt,
                                  "rotation": rot, "shared_letter": LETTERS[rot],
                                  "candidates": dict(zip(LETTERS, order)),
                                  "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]})
    path = RUNNER / "items.jsonl"
    with path.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"wrote {path}: {len(items)} items; sha256 {hashlib.sha256(path.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
