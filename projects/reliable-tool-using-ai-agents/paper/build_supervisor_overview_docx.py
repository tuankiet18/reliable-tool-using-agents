#!/usr/bin/env python3
"""Build an editable Word version of supervisor-overview.html.

Usage: uv run --with python-docx --with beautifulsoup4 build_supervisor_overview_docx.py FIG1_PNG OUT_DOCX
FIG1_PNG is Figure 1 rendered from the HTML's inline SVG (e.g. headless Chrome screenshot).
"""

import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = Path(__file__).resolve().parent
BLUE = RGBColor(0x1F, 0x4E, 0x79)
GREEN = RGBColor(0x1D, 0x6B, 0x2F)
RED = RGBColor(0xAA, 0x33, 0x33)
GREY = RGBColor(0x55, 0x55, 0x55)


def shade(cell, hex_fill: str) -> None:
    pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    pr.append(shd)


def runs(par, node, bold=False, italic=False, color=None) -> None:
    for child in node.children:
        if isinstance(child, NavigableString):
            text = str(child).replace("\n", " ")
            if text.strip() or text == " ":
                r = par.add_run(text)
                r.bold, r.italic = bold or None, italic or None
                if color:
                    r.font.color.rgb = color
            continue
        name, cls = child.name, child.get("class", [])
        if name == "br":
            par.add_run().add_break()
        elif name in ("b", "strong"):
            runs(par, child, True, italic, color)
        elif name == "i" or "en" in cls:
            runs(par, child, bold, True, color)
        elif "ok" in cls:
            runs(par, child, True, italic, GREEN)
        elif "no" in cls:
            runs(par, child, True, italic, RED)
        else:
            runs(par, child, bold, italic, color)


def add_table(doc, table) -> None:
    rows = table.find_all("tr")
    ncol = max(len(r.find_all(["th", "td"])) for r in rows)
    t = doc.add_table(rows=0, cols=ncol)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = {2: [2.5, 14.5], 3: [8.5, 3.8, 4.7], 4: [5.4, 3.4, 4.2, 4.0]}.get(ncol)
    for tr in rows:
        row = t.add_row()
        no_split = OxmlElement("w:cantSplit")
        row._tr.get_or_add_trPr().append(no_split)
        cells = row.cells
        if widths:
            for c, w in zip(cells, widths):
                c.width = Cm(w)
        for cell, src in zip(cells, tr.find_all(["th", "td"])):
            p = cell.paragraphs[0]
            runs(p, src, bold=src.name == "th")
            for r in p.runs:
                r.font.size = Pt(9.5)
            if "n" in src.get("class", []):
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if src.name == "th":
                shade(cell, "E6EDF5")
    doc.add_paragraph()


def add_box(doc, box) -> None:
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    shade(cell, "F3F7FB")
    p = cell.paragraphs[0]
    for child in box.children:
        if getattr(child, "get", None) and "formula" in child.get("class", []):
            f = cell.add_paragraph()
            f.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = f.add_run(child.get_text())
            r.bold, r.font.size = True, Pt(13)
            p = cell.add_paragraph()
        elif isinstance(child, NavigableString):
            if str(child).strip():
                p.add_run(str(child).replace("\n", " "))
        else:
            wrapper = BeautifulSoup("<x></x>", "html.parser").x
            wrapper.append(child.__copy__())
            runs(p, wrapper)
    doc.add_paragraph()


def main() -> None:
    fig, out = Path(sys.argv[1]), Path(sys.argv[2])
    soup = BeautifulSoup((HERE / "supervisor-overview.html").read_text(encoding="utf-8"), "html.parser")
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin = sec.bottom_margin = Cm(1.8)
    normal = doc.styles["Normal"]
    normal.font.name, normal.font.size = "Calibri", Pt(11)
    normal.paragraph_format.space_after = Pt(4)
    for lvl, size in (("Title", 20), ("Heading 1", 14)):
        st = doc.styles[lvl]
        st.font.name, st.font.size, st.font.color.rgb = "Calibri", Pt(size), BLUE

    for el in soup.body.children:
        if isinstance(el, NavigableString):
            continue
        name, cls = el.name, el.get("class", [])
        if name == "h1":
            doc.add_paragraph(el.get_text(), style="Title")
        elif "sub" in cls:
            p = doc.add_paragraph()
            r = p.add_run(el.get_text())
            r.font.color.rgb, r.font.size = GREY, Pt(10)
        elif name == "h2":
            doc.add_heading(el.get_text(), level=1)
        elif name == "p" or "rq" in cls:
            runs(doc.add_paragraph(), el)
        elif name == "ul":
            for li in el.find_all("li", recursive=False):
                runs(doc.add_paragraph(style="List Bullet"), li)
        elif name == "table":
            add_table(doc, el)
        elif "box" in cls:
            add_box(doc, el)
        elif "fig" in cls:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run().add_picture(str(fig), width=Cm(16.5))
        elif "cap" in cls or "foot" in cls:
            p = doc.add_paragraph()
            if "cap" in cls:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            runs(p, el, color=GREY)
            for r in p.runs:
                r.font.size = Pt(9)
    doc.save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
