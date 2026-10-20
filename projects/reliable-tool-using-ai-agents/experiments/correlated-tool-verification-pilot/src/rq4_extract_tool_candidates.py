#!/usr/bin/env python3
"""RQ4 step 2 (helper): list candidate tool definitions (name, description, file:line) per repo.

Static read only; heuristics for FastMCP decorators + docstrings, server.tool("n","d"),
registerTool("n",{description}), Tool(name=..., description=...), and {name, description} objects.
Output is reviewed by hand; the curated texts are written to data/rq4_agent_choice/tool_texts.json.
Usage: python3 rq4_extract_tool_candidates.py <repos_dir> <out.json>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SRC = {".py", ".ts", ".js", ".mjs", ".cjs", ".go", ".rs", ".java", ".kt", ".cs"}
SKIP = {"node_modules", ".git", "dist", "build", "test", "tests", "__tests__", "docs", "examples", "vendor", ".venv", "venv"}
STR = r'(?:"""(.*?)"""|\'\'\'(.*?)\'\'\'|"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'|`((?:[^`\\]|\\.)*)`)'
PATTERNS = [
    # FastMCP / decorator followed by def + docstring
    re.compile(r'@\w+\.tool\((?P<args>[^)]*)\)\s*(?:@[^\n]*\n\s*)*(?:async\s+)?def\s+(?P<name>\w+)\s*\((?P<sig>.*?)\)[^:]*:\s*' + STR, re.S),
    # server.tool("name", "description", ...)
    re.compile(r'\.tool\(\s*' + r'["\'`](?P<name>[\w.-]+)["\'`]\s*,\s*' + STR, re.S),
    # registerTool("name", { ... description: "..." })
    re.compile(r'registerTool\(\s*["\'`](?P<name>[\w.-]+)["\'`]\s*,\s*\{.*?description\s*:\s*' + STR, re.S),
    # Tool(name="x", description="y") / types.Tool(...)
    re.compile(r'Tool\(\s*name\s*=\s*["\'](?P<name>[\w.-]+)["\']\s*,\s*description\s*=\s*' + STR, re.S),
    # { name: "x", description: "y" } objects (TS/JS tool lists)
    re.compile(r'name\s*:\s*["\'`](?P<name>[\w.-]+)["\'`]\s*,\s*(?:title\s*:\s*["\'`][^"\'`]*["\'`]\s*,\s*)?description\s*:\s*' + STR, re.S),
    # "name": "x", "description": "y" (JSON-style)
    re.compile(r'"name"\s*:\s*"(?P<name>[\w.-]+)"\s*,\s*"description"\s*:\s*' + STR, re.S),
]
SERVER_NAME = re.compile(r'(?:FastMCP|McpServer|Server)\(\s*(?:name\s*=\s*|\{\s*name\s*:\s*)?["\'`]([^"\'`]+)["\'`]')


def first_group(m: re.Match) -> str:
    """The description is the last non-empty capture (the string literal)."""
    vals = [v for v in m.groups() if v is not None]
    return vals[-1] if vals else ""


def scan(repo: Path) -> dict:
    tools, names = [], []
    for p in sorted(repo.rglob("*")):
        if not p.is_file() or p.suffix not in SRC or any(x in SKIP for x in p.relative_to(repo).parts):
            continue
        if "test" in p.name.lower():
            continue
        src = p.read_text(errors="ignore")
        for m in SERVER_NAME.finditer(src):
            names.append(m.group(1))
        for pat in PATTERNS:
            for m in pat.finditer(src):
                desc = first_group(m)
                desc = re.sub(r"\s+", " ", desc).strip()
                line = src.count("\n", 0, m.start()) + 1
                tools.append({"tool": m.group("name"), "description": desc[:600], "at": f"{p.relative_to(repo)}:{line}"})
    seen, uniq = set(), []
    for t in tools:
        k = (t["tool"], t["at"])
        if k not in seen:
            seen.add(k)
            uniq.append(t)
    return {"server_names": sorted(set(names)), "tools": uniq}


def main() -> None:
    repos, out = Path(sys.argv[1]), Path(sys.argv[2])
    result = {}
    for d in sorted(repos.iterdir()):
        if (d / ".git").exists():
            result[d.name.replace("__", "/")] = scan(d)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    empty = [k for k, v in result.items() if not v["tools"]]
    print(f"{len(result)} repos; {len(empty)} with no candidate found")
    for k in empty:
        print("  none:", k)


if __name__ == "__main__":
    main()
