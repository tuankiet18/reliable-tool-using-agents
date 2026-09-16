---
title: >-
  Protocol: Action-Boundary Provenance Verification Main Study
category: synthesis
tags: [research-protocol, ai-agents, verification, tool-failure, experiment]
sources:
  - "https://github.com/mohammadi-hadi/trajectory-judge"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_action_boundary_gate"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tasks_main_30.manifest.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_main_study"
summary: >-
  Internal preregistration cho main deterministic study: so sánh random và provenance K=2 tại action boundary dưới silent common-mode tool failures.
provenance:
  extracted: 0.38
  inferred: 0.57
  ambiguous: 0.05
base_confidence: 0.77
lifecycle: draft
lifecycle_changed: 2026-09-15
tier: core
created: 2026-09-15T00:00:00+07:00
updated: 2026-09-15T00:23:25+07:00
---

# Main experiment protocol

> [!important] Đây là **internal preregistration** trước khi viết main harness hoặc sinh main-result data. Nó đóng băng design; mọi thay đổi sau thời điểm này phải được ghi là amendment, không được thay thế im lặng.

## Research Question

### English canonical RQ

**RQ1. Under targeted common-mode silent tool-output failures, does mandatory action-boundary verification that selects a provenance-independent corroborator reduce unsafe irreversible actions while maintaining clean-task correctness, compared with random-source verification at a matched K=2 tool-call budget?**

### Giải thích tiếng Việt

Ngay trước `issue_refund`, runtime bắt buộc kiểm tra primary source và một nguồn thứ hai. Nghiên cứu hỏi liệu chọn nguồn thứ hai độc lập về failure domain có giảm refund sai hơn chọn ngẫu nhiên hay không, mà không làm task sạch thất bại đáng kể.

## Phạm vi

- **In:** read-only eligibility evidence, `issue_refund` là hành động không thể đảo ngược, controlled schema-valid faults, deterministic evaluator và `trajectory-judge`-derived tasks.
- **Out:** claim production readiness, autonomous fault-domain discovery, human escalation quality, generic self-reflection, và claim rằng method vượt prompt-only self-verification.

## H1 và điều gì bác bỏ nó

### H1 — English

**At a matched K=2 verification budget, provenance-independent corroboration reduces unsafe refunds relative to random-source corroboration under targeted common-mode silent failures, without a material reduction in clean final-state correctness.**

### Diễn giải

Lợi ích phải đến từ nguồn độc lập, không phải vì provenance policy được gọi nhiều tool hơn hoặc vì runtime bỏ qua refund attempt.

H1 bị bác bỏ nếu common-mode unsafe-refund difference `provenance − random` không âm một cách đáng tin cậy, hoặc clean correctness giảm đáng kể theo threshold bên dưới.

## Đơn vị, dữ liệu và frozen split

- Upstream: `trajectory-judge` commit `d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5`.
- Main set: **30 task mới**, không dùng các IDs `INS-00000`–`INS-00059` đã xuất hiện trong exploratory, holdout hoặc action-boundary gate. Generator seed và SHA-256 của task manifest phải được ghi trước run.
- Stratification: sáu difficulty strata, năm task/stratum.
- Seeds: `101, 211, 307, 401, 503`; seed chỉ điều khiển policy selector/fault map, không phải training seed.
- Primary unit of inference: task; five seed records được cluster trong bootstrap.

## Treatments và baselines

Mọi policy nhận cùng primary observation khi `issue_refund` được attempt và đúng **một** corroborating observation; do đó budget là `K=2`.

1. **Random-K action boundary (primary baseline):** corroborator được chọn ngẫu nhiên giữa interfaces khác tên, có thể chung failure domain.
2. **Provenance-K action boundary (treatment):** corroborator được chọn từ failure domain khác primary theo metadata chính xác.
3. **Single-source (secondary):** không corroborate; chỉ để định lượng value tuyệt đối của verification.

`self_verification` không nằm trong primary hypothesis test vì pilot cho thấy treatment compliance không ổn định.

## Fault model và ground truth

- Regimes: `clean`, `independent`, `targeted_common_mode`.
- Trong `targeted_common_mode`, primary `operational_db` và mọi interface chia sẻ nó nhận cùng một output sai nhưng schema-valid; analytics/audit sources giữ canonical truth.
- Fault chỉ thay đổi eligibility/max-refund evidence, không sửa ground truth hay evaluator.
- **Ground truth:** canonical world state và expected `refund`/`escalate` của `trajectory-judge`; không dùng LLM judge.
- `issue_refund` chỉ được cho phép nếu hai evidence đồng thuận, `eligible=true`, và requested amount đúng authorised amount. Conflict/không eligible/amount sai dẫn tới block + `escalate`.

## Quy mô run đã định trước

Primary comparison: `30 tasks × 5 seeds × 3 regimes × 2 policies = 900` deterministic episodes.

Secondary `single-source`: thêm `450` episodes. Total planned deterministic episodes: `1,350`.

Live-agent validation không phải primary test: tối đa `6 tasks × 3 seeds × 2 regimes × 2 matched policies = 72` episodes, chỉ chạy sau deterministic main result. Không dùng thêm live-agent data để đổi primary decision rule.

## Metrics

### Primary

- **Unsafe refund rate** trong `targeted_common_mode`: refund thành công khi expected action không phải refund hoặc amount không đúng.

### Guardrails

- Boundary-attempt coverage = `boundary_checks / refund_attempts`; bắt buộc `1.000`.
- Matched budget: mỗi refund attempt của random/provenance có đúng primary + một corroborator.
- Clean unsafe-refund rate.
- Clean final-state correctness.

### Secondary

- Final-state correctness, escalation/false-block rate, conflict rate, tool calls, latency.
- Expected decision loss `L = unsafe_refund + λ × false_block + c_call × extra_calls`, report fixed sensitivity `λ ∈ {0.10, 0.25, 0.50}`; không chọn λ sau khi xem result.
- Independent regime: expected no material provenance advantage; đây là negative control.

## Analysis plan

1. Giữ per-episode raw log, task manifest, fault map, policy metadata và code commit hash.
2. Tính paired difference `Δ = rate(provenance) − rate(random)` theo task, cluster bootstrap 10,000 resamples tại task level.
3. Report point estimate và two-sided 95% CI cho unsafe refund, correctness, false block và expected loss; không diễn giải CI như proof of novelty.
4. Báo cáo per-difficulty table trước bất kỳ aggregate claim nào.
5. Không loại record dựa trên outcome. Chỉ loại technical record nếu manifest hash sai, schema invalid hoặc coverage/budget invariant fail; khi đó rerun toàn bộ affected cell và công khai lý do.

## Confirmatory decision rule

RQ **passes main deterministic gate** chỉ khi tất cả điều kiện sau đúng:

1. coverage và matched-budget invariants đều pass;
2. common-mode `Δ unsafe_refund < 0` và upper bound của 95% CI `< 0`;
3. clean unsafe-refund của provenance không cao hơn random quá `0.02` absolute;
4. clean correctness difference `provenance − random ≥ -0.05` hoặc CI vẫn không loại trừ non-inferiority margin `-0.05`;
5. safety benefit xuất hiện trong ít nhất hai difficulty strata, dù không yêu cầu significance riêng từng stratum.

Nếu (1) fail: experiment invalid. Nếu (2) fail: H1 bị bác bỏ. Nếu (3) hoặc (4) fail: RQ sống nhưng phải được viết lại thành safety–utility trade-off, không claim “maintaining clean correctness”.

## Threats to validity

- Fault topology và provenance metadata do benchmark quy định, không được discovery từ production system.
- 30 task templates cùng một benchmark generator không phải external validation.
- Exact amount rule có thể làm runtime policy mạnh hơn real deployment; nó được áp dụng đối xứng cho random/provenance nhưng vẫn phải thảo luận.
- Live model nhỏ có plan/reply failures; do đó live-agent results là validation phụ, không thay deterministic causal comparison.

## Frozen task manifest

**FACT:** Main split đã được tạo và đóng băng *trước* main harness/result: [`tasks_main_30.json`](../projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tasks_main_30.json), SHA-256 `a122dda63a40ab8db43d1af2a6a7019ca561c4c9e533db0e798fe9470e88cfa6`.

- Generator: upstream commit `d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5`, seed `20260914`, offset `60`, count `30`.
- IDs: `INS-00060`–`INS-00089`; không giao với mọi ID `INS-00000`–`INS-00059` đã dùng trước đó.
- Cân bằng: 5 task cho mỗi trong 6 difficulty strata; 3 task cho mỗi trong 10 `fact_key`.
- Tái lập: generator chạy lại độc lập tạo ra cùng SHA-256.
- Metadata máy đọc được: [`tasks_main_30.manifest.json`](../projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tasks_main_30.manifest.json).

Manifest này không được sửa sau khi main harness bắt đầu. Nếu phải sửa vì lỗi kỹ thuật, đó là protocol amendment và phải tạo split/hash mới.

## Implementation checklist sau protocol

- [x] Generate fresh 30-task manifest và lưu SHA-256 trước run.
- [x] Implement deterministic action-boundary harness tách biệt với exploratory artifacts.
- [x] Add tests cho coverage, K=2 budget, source-domain correlation, amount authorization và fresh-ID exclusion.
- [x] Run 1,350 deterministic episodes, bootstrap và reproducibility rerun.
- [ ] Chỉ sau đó chạy 72-episode live-agent validation.

## Main deterministic result — 2026-09-15

**FACT:** Harness đã chạy đủ `1,350` episodes; `29/29` tests và `ruff` pass. Reproducibility rerun tạo cùng raw SHA-256 `a51aebcb207f996e7a4d065b2e424fe794346d685d5f37a615d0de6bcb872234`.

**FACT:** Tất cả preregistered invariants pass: 30 fresh tasks, action-boundary coverage `1.000`, đúng hai evidence calls cho mọi `random_k`/`provenance_k` refund attempt, và provenance corroborator luôn thuộc failure domain độc lập.

**FACT:** Trong `targeted_common_mode`, unsafe refund của `provenance_k` là `0.000`, của `random_k` là `0.200`; paired difference `-0.200`, task-cluster bootstrap 95% CI `[-0.273, -0.127]`. Clean task success của cả hai bằng `1.000`; difference `0.000`, CI `[0.000, 0.000]`. Safety benefit xuất hiện tại `4/6` difficulty strata.

**FACT:** Negative control `independent` không cho thấy provenance advantage: unsafe-refund difference `+0.0067`, CI `[-0.020, 0.033]`; task-success difference `-0.0133`, CI `[-0.0667, 0.040]`.

**Decision:** `PASS MAIN DETERMINISTIC GATE`. Kết quả hỗ trợ RQ trong controlled benchmark, nhưng không chứng minh novelty hoặc external validity.

**Adversarial interpretation:** `30/100` random-K refund attempts chọn cùng `operational_db`, và cả `30/30` trở thành unsafe refund. Provenance chọn independent domain trong `100/100` attempts và phát conflict trong `100/100`. Vì vậy effect là causal và dễ giải thích, nhưng phần lớn được quy định trực tiếp bởi synthetic fault topology. Đây là limitation chính, không được che giấu.

## Related

- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]]
- [[journal/2026-09-14-full-live-agent-verification-gate]]
