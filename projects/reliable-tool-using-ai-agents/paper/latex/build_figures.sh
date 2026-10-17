#!/usr/bin/env bash
# Convert the paper SVG figures (../figures/rq2-rq3-v1/*.svg) to vector PDFs for LaTeX.
# Uses headless Chrome with a page size equal to the SVG size. Then build: latexmk -pdf main.tex
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p figures
for f in problem-common-mode rq2-j-condition rq3-surveys; do
  svg=../figures/rq2-rq3-v1/$f.svg
  w=$(grep -o 'width="[0-9.]*"' "$svg" | head -1 | tr -dc 0-9.)
  h=$(grep -o 'height="[0-9.]*"' "$svg" | head -1 | tr -dc 0-9.)
  tmp=$(mktemp --suffix=.html)
  printf '<!doctype html><html><head><style>@page{size:%spx %spx;margin:0}html,body{margin:0;padding:0}svg{display:block}</style></head><body>%s</body></html>' "$w" "$h" "$(cat "$svg")" > "$tmp"
  google-chrome --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="figures/$f.pdf" "file://$tmp" 2>/dev/null
  rm -f "$tmp"
done
