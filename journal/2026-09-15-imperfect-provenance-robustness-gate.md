---
title: >-
  2026-09-15 — Imperfect Provenance Robustness Gate
category: journal
tags: [research-log, experiment, verification, tool-failure, robustness]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_robustness_gate"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tasks_robustness_30.manifest.json"
  - "synthesis/Protocol Amendment - Imperfect Provenance and Partial Correlation.md"
summary: >-
  Robustness gate 3.750 episodes fail vì 25% wrong provenance labels làm CI chạm zero; RQ phải giới hạn ở accurate failure-domain metadata.
provenance:
  extracted: 0.91
  inferred: 0.08
  ambiguous: 0.01
base_confidence: 0.91
lifecycle: draft
lifecycle_changed: 2026-09-15
tier: core
created: 2026-09-15T11:13:14+07:00
updated: 2026-09-15T11:18:28+07:00
---

# Imperfect provenance và partial-correlation robustness gate

## Mục tiêu

Cố bác bỏ việc mở rộng RQ sau main study bằng hai stressors: failure-domain metadata bị thiếu/sai và schema-valid wrong output lan sang cross-domain source với xác suất `0–0.50`.

## Thiết kế

- Frozen tasks: `INS-00090`–`INS-00119`, không trùng mọi task trước.
- Five seeds; `random_k` baseline và bốn provenance metadata conditions.
- `3,750` deterministic episodes; paired fault maps; matched `K=2`.
- Task-cluster bootstrap `10,000` resamples.
- Không dùng LLM, API hoặc GPU.

## Validation

**FACT:** `37/37` tests và `ruff` pass. Tất cả count, pairing, clean-data, boundary-coverage, K=2 và accurate-provenance invariants pass.

**FACT:** Reproducibility rerun tạo cùng raw SHA-256 `f22e7f29c97a89eda20bdb57f9e59fa43581adb3d3b6475ee40e926492ab1982`.

## Kết quả predeclared

| Condition | Provenance unsafe | Random unsafe | Δ | 95% CI | Rule |
|---|---:|---:|---:|---:|---|
| accurate, leakage `.25` | .193 | .327 | -.133 | [-.220, -.053] | PASS |
| missing `.25`, leakage `.10` | .100 | .253 | -.153 | [-.227, -.087] | PASS |
| wrong `.25`, leakage `.10` | .187 | .253 | -.067 | [-.133, .000] | **FAIL** |

Clean guardrail pass: `750/750` clean records correct, zero unsafe refund.

## Decision

`FAIL ROBUSTNESS`. Ba required fault conditions phải cùng pass; wrong-label condition không đạt strict upper-CI-below-zero rule.

## Điều học được

**FACT:** Trong các refund attempts, `missing_25` có fallback rate `.290`; ở leakage `.10`, true-domain diversity vẫn `.930`. Metadata được dùng có accuracy `1.000` vì condition này chỉ xóa label, không tạo label sai.

**FACT:** `wrong_25` có average metadata accuracy `.767`; tại leakage `.10`, true-domain diversity giảm xuống `.790`. Unsafe refund vẫn thấp hơn point estimate của random nhưng uncertainty chưa loại trừ zero advantage.

**INFERENCE:** Missing metadata là uncertainty nhìn thấy được nên có thể fallback; wrong metadata tạo false confidence và chọn same-domain source. Đây là lý do plausible khiến wrong labels phá evidence mạnh hơn missing labels.

**CAVEAT:** Fault draws giữa leakage levels không nested, nên point estimates không bắt buộc giảm/tăng đều. Không dùng sự không monotonic làm substantive claim.

## Implementation audit

`impl-validator` phát hiện bản chạy đầu đã chọn corroborator ngay cả khi primary observation không dẫn đến refund attempt. Việc này không thay đổi action hoặc unsafe-refund metric, nhưng làm fallback-rate denominator lệch khỏi action-boundary semantics. Implementation được sửa để chỉ chọn corroborator tại refund attempt, thêm regression test, rồi rerun toàn bộ `3,750` episodes. Decision và primary estimates không đổi; hash cũ bị thay thế bởi final hash đã ghi ở trên.

## Tác động lên RQ

RQ rộng về imperfect provenance bị bác bỏ. RQ hẹp với **accurate failure-domain metadata** vẫn được controlled main study hỗ trợ. Gap tiếp tục `PRELIMINARY`, vì chưa có second environment và chưa biết cách bảo đảm metadata đúng trong thực tế.

## Bước tiếp theo duy nhất

Thực hiện adversarial prior-art search riêng cho provenance/dependency metadata validation và uncertainty-aware source selection. Không implement một “metadata verifier” trước khi biết literature đã giải quyết đến đâu.

## Related

- [[synthesis/Protocol Amendment - Imperfect Provenance and Partial Correlation]]
- [[synthesis/Candidate RQ - Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Preliminary Gap - Provenance-Aware Verification under Correlated Tool Failures]]
- [[journal/2026-09-15-action-boundary-main-study]]
