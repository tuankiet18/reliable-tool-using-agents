---
title: >-
  Retry, Switch, or Abstain? Learning Strategy-Aware Tool-Use Policies via Controlled Error Injection
category: references
tags: [paper, ai-agents, recovery, tool-failure, reinforcement-learning]
sources: [https://arxiv.org/abs/2608.11977, https://arxiv.org/html/2608.11977v1]
source_url: https://arxiv.org/abs/2608.11977
summary: >-
  Prior art trực tiếp: BENCH2ROBUST tạo scenario yêu cầu retry, switch hoặc abstain; BTM và RL tạo hành vi phục hồi theo strategy dưới lỗi tool có kiểm soát.
provenance:
  extracted: 0.92
  inferred: 0.08
  ambiguous: 0.00
base_confidence: 1.00
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# Retry, Switch, or Abstain? Learning Strategy-Aware Tool-Use Policies via Controlled Error Injection

> [!tldr] Đây là counterexample trực tiếp với broad gap: paper tạo scenario mà retry, switch/fallback, hoặc abstain/escalate là phản ứng phù hợp khác nhau và huấn luyện/đánh giá hành vi recovery tương ứng.

## Vấn đề

Tool agent phải phân biệt lúc retry đủ, lúc primary path bị chặn và phải switch sang tool tương đương, và lúc không còn path khả thi thì abstain/escalate. Paper nhấn mạnh retry mù quáng có thể trông tốt chỉ vì stochastic fault tự biến mất.

## Agent setting, failure model và injection

BENCH2ROBUST là lớp chèn lỗi nằm giữa agent và tool execution; tích hợp được benchmark có dạng `tool_call(name, args) → response`. Nó đánh giá `τ²-bench`, Retail-3I/Airline-3I và BFCL multi-turn.

- S1 `retry_works`: original path không bị chặn vĩnh viễn; retry có thể phục hồi.
- S2 `switch_needed`: một tool trong fallback-equivalence class bị chặn cả episode; phải switch.
- S3 `impossible`: mọi viable tool path bị chặn; escalation là hành vi được chỉ định.
- Lỗi tool response gồm timeout, rate limit, server/auth error, malformed response, schema drift, partial data, stale value và factual error.

## Observable signals, policy và action space

**Tín hiệu:** tool/error observation hiện tại; fallback map; verification constraint; thống kê recoverability theo cặp `(tool, error)` và source→target; trajectory/rollout history dùng tạo BTM.

**Action space thật sự được kiểm tra:** `retry`, `switch` sang fallback-equivalent tool, và `abstain/escalate`. Verification là constraint/hành vi hỗ trợ. Paper **không** đánh giá rollback, modified retry riêng biệt, hoặc lựa chọn giữa nhiều loại human escalation.

**Recovery policy:** **✓ Có.** BTM đưa structured runtime recovery context để model chọn boundary; curriculum DAPO RL huấn luyện policy theo S1/S2/S3. Vì vậy đây không chỉ là “phát hiện lỗi rồi retry”. Tuy nhiên posterior calibration không phải nguồn lợi ích chính; fallback map và recovery constraint đóng góp phần lớn.

## Intervention timing, baselines và metric

Intervention diễn ra online sau tool response qua context/policy trong lần chạy. So sánh base, `+BTM`, `+RL`, `+RL+BTM`; báo cáo clean/injected pass rate, S1 retry success, S2 switch success, premature escalation, token và transfer.

Trên 402 Retail task held-out, 4B base đạt 20.1% (inject không alternatives) và 31.9% (có alternatives); `+BTM` đạt 36.9%/43.6%; `+RL+BTM` đạt 40.8%/45.5%, trung bình 5 injection seed. S2 switch success của `RL` là 35.3% so với 16.8% của `Base+BTM`; paper cảnh báo đây là bằng chứng suggestive vì scenario class được gán post-hoc theo trajectory của mỗi policy.

## Hạn chế then chốt

- S3 chỉ dùng trong training: evaluator không thưởng dương cho task bất khả thi, nên paper **không claim fully learned abstention**.
- Tool failure ở response layer; không đo rollback hoặc external irreversible side effect.
- `+BTM` tăng token đáng kể (ví dụ 64K base lên 89K full BTM trong decomposition); cost chỉ được đo bằng token, không có monetary/API cost hay safety cost của side effect.
- Chưa thấy code/repository chính thức được liên kết trên arXiv v1; training RL Qwen3-4B/8B không phù hợp với 12 tuần nếu phải tái tạo.

## Hệ quả cho gap

**FACT:** Broad claim “existing work does not study dynamic selection giữa retry, fallback và escalation dưới tool failure” bị công trình này bác bỏ.

## Liên hệ

- [[synthesis/Prior-Art Threat: Recovery-Action Selection]]
- [[synthesis/Preliminary Gap: Selective Recovery Routing]]
- [[concepts/agent-recovery-policy]]

