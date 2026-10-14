#!/usr/bin/env python3
"""Shallow-clone repositories and statically scan them. Never executes repository code.

Usage: python3 -I scan.py <clone_dir> owner/repo [owner/repo ...]  -> one JSON line per repo
"""
import json, os, re, subprocess, sys
from pathlib import Path

SRC_EXT = {'.py', '.ts', '.js', '.mjs', '.cjs', '.go', '.rs', '.java', '.kt', '.cs', '.rb', '.php',
           '.properties', '.yml', '.yaml', '.toml', '.example'}
SKIP_DIRS = {'node_modules', '.git', 'dist', 'build', 'test', 'tests', '__tests__', 'examples', 'example',
             'docs', '.github', 'vendor'}
URL = re.compile(r'https?://([A-Za-z0-9.-]+\.[A-Za-z]{2,})')
NOISE = ('github.com', 'localhost', '127.0.0.1', 'modelcontextprotocol.io', 'npmjs', 'pypi.org', 'schema.org',
         'json-schema.org', 'w3.org', 'example.com', 'githubusercontent.com', 'shields.io', 'opensource.org',
         'apache.org', 'mozilla.org', 'readthedocs')
MCP = re.compile(r'(@modelcontextprotocol/sdk|from mcp|import mcp|FastMCP|fastmcp|mcp\.server|McpServer|mcp-go|rmcp|modelcontextprotocol|mcp-core|spring-ai-mcp|tools/list)')
TOOL = re.compile(r'(server\.tool\(|\.tool\(|@mcp\.tool|@server\.tool|@app\.tool|registerTool|mcp\.NewTool|@Tool\(|Tool\(\s*name|ListToolsRequestSchema|#\[tool)')


def main() -> None:
    repos = Path(sys.argv[1]); repos.mkdir(parents=True, exist_ok=True)
    for full in sys.argv[2:]:
        d = repos / full.replace('/', '__')
        if not d.exists():
            r = subprocess.run(['git', 'clone', '-q', '--depth', '1', f'https://github.com/{full}.git', str(d)],
                               capture_output=True, text=True, timeout=180, env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'})
            if r.returncode:
                print(json.dumps({'repo': full, 'error': r.stderr.strip()[:200]})); continue
        sha = subprocess.run(['git', '-C', str(d), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        hosts, mcp, tools, nsrc = {}, set(), [], 0
        for p in d.rglob('*'):
            if not p.is_file() or p.suffix not in SRC_EXT or any(x in SKIP_DIRS for x in p.relative_to(d).parts):
                continue
            nsrc += 1
            try:
                lines = p.read_text(errors='ignore').splitlines()
            except Exception:
                continue
            rel = str(p.relative_to(d))
            for i, line in enumerate(lines, 1):
                for h in URL.findall(line):
                    if not any(n in h for n in NOISE):
                        hosts.setdefault(h.lower(), f'{rel}:{i}')
                if MCP.search(line):
                    mcp.add(rel)
                if TOOL.search(line) and len(tools) < 6:
                    tools.append(f'{rel}:{i}: {line.strip()[:110]}')
        print(json.dumps({'repo': full, 'sha': sha, 'src_files': nsrc, 'mcp_files': len(mcp), 'hosts': hosts,
                          'tool_lines': tools}, ensure_ascii=False))


if __name__ == '__main__':
    main()
