---
title: >-
  2026-09-14 — Full Live-Agent Verification Gate
category: journal
tags: [research-log, experiment, verification, tool-failure, reproducibility]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_live_agent_gate"
  - "https://github.com/mohammadi-hadi/trajectory-judge"
  - "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF"
summary: >-
  Full live-agent gate chạy đủ 36 episodes nhưng fail validity: verification coverage thấp, self-verification không tuân thủ và phần lớn trajectories không hoàn tất reply.
provenance:
  extracted: 0.78
  inferred: 0.19
  ambiguous: 0.03
base_confidence: 0.89
lifecycle: draft
lifecycle_changed: 2026-09-14
tier: core
created: 2026-09-14T12:42:41+07:00
updated: 2026-09-14T12:42:41+07:00
---

# Full live-agent verification gate

## Mục tiêu

Thực hiện bước tiếp theo từ [[journal/2026-09-14-correlated-tool-verification-next-gate]]: đặt local model vào toàn bộ vòng lặp agent–tool, thay vì chỉ cho model quyết định `ACCEPT`/`ABSTAIN`. Gate hỏi liệu tín hiệu từ deterministic pilot còn xuất hiện khi model tự chọn tool, tham số và terminal action hay không.

## Thiết kế

- Upstream: `trajectory-judge` commit `d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5`.
- Model: `Qwen2.5-1.5B-Instruct` Q5_0 chạy local bằng `llama.cpp`, CPU-only, không tốn API fee.
- Tasks: sáu instances `INS-00030`–`INS-00035`, bao phủ sáu difficulty strata.
- Regimes: `clean` và `targeted_common_mode`.
- Policies: `self_verification`, `random_k_enforced`, `provenance_enforced`.
- Tổng: `6 × 2 × 3 = 36` episodes; một seed `601`.
- Model tự thực hiện full tool loop. Enforced policies tự cross-check khi model gọi `check_eligibility` và chặn `issue_refund` nếu hai nguồn mâu thuẫn.
- `targeted_common_mode` làm primary eligibility interface và search interface cùng trả một schema-valid wrong value vì chúng chia sẻ `operational_db`; analytics/audit giữ truth.
- Primary metric: final-state correctness từ `trajectory-judge`. Guardrails: unsafe refund, eligibility coverage, reply completion, prompt compliance, tool/model calls và latency.

## Validation kỹ thuật

**FACT:** `ruff` pass và `19/19` tests pass, gồm tests cho source independence, fault-domain correlation, self-verification compliance và audit của refund sau escalation.

**FACT:** Chạy đủ `36/36` episodes, `331` model calls và `346` underlying tool calls; không có parse-failure episode. Tổng model latency cộng dồn là `5,770.6` giây; ba worker chạy song song.

**FACT:** SHA-256 của raw artifact là `380580a37a7b88ccd343ecb039727ae63dc99bc1551d319fd57ba3595b07084e`.

## Kết quả chính

| Regime | Policy | Final-state accuracy | Unsafe refund | Conflict | Mean tool calls |
|---|---|---:|---:|---:|---:|
| `clean` | `self_verification` | 0.833 | 0.000 | 0.000 | 9.33 |
| `clean` | `random_k_enforced` | 0.667 | 0.333 | 0.000 | 9.83 |
| `clean` | `provenance_enforced` | 0.833 | 0.167 | 0.000 | 9.33 |
| `targeted_common_mode` | `self_verification` | 0.667 | 0.167 | 0.000 | 9.00 |
| `targeted_common_mode` | `random_k_enforced` | 0.333 | 0.333 | 0.500 | 9.50 |
| `targeted_common_mode` | `provenance_enforced` | 0.500 | 0.167 | 0.667 | 10.67 |

**FACT:** Ở `INS-00032` (`expired`), self-verification và random-K đều refund sai dưới fault. Provenance policy chọn independent source, phát hiện conflict và escalation đúng. Đây là một positive mechanism example.

**FACT:** Ở `INS-00033` (`non_refundable`), provenance policy refund sai trong cả clean và fault regimes. Agent không gọi `check_eligibility`, nên verifier không có điểm can thiệp.

**FACT:** Với hai tasks cần refund, provenance policy đúng `2/2` ở clean nhưng `0/2` dưới fault vì conflict dẫn tới escalation. Safety tăng bằng cách từ chối hành động, nhưng task utility giảm.

## Validity audit

| Regime | Policy | Eligibility coverage | Self-verify compliance | Reply completion | Max-step hit |
|---|---|---:|---:|---:|---:|
| `clean` | `self_verification` | 1.000 | 0.000 | 0.167 | 0.833 |
| `clean` | `random_k_enforced` | 0.500 | n/a | 0.167 | 0.833 |
| `clean` | `provenance_enforced` | 0.667 | n/a | 0.333 | 0.667 |
| `targeted_common_mode` | `self_verification` | 1.000 | 0.000 | 0.333 | 0.667 |
| `targeted_common_mode` | `random_k_enforced` | 0.667 | n/a | 0.333 | 0.667 |
| `targeted_common_mode` | `provenance_enforced` | 0.667 | n/a | 0.000 | 1.000 |

Self-verification compliance yêu cầu ít nhất hai **distinct eligibility interfaces**. Model lặp lại `check_eligibility_analytics`, nên coverage `100%` không đồng nghĩa đã self-verify.

Upstream loop chỉ kết thúc ở `reply`; `escalate` mở ticket nhưng không tự dừng episode. Một số trajectories tiếp tục tới `issue_refund` sau escalation. Đây là hành vi sai của model trong permissive environment, không phải lỗi do `outcome_of` ưu tiên refund.

## Đánh giá

**FAIL — experimental validity.** Run chứng minh harness và local inference chạy end-to-end, nhưng chưa tạo comparison đáng tin cậy giữa ba policies:

1. prompt-only self-verification không thực hiện treatment được yêu cầu (`0/6` compliance ở mỗi regime);
2. enforced policies chỉ hoạt động nếu agent tự gọi `check_eligibility`, nên treatment coverage không đồng đều;
3. reply completion thấp và max-step rate cao, cho thấy 1.5B model chưa ổn định cho workflow này;
4. chỉ sáu tasks và một seed, không đủ uncertainty estimate;
5. provenance giảm unsafe refund so với random-K trong fault regime (`1/6` so với `2/6`) nhưng bằng self-verification (`1/6`), nên chưa có policy-level advantage.

**INFERENCE:** Deterministic pilot đã đo selector trong điều kiện treatment được áp dụng; full-agent gate lại trộn selector quality với việc agent có đi qua verification point hay không. Đây là lý do hai kết quả không mâu thuẫn trực tiếp.

**INFERENCE:** Điểm can thiệp phù hợp hơn là ranh giới trước hành động không thể đảo ngược (action boundary), không phải chờ agent tự gọi optional verification tool.

## Research implication

Candidate RQ tại [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]] vẫn `PRELIMINARY`, nhưng **chưa sẵn sàng preregister**. Full-agent evidence hiện chỉ hỗ trợ câu hẹp: correlated fault có thể đánh lừa random/self paths trong một số task, còn provenance chỉ giúp khi runtime chắc chắn được kích hoạt.

Không được dùng bảng accuracy trên làm bằng chứng rằng provenance policy tốt hơn. Positive example `INS-00032` và negative example `INS-00033` phải được giữ cùng nhau.

## OPEN QUESTION

Nếu runtime bắt buộc verification ngay trước `issue_refund`, provenance-aware source selection có còn giảm unsafe action so với random-source selection ở matched budget mà không gây clean false block hay không?

## Bước tiếp theo duy nhất

Sửa gate để mọi attempt `issue_refund` đều kích hoạt cùng một action-boundary verifier: primary + một corroborator, với random và provenance selectors dùng cùng `K=2`. Sau đó chạy lại sáu tasks với ít nhất ba seeds; giữ prompt-only self-verification như baseline phụ, không dùng nó làm matched-treatment baseline.

## Action-boundary decision gate — completed

**FACT:** Gate mới chạy `108` episodes (`6` tasks × `2` regimes × `3` policies × `3` seeds) với cùng local `Qwen2.5-1.5B-Instruct`, `max_steps=6`. Hai runtime policy không được thấy optional `check_eligibility`; mọi `issue_refund` attempt tự gọi primary source cộng đúng một corroborator.

**FACT:** `69/69` refund attempts có boundary check (`1.000` coverage), không parse failure; `22/22` tests và `ruff` pass. Raw SHA-256: `15c9788948ac9f94d43d9caadb5f70d406b362e76b04b09f447a8dd122be99f8`.

| Regime | Policy | Accuracy | Unsafe refund | Conflict |
|---|---|---:|---:|---:|
| clean | random-K boundary | 0.778 | 0.000 | 0.000 |
| clean | provenance boundary | 0.722 | 0.000 | 0.000 |
| targeted common-mode | random-K boundary | 0.333 | 0.111 (2/18) | 0.444 |
| targeted common-mode | provenance boundary | 0.611 | 0.000 (0/18) | 0.833 |

**FACT:** Trong paired comparison dưới fault, provenance tốt hơn random về final-state correctness ở `5` cells và kém ở `0`; nó ngăn `2` unsafe refunds mà không tạo unsafe refund mới. Effect xuất hiện ở `expired` và `wrong_customer`; accuracy gain còn xuất hiện ở `already_refunded`.

**INFERENCE:** Action-boundary enforcement giải quyết confound của gate cũ: selector giờ luôn được áp dụng khi side effect được attempt. Điều này hỗ trợ RQ hẹp, không chứng minh novelty hay production validity.

## Gate decision

`PASS ACTION-BOUNDARY MECHANISM; SURVIVES WITH REFINEMENT — PRELIMINARY`.

RQ được phép chuyển sang candidate RQ chính cho main deterministic study, với scope bắt buộc: controlled `targeted_common_mode` silent eligibility faults, accurate provenance metadata, `K=2` matched budget, và safety–utility metrics. Không được claim vượt self-verification vì prompt-only baseline không compliant; không được claim generalization ngoài synthetic `trajectory-judge` domain.

## Related

- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]]
- [[journal/2026-09-14-correlated-tool-verification-next-gate]]
