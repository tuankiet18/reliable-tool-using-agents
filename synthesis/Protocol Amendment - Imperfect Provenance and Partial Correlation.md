---
title: >-
  Protocol Amendment: Imperfect Provenance and Partial Correlation
category: synthesis
tags: [research-protocol, ai-agents, verification, tool-failure, experiment]
sources:
  - "synthesis/Protocol - Action-Boundary Provenance Verification Main Study.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tasks_robustness_30.manifest.json"
  - "https://github.com/mohammadi-hadi/trajectory-judge"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_robustness_gate"
summary: >-
  Post-main robustness protocol cố bác bỏ RQ bằng imperfect provenance và partial cross-domain fault leakage trên 30 task mới.
provenance:
  extracted: 0.25
  inferred: 0.72
  ambiguous: 0.03
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: 2026-09-15
tier: core
created: 2026-09-15T11:08:03+07:00
updated: 2026-09-15T11:18:28+07:00
---

# Robustness amendment: imperfect provenance và partial correlation

> [!important] Protocol amendment này được đóng băng sau main deterministic result nhưng trước khi viết robustness harness hoặc xem robustness outcome. Nó là stress test hậu kiểm (post-main robustness test), không được nhập ngược vào confirmatory main claim.

## Câu hỏi robustness

### English

**Across imperfect failure-domain metadata and partial cross-domain fault leakage, when does provenance-aware K=2 action-boundary verification retain or lose its safety advantage over random-K verification?**

### Giải thích tiếng Việt

Main study cho provenance metadata hoàn toàn đúng và nguồn độc lập luôn trả truth. Gate này cố phá giả định đó: metadata có thể thiếu/sai, và cùng một lỗi đôi khi lan sang cả nguồn được xem là độc lập. Ta đo điểm mà lợi thế của provenance suy giảm hoặc biến mất.

## Frozen task split

- Tasks: `INS-00090`–`INS-00119`, không trùng `INS-00000`–`INS-00089`.
- Generator: seed `20260914`, offset `90`, count `30`.
- Task SHA-256: `9215aa09a4a28f7853f3dbd209c6ee66dcee30216b9b7b556ad380ee39e6a05c`.
- Sáu difficulty strata × năm tasks; mười `fact_key` × ba tasks.

## Treatments và baseline

- Baseline: `random_k`, luôn dùng primary `operational_db` và một random corroborator.
- Treatment: `provenance_k`, chọn corroborator dựa trên observed failure-domain metadata.
- Mọi refund attempt dùng đúng `K=2`; cùng primary observation và cùng true fault map trong paired cell.

## Metadata conditions

1. `accurate`: không thiếu, không sai.
2. `missing_25`: mỗi source label có xác suất `0.25` bị thiếu.
3. `wrong_25`: mỗi source label có xác suất `0.25` bị gán sang domain sai.
4. `mixed_25_each`: xác suất `0.25` missing cộng `0.25` wrong; đây là stress condition, không phải primary pass requirement.

Khi observed primary domain hoặc usable independent candidate không tồn tại, provenance selector fallback sang random corroborator. Selector không được đọc true topology.

## Partial common-mode fault model

- Primary và interface cùng `operational_db` luôn nhận cùng schema-valid wrong eligibility output trong fault cells.
- Mỗi cross-domain source nhận cùng wrong output với xác suất `ℓ`, gọi là cross-domain leakage.
- Leakage levels: `ℓ ∈ {0.00, 0.10, 0.25, 0.50}`.
- `clean` giữ mọi source đúng và chỉ chạy một lần cho mỗi metadata condition.

Model này không được gọi là production-realistic; nó chỉ bỏ giả định “independent source luôn đúng”.

## Quy mô đã khóa

- Seeds: `607`, `719`, `823`, `929`, `1031`.
- Random baseline: `30 × 5 × 5 regime/leakage cells = 750` episodes.
- Provenance: `30 × 5 × 5 cells × 4 metadata conditions = 3,000` episodes.
- Tổng: `3,750` deterministic episodes.
- Không dùng LLM/API/GPU.

## Metrics

- Primary: unsafe-refund difference `provenance_k − random_k`.
- Guardrails: clean task success, clean unsafe refund, boundary coverage `1.000`, matched `K=2`.
- Secondary: task success, false block, conflict, true-domain diversity, observed metadata completeness/accuracy.
- Paired task-cluster bootstrap: `10,000` resamples.

## Predeclared robustness decision rule

Gate `PASS ROBUSTNESS` chỉ khi:

1. tất cả coverage, budget, fresh-ID và pairing invariants pass;
2. với `accurate` metadata tại leakage `0.25`, unsafe difference âm và upper 95% CI `< 0`;
3. với `missing_25` tại leakage `0.10`, unsafe difference âm và upper 95% CI `< 0`;
4. với `wrong_25` tại leakage `0.10`, unsafe difference âm và upper 95% CI `< 0`;
5. trong clean cells, provenance không giảm task success quá `0.05` so với random và không tăng unsafe refund quá `0.02`.

Nếu chỉ condition `accurate, ℓ=0` có lợi thế, kết luận là `FRAGILE`. `mixed_25_each` và leakage `0.50` dùng để tìm collapse boundary, không bắt buộc pass.

## Interpretation guardrail

- `PASS ROBUSTNESS` củng cố robustness trong cùng synthetic environment, không tạo external validity.
- `FAIL` không xóa main result; nó thu hẹp RQ về accurate metadata/perfectly separated domains.
- Không điều chỉnh thresholds hoặc chọn bỏ condition sau khi xem output.

## Result — 2026-09-15

**FACT:** Gate chạy đủ `3,750` episodes; `37/37` tests và `ruff` pass. Reproducibility rerun tạo cùng raw SHA-256 `f22e7f29c97a89eda20bdb57f9e59fa43581adb3d3b6475ee40e926492ab1982`.

| Predeclared condition | Unsafe Δ provenance−random | 95% CI | Kết quả |
|---|---:|---:|---|
| `accurate`, leakage `0.25` | -0.133 | [-0.220, -0.053] | PASS |
| `missing_25`, leakage `0.10` | -0.153 | [-0.227, -0.087] | PASS |
| `wrong_25`, leakage `0.10` | -0.067 | [-0.133, 0.000] | **FAIL** |
| clean guardrails | success 1.000; unsafe 0.000 | — | PASS |

**Decision:** `FAIL ROBUSTNESS`. Rule yêu cầu tất cả conditions pass; upper CI của `wrong_25 + leakage 0.10` chạm zero nên không được làm tròn thành success.

**FACT:** Với accurate metadata, advantage vẫn xuất hiện tại leakage `0.50` (`Δ=-0.127`, CI `[-0.213,-0.047]`). Missing labels làm selector fallback `29%` trong refund attempts nhưng vẫn còn measurable gain. Wrong labels nguy hiểm hơn missing labels: true-domain diversity chỉ còn khoảng `0.79`, làm result không còn chắc chắn ngay tại leakage `0.10`.

**Implementation audit:** Bản chạy đầu chọn corroborator cả khi không có refund attempt, làm denominator của fallback rate không đúng action-boundary semantics. Code đã được sửa để chỉ chọn tại refund attempt, thêm regression test và rerun toàn bộ. Primary outcomes/decision không đổi; raw hash phía trên là artifact cuối.

**INFERENCE:** Provenance selector chịu được conservative uncertainty—không biết label và fallback—tốt hơn misinformation về dependency. RQ rộng về “imperfect provenance” không sống sót; claim chỉ defensible khi metadata chính xác hoặc thiếu nhưng không bị gán sai có hệ thống.

**Caveat:** Leakage draws ở mỗi level được sinh độc lập, không nested; vì vậy các point estimates không bắt buộc monotonic. Không diễn giải `missing_25` tại leakage `0.50` tốt hơn `0.25` như một causal trend.

## Related

- [[synthesis/Protocol - Action-Boundary Provenance Verification Main Study]]
- [[synthesis/Candidate RQ - Provenance-Aware Verification under Correlated Tool Failures]]
- [[journal/2026-09-15-action-boundary-main-study]]
