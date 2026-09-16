---
title: "2026-09-13 — Correlated Tool Verification Pilot"
category: journal
tags: [research-log, experiment, verification, tool-failure, reproducibility]
sources:
  - "https://github.com/mohammadi-hadi/trajectory-judge"
  - "https://arxiv.org/abs/2603.02345"
summary: >-
  Exploratory pilot 600 paired episodes xác nhận common-mode mechanics và phát hiện safety–abstention trade-off; provenance-aware hơn fixed-K về unsafe acceptance nhưng chưa rõ hơn random-K.
provenance:
  extracted: 0.20
  inferred: 0.77
  ambiguous: 0.03
base_confidence: 0.90
lifecycle: draft
lifecycle_changed: 2026-09-13
tier: core
created: 2026-09-13T00:00:00Z
updated: 2026-09-14T00:00:00+07:00
---

# Pilot: provenance-aware verification dưới correlated tool failures

## Mục tiêu

Kiểm tra fault-model mechanics trước khi dùng live LLM hoặc mở rộng benchmark. Pilot không nhằm xác nhận novelty hay end-to-end agent benefit.

## Thiết kế

- 10 task fixtures sinh từ `trajectory-judge` commit `d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5`, seed `7`.
- 5 tool interfaces thuộc 3 failure domains.
- Regimes: `clean`, `independent`, `common_mode`.
- Policies: `single`, `fixed_k`, `random_k`, `provenance_aware`.
- Seeds: `11, 23, 37, 51, 79`.
- Tổng: `10 × 3 × 5 × 4 = 600` paired episodes.
- `K=2` policies dùng cùng một extra tool call.
- Fault map được tạo một lần cho từng task/regime/seed rồi dùng lại cho mọi policy.

## Validation

- 7/7 implementation tests pass.
- Clean false alarms: `0` cho mọi policy.
- Common-mode corruptions luôn dùng cùng wrong value trong đúng một failure domain.
- Fixed-K chọn hai tool khác tên nhưng cùng domain; provenance-aware chọn hai domain khác nhau.
- Paired cluster bootstrap resample theo task (`n=10`), giữ cả năm seeds; 10,000 resamples.

## Main results

| Regime | Policy | Detection recall | Unsafe accept | Correct accept | Abstain |
|---|---:|---:|---:|---:|---:|
| common-mode | fixed-K | 0.000 | 0.340 | 0.660 | 0.000 |
| common-mode | random-K | 0.889 | 0.060 | 0.460 | 0.480 |
| common-mode | provenance-aware | 1.000 | 0.000 | 0.360 | 0.640 |
| independent | fixed-K | 0.955 | 0.020 | 0.560 | 0.420 |
| independent | random-K | 0.882 | 0.040 | 0.660 | 0.300 |
| independent | provenance-aware | 0.947 | 0.020 | 0.620 | 0.360 |

Provenance-aware so với fixed-K dưới common-mode:

- unsafe acceptance difference `-0.34`, cluster-bootstrap 95% CI `[-0.42, -0.26]`;
- abstention difference `+0.64`, CI `[0.52, 0.78]`;
- correct-accept difference `-0.30`, CI `[-0.42, -0.18]`.

So với random-K, unsafe difference chỉ `-0.06`, CI `[-0.12, 0.00]`; chưa đủ mạnh để nói provenance metadata tạo gain ngoài diversity ngẫu nhiên.

## Expected-loss analysis

Chuẩn hóa wrong accept cost bằng `1` và đặt abstention cost là `λ`:

`L = P(unsafe accept) + λ·P(abstain)`.

- `λ = 0–0.25`: provenance-aware có loss thấp nhất.
- `λ = 0.5`: random-K thấp nhất trong sample.
- `λ = 0.75–1.0`: fixed-K thấp nhất vì không abstain.

**INFERENCE:** method phù hợp hơn cho domain nơi wrong action đắt hơn human escalation; không thể tuyên bố universally better.

## Gate decision

`PASS MECHANICS, NOT CLAIM.`

- Pass: effect >10 percentage points so với fixed-K, zero clean false alarms và xuất hiện trên cả sáu difficulty strata.
- Chưa pass external validity: synthetic source topology và scripted verification.
- Chưa pass strong-baseline gate: provenance-vs-random uncertainty còn chạm zero.

## RQ refinement

RQ được đổi từ “improve detection per tool call” sang “reduce expected decision loss across unsafe-acceptance/abstention cost ratios”. Main study phải preregister trên disjoint tasks/seeds.

## Artifacts

- `projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/README.md`
- `projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results/summary.md`
- `projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results/inference.md`

## Next gate

Trước full experiment, mở rộng pilot sang disjoint 30 tasks với noisy/incomplete dependency metadata và ít nhất một live-agent subset. Nếu provenance-aware không vượt random-K ở bất kỳ plausible low-abstention-cost region nào, bỏ method claim và chỉ giữ RQ characterization về common-mode vulnerability.

**Update 2026-09-14:** Gate deterministic 30 task và partial local-model subset đã hoàn tất tại [[journal/2026-09-14-correlated-tool-verification-next-gate]]. Characterization sống sót ở low-abstention-cost region; full live-agent validation vẫn chưa pass.

## Related

- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]]
