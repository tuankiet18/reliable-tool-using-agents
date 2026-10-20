#!/usr/bin/env python3
"""RQ4 step 3: build the frozen tool texts and the C0/C1/C2 stimuli (protocol §3–4).

Each server contributes ONE tool: the information-type tool that calls the upstream recorded by
coder A. Texts are copied verbatim from the code at the pinned commit (static read). Selections were
made by hand after inspecting the code; for most servers the description comes from the automatic
candidate list, for the rest it is given explicitly below. Every description is then verified to
occur verbatim (whitespace-normalised) in its source file, near the tool name.

Usage: python3 rq4_build_stimuli.py <repos_dir> <candidates.json>
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "rq4_agent_choice"
MAXLEN = 400

# server_id -> (tool name, "file:line") picked from the automatic candidates (verified by hand)
FROM_CANDIDATES = {
    "air_quality/hayrapetian/yerevan-aqi-mcp": ("get_device_current", "src/index.ts:26"),
    "crypto_prices/desk3/cryptocurrency-mcp-server": ("get_token_price", "src/desk3_service/server.py:559"),
    "crypto_prices/smhnkmr/realtime-crypto-mcp-server": ("get-rates", "src/tools/getRates.ts:78"),
    "stock_quotes/archiephan78/ssi-stock-mcp-server": ("get_daily_ohlc", "src/ssi_stock_mcp_server/server.py:345"),
    "stock_quotes/peikuo/china-stock-mcp-server": ("stock_zh_a_spot", "main.py:156"),
    "translation/kunalchhabra/translation-mcp-server": ("add_translation", "src/mcp/tools/translation_tools.py:45"),
    "geocoding/webcoderz/MCP-Geo": ("geocode_location", "geo.py:72"),
    "stock_quotes/sachinjhamb/stockMcpServerAQnpm": ("get_stock_details", "index.js:45"),
}
# server_id -> (tool name, "file:line", description or None to read the next string literal)
EXPLICIT = {
    "air_quality/sr5434/aqi-mcp": ("get_aqi", "main.py:13", ""),
    "crypto_prices/PelleNybe/Crypto-MCP-Server---by-Corax-CoLAB": ("price", "coingecko_mcp.py:32", ""),
    "crypto_prices/NalinKaushik/crypto-mcp-server": ("get_price", "src/crypto_mcp/server.py:51", "Get current cryptocurrency price."),
    "crypto_prices/akshaygp18/crypto-mcp-server": ("get_coin_price", "src/crypto_mcp_server/server.py:393",
        "Get current prices for one or more coins in one or more currencies, optionally with market cap, 24-hour volume, and 24-hour change. Batch coins into a single call rather than calling once per coin."),
    "currency_exchange/RichGom84/exchange_rate_MCP": ("get_usd_krw_exchange_rate", "server.py:35",
        "Get the latest USD/KRW exchange rate. Use this when the user asks in Korean or English about the dollar-won exchange rate, USD to KRW, or how much 1 US dollar is in Korean won."),
    "currency_exchange/sin4ch/exchange-rate-mcp": ("convert_currency", "main.py:16", None),
    "geocoding/adelie-ai/geocode-mcp": ("geocode", "src/service.rs:67",
        "Resolve a location name to geographic coordinates (latitude and longitude) using the Photon geocoding API (powered by OpenStreetMap). Returns up to 'count' matching locations with their coordinates, country, country code, region, and place type. Supports cities, addresses, and points of interest."),
    "movies/Shaamam/movie-mcp-server": ("getMovieInfo", "src/main/java/io/shaama/movieserver/tools/MovieInformation.java:28", "Gets the Information about the Movie"),
    "movies/saravana87/Movie-MCP-Server": ("search_web", "mcp_moviedb_server.py:37", ""),
    "news/deficlow/zipp-mcp": ("search", "src/zipp_mcp/server.py:66",
        "Full-text search across Zipp's news catalogue. Returns recent matching stories ordered by recency (with relevance as a tiebreaker). Use for questions like 'what's happening with Bitcoin ETFs?' or 'find news about Solana hacks'."),
    "news/the0807/GeekNews-MCP-Server": ("get_articles", "src/server.py:71", None),
    "stock_quotes/agilesolutions/stock-mcp-server": ("getLatestStockPrices", "src/main/java/com/agilesolutions/mcp/tools/StockTools.java:31", "get actual stock prices"),
    "stock_quotes/imdurgadas/cf-stock-mcp-server": ("analyze_stock", "src/index.ts:86", ""),
    "stock_quotes/yadinae/stock-mcp-server": ("get_global_quote", "tools/handlers/quote.py:102", None),
    "weather/Cooosin/WeatherMcpServer": ("getWeather", "src/main/java/com/coosin/mcpserver/service/WeatherService.java:38", "获取某个城市的实时天气"),
    "weather/Krytons/Weather-MCP-Server": ("getCurrentWeather", "src/tools/WeatherTools.ts:51", "Get the current weather for a specified city"),
    "weather/ezh0v/weather-mcp-server": ("current_weather", "internal/server/tools/weather.go:12", None),
    "weather/jjyaoao/weather-mcp-server": ("get_weather", "server.py:44", None),
    "web_search/PROJECT-B-26/groundroute-mcp": ("search", "server.py:147", None),
    "web_search/menesekinci/search-mcp": ("web_search", "main.go:31", None),
    "translation/Deep-Intelligent-Pharma/Translationx-mcp-server": ("submit_translation", "src/tools/file_tools.py:50", None),
    "movies/Grinv/tmdb-mcp": ("search_movies", "src/tools/tmdb/search.ts:36", "CONCAT"),
}
LITERAL = re.compile(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'|`((?:[^`\\]|\\.)*)`', re.S)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def literal_after(path: Path, line: int) -> str:
    src = path.read_text(errors="ignore")
    offset = sum(len(l) + 1 for l in src.split("\n")[: line - 1])
    m = LITERAL.search(src, offset)
    return norm(next(g for g in m.groups() if g is not None))


def concat_after(path: Path, line: int) -> str:
    """Join a JS/TS description built as "a" + "b" + ... starting at `line`."""
    src = path.read_text(errors="ignore")
    offset = sum(len(l) + 1 for l in src.split("\n")[: line - 1])
    m = re.compile(r'"((?:[^"\\]|\\.)*)"(\s*\+\s*"((?:[^"\\]|\\.)*)")*').search(src, offset)
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(0))
    return norm("".join(parts))


def provider_names(row: dict) -> list[str]:
    names = set()
    for key in ("upstream_providers", "l1_declared_provider", "l2_declared_provider", "origin_a"):
        for p in row.get(key, "").split(";"):
            p = p.strip()
            if p and p.lower() not in ("unknown", "ambiguous"):
                names.add(p)
                base = re.sub(r"\s*\(.*?\)\s*", " ", p).strip()
                names.add(base)
                names.add(base.replace(" ", ""))
    return sorted((n for n in names if len(n) >= 3), key=len, reverse=True)


def main() -> None:
    repos, cands = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
    needed = json.loads((OUT / "servers_needed.json").read_text())
    coding = {}
    for f in (ROOT / "data" / "tool_survey" / "coding.csv", ROOT / "data" / "tool_survey_2" / "coding.csv"):
        for r in csv.DictReader(f.open(encoding="utf-8")):
            coding[r["server_id"]] = r
    texts, problems = {}, []
    for s in needed:
        sid = s["server_id"]
        repo = repos / sid.replace("/", "__")
        if sid in EXPLICIT:
            tool, at, desc = EXPLICIT[sid]
            file, line = at.rsplit(":", 1)
            if desc is None:
                desc = literal_after(repo / file, int(line))
            elif desc == "CONCAT":
                desc = concat_after(repo / file, int(line))
        else:
            if sid in FROM_CANDIDATES:
                tool, at = FROM_CANDIDATES[sid]
                pick = next((t for t in cands[sid]["tools"] if t["tool"] == tool and t["at"] == at), None)
            else:
                pick = json.loads((Path(sys.argv[2]).parent / "auto_picks.json").read_text())[sid]
            if pick is None:
                problems.append(f"{sid}: candidate not found")
                continue
            tool, at, desc = pick["tool"], pick["at"], pick["description"]
        file, line = at.rsplit(":", 1)
        src = (repo / file).read_text(errors="ignore")
        desc = norm(desc)
        if desc and desc[:60] not in norm(src):
            problems.append(f"{sid}: description not found verbatim in {file}")
        lines = src.split("\n")
        lo, hi = max(0, int(line) - 40), int(line) + 40
        if tool not in "\n".join(lines[lo:hi]):
            problems.append(f"{sid}: tool name '{tool}' not within 40 lines of {at}")
        truncated = len(desc) > MAXLEN
        texts[sid] = {"server": sid.split("/", 1)[1], "tool": tool,
                      "description": (desc[:MAXLEN].rstrip() + " …") if truncated else desc,
                      "truncated": truncated, "source": f"{s['repo_url']}/blob/{s['commit_sha']}/{at.replace(':', '#L')}",
                      "providers": s["providers"], "strip_names": provider_names(coding[sid])}
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  " + p)
        raise SystemExit(1)
    path = OUT / "tool_texts.json"
    path.write_text(json.dumps(texts, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {path}: {len(texts)} tools, {sum(t['truncated'] for t in texts.values())} truncated, "
          f"{sum(not t['description'] for t in texts.values())} without description; "
          f"sha256 {hashlib.sha256(path.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
