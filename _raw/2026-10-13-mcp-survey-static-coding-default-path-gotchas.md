---
title: "MCP server survey coding: gotchas when reading the default upstream path statically"
category: skills
tags:
  - topic/mcp
  - research-methods
  - provenance
  - evidence
summary: "Survey 2 coder A labelling of 78 MCP servers found 4 screening errors and several library/config gotchas that only show up when tracing the default code path, not URLs or READMEs."
tier: supporting
related: []
extends: null
contradicts: null
superseded_by: null
capture_source: claude-session
project: "reliable-tool-using-ai-agents"
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-10-13
provenance:
  extracted: 0.8
  inferred: 0.2
sources:
  - "reliable-tool-using-ai-agents session (2026-10-13)"
---

## Sàng lọc phải lần theo đường đi mặc định của tool, không chỉ tìm URL

**Behavior:** Bốn repo đã được sàng lọc là "include" nhưng thực ra không có upstream mặc định: tool trả chuỗi giả ("Implementation in progress"); provider dịch mặc định là `prototype` trả `"[Korean] text"`; Baidu Translate bị tắt bởi `BAIDU_TRANSLATE_ENABLED="false"` nên dùng từ điển cục bộ; URL lấy từ biến môi trường không có mặc định (`env.example` = `xxxx`), còn tool ExchangeRate-API thì bị comment.

**Why it matters:** Có URL API trong repo, hoặc README nói "dùng API X", không chứng minh được rằng tool gọi API đó theo mặc định. Cách bắt lỗi: đọc handler của tool → hàm helper → giá trị mặc định của config/env.

**How to apply:** Ghi lại theo luật sửa lỗi sàng lọc của protocol (thay bằng repo đủ tiêu chí kế tiếp theo hạng) vào `data/tool_survey_2/coding_partial/screening_corrections.json`. Nếu server bị loại nằm trong tập của người gán nhãn đã khóa thì vẫn gán nhãn nó để tính agreement, nhưng loại khỏi ước lượng.

## `ddgs` 9.x mặc định là aggregator nhiều engine, không chỉ DuckDuckGo

**Behavior:** `DDGS().text(q)` với `backend="auto"` (ddgs 9.13.0, `ddgs/ddgs.py:87-90`) truy vấn Wikipedia và Grokipedia trước, sau đó xáo trộn mọi text engine đang bật: Brave, DuckDuckGo, Google, Mojeek, Yahoo, Yandex (Bing bị tắt). Thư viện tự gán `provider="bing"` cho engine duckduckgo và yahoo.

**How to apply:** Một server tự mô tả "search bằng DuckDuckGo qua ddgs" thực chất có cả tập engine trên làm upstream mặc định (theo luật aggregator). Cần đọc thư viện ở đúng phiên bản repo ghim.

## Cấu hình SearXNG: danh sách engine không cho biết engine nào thuộc nhóm "general"

**Behavior:** Trong `settings.yml` đầy đủ, nhiều engine (google, duckduckgo) không khai báo `categories`. Nhóm mặc định của chúng nằm trong module engine của SearXNG, không nằm trong file. Lọc ngây thơ sẽ ra cả bing images, wttr.in…

**How to apply:** Chỉ lấy các web engine đang bật (google, duckduckgo, brave, startpage, wikipedia, wikidata), ghi là INFERRED như cách làm ở survey 1.

## Các quy tắc diễn giải đã dùng (chờ tác giả xác nhận)

- Nguồn tin tức tính là mặc định nếu được gọi khi người dùng có đủ credential, mà không phải đổi thiết lập chọn nguồn.
- Server có nhiều tool cùng loại thông tin: lấy hợp các nguồn mặc định.
- Đổi được base URL qua biến môi trường → `configurable_upstream=True`.
- Tên server chỉ chủ đề (aws-news, youtube-translate, yerevan-aqi) không tính là nêu tên provider.
- SearXNG instance công khai và Ollama chạy cục bộ → `AMBIGUOUS`.
- FastMCP `instructions` không thuộc L1. Mô tả tham số trong input schema thì thuộc L1.
