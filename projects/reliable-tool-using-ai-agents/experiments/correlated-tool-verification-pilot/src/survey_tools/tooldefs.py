#!/usr/bin/env python3
"""Print agent-visible tool-definition blocks (server name, tool names, descriptions). Static read only.

Usage: python3 -I tooldefs.py <repo_dir> [lines_per_block]
"""
import re, sys
from pathlib import Path

SRC = {'.py', '.ts', '.js', '.mjs', '.go', '.rs', '.java', '.kt', '.cs'}
SKIP = {'node_modules', '.git', 'dist', 'build', 'test', 'tests', '__tests__', 'docs', 'examples', 'vendor'}
START = re.compile(r'(@(mcp|server|app)\.tool|\.tool\(|registerTool|mcp\.NewTool|@Tool\(|FastMCP\(|new (Mcp)?Server\(|McpServer\(|Server\(\s*\{|ListToolsRequestSchema|name:\s*["\'][\w-]+["\'],?\s*$|"name":\s*"[\w-]+"|#\[tool|Tool\s*\{|tool\(name|Tool\(\s*$|Tool\(\s*name)')


def main() -> None:
    repo = Path(sys.argv[1]); maxlines = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    seen = 0
    for p in sorted(repo.rglob('*')):
        if not p.is_file() or p.suffix not in SRC or any(x in SKIP for x in p.relative_to(repo).parts):
            continue
        if 'test' in p.name.lower():
            continue
        lines = p.read_text(errors='ignore').splitlines()
        i = 0
        while i < len(lines):
            if START.search(lines[i]):
                print(f'--- {p.relative_to(repo)}:{i + 1}')
                for line in lines[i:i + maxlines]:
                    print('   ', line.rstrip()[:150])
                seen += 1; i += maxlines
                if seen >= 16:
                    return
            else:
                i += 1


if __name__ == '__main__':
    main()
