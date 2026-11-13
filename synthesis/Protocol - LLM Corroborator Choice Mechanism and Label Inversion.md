---
title: "Protocol: Cơ chế chọn corroborator của LLM và thí nghiệm đảo nhãn (RQ4 mở rộng)"
category: synthesis
tags: [research-protocol, experiment, provenance, tool-use, ai-agents]
sources:
  - "journal/2026-11-08-rq4-agent-choice-results.md"
  - "synthesis/Protocol - Agent Corroborator Choice with Real Tool Metadata.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_rq4_20261108/analysis.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_rq4_breakdowns_20261108/breakdowns.json"
created: 2026-11-12T09:00:00+07:00
updated: 2026-11-13T09:00:00+07:00
summary: >-
  Protocol cho thí nghiệm tiếp theo của RQ4: đảo nhãn provider để kiểm tra LLM có thực sự làm theo nhãn không, thêm prompt "nhất quán" để kiểm tra giải thích cho kết quả ngược ở prompt trung tính, và thêm một model lớn hơn (gpt-4.1). Tác giả xác nhận 2026-11-13; có Amendment B1 trước lời gọi đầu tiên.
lifecycle: active
lifecycle_changed: 2026-11-13
---

# Protocol: cơ chế chọn corroborator của LLM và thí nghiệm đảo nhãn (RQ4 mở rộng)

> [!important] **ĐÃ XÁC NHẬN (2026-11-13), kèm Amendment B1 ghi trước lời gọi model đầu tiên (§9).** Viết ngày 2026-11-12, **trước khi** dựng stimuli mới và **trước mọi lời gọi model**. Đây là protocol nội bộ, không phải preregistration trên registry độc lập. Số RQ trong ghi chú này theo vault (RQ4 = thí nghiệm LLM; trong paper là RQ3).

## 1. Vì sao cần thí nghiệm này

RQ4 (đã xong, 2026-11-08) cho kết quả: với prompt nhắc độc lập, nhãn provider giảm mạnh việc chọn tool cùng nguồn; với prompt trung tính, nhãn lại **tăng** việc chọn tool cùng nguồn lên khoảng 0,80. Ba điểm yếu còn lại:

1. **Cơ chế chưa đo.** Câu `reason` gợi ý model đọc nhãn và hiểu "cùng provider" là "nhất quán", nhưng lý do do model tự viết có thể là hợp lý hóa sau khi chọn. Chưa có phép đo nhân quả.
2. **Nhãn luôn đúng hoàn toàn** (`J = 1`, `k = 1`), nên kết quả chưa nói gì về nhãn sai, trong khi RQ2 (điều kiện `J`) nói nhãn sai có thể gây hại.
3. **Chỉ hai model nhỏ cùng hãng.**

Chi phí thật của RQ4 chỉ khoảng **0,29 USD** (ước từ token ghi trong file raw và giá niêm yết: `gpt-4o-mini` ~0,08, `gpt-4.1-mini` ~0,21), thấp hơn nhiều so với ngân sách ~5 USD, nên có chỗ cho một thí nghiệm lớn hơn.

## 2. Ý tưởng chính: đảo nhãn (label inversion)

Nếu model thật sự **làm theo nhãn**, thì đảo nhãn sẽ đảo kết quả, và hướng đảo cho biết model hiểu nhãn theo nghĩa nào:

- **Điều kiện C4 (đảo nhãn):** trong mỗi bộ, candidate *thật sự* dùng chung provider với primary bị gắn một provider **giả** (decoy); đúng **một** candidate *thật sự* độc lập bị gắn provider **của primary**; candidate độc lập còn lại giữ nhãn đúng. Nhãn của primary luôn đúng. Đây là trường hợp `J = −1` ở mức từng bộ.
- **Nếu model dùng nhãn theo nghĩa "tìm nguồn khác"** (prompt nhắc độc lập): nó sẽ tránh candidate mang nhãn trùng primary, tức tránh tool *độc lập thật* và chọn nhầm tool *chung thật* (gắn nhãn decoy) → shared-choice rate **tăng** so với C0.
- **Nếu model dùng nhãn theo nghĩa "tìm nguồn nhất quán"** (prompt trung tính): nó sẽ chọn candidate mang nhãn trùng primary, tức tool độc lập thật → shared-choice rate **giảm** so với C0.
- **Nếu model bỏ qua nhãn:** C4 không khác C0.

Đây là phép đo nhân quả (can thiệp vào nhãn, giữ nguyên mô tả), khác với việc đọc `reason`.

## 3. Điều kiện, prompt và model

**Stimuli:** dùng lại 56 bộ và `tool_texts.json` của RQ4. `items.jsonl` cũ (SHA-256 `e0b33c12…be086`) **không đổi**; các dòng C0, C1 của prompt chính và trung tính được **dùng lại** (không gọi lại) để so sánh theo cặp. File mới `items_b.jsonl` chỉ chứa các ô mới và được khóa bằng SHA-256 trước lời gọi đầu tiên.

**Điều kiện:** C0 (gốc), C1 (nhãn đúng), **C4 (đảo nhãn, mới)**. Decoy cho candidate chung: một provider lấy từ **một bộ khác cùng category** (không phải provider thật của bất kỳ tool nào trong bộ này), chọn xác định bằng seed `20261112`; nếu không có thì ghi `no_decoy` và loại bộ đó khỏi phân tích C4 (báo số bộ bị loại). Ba vòng xoay vị trí như cũ.

**Prompt:**
- **main** và **neutral**: giữ nguyên văn như RQ4.
- **consistency (mới):** giống neutral nhưng nói *"choose the tool whose result is most likely to be consistent with the primary tool's result"*. Dùng để kiểm tra trực tiếp giải thích "nhất quán".

**Ô thí nghiệm** (mỗi ô là 56 bộ × 3 vòng xoay = 168 lời gọi):

| Prompt | C0 | C1 | C4 |
|---|---|---|---|
| main | dùng lại | dùng lại | **mới** |
| neutral | dùng lại | dùng lại | **mới** |
| consistency | **mới** | **mới** | **mới** |

**Model:**
- `gpt-4o-mini-2024-07-18` và `gpt-4.1-mini-2025-04-14`: chỉ chạy các ô mới (**696** lời gọi mỗi model sau khi dựng stimuli; xem Amendment B1: C4 chỉ có ở 40/56 bộ).
- **`gpt-4.1` (model lớn hơn, bản snapshot ghi khi chạy):** chạy **toàn bộ** các ô, kể cả C0/C1 của main và neutral, để có đường chuẩn riêng: toàn bộ **1.368** lời gọi (không chạy C2).

Cấu hình gọi giữ như RQ4 (Chat Completions, `response_format: json_object`, temperature 0, seed 0, tối đa 200 token, retry 1 lần, ngưỡng invalid 10%).

**Chi phí ước tính:** ~840 × 2 + 1.512 ≈ 3.200 lời gọi, ước 1,5–2,5 USD (gpt-4.1 đắt hơn khoảng 5 lần so với gpt-4.1-mini theo giá niêm yết; ước từ token của RQ4). **Trần cứng 3 USD**: dừng nếu vượt, báo tác giả trước khi tiếp tục. Chạy `--limit 20` vào file riêng để đo token thật trước khi chạy đầy đủ.

## 4. Hypothesis (ghi trước)

Shared-choice rate như RQ4. Phân tích theo từng model, đơn vị là bộ lựa chọn, hiệu theo cặp trên cùng bộ.

- **H-B1 (tránh nhãn trùng primary, prompt chính) — theo Amendment B1.** Gọi *mimic* là candidate độc lập thật bị gắn nhãn của primary ở C4, và `d = P(chọn mimic | C4) − P(chọn đúng candidate đó ở cùng vị trí | C0)`, trung bình theo bộ qua 3 vòng xoay (số hạng C0 khử thiên lệch vị trí). *With the main prompt, models choose the candidate that carries the primary's provider label less often than the same candidate without labels (d < 0).* Đạt nếu cận trên 95% CI của `d` nhỏ hơn 0.
- **H-B2 (hướng nhất quán, prompt trung tính) — theo Amendment B1.** *With the neutral prompt, models choose the candidate that carries the primary's provider label more often than the same candidate without labels (d > 0).* Đạt nếu cận dưới 95% CI của `d` lớn hơn 0. Đây là dự đoán của cách giải thích "cùng provider = nhất quán"; nếu sai, cách giải thích đó bị bác bỏ.
- *Đối chiếu phụ (mô tả, không Holm):* hiệu `C4 − C0` của shared-choice rate ở prompt chính và trung tính, như bản nháp ban đầu.
- **H-B3 (kiểm tra trực tiếp).** *With the consistency prompt, the shared-choice rate is higher under correct provider labels (C1) than under original descriptions (C0).* Đạt nếu cận dưới 95% CI của `C1 − C0` lớn hơn 0.
- **H-B4 (nhân rộng).** Với `gpt-4.1`, H-A1 và H-A2 của RQ4 được đánh giá lại bằng đúng quy tắc cũ (prompt chính, C1 so với C0 và so với 1/3).

**Hiệu chỉnh nhiều kiểm định:** Holm trên mọi kiểm định ở trên (H-B1, H-B2, H-B3 cho cả 3 model = 9; H-A1, H-A2 cho `gpt-4.1` = 2; tổng 11) ở α = 0,025 một phía, cách làm như RQ4 (bootstrap 10.000 lần, seed `20261112`). Hai model đã có (RQ4) không đánh giá lại H-A1/H-A2.

**Diễn giải trước khi biết kết quả:**

| Kết quả | Hiểu là |
|---|---|
| H-B1 đạt, H-B2 đạt, H-B3 đạt | Model đọc nhãn và hiểu theo nghĩa "nhất quán" khi không được nhắc độc lập; giải thích của RQ4 được ủng hộ |
| H-B1 đạt, H-B2 không đạt | Model làm theo nhãn khi được nhắc độc lập nhưng bias ở prompt trung tính **không** do đọc nhãn theo nghĩa "nhất quán" (cơ chế khác, chưa rõ) |
| H-B1 không đạt | Hiệu ứng giảm ở C1 (RQ4) không đến từ việc dùng giá trị của nhãn (có thể từ sự hiện diện của dòng đó), nên cần xem lại diễn giải của RQ4 |

Mô tả cũ ở bảng trên nói theo hướng "shared-choice rate"; với đại lượng `d` của Amendment B1, "làm theo nhãn khi nhắc độc lập" tương ứng `d < 0` (tránh mimic) và "đọc theo nghĩa nhất quán" tương ứng `d > 0` ở prompt trung tính.

## 5. Phân tích mô tả (không kiểm định)

- Tỷ lệ chọn candidate **mang nhãn trùng primary** (bất kể nhãn đúng hay giả), theo điều kiện và prompt; đây là đại lượng trực tiếp nhất của "làm theo nhãn".
- Kết quả theo loại thông tin, thiên lệch vị trí, tỷ lệ `reason` nhắc provider (quy tắc từ khóa dùng lại của `rq4_breakdowns.py`, ghi rõ quy tắc đã cố định từ trước).
- So sánh `gpt-4.1` với hai model nhỏ.

## 6. Giới hạn biết trước

- Cả ba model đều của OpenAI (đóng), nên chưa trả lời được "model hãng khác"; một model open-weight chạy local bị hạn chế bởi GPU 4 GB.
- Tác vụ vẫn là **chọn một lần** và nhãn đảo là **can thiệp nhân tạo**, không phải nhãn sai tự nhiên của các MCP server.
- C4 là trường hợp cực đoan `J = −1`; nó không phủ các mức nhãn thiếu hoặc sai một phần.
- Decoy lấy từ bộ khác cùng category; có thể hợp lý hơn hoặc kém hơn so với nhãn sai thật.
- Seed của OpenAI không bảo đảm hoàn toàn xác định; ghi `system_fingerprint`.
- Thí nghiệm được đặt **sau** khi đã thấy kết quả RQ4, để giải thích kết quả đó; nó kiểm định một giải thích, không phải câu hỏi có từ đầu.

## 7. Quy trình thực hiện (sau khi tác giả xác nhận)

1. Viết `build_items_b.py` tạo `items_b.jsonl` xác định (seed `20261112`); khóa SHA-256 ở §9 **trước** lời gọi đầu tiên.
2. Viết `rq4b_analyze.py` và chạy thử trên dữ liệu giả (model ngẫu nhiên: không hypothesis nào đạt; model "làm theo nhãn" lý tưởng: H-B1 đạt; model "nhất quán" lý tưởng: cả ba đạt).
3. `--limit 20` pilot vào file riêng để đo token và chi phí; không dùng cho phân tích.
4. Chạy đầy đủ; dừng ngay khi `insufficient_quota` hoặc chi phí vượt 3 USD.
5. Phân tích → journal → ledger → paper (đầy đủ, rút gọn, LaTeX), theo thứ tự đã thống nhất.

## 8. Phạm vi so với thời hạn nộp

Còn khoảng hai tuần đến hạn nộp (tính từ 2026-11-08). Thí nghiệm này chạy trong vài giờ và tốn vài USD; nếu không kịp hoặc kết quả không rõ, paper vẫn nộp được với RQ4 như hiện tại (đã ghi rõ cơ chế chưa đo).

## 9. Nhật ký khóa và amendment

| Ngày | Sự kiện | Ghi chú |
|---|---|---|
| 2026-11-12 | Protocol v0.1 được viết (bản nháp) | Chưa dựng stimuli mới, chưa gọi model nào; chờ tác giả xác nhận |
| 2026-11-13 | **Tác giả xác nhận protocol v0.1** ("Xác nhận, chạy") | Trước khi dựng stimuli; chưa gọi model nào |
| 2026-11-13 | **Dựng stimuli:** `src/rq4b_make_items.py` → `runner/items_b.jsonl` (1.368 item; 696 item mới) | SHA-256 `609a39e1ec608c4e590907fc6d96c036063f992d966ebf028b23ecb99707ac26`. Các item main/neutral C0, C1 được kiểm tra **byte-identical** với `items.jsonl` cũ. 16/56 bộ **không có decoy cùng category** (s1-05, s1-06, s1-07, s2-17, s2-18, s2-25..s2-32, s2-53, s2-54, s2-56) nên bị loại khỏi C4 theo §3; C4 chạy trên **40 bộ**, các so sánh theo cặp liên quan C4 dùng 40 bộ đó |
| 2026-11-13 | **Amendment B1: đổi đại lượng của H-B1 và H-B2, ghi trước lời gọi model đầu tiên** | Lý do: self-test trên dữ liệu giả cho thấy hiệu `C4 − C0` của shared-choice rate chỉ có hiệu ứng kỳ vọng khoảng +0,17 ngay cả với model "làm theo nhãn" hoàn hảo, và không đạt ngưỡng khi model chọn ngẫu nhiên trong phần còn lại, nên H-B1 gốc thiếu power. Thay bằng `d` (xác suất chọn mimic ở C4 trừ xác suất chọn đúng candidate đó ở cùng vị trí ở C0; hiệu ứng kỳ vọng −0,33 và +0,68), trực tiếp hơn và khử thiên lệch vị trí. Hiệu `C4 − C0` gốc giữ làm đối chiếu phụ. H-B3, H-B4, Holm (11 kiểm định), seed và model giữ nguyên. Self-test (`rq4b_analyze.py --selftest`): model ngẫu nhiên không đạt gì; model "tránh nhãn" đạt H-B1; model "nhất quán" đạt H-B1, H-B2, H-B3 |
| 2026-11-13 | **Chạy xong và phân tích** | Ba model, 0 câu không hợp lệ; `analysis_b.json` SHA `6fba6342…c857`; cả 11 kiểm định đạt. Chi tiết: [[journal/2026-11-13-rq4-label-inversion-results]]. Pilot 20 lời gọi của `gpt-4.1` không dùng trong phân tích và đã xóa |

## Liên quan

- [[synthesis/Protocol - Agent Corroborator Choice with Real Tool Metadata]]
- [[journal/2026-11-08-rq4-agent-choice-results]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
