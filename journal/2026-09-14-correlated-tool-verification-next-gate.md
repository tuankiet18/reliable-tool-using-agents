---
title: >-
  2026-09-14 — Correlated Tool Verification Next Gate
category: journal
tags: [research-log, experiment, verification, tool-failure, reproducibility]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_next_gate"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_live_subset"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_live_subset_1_5b"
  - "https://github.com/mohammadi-hadi/trajectory-judge"
  - "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF"
  - "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF"
summary: >-
  Gate 30 task xác nhận safety–abstention trade-off và đo suy giảm khi provenance metadata sai; partial live-model subset cho thấy quyết định safety phụ thuộc mạnh vào model.
provenance:
  extracted: 0.72
  inferred: 0.25
  ambiguous: 0.03
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: 2026-09-14
tier: core
created: 2026-09-14T00:00:00+07:00
updated: 2026-09-14T12:42:41+07:00
---

# 30-task holdout và imperfect-metadata gate

## Mục tiêu

Thực hiện gate tiếp theo của [[journal/2026-09-13-correlated-tool-verification-pilot]]:

1. thay 10 exploratory fixtures bằng 30 task mới, không trùng task ID;
2. giữ cùng primary tool và cùng `K=2` budget cho các policy;
3. làm provenance metadata bị thiếu hoặc sai;
4. thêm một local model vào bước quyết định verification;
5. kiểm tra lại claim so với strong baseline `random-K`.

## Thiết kế deterministic

- Upstream: `trajectory-judge` commit `d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5`.
- Holdout: `INS-00030`–`INS-00059`, generator seed `20260914`; không trùng 10 task pilot.
- Sáu difficulty strata cân bằng, mỗi stratum năm task.
- Mười fact types cân bằng, mỗi type ba task.
- Seeds: `101, 211, 307, 401, 503`.
- Regimes: `clean`, `independent`, `common_mode`.
- Policies: `single`, `fixed_k`, `random_k`, và `provenance_aware` dưới năm metadata conditions.
- Mọi `K=2` policy bắt đầu bằng `order_api` và dùng đúng một corroborating call.
- Tổng cộng `3,600` paired deterministic episodes.

Metadata conditions:

- `accurate`: đầy đủ và đúng;
- `missing_25`: mỗi metadata entry có xác suất 25% bị thiếu;
- `wrong_25`: mỗi entry có xác suất 25% bị gán sai failure domain;
- `mixed_25_each`: 25% missing cộng 25% wrong;
- `wrong_50`: mỗi entry có xác suất 50% bị gán sai.

## Validation artifact

- `12/12` unit tests pass.
- `ruff check` pass.
- 30/30 task IDs unique, giao với pilot bằng rỗng.
- Task generator tạo lại đúng cùng SHA-256 `f587ec9afa9ce5ffe55d49e60379e1ed7f6602c9f956d889a8b82e056e985ec9`.
- Rerun giữ nguyên hashes của raw results và summaries.
- Mọi `K=2` episode có một extra tool call; mọi `single` episode có zero extra calls.
- Primary observation giống nhau giữa các policy trong cùng task/regime/seed cell.
- Clean regime có zero alarm và zero unsafe accept trong deterministic evaluator.

## Kết quả common-mode

| Policy | Unsafe accept | Correct accept | Abstain | True source diversity |
|---|---:|---:|---:|---:|
| `fixed_k` | 0.320 | 0.680 | 0.000 | 0.000 |
| `random_k` | 0.093 | 0.500 | 0.407 | 0.700 |
| `provenance/accurate` | 0.000 | 0.347 | 0.653 | 1.000 |
| `provenance/missing_25` | 0.020 | 0.367 | 0.613 | 0.947 |
| `provenance/wrong_25` | 0.027 | 0.387 | 0.587 | 0.880 |
| `provenance/mixed_25_each` | 0.073 | 0.393 | 0.533 | 0.833 |
| `provenance/wrong_50` | 0.087 | 0.440 | 0.473 | 0.753 |

**FACT:** Với accurate metadata, provenance-aware giảm unsafe acceptance so với random-K `-0.093`, paired task-cluster bootstrap 95% CI `[-0.147, -0.047]`.

**FACT:** So với fixed-K, difference là `-0.320`, CI `[-0.387, -0.253]`.

**FACT:** Dưới independent faults, accurate provenance không khác random-K về unsafe acceptance: difference `0.000`, CI `[-0.033, 0.033]`. Kết quả này phù hợp với H1.

## Expected decision loss

Với `L = unsafe_accept + λ × abstain`:

- ở `λ=0.10`, accurate provenance tốt hơn random-K `-0.069`, CI `[-0.118, -0.025]`;
- ở `λ=0.25`, point estimate vẫn tốt hơn `-0.032`, nhưng CI `[-0.078, 0.013]` chạm zero;
- ở `λ=0.50`, không có evidence provenance tốt hơn random-K: difference `+0.030`, CI `[-0.027, 0.083]`;
- so với fixed-K, provenance còn tốt ở `λ=0.25`, nhưng không rõ ở `λ=0.50`.

**INFERENCE:** Câu “unsafe acceptance đắt hơn abstention” còn quá rộng. Evidence hiện chỉ rõ trong vùng bất đối xứng cao, gần `C_abstain/C_wrong = 0.10`; ở `0.25` lợi ích so với random-K chưa chắc chắn.

## Metadata robustness

Khi metadata xấu đi, true-source diversity và safety gain cùng giảm. `missing_25` vẫn giữ diversity `94.7%`; `wrong_50` chỉ còn `75.3%` và unsafe acceptance `8.7%`, gần `random-K` là `9.3%`.

**INFERENCE:** Metadata bị thiếu ít nguy hiểm hơn metadata bị gán sai: missing entry có thể bị bỏ qua, còn wrong entry có thể khiến selector tin nhầm rằng hai tool cùng backend là độc lập.

## Partial local-model gate

Không dùng paid API. `llama.cpp` commit `093a2f86c3e37c54fa3e1f9efb17b304f3433abd` chạy CPU với hai Apache-2.0 GGUF models:

- `Qwen2.5-0.5B-Instruct` Q5_0;
- `Qwen2.5-1.5B-Instruct` Q5_0.

Subset có sáu tasks, hai seeds, ba regimes, hai policies và hai enum orders: `144` records/model. Deterministic selector chọn observations; LLM chỉ quyết định `ACCEPT` hoặc `ABSTAIN`. Vì vậy đây là **partial live-model evidence**, chưa phải full end-to-end live-agent evidence.

### 0.5B

- Parse success `100%`.
- Model trả `ACCEPT` trong toàn bộ 144 records.
- Dưới common-mode provenance observations, unsafe accept `41.7%` và abstain `0%`.

### 1.5B

- Parse success `100%`.
- Dưới common-mode provenance observations, decision adherence `100%`, unsafe accept `0%`, abstain `75%`.
- Clean regime có false abstention `16.7%`, tập trung ở `order_status`; model trộn câu hỏi equality với semantics của refund task.
- Hai enum orders tạo cùng pattern, nên result này không được giải thích chỉ bằng enum ordering.

**INFERENCE:** Không nên giao enforcement cuối cùng cho agent self-assessment. Một deterministic runtime monitor nên cưỡng chế abstention khi observations không đồng thuận; LLM có thể giải thích hoặc xử lý escalation sau đó.

## Threats to validity

- Source topology vẫn synthetic và common-mode effect phần lớn theo construction.
- 30 tasks khác dữ liệu nhưng dùng cùng generator/domain; đây chưa phải external validation.
- Metadata corruption là random label perturbation, chưa phản ánh dependency discovery ngoài production.
- Partial local-model gate không cho LLM tự chọn và gọi tools, không đo final task success.
- Hai models nhỏ thuộc cùng family; chưa có cross-family evidence.
- Cost ratio `λ` chưa có empirical estimate từ một application thật.

## Gate decision

`PASS CHARACTERIZATION; PARTIAL ROBUSTNESS; FAIL FULL LIVE-AGENT VALIDATION.`

- Task-holdout mechanics: `PASS`.
- Accurate provenance vs fixed-K safety: `PASS`.
- Accurate provenance vs random-K: `PASS` cho unsafe acceptance và expected loss ở `λ=0.10`; không pass ở `λ≥0.25`.
- Metadata robustness: `PARTIAL`; moderate missingness chịu được, wrong metadata làm gain biến mất nhanh.
- Full live-agent/external validity: `NOT PASSED`.

## Kết luận

RQ về **trade-off** vẫn sống sót, nhưng broad method claim phải thu hẹp. Evidence hiện hỗ trợ characterization sau:

> Provenance-aware selection có thể giảm unsafe acceptance dưới common-mode faults khi source metadata đủ chính xác, nhưng chỉ giảm expected decision loss so với random diversity khi abstention rẻ hơn wrong acceptance rất nhiều. Lợi ích không xuất hiện dưới independent faults và không nên phụ thuộc vào LLM tự quyết định enforcement.

Gap vẫn `SURVIVES WITH REFINEMENT — PRELIMINARY`; chưa có external validity và chưa confirmed novelty.

## Next action

**Đã thực hiện.** Full live tool-using subset chạy đủ 36 episodes; xem [[journal/2026-09-14-full-live-agent-verification-gate]]. Gate kỹ thuật pass nhưng experimental validity fail vì verification coverage và agent procedure compliance thấp.

Next action mới: đặt verifier bắt buộc tại action boundary trước `issue_refund`, rồi rerun sáu tasks với ít nhất ba seeds.

## Related

- [[synthesis/Candidate RQ - Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Preliminary Gap - Provenance-Aware Verification under Correlated Tool Failures]]
- [[journal/2026-09-13-correlated-tool-verification-pilot]]
- [[journal/2026-09-14-full-live-agent-verification-gate]]
