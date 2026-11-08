---
title: >-
  So sánh sâu ba anchor work về recovery của AI Agent
category: synthesis
tags: [ai-agents, recovery, tool-failure, comparison, research]
sources:
  - "https://openreview.net/pdf?id=j7YsSnA64D"
  - "https://openreview.net/forum?id=d3Qq4weuwz"
  - "https://arxiv.org/abs/2607.06273"
summary: >-
  So sánh Failing Tools, Adaptive Fault Injection và AgentTether theo failure model, observability, timing, recovery action, policy, metric và khả năng tái lập.
provenance:
  extracted: 0.78
  inferred: 0.17
  ambiguous: 0.05
base_confidence: 0.91
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# So sánh sâu ba anchor work về recovery của AI Agent

## Kết luận ngắn

Ba anchor work không cùng loại: [[references/failing-tools]] là benchmark quan sát/evaluate recovery; [[references/adaptive-fault-injection-task-failure-forecasting]] là forecaster dự báo terminal failure từ partial trace; [[references/agenttether]] là repair wrapper sau failed run kèm guarded rerun. Không anchor nào, theo bằng chứng hiện có, là action router chuẩn hóa giữa `retry`, `replan`, `fallback`, `rollback`, `stop` và `human escalation` trong cùng một evaluator. Tuy nhiên, điều này **không cứu broad gap**, vì [[references/retry-switch-or-abstain]] đã trực tiếp nghiên cứu phần lõi `retry/switch/abstain`.

## Ma trận side-by-side

Ký hiệu: ✓ supported; △ partial; ✗ absent; ? insufficient evidence. Dấu ✓ ở mỗi cột được giải thích ngay sau bảng.

| Dimension | Failing Tools | Adaptive Fault Injection | AgentTether |
|---|---:|---:|---:|
| detects failure | ✓ | △ | ✓ |
| predicts failure | ✗ | ✓ | ✗ |
| localizes failure | △ trajectory criteria | △ step-local labels | ✓ CTG/RCA |
| diagnoses root cause | △ đánh giá agent | ✗ | ✓ analyst + CTG |
| temporary vs persistent failure | ✓ | ? | ✗ không phải fault taxonomy |
| runtime intervention | △ agent hành động trong benchmark | ✓ trigger được nêu, selection ? | △ chỉ khi rerun sau failed initial run |
| retry | ✓ đo hành vi | △ intervention ví dụ | △ rerun, không retry action riêng |
| modified retry | ? | ? | △ guidance sửa hành vi |
| replan | ? | △ intervention ví dụ | △ rerun có guidance, không action label |
| fallback | ✓ đo hành vi | ? | ✗ |
| rollback | ✗ | ✗ | ✗ |
| stop | △ residual uncertainty | △ risk trigger | △ dừng khi hết repair budget/task resolved |
| human escalation | △ faithful communication, evaluator check | △ ví dụ intervention | ✗ |
| selects among recovery actions | ✗ benchmark không controller | ✗ chỉ failure forecast | ✗ chọn injection strength, không menu recovery action |
| uses trajectory signals | ✓ | ✓ | ✓ |
| learned recovery policy | ✗ | ✗ forecaster được train | ✗ |
| rule-based policy | ✗ | ✗ | ✓ guards/checks |
| LLM-based recovery decision | △ acting agent | △ forecaster/acting agent | ✓ analyst LLM tạo guidance |
| considers cost | △ strategy/safety/calibration score | ✓ forecaster cost claim | ✓ turns/tokens/duration |
| considers tool-call overhead | △ trajectory-level criteria | ? | ✓ Avg Steps |
| considers unsafe side effects | ✓ safety criteria | ✗ | △ destructive-action guard |
| evaluates recovery-action choice | ✓ strategy appropriateness | ✗ | ✗ repair outcome, không action menu |
| public benchmark | ? anonymous review PDF | ? benchmark details/code not found | ✓ uses τ-bench |
| public code | ? | ? | ? no official repository found |
| reproducible in 3 months | △ only if artifacts released | ✗ likely training/rollout heavy | △ API-heavy, implementation unavailable |

## Bằng chứng cho các ô quan trọng

- **Failing Tools:** abstract/PDF mô tả 218 scenario, failure gồm availability denial, stale data, silent no-op, corrupted state, schema mismatch, disambiguation failure và cascade; phân biệt transient/permanent và chấm detection, recovery strategy, safety, calibration. Không tìm thấy repository/license chính thức trong adversarial search, nên artifact là `?`.
- **Adaptive Fault Injection:** paper định nghĩa `P(terminal failure | partial trace, current policy)`; dùng perturbation + rollout để label high-risk prefix và train Qwen-3-8B. Những action như reflection/resampling/human handoff là lý do cần dự báo, không phải action space được so sánh.
- **AgentTether:** trace có observation, belief/reasoning, action, feedback, execution status và error signature. CTG + offline HGT/run-local detector + analyst LLM tạo guidance sau failed run; Check–Decide–Inject can thiệp tại tool-return/text-response hook trong rerun. Evaluation là blind retry, outcome feedback, Reflexion, post-run-only và full AgentTether—không có fallback/rollback/escalation action baseline.

## Artifact và reproducibility gate

| Work | Trạng thái/artifact | Rủi ro tái lập |
|---|---|---|
| Failing Tools | ACL anonymous submission PDF; 218 scenario; code/dataset/license chưa xác minh | Cao: không thể lấy benchmark làm nền chính khi artifact chưa công khai |
| Adaptive Fault Injection | ICML 2026 workshop metadata; PDF anonymous version; code/dataset/license chưa thấy | Cao: cần Qwen3-8B và rollout-based synthetic supervision |
| AgentTether | arXiv v1, dùng τ-bench 261 task; no official code located | Trung bình–cao: phụ thuộc nhiều API model và auxiliary model; chỉ 123 initially failed task ở bảng chính |

## Hàm ý nghiên cứu

**INFERENCE:** Ba anchor work là background tốt cho detection/diagnosis/evaluation, nhưng không còn là bằng chứng đủ để gọi selective recovery routing là gap. Việc sử dụng chúng làm baseline/reproduction project cũng không tốt bằng benchmark có code/data công khai. ^[inferred]

## Liên hệ

- [[references/retry-switch-or-abstain]] — counterexample trực tiếp của broad gap.
- [[synthesis/Prior-Art Threat - Recovery-Action Selection]]
- [[synthesis/Preliminary Gap - Selective Recovery Routing]]
