#!/usr/bin/env python3
"""Build the author blind-coding workbook (protocol "Author Blind Coding of Survey 2 Subset" v1.0).

Selects 15 servers from the survey-2 estimation set that the author has not seen (excludes the
coder-2 subset, the adjudication cases and the evidence spot-check), by smallest
sha256(server_id + "|author-blind-2026-10-18"). The workbook contains NO coder-A labels.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tool_survey_2"
OUT = DATA / "author_blind"
SALT = "|author-blind-2026-10-18"
N = 15
ADJUDICATED = {
    "books/VmLia/books-mcp-server", "currency_exchange/NotNull92/exchange-rate-mcp",
    "news/wudalu/mcp-hot-news-server", "crypto_prices/blockchainacademics/bca-mcp",
    "movies/Grinv/tmdb-mcp", "web_search/MemoryClear/claude-web-search-mcp",
    "news/corey-coders/mcp-finance-news",
}
TYPE_VI = {
    "weather": "thời tiết", "currency_exchange": "tỷ giá ngoại tệ", "stock_quotes": "giá cổ phiếu",
    "crypto_prices": "giá tiền mã hóa", "web_search": "tìm kiếm web", "news": "tin tức",
    "translation": "dịch thuật", "movies": "thông tin phim", "books": "thông tin sách",
    "air_quality": "chất lượng không khí",
}
FONT, BOLD = Font(name="Arial", size=10), Font(name="Arial", size=10, bold=True)
TITLE = Font(name="Arial", size=13, bold=True, color="1F4E79")
GREY = Font(name="Arial", size=9, italic=True, color="666666")
HEAD, INPUT, EXAMPLE = (PatternFill("solid", fgColor=c) for c in ("E6EDF5", "FFF2CC", "F2F2F2"))
THIN = Side(style="thin", color="BBBBBB")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")

GUIDE = [
    ("Gán nhãn mù 15 server — survey 2", TITLE),
    ("TỰ LÀM, KHÔNG DÙNG AI (kể cả để dịch hay tóm tắt code), không mở file nhãn nào khác, không hỏi Claude về server cụ thể cho tới khi nộp.", BOLD),
    ("Chỉ điền vào ô NỀN VÀNG ở sheet '2. Server'. Khoảng 15–20 phút mỗi server; chia làm nhiều buổi được. Ghi thời gian làm vào cột cuối.", FONT),
    ("", FONT),
    ("CÁC BƯỚC VỚI MỖI SERVER", BOLD),
    ("1. Mở link repo (đúng commit đã ghim). Cột 'Loại thông tin' cho biết cần xét tool nào (ví dụ: tool trả về thời tiết).", FONT),
    ("2. Tìm chỗ khai báo tool: tìm trong repo các chuỗi như  server.tool(  /  @mcp.tool  /  Tool(name=  /  registerTool  /  tools/list.", FONT),
    ("3. UPSTREAM: tool đó gọi API nào theo cấu hình MẶC ĐỊNH? Tìm 'https://', 'api.', 'BASE_URL', 'endpoint'. Ghi tên TỔ CHỨC sở hữu hostname (api.openweathermap.org → OpenWeather). Nhiều nguồn mặc định → cách nhau bằng ';'. Ghi bằng chứng dạng file:dòng.", FONT),
    ("   Gọi qua thư viện (SDK) → ghi dịch vụ mà thư viện đó gọi (yfinance → Yahoo Finance) và ghi tên thư viện vào Ghi chú.", FONT),
    ("4. L1 (thứ agent thấy): chỉ đọc TÊN SERVER, TÊN TOOL, DESCRIPTION của tool và mô tả THAM SỐ. Nếu tên provider được nêu ĐÍCH DANH → ghi tên đó; nếu không → ghi unknown. Không suy luận.", FONT),
    ("5. L2: như L1 nhưng được đọc thêm README.", FONT),
    ("", FONT),
    ("LUẬT CODEBOOK (gồm cả 4 luật anh đã quyết ngày 16/10)", BOLD),
    ("• R1 — Metadata nêu tên NGUỒN DỮ LIỆU CUỐI CÙNG đứng sau API (ví dụ 'giá lấy via CoinGecko') → TÍNH là đã khai báo tên đó.", FONT),
    ("• R2 — Provider chỉ được nhắc mà KHÔNG bật mặc định (phải đổi config mới dùng) → KHÔNG tính (cả upstream lẫn L1/L2).", FONT),
    ("• R3 — Hai thương hiệu khác nhau của cùng công ty mẹ (ví dụ WSJ và MarketWatch) → tính là HAI provider.", FONT),
    ("• R4 — Tên thương hiệu trong metadata (ví dụ 'wsj') → TÍNH, giữ tên thương hiệu.", FONT),
    ("• Server gom nhiều nguồn: nguồn tính là mặc định nếu tool gọi nó khi người dùng chỉ cần đưa API key, không phải đổi thiết lập chọn nguồn.", FONT),
    ("• Server có nhiều tool cùng loại thông tin: ghi HỢP các nguồn mặc định của các tool đó.", FONT),
    ("• URL provider đổi được bằng biến môi trường nhưng có giá trị mặc định: ghi provider mặc định, thêm 'configurable' vào Ghi chú.", FONT),
    ("• Tên server chỉ nói chủ đề/địa danh (ví dụ 'yerevan-aqi') KHÔNG tính là nêu tên provider.", FONT),
    ("• Bộ dữ liệu tĩnh phát qua CDN (jsDelivr, GitHub raw…): provider là CHỦ BỘ DỮ LIỆU, ghi tên CDN vào Ghi chú.", FONT),
    ("• SearXNG tự host/công khai hoặc Ollama chạy cục bộ: ghi tên đó và viết AMBIGUOUS vào Ghi chú.", FONT),
    ("• Không tìm được URL nào / không chắc: ghi ambiguous và giải thích ngắn trong Ghi chú. KHÔNG đoán.", FONT),
    ("", FONT),
    ("Dòng đầu (nền xám) ở sheet 2 là VÍ DỤ cách điền, không phải server cần làm.", GREY),
]


def select() -> list[dict]:
    rows = [r for r in csv.DictReader((DATA / "coding.csv").open(encoding="utf-8"))
            if r["category"] not in ("geocoding", "ip_geolocation")]
    human = {r["server_id"] for r in csv.DictReader((DATA / "human_coder_template.csv").open(encoding="utf-8-sig"))}
    spot = {s["server"] for s in json.loads((DATA / "adjudication" / "adjudication_key.json").read_text())["spot_check"]}
    seen = human | spot | ADJUDICATED
    pool = [r for r in rows if r["server_id"] not in seen]
    assert len(pool) == 48, len(pool)
    pool.sort(key=lambda r: hashlib.sha256((r["server_id"] + SALT).encode()).hexdigest())
    return pool[:N]


def cell(ws, row, col, value, font=FONT, fill=None):
    c = ws.cell(row=row, column=col, value=value)
    c.font, c.border, c.alignment = font, BOX, WRAP
    if fill:
        c.fill = fill
    return c


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sample = select()
    wb = Workbook()
    ws = wb.active
    ws.title = "1. Hướng dẫn"
    ws.column_dimensions["A"].width = 130
    for i, (text, font) in enumerate(GUIDE, start=1):
        c = ws.cell(row=i, column=1, value=text)
        c.font, c.alignment = font, Alignment(wrap_text=True)

    ws = wb.create_sheet("2. Server")
    heads = ["#", "Server", "Loại thông tin", "Link repo (đúng commit)", "Upstream provider (mặc định)",
             "Bằng chứng upstream (file:dòng)", "L1: provider được nêu (hoặc unknown)", "Bằng chứng L1 (trích ≤10 từ)",
             "L2: provider được nêu (hoặc unknown)", "Bằng chứng L2", "Ghi chú", "Thời gian (phút)"]
    widths = (4, 32, 14, 48, 22, 26, 24, 26, 24, 22, 28, 10)
    for i, (h, w) in enumerate(zip(heads, widths), start=1):
        cell(ws, 1, i, h, BOLD, HEAD)
        ws.column_dimensions[chr(64 + i)].width = w
    example = ["VD", "weather/example/weather-mcp", "thời tiết", "https://github.com/example/weather-mcp/tree/<commit>",
               "Open-Meteo", "src/weather.py:18", "unknown", "", "Open-Meteo", "README.md:3 'Powered by Open-Meteo'",
               "description chỉ ghi 'Get forecast for a city'", "15"]
    for i, v in enumerate(example, start=1):
        cell(ws, 2, i, v, GREY, EXAMPLE)
    for k, r in enumerate(sample, start=1):
        row = k + 2
        repo = r["repo_url"].rstrip("/")
        cell(ws, row, 1, k)
        cell(ws, row, 2, r["server_id"])
        cell(ws, row, 3, TYPE_VI.get(r["category"], r["category"]))
        link = cell(ws, row, 4, f"{repo}/tree/{r['commit_sha']}")
        link.hyperlink = f"{repo}/tree/{r['commit_sha']}"
        for col in range(5, 13):
            cell(ws, row, col, None, fill=INPUT)
    ws.freeze_panes = "C2"
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="300", allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"L3:L{N + 2}")

    path = OUT / "author_blind_template.xlsx"
    wb.save(path)
    (OUT / "selection.json").write_text(json.dumps(
        {"salt": SALT, "n": N, "pool_size": 48, "servers": [r["server_id"] for r in sample]}, indent=2) + "\n")
    print(f"wrote {path}")
    for r in sample:
        print(" ", r["server_id"])


if __name__ == "__main__":
    main()
