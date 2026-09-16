---
title: >-
  2026-09-15 — Action-Boundary Provenance Verification Main Study
category: journal
tags: [research-log, experiment, verification, tool-failure, reproducibility]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_main_study"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tasks_main_30.manifest.json"
  - "https://github.com/mohammadi-hadi/trajectory-judge"
summary: >-
  Main deterministic study chạy 1.350 episodes và pass preregistered gate; provenance giảm targeted common-mode unsafe refunds nhưng effect phụ thuộc trực tiếp vào synthetic known topology.
provenance:
  extracted: 0.91
  inferred: 0.08
  ambiguous: 0.01
base_confidence: 0.93
lifecycle: draft
lifecycle_changed: 2026-09-15
tier: core
created: 2026-09-15T00:23:25+07:00
updated: 2026-09-15T00:23:25+07:00
---

# Action-boundary main deterministic study

## Mục tiêu

Thực hiện confirmatory gate tại [[synthesis/Protocol: Action-Boundary Provenance Verification Main Study]] trên frozen split [[journal/2026-09-15-main-study-manifest]]. So sánh chính là `provenance_k` với `random_k`, cùng primary source và matched `K=2` tại mọi refund attempt.

## Thiết kế đã chạy

- 30 tasks: `INS-00060`–`INS-00089`.
- Seeds: `101`, `211`, `307`, `401`, `503`.
- Regimes: `clean`, `independent`, `targeted_common_mode`.
- Policies: `single_source`, `random_k`, `provenance_k`.
- Tổng: `1,350` deterministic episodes; không dùng LLM/API/GPU.
- Inference: paired task-cluster bootstrap, `10,000` resamples.

## Validation

**FACT:** `29/29` tests và `ruff` pass. Tất cả invariants pass: 30 fresh tasks, action-boundary coverage `1.000`, matched `K=2`, independent-domain selection `1.000`, clean observations không bị corrupt.

**FACT:** Reproducibility rerun tạo cùng raw SHA-256 `a51aebcb207f996e7a4d065b2e424fe794346d685d5f37a615d0de6bcb872234`.

## Kết quả

| Regime | Policy | Success | Unsafe refund | False block | Conflict |
|---|---|---:|---:|---:|---:|
| `clean` | `random_k` | 1.000 | 0.000 | 0.000 | 0.000 |
| `clean` | `provenance_k` | 1.000 | 0.000 | 0.000 | 0.000 |
| `independent` | `random_k` | 0.807 | 0.040 | 0.153 | 0.193 |
| `independent` | `provenance_k` | 0.793 | 0.047 | 0.160 | 0.193 |
| `targeted_common_mode` | `random_k` | 0.467 | 0.200 | 0.333 | 0.467 |
| `targeted_common_mode` | `provenance_k` | 0.667 | 0.000 | 0.333 | 0.667 |

Primary targeted-common-mode unsafe-refund difference `provenance_k − random_k = -0.200`, 95% CI `[-0.273, -0.127]`. Clean success difference `0.000`, CI `[0.000, 0.000]`. Safety benefit xuất hiện ở `4/6` strata: `already_refunded`, `expired`, `non_refundable`, `wrong_customer`.

Independent negative control phù hợp prediction: unsafe-refund difference `+0.0067`, CI `[-0.020, 0.033]`; không có evidence về advantage.

## Decision theo protocol

`PASS MAIN DETERMINISTIC GATE` — toàn bộ năm confirmatory conditions đều pass.

## Adversarial interpretation

**FACT:** Trong 100 targeted-common-mode refund attempts của random-K, 30 lần chọn corroborator cùng `operational_db`; cả `30/30` dẫn tới unsafe refund. Trong 100 provenance attempts, corroborator độc lập `100/100` và conflict được phát hiện `100/100`.

**INFERENCE:** Kết quả cho thấy đúng causal mechanism dự kiến, nhưng cũng gần như được quyết định bởi fault topology đã dựng. Task content không tạo ra nhiều heterogeneity cho verifier: khác biệt chủ yếu là random selector có chọn nhầm same-domain source hay không.

**Không được kết luận:** provenance-aware verification đã được xác nhận novel, hoạt động với metadata sai, hoặc generalize sang production tools.

## Trạng thái RQ

`SUPPORTED IN CONTROLLED MAIN STUDY; GAP REMAINS PRELIMINARY`.

## Evidence còn thiếu

- Correlated faults không hoàn toàn trùng nhau hoặc thay đổi theo thời gian.
- Provenance metadata phải được suy ra/ước lượng thay vì được benchmark cung cấp chính xác.
- Một second environment hoặc live-agent subset đủ ổn định.
- Adversarial novelty check cụ thể cho action-boundary, failure-domain-aware verification.

## Bước tiếp theo duy nhất

Thiết kế một external-validity mini-gate với imperfect provenance và ít nhất một fault topology không tạo conflict hoàn hảo; đóng băng protocol amendment trước khi chạy. Không mở rộng main claim cho tới khi gate này có result.

## Related

- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Protocol: Action-Boundary Provenance Verification Main Study]]
