# Paper (LaTeX, English)

Build: `latexmk -pdf main.tex` (pdflatex + BibTeX). Regenerate figures after the SVGs change: `./build_figures.sh`.

| File | Contents |
|---|---|
| `main.tex` | Document class and the order of sections only |
| `preamble.tex` | Packages and macros (`\code`, `\E`) |
| `sections/00-front.tex` | Title, author, abstract, keywords |
| `sections/01-…09-*.tex` | One file per section |
| `refs.bib` | Bibliography (BibTeX keys used with `\cite`) |
| `figures/*.pdf` | Vector figures built from `../figures/rq2-rq3-v1/*.svg` |

## Common edits

- **Change a section:** edit its file in `sections/`. Reorder or drop sections in `main.tex`.
- **Switch to a venue template** (e.g. IEEE, ACM): change `\documentclass` in `main.tex`, then remove from
  `preamble.tex` the packages the class already handles (`geometry`, `caption`, `lmodern`), and move the
  abstract into the form the class expects. Section files usually need no change.
- **Citation style:** change `\bibliographystyle{plain}` in `main.tex` (e.g. `IEEEtran`, `ACM-Reference-Format`).
- **Author name with Vietnamese diacritics:** needs XeLaTeX or LuaLaTeX with a font such as TeX Gyre Termes;
  the default pdflatex build keeps the name without diacritics.

Generated files (`main.pdf`, `*.aux`, `*.log`, …) are not committed; see `.gitignore`.
