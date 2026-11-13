---
title: "2026-11-13 — RQ4 mở rộng: đảo nhãn cho thấy LLM thật sự làm theo nhãn provider (gpt-4o-mini, gpt-4.1-mini, gpt-4.1)"
category: journal
tags: [research-log, provenance, tool-use, ai-agents, evidence]
sources:
  - "synthesis/Protocol - LLM Corroborator Choice Mechanism and Label Inversion.md"
  - "journal/2026-11-08-rq4-agent-choice-results.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/rq4b_make_items.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/rq4b_analyze.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_rq4b_20261113/analysis_b.json"
created: 2026-11-13T15:00:00+07:00
updated: 2026-11-13T15:00:00+07:00
summary: >-
  Thí nghiệm đảo nhãn của RQ4: cả 11 kiểm định ghi trước đều đạt ở cả ba model. Model tránh candidate mang nhãn của primary khi được nhắc độc lập, chọn nó nhiều hơn khi không được nhắc, và chọn tool cùng nguồn rất nhiều (0,86–0,92) khi được yêu cầu "nhất quán". Giải thích "đọc nhãn rồi hiểu là nhất quán" được ủng hộ bằng can thiệp nhân quả.
provenance:
  extracted: 0.80
  inferred: 0.20
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: 2026-11-13
---

# RQ4 mở rộng — đảo nhãn (2026-11-13)

PRELIMINARY: chưa vào ledger/paper tại thời điểm viết. Chạy theo [[synthesis/Protocol - LLM Corroborator Choice Mechanism and Label Inversion]] (xác nhận 2026-11-13, kèm Amendment B1 ghi trước lời gọi đầu tiên). Số RQ theo vault (RQ4 = thí nghiệm LLM; trong paper là RQ3).

## Làm gì (FACT)

- **Điều kiện C4 (đảo nhãn):** candidate *thật sự* cùng nguồn bị gắn provider **giả**; một candidate *thật sự* độc lập bị gắn provider **của primary** (gọi là *mimic*); phần còn lại giữ nhãn đúng. Chạy trên **40/56 bộ** (16 bộ không có provider giả cùng category nên bị loại theo protocol).
- **Prompt thứ ba (consistency):** yêu cầu chọn tool có kết quả "most likely to be consistent with the primary".
- **Model:** `gpt-4o-mini-2024-07-18`, `gpt-4.1-mini-2025-04-14` (chỉ các ô mới, 696 lời gọi mỗi model) và **`gpt-4.1-2025-04-14`** (toàn bộ 1.368 lời gọi). Không câu nào không hợp lệ.
- **Đại lượng chính `d`** (Amendment B1): xác suất chọn mimic ở C4 trừ xác suất chọn đúng candidate đó ở cùng vị trí ở C0 (khử thiên lệch vị trí).
- Stimuli SHA-256 `609a39e1…ac26`; raw `gpt-4.1` `88326133…1839`, `gpt-4o-mini` `dfae5fb5…72f7`, `gpt-4.1-mini` `01044009…4666`; `analysis_b.json` `6fba6342…c857`. Chi phí ước khoảng 1,6 USD (từ token ghi trong file raw, chưa đối chiếu dashboard). Pilot 20 lời gọi của `gpt-4.1` không dùng trong phân tích và đã xóa.

## Kết quả

**Cả 11 kiểm định ghi trước đều đạt** (Holm, α = 0,025).

| Kiểm định | gpt-4o-mini | gpt-4.1-mini | gpt-4.1 |
|---|---|---|---|
| **H-B1** prompt chính: `d < 0` (tránh mimic) | −0,183 [−0,267; −0,100] | −0,208 [−0,317; −0,108] | −0,258 [−0,383; −0,142] |
| **H-B2** prompt trung tính: `d > 0` (chọn mimic nhiều hơn) | +0,242 [+0,150; +0,342] | +0,183 [+0,083; +0,292] | +0,217 [+0,092; +0,350] |
| **H-B3** prompt "nhất quán": shared-choice C1 − C0 > 0 | +0,292 [+0,196; +0,393] | +0,298 [+0,202; +0,393] | +0,333 [+0,226; +0,446] |
| **H-B4** (chỉ gpt-4.1) H-A1: C1 − C0 < 0 | | | −0,250 [−0,357; −0,149] |
| **H-B4** (chỉ gpt-4.1) H-A2: tỷ lệ C1 < 1/3 | | | 0,036 [0,006; 0,071] |

**Mô tả (không kiểm định):**

- Ở prompt chính, tỷ lệ model chọn mimic ở C4 gần 0 (`0,025`, `0,000`, `0,000`): model **tránh candidate mang nhãn của primary**, dù candidate đó thật sự độc lập.
- Ở prompt "nhất quán", shared-choice rate ở C1 là `0,881`, `0,863`, `0,917` (so với C0 `0,589`, `0,565`, `0,583`): khi được yêu cầu tìm nguồn nhất quán, model chọn tool cùng provider gần như luôn luôn. Ngay cả ở C0 (không nhãn) tỷ lệ này đã cao hơn `1/3`, nên phần "giống" còn đến từ chính mô tả tool.
- Ở prompt trung tính, model chọn mimic ở C4 với tỷ lệ `0,442`, `0,450`, `0,483` (khoảng +0,18 đến +0,24 so với cùng candidate ở C0): hành vi là **hỗn hợp**, nghiêng về "nhất quán" nhưng không hoàn toàn.
- Model lớn `gpt-4.1` có cùng hướng với hai model nhỏ; kết quả ngược ở prompt trung tính nhẹ hơn: C1 `0,607` so với C0 `0,530`, trong khi hai model nhỏ tăng từ khoảng `0,5–0,6` lên `0,79–0,80`. Đây là mô tả, không kiểm định.
- `gpt-4.1` ở prompt chính C0 chọn tool cùng nguồn `0,286` và C1 `0,036`: nhân rộng RQ4 ở một model lớn hơn.
- Đối chiếu phụ `C4 − C0` của shared-choice rate (ở prompt trung tính): −0,208, −0,167, −0,250 (CI không chứa 0); ở prompt chính CI chứa 0 cho hai model nhỏ, còn `gpt-4.1` là +0,125 [−0,017; +0,267].

## INFERENCE và giới hạn

- **INFERENCE (được ủng hộ bởi can thiệp):** model **thật sự dùng giá trị của nhãn**; giải thích ở [[journal/2026-11-08-rq4-agent-choice-results]] ("đọc nhãn rồi hiểu cùng provider là nhất quán") được ủng hộ mạnh hơn trước, vì đảo nhãn đảo hành vi theo đúng hướng dự đoán ở cả ba model. Điều này loại cách giải thích "hiệu ứng ở C1 chỉ do sự hiện diện của dòng chữ".
- **OPEN QUESTION:** hành vi ở prompt trung tính là hỗn hợp; chưa biết tỷ lệ nào là "nhất quán" so với các yếu tố khác (như độ giống của mô tả).
- **Giới hạn:** cả ba model đều của OpenAI; tác vụ chọn một lần; nhãn đảo là can thiệp nhân tạo (`J = −1` ở từng bộ), không phải nhãn sai tự nhiên; C4 chỉ trên 40 bộ (16 bộ không có provider giả cùng category: cả 7 bộ currency_exchange, cả 3 geocoding, 3/4 web_search, cả 2 books và 1/6 movies; kết quả C4 vì vậy không đại diện cho các loại này); ngưỡng tương đương không áp dụng; thí nghiệm đặt **sau** khi thấy kết quả RQ4 để kiểm định một giải thích; Amendment B1 đổi đại lượng chính trước lời gọi đầu tiên sau khi self-test cho thấy đại lượng gốc thiếu power (đại lượng gốc vẫn được báo cáo phụ).

## Bước tiếp theo

Journal (xong) → ledger (C53–C55) → paper đầy đủ, bản rút gọn, LaTeX. Chưa commit.

Liên quan: [[synthesis/Protocol - LLM Corroborator Choice Mechanism and Label Inversion]], [[journal/2026-11-08-rq4-agent-choice-results]].
