---
title: >-
  Protocol: Agent Corroborator Choice with Real Tool Metadata
category: synthesis
tags: [research-protocol, provenance, tool-use, ai-agents, evidence]
sources:
  - "synthesis/Protocol: Expanded Real-Tool Metadata Survey.md"
  - "projects/reliable-tool-using-ai-agents/paper/paper-short.md"
  - "projects/reliable-tool-using-ai-agents/paper/proof-j-condition.md"
created: 2026-10-18T10:00:00+07:00
updated: 2026-10-18T10:00:00+07:00
summary: >-
  Protocol thí nghiệm agent thật (RQ4): LLM chọn một corroborator trong 3 tool MCP thật; so sánh mô tả gốc, mô tả có thêm tên provider, và mô tả đã xóa tên provider. Viết trước khi trích mô tả tool và trước mọi lời gọi model.
lifecycle: draft
lifecycle_changed: 2026-10-18
protocol_version: "1.0"
protocol_status: awaiting-author-confirmation
---

# Protocol: Agent chọn corroborator với metadata tool thật (RQ4)

> [!important] **PROSPECTIVE.** Viết ngày 2026-10-18, **trước khi** trích mô tả tool và **trước mọi lời gọi model**. Đây là protocol nội bộ, không phải preregistration trên registry độc lập. Mọi thay đổi sau khi khóa phải ghi thành amendment có ngày ở §9.

## 1. Mục tiêu

Paper hiện chỉ **chiếu** số liệu survey lên selector model (§6.2 của paper-short). Thí nghiệm này **đo hành vi của LLM thật**: khi agent phải chọn một tool để kiểm tra chéo, việc mô tả tool có nêu tên provider có giúp agent tránh chọn tool dùng chung nguồn với primary không?

**RQ4. When an LLM agent must choose a corroborating tool from real MCP tool descriptions, does adding the upstream provider to the descriptions reduce how often it chooses a corroborator that shares the primary's provider?**

Giải thích: nếu ghi rõ "Upstream provider: X" trong mô tả tool, như paper khuyến nghị, thì agent có chọn nguồn độc lập tốt hơn không?

## 2. Hypothesis (ghi trước)

Gọi **shared-choice rate** là tỷ lệ lần model chọn đúng candidate dùng chung provider với primary. Chọn ngẫu nhiên cho 1/3.

- **H-A1 (chính).** *With the primary prompt, the shared-choice rate is lower when every description states its upstream provider (C1) than with the original descriptions (C0).* Đạt nếu chênh lệch C1 − C0 có cận trên của 95% CI nhỏ hơn 0.
- **H-A2 (chính).** *With provider-annotated descriptions (C1), the shared-choice rate is below random (1/3).* Đạt nếu cận trên 95% CI của tỷ lệ ở C1 nhỏ hơn 1/3.
- **Mô tả, không kiểm định:**
  - C0 so với 1/3;
  - C2 (xóa tên provider) so với C0;
  - prompt trung tính so với prompt chính;
  - kết quả riêng theo từng model và từng loại thông tin;
  - tỷ lệ câu giải thích (`reason`) có nhắc tới nguồn dữ liệu.

**Dự đoán định tính, rút từ RQ2 và RQ3.** Ở C1, nhãn đầy đủ và đúng (`J = 1`, `k = 1`), nên shared-choice rate gần 0 nếu model dùng được thông tin này. Ở C0, phần lớn mô tả thiếu tên provider, nên tỷ lệ gần 1/3, trừ khi model đoán provider từ tên repo hoặc kiến thức có sẵn.

## 3. Stimuli: bộ lựa chọn

- **Nguồn:** nhãn coder A đã khóa của survey 1 (`data/tool_survey/coding.csv`) và survey 2 (`data/tool_survey_2/coding.csv`, chỉ tập ước lượng). Bỏ server có cờ `AMBIGUOUS` và server không có upstream xác định. Ground truth là provider ở **operator level**.
- **Primary dùng được:** trong cùng survey và cùng loại thông tin, có ít nhất 1 server dùng chung provider và ít nhất 2 server độc lập. Kiểm tra ngày 2026-10-18 cho **56 primary**. Mỗi primary tạo **một bộ lựa chọn**: 1 candidate dùng chung và 2 candidate độc lập, chọn ngẫu nhiên với seed `20261018`.
- **Văn bản của mỗi tool:** tên server, cùng tên và description của **tool thuộc loại thông tin** đó, trích **nguyên văn** từ code tại commit đã ghim, chỉ đọc tĩnh. Giới hạn 400 ký tự; nếu dài hơn thì cắt và ghi rõ. File stimuli được khóa bằng SHA-256 ở §9 **trước** lời gọi model đầu tiên.

## 4. Điều kiện (mọi bộ lựa chọn đều qua cả ba điều kiện)

| Mã | Điều kiện | Nội dung mỗi tool |
|---|---|---|
| C0 | Gốc | Văn bản trích nguyên văn |
| C1 | Có tên provider | Văn bản gốc, thêm dòng `Upstream provider: <provider>` (operator level, theo nhãn coder A) |
| C2 | Xóa tên provider | Văn bản gốc, thay mọi tên provider (tên khai báo và tên upstream của server đó) bằng `[provider]` |

Mỗi bộ được trình bày theo **3 vòng xoay vị trí**, để candidate dùng chung lần lượt nằm ở A, B và C. Cách này khử thiên lệch theo vị trí.

## 5. Prompt

- **Prompt chính.** Agent được cho biết: kết quả của primary cần được kiểm chứng trước khi hành động; phải chọn **một** tool trong A/B/C *"most likely to provide an independent check, i.e. not relying on the same underlying data source as the primary"*. Trả lời bằng JSON `{"choice": "A|B|C", "reason": "<một câu>"}`.
- **Prompt trung tính (phụ).** Giống prompt chính nhưng chỉ nói *"choose the best tool to double-check the primary's result"*, không nhắc tới độc lập.
- Văn bản prompt đầy đủ được ghi vào file và khóa SHA-256 cùng stimuli.

## 6. Model và cách chạy

**Phương án đã chọn (tác giả, 2026-10-18): chạy local trên một máy mượn có RTX 4060 8 GB VRAM**, qua Ollama, chi phí 0. Hai model 7–8B, lượng tử hóa 4-bit (`q4_K_M`), thuộc hai họ khác nhau:

- `qwen2.5:7b-instruct-q4_K_M` (Qwen2.5-7B-Instruct)
- `llama3.1:8b-instruct-q4_K_M` (Llama-3.1-8B-Instruct)

Máy chạy chỉ cần Python 3 và Ollama. Claude chuẩn bị một gói chạy độc lập gồm stimuli, prompt và script gọi API Ollama tại `localhost:11434`. Tác giả chạy gói đó trên máy mượn và mang file kết quả JSONL về. Script ghi lại digest của từng model (`ollama show`), phiên bản Ollama và thông tin GPU vào file kết quả.

Tên và phiên bản model chính xác được ghi ở §9 khi khóa. Temperature 0, tối đa 200 token output. Mỗi model chạy 56 bộ × 3 vòng xoay × 3 điều kiện × 2 prompt = **1.008 lời gọi**.

**Output không hợp lệ** (không parse được JSON hoặc chọn ngoài A/B/C): gọi lại 1 lần với cùng input. Nếu vẫn không hợp lệ thì ghi `invalid`, và loại khỏi mẫu số khi tính tỷ lệ. Nếu một model có hơn **10%** output không hợp lệ ở prompt chính, model đó được báo cáo là **thất bại manipulation check** và không dùng để đánh giá H-A1 và H-A2.

## 7. Phân tích

- **Đơn vị:** bộ lựa chọn. Tỷ lệ của mỗi bộ là trung bình qua 3 vòng xoay.
- **CI:** bootstrap theo bộ lựa chọn, 10.000 lần, seed `20261018`. Hiệu C1 − C0 tính theo cặp trên cùng bộ.
- **Phân tích riêng từng model**, không gộp. H-A1 và H-A2 được đánh giá trên mỗi model; hiệu chỉnh Holm trên 4 kiểm định (2 hypothesis × 2 model), tính p bằng bootstrap.
- **Báo cáo đầy đủ:** số lời gọi, số output không hợp lệ, tỷ lệ chọn theo vị trí, kết quả theo loại thông tin.
- **Script phân tích được viết và chạy thử trên dữ liệu giả trước khi gọi model.**

## 8. Giới hạn biết trước

- Đây là **tác vụ chọn một lần**, không phải một vòng agent đầy đủ; không có lỗi thật được inject.
- Model có thể đoán provider từ tên repo hoặc kiến thức có sẵn, nên C2 không xóa hết thông tin.
- C1 dùng nhãn coder A (AI) làm sự thật; nếu nhãn sai thì thông tin "Upstream provider" cũng sai.
- Model 7–8B chạy local có thể không đại diện cho agent thật dùng model lớn.
- Thí nghiệm được đặt ra **sau** khi đã có kết quả survey; nó kiểm định một khuyến nghị của paper, không phải câu hỏi có từ đầu.

## 9. Nhật ký khóa và amendment

| Ngày | Sự kiện | Ghi chú |
|---|---|---|
| 2026-10-18 | Protocol v1.0 được viết | Chưa trích mô tả tool, chưa gọi model nào |
| 2026-10-18 | Tác giả chọn chạy local trên RTX 4060 8 GB | §6 cố định 2 model 7–8B; protocol vẫn chờ tác giả xác nhận |

## Liên quan

- [[synthesis/Protocol: Expanded Real-Tool Metadata Survey]]
- [[synthesis/Protocol: Author Blind Coding of Survey 2 Subset]]
- [[projects/reliable-tool-using-ai-agents/paper/proof-j-condition]]
