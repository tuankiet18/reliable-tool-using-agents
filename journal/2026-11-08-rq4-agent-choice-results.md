---
title: "2026-11-08 — Kết quả RQ4: agent chọn corroborator với metadata tool thật (gpt-4o-mini, gpt-4.1-mini)"
category: journal
tags: [research-log, provenance, tool-use, ai-agents, evidence]
sources:
  - "synthesis/Protocol - Agent Corroborator Choice with Real Tool Metadata.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/rq4_agent_choice/runner/run_rq4.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/rq4_agent_choice/runner/results_gpt4omini.jsonl"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/rq4_agent_choice/runner/results_gpt41mini.jsonl"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_rq4_20261108/analysis.json"
created: 2026-11-08T21:00:00+07:00
updated: 2026-11-08T21:00:00+07:00
summary: >-
  RQ4 chạy xong theo Amendment A2 (OpenAI API, 1.008 lời gọi mỗi model, 0 output invalid). H-A1 và H-A2 đều được ủng hộ ở cả hai model với prompt chính; nhưng prompt trung tính cho kết quả ngược: thêm tên provider làm tăng shared-choice rate lên khoảng 0,8.
provenance:
  extracted: 0.80
  inferred: 0.20
base_confidence: 0.6
lifecycle: draft
lifecycle_changed: 2026-11-08
---

# Kết quả RQ4 — 2026-11-08

PRELIMINARY: chưa đưa vào ledger và paper. Chạy theo [[synthesis/Protocol - Agent Corroborator Choice with Real Tool Metadata]] sau Amendment A2 (đổi từ Ollama local sang OpenAI API vì máy chỉ có RTX 3050 4 GB).

## Cách chạy (FACT)

- Model: `gpt-4o-mini-2024-07-18` và `gpt-4.1-mini-2025-04-14`; temperature 0, seed 0, tối đa 200 token; `items.jsonl` SHA-256 khớp khóa.
- Mỗi model 1.008 lời gọi, 0 output invalid, manipulation check PASS cho cả hai.
- Chạy bị ngắt vài lần do hạn mức API (key cũ bị giới hạn 50 request/ngày dù tài khoản đã lên tier Build); đổi sang key mới thì chạy tiếp được. Script bỏ qua câu đã làm nên không có câu trùng. Pilot 20 câu nằm ở file riêng và không dùng trong phân tích.

## Kết quả (shared-choice rate, CI 95% bootstrap theo bộ lựa chọn, 56 bộ)

| Điều kiện | gpt-4o-mini | gpt-4.1-mini |
|---|---|---|
| Prompt chính, C0 (mô tả gốc) | 0,423 [0,327; 0,518] | 0,339 [0,238; 0,446] |
| Prompt chính, C1 (thêm provider) | 0,107 [0,048; 0,173] | 0,054 [0,018; 0,095] |
| Prompt chính, C2 (xóa provider) | 0,435 [0,351; 0,524] | 0,387 [0,292; 0,482] |
| Prompt trung tính, C0 | 0,583 | 0,518 |
| Prompt trung tính, C1 | 0,804 | 0,786 |
| Prompt trung tính, C2 | 0,542 | 0,482 |

- **H-A1 (C1 − C0 < 0):** ủng hộ ở cả hai model (−0,315 và −0,286; p Holm < 0,0001).
- **H-A2 (C1 < 1/3):** ủng hộ ở cả hai model (0,107 và 0,054; p Holm < 0,0001).
- Position bias rõ: vị trí C ít được chọn nhất (0,13–0,14); vị trí A nhiều nhất.

## INFERENCE và OPEN QUESTION

- **INFERENCE:** khi prompt nhắc tới "độc lập", model dùng được dòng `Upstream provider` để né tool cùng nguồn. Ủng hộ khuyến nghị gắn nhãn provider của paper, nhưng chỉ cho prompt chính.
- **Phát hiện ngoài dự đoán:** ở prompt trung tính (không nói "độc lập"), C1 làm shared-choice rate **tăng** lên khoảng 0,8, nghĩa là model đọc provider trùng với primary như dấu hiệu "tool phù hợp để kiểm tra". Hiệu ứng này chỉ được mô tả, không nằm trong H-A1/H-A2 (protocol §2 xếp prompt trung tính vào phần mô tả).
- **OPEN QUESTION:** đây là cách đọc thông tin hay chỉ là bias "chọn tool giống primary"? Chưa có phép đo để phân biệt; không nên viết thành cơ chế. (Cập nhật cùng ngày: phân tích `reason` bên dưới cho thấy model có đọc nhãn và diễn giải nó là "nhất quán".)

## Phân tích phụ theo loại thông tin và câu `reason` (FACT, mô tả)

Script `src/rq4_breakdowns.py` (SHA `67ccb128…5acd`), đầu ra `results_rq4_breakdowns_20261108/breakdowns.json` (SHA `d0b1d705…51d0`). Đây là hai phần protocol §2 và §7 đã hứa. **Quy tắc từ khóa cho `reason` được viết sau khi đã biết kết quả chính**, là quy tắc từ vựng thô, không phải đánh giá của người hay model.

- **Theo loại thông tin** (11 loại, mỗi loại 2–10 bộ nên chỉ mô tả, không CI diễn giải): ở prompt chính, C1 gần 0 ở hầu hết loại (crypto, weather, movies, geocoding, air quality, books đều `0.00` ở cả hai model); còn cao hơn ở news (`0.28`/`0.17`), web_search (`0.25`/`0.17`), translation (`0.33`/`0.17`), stock (`0.24`/`0.05`) và currency (`0.14`/`0.10`). Ở prompt trung tính, C1 tăng ở hầu hết loại (crypto `1.00` cả hai model), nhưng không tăng ở web_search (`0.00`/`0.17`, thấp hơn C0) và translation (`0.33`/`0.50`).
- **`reason` có nhắc tới nguồn** (regex `provider|upstream|source|underlying|same/different api…`): ở prompt chính, 90% và 98% lý do ở C1 nhắc nguồn, so với 61% và 89% ở C0. Từ `provider`/`upstream` chỉ xuất hiện ở C1 (`0.41`, `0.39`) và gần như không ở C0 (`0.00`, `0.01`).
- **Prompt trung tính, C1:** `0.42` và `0.54` lý do dùng từ `provider`/`upstream`, so với `0.00` ở C0. Khi model chọn tool **cùng nguồn**, `0.52` (gpt-4o-mini) và `0.65` (gpt-4.1-mini) lý do nhắc provider; khi chọn tool khác nguồn chỉ `0.03` và `0.14`. Đọc mẫu ngẫu nhiên các lý do: nhiều câu có dạng "uses the same upstream provider … ensuring consistency", tức model **đọc nhãn** nhưng diễn giải "cùng provider" là "dữ liệu nhất quán, phù hợp để kiểm tra".

**INFERENCE:** thiên lệch ở prompt trung tính không phải do model bỏ qua nhãn; model dùng nhãn nhưng hiểu "kiểm tra lại" là tìm tool nhất quán, không phải độc lập. Lưu ý lý do do model tự viết nên có thể là hợp lý hóa sau khi chọn; điều này chưa được kiểm tra bằng thí nghiệm (ví dụ prompt đảo nghĩa), nên `OPEN QUESTION` về cơ chế vẫn còn, nhưng khả năng "model không nhìn thấy nhãn" bị loại.

## Giới hạn (theo §8 và A2)

Tác vụ chọn một lần, không có lỗi được inject; chỉ hai model nhỏ cùng hãng, model đóng; OpenAI không bảo đảm seed hoàn toàn xác định (đã ghi `system_fingerprint`); nhãn provider ở C1 là nhãn coder A (AI). Không viết "agent thật nói chung" hay "human-validated".

## Bước tiếp theo

Cập nhật ledger (claim mới cho RQ4, gồm kết quả prompt trung tính) → paper đầy đủ, bản rút gọn, LaTeX. Chưa commit.

Liên quan: [[synthesis/Protocol - Agent Corroborator Choice with Real Tool Metadata]], [[projects/reliable-tool-using-ai-agents/HANDOFF-2026-11-08]].
