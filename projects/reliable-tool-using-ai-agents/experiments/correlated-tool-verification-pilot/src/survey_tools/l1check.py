#!/usr/bin/env python3
"""Show where provider keywords appear: source lines (excluding URLs/imports) vs README. Static read only.

Usage: python3 -I l1check.py <repo_dir> keyword [keyword ...]
"""
import re, sys
from pathlib import Path

SRC = {'.py', '.ts', '.js', '.mjs', '.go', '.rs', '.java', '.kt', '.cs', '.json', '.yaml', '.yml', '.toml', '.properties'}
SKIP = {'node_modules', '.git', 'dist', 'build', 'test', 'tests', '__tests__', 'docs', '.github', 'vendor', 'examples'}
LOCKS = {'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'uv.lock', 'poetry.lock', 'Cargo.lock'}


def main() -> None:
    repo = Path(sys.argv[1]); kws = [k.lower() for k in sys.argv[2:]]
    pat = re.compile('|'.join(re.escape(k) for k in kws), re.I)
    src_hits, readme_hits = [], []
    for p in repo.rglob('*'):
        if not p.is_file() or any(x in SKIP for x in p.relative_to(repo).parts) or p.name in LOCKS:
            continue
        rel = str(p.relative_to(repo)); is_readme = p.name.lower().startswith('readme')
        if not is_readme and p.suffix not in SRC:
            continue
        try:
            lines = p.read_text(errors='ignore').splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            if not pat.search(line):
                continue
            s = line.strip()
            if is_readme:
                readme_hits.append(f'{rel}:{i}: {s[:120]}')
            elif not re.search(r'https?://|^\s*(import|from|use|require|package)\b', s):
                src_hits.append(f'{rel}:{i}: {s[:150]}')
    print(f'SRC ({len(src_hits)})'); [print('  ', h) for h in src_hits[:14]]
    print(f'README ({len(readme_hits)})'); [print('  ', h) for h in readme_hits[:3]]


if __name__ == '__main__':
    main()
