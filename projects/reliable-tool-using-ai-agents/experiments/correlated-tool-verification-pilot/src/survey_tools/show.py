#!/usr/bin/env python3
"""One-line summary per scan.py JSON line."""
import json, sys
for line in open(sys.argv[1]):
    d = json.loads(line)
    if 'error' in d:
        print('ERR', d['repo'], d['error'][:60]); continue
    hosts = [h for h, _ in list(d['hosts'].items())[:4]]
    print(f"{d['repo'][:52]:<52} src={d['src_files']:<3} mcp={d['mcp_files']:<2} tools={len(d['tool_lines'])} hosts={hosts}")
