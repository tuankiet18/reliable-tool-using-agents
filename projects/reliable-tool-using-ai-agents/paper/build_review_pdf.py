"""Export the living Markdown manuscript as a readable, non-submission PDF.

This is a layout-only export. The source manuscript and appendix are not edited.
Requires Python ``markdown``, LibreOffice, ImageMagick, and bundled ``pypdf``.
"""

from __future__ import annotations

import base64
import hashlib
import html
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import markdown


PAPER_DIR = Path(__file__).resolve().parent
PAPER = PAPER_DIR / "paper-draft.md"
APPENDIX = PAPER_DIR / "supplementary-appendix.md"
OUTPUT = PAPER_DIR / "review" / "paper-review-v0.9-2026-10-05.pdf"


def body(path: Path, *, stop_at: str | None = None) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n.*?\n---\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Missing frontmatter: {path}")
    text = text[match.end() :]
    if stop_at:
        text, separator, _ = text.partition(stop_at)
        if not separator:
            raise ValueError(f"Missing manuscript boundary: {stop_at}")
    return text.strip()


def build() -> None:
    paper_bytes = PAPER.read_bytes()
    source_hash = hashlib.sha256(paper_bytes).hexdigest()
    manuscript = body(PAPER, stop_at="\n## Writing status\n")
    appendix = body(APPENDIX)
    vault_sources: dict[str, int] = {}

    def vault_reference(match: re.Match[str]) -> str:
        target = match.group(1).split("|", 1)[0]
        index = vault_sources.setdefault(target, len(vault_sources) + 1)
        return f'<a class="vaultref" href="#vault-source-{index}">[V{index}]</a>'

    def embed_figure(match: re.Match[str]) -> str:
        alt, relative_path = match.group(1), match.group(2)
        figure_path = (PAPER_DIR / relative_path).resolve()
        if not figure_path.is_relative_to(PAPER_DIR.resolve()) or not figure_path.is_file():
            raise ValueError(f"Figure does not resolve within paper directory: {relative_path}")
        converted = subprocess.run(
            ["convert", "-background", "white", "-density", "160", str(figure_path), "png:-"],
            capture_output=True,
            timeout=30,
        )
        if converted.returncode != 0:
            raise RuntimeError(f"Figure conversion failed: {converted.stderr[-500:]!r}")
        encoded = base64.b64encode(converted.stdout).decode("ascii")
        return (
            f'<img src="data:image/png;base64,{encoded}" width="640" '
            f'alt="{html.escape(alt, quote=True)}">'
        )

    manuscript = re.sub(r"!\[([^]]*)\]\((figures/[^)]+)\)", embed_figure, manuscript)

    def render_markdown(text: str) -> str:
        text = text.replace(
            "> [!important] **Living paper — version 0.9.**",
            "> **Ghi chú phiên bản 0.9.**",
        )
        text = re.sub(r"\[\[([^]]+)\]\]", vault_reference, text)
        text = re.sub(
            r"\$\$\s*\\mathbb\{E\}\[U_\{random\}\]=\\pi q=2/9\\approx 0\.2222,\\qquad\s*\\mathbb\{E\}\[U_\{provenance\}\]=0\.\s*\$\$",
            '<div class="equation">E[U<sub>random</sub>] = πq = 2/9 ≈ 0.2222; '
            'E[U<sub>provenance</sub>] = 0.</div>',
            text,
        )
        if "$$" in text:
            raise ValueError("Unrendered display math remains")
        result = markdown.markdown(
            text,
            extensions=["tables", "fenced_code", "sane_lists"],
            output_format="html5",
        )
        if "[[" in result or "]]" in result:
            raise ValueError("Unresolved Obsidian wikilink remains")
        return result

    rendered_manuscript = render_markdown(manuscript)
    rendered_appendix = render_markdown(appendix)
    sources_html = "\n".join(
        f'<li id="vault-source-{index}"><span>[V{index}]</span> '
        f'<code>{html.escape(path)}</code></li>'
        for path, index in vault_sources.items()
    )
    style = f"""<style>
  @page {{ size: A4; margin: 17mm 17mm 19mm; @bottom-center {{ content: counter(page); color: #64748b; font: 8pt 'Noto Sans', sans-serif; }} }}
  html {{ font-family: 'Noto Serif', serif; color: #172033; font-size: 9.7pt; line-height: 1.48; }}
  body {{ max-width: 100%; }}
  h1, h2, h3, h4 {{ font-family: 'Noto Sans', sans-serif; line-height: 1.25; color: #122e4f; break-after: avoid; }}
  h1 {{ font-size: 17pt; margin: 0 0 12pt; }}
  h2 {{ font-size: 12.4pt; border-bottom: 0.45pt solid #d5deea; padding-bottom: 3pt; margin: 18pt 0 7pt; }}
  h3 {{ font-size: 10.6pt; margin: 12pt 0 4pt; }}
  h4 {{ font-size: 9.7pt; margin: 10pt 0 3pt; }}
  p {{ margin: 0 0 7pt; orphans: 3; widows: 3; }}
  ul, ol {{ padding-left: 20pt; margin: 5pt 0 8pt; }}
  li {{ margin: 2pt 0; break-inside: avoid; }}
  blockquote {{ margin: 8pt 0; padding: 6pt 9pt; border-left: 3pt solid #3185b7; background: #f0f7fb; }}
  blockquote p:last-child {{ margin-bottom: 0; }}
  a {{ color: #145b88; text-decoration: none; overflow-wrap: anywhere; }}
  a.vaultref {{ font: 8pt 'Noto Sans', sans-serif; color: #6b4a22; white-space: nowrap; }}
  code, pre {{ font-family: 'DejaVu Sans Mono', monospace; font-size: 8.1pt; }}
  code {{ background: #f4f6f8; padding: 0 1pt; overflow-wrap: anywhere; }}
  pre {{ white-space: pre-wrap; background: #f4f6f8; border: 0.5pt solid #e0e5eb; padding: 7pt; break-inside: avoid; }}
  table {{ width: 100%; border-collapse: collapse; table-layout: auto; font-size: 7.4pt; margin: 7pt 0 11pt; break-inside: auto; }}
  thead {{ display: table-header-group; }}
  tr {{ break-inside: avoid; }}
  th, td {{ border: 0.45pt solid #d4dde7; padding: 4pt 5pt; vertical-align: top; overflow-wrap: anywhere; }}
  th {{ background: #e9f1f8; font-family: 'Noto Sans', sans-serif; text-align: left; }}
  img {{ display: block; max-width: 100%; max-height: 170mm; margin: 9pt auto 3pt; break-inside: avoid; }}
  p:has(> img) {{ break-inside: avoid; }}
  .equation {{ font-family: 'Noto Sans', sans-serif; text-align: center; margin: 11pt 0; padding: 6pt; background: #f8fafc; }}
  .review-banner {{ margin: 0 0 14pt; padding: 8pt 10pt; border-left: 3pt solid #c47b27; background: #fff8ed; font: 8.5pt 'Noto Sans', sans-serif; }}
  .review-banner p {{ margin: 0 0 3pt; }}
  .review-banner p:last-child {{ margin: 0; }}
  .vault-index ol {{ font-size: 8pt; }}
  .vault-index code {{ font-size: 7.1pt; }}
</style>"""
    banner = f"""
<aside class="review-banner">
  <p><strong>Bản đọc để góp ý - chưa phải bản nộp.</strong> Xuất từ living manuscript v0.9 ngày 2026-10-05; định dạng A4 một cột trung tính. Phụ lục nằm sau References.</p>
  <p>Đề nghị giảng viên góp ý phạm vi RQ, actor/oracle/fault model, baseline và mức contribution. Main study đo quyết định mô phỏng, không phải giao dịch thật hoặc live-agent effect; novelty vẫn PRELIMINARY và chưa có human sign-off.</p>
  <p>SHA-256 của paper-draft.md: <code>{source_hash}</code></p>
</aside>
"""
    documents = {
        "paper": banner + rendered_manuscript,
        "appendix": rendered_appendix,
        "vault-index": f"""<section class="vault-index"><h1>Đường dẫn hồ sơ nội bộ được nhắc trong bản thảo</h1>
<p>Các mã [V…] là cross-reference tới Obsidian vault, không phải citation học thuật hoặc bằng chứng độc lập.</p>
<ol>{sources_html}</ol></section>""",
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="paper-review-") as tmp:
        part_pdfs = []
        soffice = "/home/kiet/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/soffice"
        for name, content in documents.items():
            html_path = Path(tmp) / f"{name}.html"
            html_path.write_text(
                f'<!doctype html><html lang="vi"><head><meta charset="utf-8">{style}</head>'
                f"<body>{content}</body></html>",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    soffice,
                    f"-env:UserInstallation={(Path(tmp) / f'lo-profile-{name}').as_uri()}",
                    "--headless",
                    "--convert-to",
                    "pdf:writer_pdf_Export",
                    "--outdir",
                    tmp,
                    str(html_path),
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            converted = Path(tmp) / f"{name}.pdf"
            if result.returncode != 0 or not converted.is_file():
                raise RuntimeError(f"LibreOffice PDF export failed: {result.stderr[-2000:]}")
            part_pdfs.append(converted)

        merged = Path(tmp) / "merged.pdf"
        merge_script = (
            "from pypdf import PdfWriter; import sys; "
            "writer=PdfWriter(); [writer.append(path) for path in sys.argv[1:-1]]; "
            "writer.write(sys.argv[-1])"
        )
        subprocess.run(
            [
                "/home/kiet/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
                "-c",
                merge_script,
                *(str(path) for path in part_pdfs),
                str(merged),
            ],
            check=True,
            timeout=60,
        )
        shutil.copyfile(merged, OUTPUT)
    print(f"PDF: {OUTPUT}")
    print(f"Paper SHA-256: {source_hash}")
    print(f"Internal source pointers: {len(vault_sources)}")


if __name__ == "__main__":
    build()
