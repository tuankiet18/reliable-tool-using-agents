#!/usr/bin/env python3
"""Build the author-adjudication workbook for survey 2 (protocol Amendment A3).

Coder answers in the fact cases are blinded as X/Y in a seeded random order; the key is written
to a separate JSON file. The spot-check samples 10 coder-A evidence citations with a fixed seed.
"""

from __future__ import annotations

import csv
import json
import random
import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tool_survey_2"
OUT = DATA / "adjudication"
SEED = 20261015

FONT = Font(name="Arial", size=10)
BOLD = Font(name="Arial", size=10, bold=True)
TITLE = Font(name="Arial", size=13, bold=True, color="1F4E79")
LINK = Font(name="Arial", size=10, color="0563C1", underline="single")
GREY = Font(name="Arial", size=9, italic=True, color="666666")
HEAD_FILL = PatternFill("solid", fgColor="E6EDF5")
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
EXAMPLE_FILL = PatternFill("solid", fgColor="F2F2F2")
THIN = Side(style="thin", color="BBBBBB")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")


def gh(repo: str, sha: str, path: str, line: int | None = None, end: int | None = None) -> str:
    url = f"https://github.com/{repo}/blob/{sha}/{path}"
    if line:
        url += f"#L{line}" + (f"-L{end}" if end else "")
    return url


SHA = {
    "bca": ("blockchainacademics/bca-mcp", "07e3f896c068acab102a820282dd57798d6c643d"),
    "grinv": ("Grinv/tmdb-mcp", "d2636c6518f67fbcc665194d3dc02bfc979f3c26"),
    "wudalu": ("wudalu/mcp-hot-news-server", "e2026a37f76d5e508eed83d3d2e2449d06d19959"),
    "memory": ("MemoryClear/claude-web-search-mcp", "010535a5be854b22b84c51829ac1db284e735509"),
    "corey": ("corey-coders/mcp-finance-news", "7c45d35a44725e0713764643fe61bbb35be3abda"),
    "vmlia": ("VmLia/books-mcp-server", "e81a33ca2ad85b704d42bc4f075c313f36d96101"),
    "notnull": ("NotNull92/exchange-rate-mcp", "3e3afeffc59850b134550abbc7372b6782e79ede"),
}

RULES = [
    {
        "id": "R1",
        "question": "Metadata nêu tên NGUỒN DỮ LIỆU đứng sau API mà tool thực sự gọi. Có tính tên đó là provider được khai báo (declared provider) không?",
        "examples": [
            ("bca-mcp: tool gọi API của Blockchain Academics, description ghi 'Spot price … via CoinGecko'", gh(*SHA["bca"], "src/tools/market.ts", 31)),
            ("tmdb-mcp: tool gọi OMDb, title ghi 'Get IMDb/RT/Metacritic ratings'", gh(*SHA["grinv"], "src/tools/omdb.ts", 14)),
            ("mcp-hot-news-server: tool gọi vvhan, tham số ghi 'weibo, zhihu, baidu, google_trends …'", gh(*SHA["wudalu"], "src/mcp_hot_news/server.py", 895)),
        ],
        "options": "Tính,Không tính",
        "hint": "Tính: agent đọc thấy 'CoinGecko' sẽ coi tool này cùng nguồn với các tool CoinGecko khác. Không tính: chỉ tên bên vận hành API (operator) mới được tính.",
    },
    {
        "id": "R2",
        "question": "README nêu tên provider mà tool KHÔNG gọi theo mặc định (phải bật thêm trong config). Có tính vào L2 không?",
        "examples": [
            ("claude-web-search-mcp: README liệt kê '必应中文', 'Bing', 'SerpAPI' nhưng các engine này bị tắt mặc định", gh(*SHA["memory"], "README.md", 7, 8)),
        ],
        "options": "Tính,Không tính",
        "hint": "Tính: L2 = mọi provider README nêu tên. Không tính: L2 chỉ gồm provider được gọi mặc định.",
    },
    {
        "id": "R3",
        "question": "UPSTREAM: hai feed của hai thương hiệu thuộc cùng một công ty mẹ (WSJ tại feeds.a.dj.com và MarketWatch tại marketwatch.com, đều thuộc Dow Jones). Ghi thế nào?",
        "examples": [
            ("mcp-finance-news: các URL feed", gh(*SHA["corey"], "main.py", 19, 34)),
        ],
        "options": "Một provider (Dow Jones),Hai provider (WSJ; MarketWatch)",
        "hint": "Codebook: provider là TỔ CHỨC vận hành hostname API.",
    },
    {
        "id": "R4",
        "question": "L1: tool description liệt kê lựa chọn 'wsj', 'marketwatch' (tên thương hiệu, không nêu Dow Jones). Có tính là đã khai báo provider không?",
        "examples": [
            ("mcp-finance-news: docstring tham số source", gh(*SHA["corey"], "main.py", 99, 100)),
        ],
        "options": "Tính (quy về chủ sở hữu),Không tính",
        "hint": "Tính: agent thấy 'wsj' và 'marketwatch' có thể suy ra hai nguồn. Không tính: chỉ tên tổ chức vận hành mới tính.",
    },
]

CASES = [
    {
        "id": "C1", "server": "books/VmLia/books-mcp-server", "field": "upstream_providers",
        "question": "Tool scrape trang www.shuchacha.net; repo không nói ai sở hữu trang này. Ghi provider thế nào?",
        "link": gh(*SHA["vmlia"], "main.py", 24),
        "A": "shuchacha.net (ghi tên miền)", "B": "ambiguous",
    },
    {
        "id": "C2", "server": "currency_exchange/NotNull92/exchange-rate-mcp", "field": "l2_declared_provider",
        "question": "README dòng 15 ghi 'Frankfurter public API (based on European Central Bank data)'. L2 có nêu ECB không?",
        "link": gh(*SHA["notnull"], "README.md", 15),
        "A": "Có: L2 gồm ECB", "B": "Không: L2 chỉ có Frankfurter",
    },
    {
        "id": "C3", "server": "currency_exchange/NotNull92/exchange-rate-mcp", "field": "l2_declared_provider",
        "question": "README dòng 28 ghi 'Fallback API (Currency-API via JSDelivr)'. Có tính là đã nêu chủ bộ dữ liệu (fawazahmed0) không?",
        "link": gh(*SHA["notnull"], "README.md", 28),
        "A": "Có: Currency-API = bộ dữ liệu của fawazahmed0", "B": "Không: README không nêu đích danh fawazahmed0",
    },
    {
        "id": "C4", "server": "news/wudalu/mcp-hot-news-server", "field": "l1_declared_provider",
        "question": "Mô tả tham số liệt kê 'news_api' (và tool thực sự gọi newsapi.org). Có tính là đã nêu tên NewsAPI không?",
        "link": gh(*SHA["wudalu"], "src/mcp_hot_news/server.py", 895),
        "A": "Có: 'news_api' là tên NewsAPI", "B": "Không: 'news_api' là nhãn chung chung",
    },
]

MERGES = [
    ("Google Maps Platform", "Google"), ("Google Books", "Google"),
    ("Amazon Location Service", "Amazon Web Services"), ("Eastmoney", "East Money"),
    ("Hacker News (Y Combinator)", "Hacker News"), ("360 Search", "Qihoo 360"),
    ("Grokipedia (xAI)", "SpaceXAI"), ("Wikipedia", "Wikimedia Foundation"),
    ("fawazahmed0 exchange-api", "fawazahmed0"), ("Baidu Translate", "Baidu"),
]


def style_header(ws, row: int, ncol: int) -> None:
    for c in range(1, ncol + 1):
        cell = ws.cell(row=row, column=c)
        cell.font, cell.fill, cell.border, cell.alignment = BOLD, HEAD_FILL, BOX, WRAP


def cell(ws, row, col, value, font=FONT, fill=None, link=None):
    c = ws.cell(row=row, column=col, value=value)
    c.font, c.border, c.alignment = (LINK if link else font), BOX, WRAP
    if fill:
        c.fill = fill
    if link:
        c.hyperlink = link
    return c


def dropdown(ws, options: str, ref: str) -> None:
    dv = DataValidation(type="list", formula1=f'"{options}"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(ref)


def evidence_sample() -> list[dict]:
    rows = list(csv.DictReader((DATA / "coding.csv").open(encoding="utf-8")))
    pat = re.compile(r"([\w./-]+\.\w+):(\d+)")
    pool = []
    for r in rows:
        m = pat.search(r["upstream_evidence"])
        if m:
            repo = r["repo_url"].split("github.com/")[1]
            pool.append({"server": r["server_id"], "claim": r["upstream_providers"], "file": m.group(1),
                         "line": int(m.group(2)), "link": gh(repo, r["commit_sha"], m.group(1), int(m.group(2))),
                         "evidence": r["upstream_evidence"][:160]})
    return random.Random(SEED).sample(pool, 10)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    key = {}
    wb = Workbook()

    ws = wb.active
    ws.title = "0. Hướng dẫn"
    ws.column_dimensions["A"].width = 110
    lines = [
        ("Phân xử bất đồng giữa hai coder — survey 2", TITLE),
        ("Người làm: tác giả (Lương Tuấn Kiệt). TỰ LÀM, KHÔNG HỎI AI — nếu hỏi AI thì lại thành AI phân xử AI.", BOLD),
        ("Thời gian: khoảng 45–60 phút. Chỉ điền vào các ô NỀN VÀNG. Ô có mũi tên thì chọn trong danh sách.", FONT),
        ("", FONT),
        ("Sheet 1. Luật (4 câu): quyết định một luật cho codebook. Mở link ví dụ, đọc dòng được đánh dấu, rồi chọn.", FONT),
        ("Sheet 2. Trường hợp (4 câu): hai coder trả lời khác nhau, được che tên là X và Y. Mở link, đọc, chọn X, Y hoặc 'Cả hai sai'.", FONT),
        ("Sheet 3. Gộp tên (10 cặp): hai tên có phải cùng MỘT tổ chức không? Chỉ dùng để tính agreement.", FONT),
        ("Sheet 4. Kiểm tra bằng chứng (10 dòng): mở link, xem dòng code có đúng là gọi provider được ghi không.", FONT),
        ("", FONT),
        ("Mẹo: link GitHub mở đúng commit và tô vàng đúng dòng. Không cần hiểu cả repo, chỉ cần đọc dòng đó và vài dòng xung quanh.", FONT),
        ("Không có đáp án 'đúng' theo ý tác giả paper: hãy chọn theo điều anh thấy hợp lý nhất cho câu hỏi 'agent đọc thấy gì thì sẽ hiểu gì'.", FONT),
        ("Cột 'Lý do' chỉ cần một câu. Không chắc thì chọn 'Không chắc' và ghi lý do.", FONT),
        ("", FONT),
        ("Kết quả chính P1–P6 KHÔNG đổi. Quyết định của anh được dùng cho một sensitivity analysis (protocol Amendment A3).", GREY),
    ]
    for i, (t, f) in enumerate(lines, start=1):
        c = ws.cell(row=i, column=1, value=t)
        c.font, c.alignment = f, Alignment(wrap_text=True)

    ws = wb.create_sheet("1. Luật")
    heads = ["ID", "Câu hỏi", "Ví dụ (mở link)", "Link", "Gợi ý hai lựa chọn", "Quyết định", "Lý do (1 câu)"]
    for c, w in zip("ABCDEFG", (5, 45, 45, 14, 40, 22, 35)):
        ws.column_dimensions[c].width = w
    for c, h in enumerate(heads, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(heads))
    r = 2
    for rule in RULES:
        first = r
        for text, url in rule["examples"]:
            cell(ws, r, 3, text)
            cell(ws, r, 4, "Mở link", link=url)
            r += 1
        for row in range(first, r):
            for col in (1, 2, 5, 6, 7):
                cell(ws, row, col, None, fill=INPUT_FILL if col in (6, 7) else None)
        if r - first > 1:
            for col in (1, 2, 5, 6, 7):
                ws.merge_cells(start_row=first, start_column=col, end_row=r - 1, end_column=col)
        ws.cell(row=first, column=1, value=rule["id"]).font = BOLD
        ws.cell(row=first, column=2, value=rule["question"])
        ws.cell(row=first, column=5, value=rule["hint"])
        dropdown(ws, rule["options"] + ",Không chắc", f"F{first}")

    ws = wb.create_sheet("2. Trường hợp")
    heads = ["ID", "Server", "Câu hỏi", "Link", "Trả lời X", "Trả lời Y", "Anh chọn", "Lý do (1 câu)"]
    for c, w in zip("ABCDEFGH", (6, 28, 45, 10, 28, 28, 14, 35)):
        ws.column_dimensions[c].width = w
    for c, h in enumerate(heads, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(heads))
    example = ["VÍ DỤ", "weather/example/weather-mcp", "README có nêu provider không?", "Mở link",
               "Có: OpenWeather", "Không", "X", "README dòng 3 ghi 'Powered by OpenWeather'."]
    for c, v in enumerate(example, 1):
        cell(ws, 2, c, v, font=GREY, fill=EXAMPLE_FILL)
    for i, case in enumerate(CASES, start=3):
        flip = rng.random() < 0.5
        x, y = (case["B"], case["A"]) if flip else (case["A"], case["B"])
        key[case["id"]] = {"X": "coder_2_codex" if flip else "coder_A_claude", "Y": "coder_A_claude" if flip else "coder_2_codex",
                           "server": case["server"], "field": case["field"]}
        for c, v in enumerate([case["id"], case["server"], case["question"]], 1):
            cell(ws, i, c, v)
        cell(ws, i, 4, "Mở link", link=case["link"])
        cell(ws, i, 5, x)
        cell(ws, i, 6, y)
        cell(ws, i, 7, None, fill=INPUT_FILL)
        cell(ws, i, 8, None, fill=INPUT_FILL)
    dropdown(ws, "X,Y,Cả hai sai,Không chắc", f"G3:G{2 + len(CASES)}")

    ws = wb.create_sheet("3. Gộp tên")
    heads = ["Tên 1", "Tên 2", "Cùng một tổ chức?", "Ghi chú"]
    for c, w in zip("ABCD", (30, 30, 20, 40)):
        ws.column_dimensions[c].width = w
    for c, h in enumerate(heads, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(heads))
    for i, (a, b) in enumerate(MERGES, start=2):
        cell(ws, i, 1, a)
        cell(ws, i, 2, b)
        cell(ws, i, 3, None, fill=INPUT_FILL)
        cell(ws, i, 4, None, fill=INPUT_FILL)
    dropdown(ws, "Có,Không,Không chắc", f"C2:C{1 + len(MERGES)}")

    ws = wb.create_sheet("4. Kiểm tra bằng chứng")
    heads = ["#", "Server", "Coder A ghi provider là", "Bằng chứng coder A ghi", "Link", "Dòng code có gọi đúng provider đó?", "Ghi chú"]
    for c, w in zip("ABCDEFG", (4, 34, 24, 45, 10, 18, 30)):
        ws.column_dimensions[c].width = w
    for c, h in enumerate(heads, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(heads))
    sample = evidence_sample()
    for i, s in enumerate(sample, start=2):
        for c, v in enumerate([i - 1, s["server"], s["claim"], s["evidence"]], 1):
            cell(ws, i, c, v)
        cell(ws, i, 5, "Mở link", link=s["link"])
        cell(ws, i, 6, None, fill=INPUT_FILL)
        cell(ws, i, 7, None, fill=INPUT_FILL)
    dropdown(ws, "Đúng,Sai,Không chắc", f"F2:F{1 + len(sample)}")

    for sheet in wb.worksheets[1:]:
        sheet.freeze_panes = "A2"
    path = OUT / "author_adjudication.xlsx"
    wb.save(path)
    (OUT / "adjudication_key.json").write_text(json.dumps(
        {"seed": SEED, "blinding": key, "rules": [r["id"] for r in RULES],
         "spot_check": [{k: s[k] for k in ("server", "claim", "file", "line")} for s in sample]},
        indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
