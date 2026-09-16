---
title: "Prior-Art Threat: Provenance Metadata and Source Selection"
category: synthesis
tags: [prior-art, novelty, ai-agents, provenance, verification]
sources:
  - "https://arxiv.org/abs/2602.21517"
  - "https://arxiv.org/abs/2606.18037"
  - "https://arxiv.org/abs/2607.01236"
  - "https://arxiv.org/abs/2605.08828"
  - "https://arxiv.org/abs/2606.22741"
  - "https://arxiv.org/abs/2607.01640"
  - "https://aclanthology.org/2024.findings-emnlp.978/"
  - "https://arxiv.org/abs/2609.01360"
created: 2026-09-15T15:34:48+07:00
updated: 2026-09-15T16:27:33+07:00
summary: >-
  Adversarial search bác bỏ novelty ở mức rộng cho tool-trust selection, provenance-aware action gating và dependency validation; exact RQ chỉ sống với phạm vi failure-domain independence dưới correlated silent failures.
---

# Prior-art threat — Provenance metadata và source selection

## Câu hỏi bị tấn công

Prior art đã nghiên cứu việc validate/calibrate provenance/dependency metadata và dùng uncertainty để chọn source/tool đủ gần với RQ hiện tại hay chưa?

## Kết luận ngắn

`SURVIVES WITH REFINEMENT — PRELIMINARY` cho **exact RQ**, nhưng ba novelty claim rộng đã bị bác bỏ. Không được nói rằng project là hệ thống đầu tiên chọn tool theo trust, đầu tiên dùng provenance để gate action, hoặc đầu tiên kiểm tra dependency metadata.

## Prior-art threat matrix

| Work | Setting | Nó estimate/validate gì? | Dynamic selection/intervention? | Correlated tool faults? | Metadata uncertainty? | Irreversible action boundary? | Same problem? |
|---|---|---|---|---|---|---|---|
| [[references/tea-cxa]] | Medical multimodal tools | Learned per-tool expertise theo query type | ✓ chọn response nên tin | ✗ | △ learned trust | ✗ | PARTIAL |
| [[references/provenanceguard-source-aware-factuality]] | MCP medical traces | Claim–source attribution/support | ✓ allow/block answer | ✗ | △ thiếu source ID có fallback | ✗ | PARTIAL |
| [[references/provenanceguard-misalignment-provenance-analysis]] | Generic tool agents | Action justification từ query/docs/history/plan | ✓ pre-execution block | ✗ | △ plan reconstructed | ✓ | PARTIAL |
| [[references/grade-agent-dependency-execution]] | Tool, coding, web agents | Dependency edges: observed/declared/inferred | ✗ selection; ✓ diagnosis | ✗ | ✓ evidence grade và controls | ✗ | PARTIAL |
| [[references/agentflow-agent-dependency-graphs]] | Agent source code | Static component/control/data dependencies | ✗ | ✗ | △ static overapproximation | ✗ | NO |
| [[references/envtrustbench]] | Files/logs/APIs/commands | Oracle cho true state và false path | ✗ method; benchmark only | ✗ explicit shared domains | △ stale/wrong/malicious evidence | △ consequential false path | PARTIAL |
| `ProbeCal` | Tool-using language agents | Calibrated expected effectiveness của prompt/trace | ✓ execution-path selection | ✗ | ✓ model uncertainty | ✗ | NO |
| `EDGE` | Multi-agent failures | Counterfactual validation của error-dependency edges | △ guides attribution/repair | ✗ tool-source faults | ✓ observational vs intervention-validated | ✗ | NO |

Legend: `✓` rõ ràng có; `△` một phần; `✗` không có trong setting được báo cáo.

## Falsification theo từng claim

### 1. “Uncertainty-aware source/tool selection chưa tồn tại”

**REJECTED.** TEA-CXA học tool expertise và chọn response nên tin khi tools xung đột. `ProbeCal` cũng dùng calibrated uncertainty để chọn prompts/execution traces. Đây không phải exact failure-domain policy, nhưng đủ bác bỏ novelty wording rộng.

### 2. “Provenance-aware runtime action gating chưa tồn tại”

**REJECTED.** `Safeguarding LLM Agents from Misalignment through Provenance Analysis` chặn tool calls trước execution dựa trên provenance của tool, parameters và interpretation.

### 3. “Dependency/provenance metadata chưa được validate”

**REJECTED ở mức rộng.** GRADE phân loại dependency edges theo cách chúng được biết và kiểm tra inferred structure bằng controls; EDGE dùng counterfactual rollout để giữ causal subset; AgentFlow derive dependency graph từ source code. Các work này chưa validate `failure_domain_id`, nhưng câu tuyên bố rộng không còn đúng.

### 4. “Realistic incorrect environmental evidence chưa có benchmark”

**REJECTED.** EnvTrustBench tạo stale/wrong/malicious environmental evidence, lưu trajectory và dùng machine oracle. Tuy nhiên public artifact hiện chưa đủ cho full reproduction.

### 5. Tổ hợp exact RQ

**Chưa tìm thấy direct match** đồng thời có đủ:

1. schema-valid silent tool-output corruption;
2. shared/common failure domains giữa các tool interfaces;
3. mandatory verification ngay trước irreversible action;
4. selector chọn corroborator độc lập theo failure domain;
5. comparison với random source ở matched `K=2`;
6. unsafe-action và clean-task utility metrics.

Đây là negative search result, không phải bằng chứng về confirmed novelty.

## Contradictions và implications

- TEA-CXA cho thấy learned trust có thể resolve conflict, nhưng cần heavy RL và domain-specific reward; RQ hiện tại dùng deterministic metadata và không training.
- GRADE cho thấy inferred dependency structure có thể transfer kém. Robustness gate của project cũng cho thấy wrong labels nhanh chóng phá safety gain. Hai nguồn cùng chống giả định “graph/metadata có là dùng được”.
- ProvenanceGuard (ASE) giảm misaligned actions nhưng provenance chỉ chứng minh action có căn cứ trong context; nếu context/tool output cùng sai, guard không giải quyết truthfulness.
- EnvTrustBench chứng minh environmental misgrounding phổ biến, nhưng chưa cung cấp redundant-source/failure-domain treatment cần cho exact comparison.

## Novelty boundary phải dùng

Không claim một method hoàn toàn mới. Claim có thể bảo vệ là:

> **PRELIMINARY:** empirical characterization of when failure-domain-independent corroboration reduces unsafe irreversible actions under controlled correlated silent tool failures at matched verification cost.

## Có nên đổi RQ sang metadata validation không?

**Không.** Đây sẽ là scope creep. Derive/validate failure-domain metadata là một bài toán riêng, có threat trực tiếp từ GRADE, EDGE và AgentFlow, đồng thời cần ground truth về backend dependencies khó xây trong 12 tuần. RQ hiện tại nên giữ assumption `given accurate failure-domain metadata` và nêu đây là external-validity limitation.

## Gap survival status

`SURVIVES WITH REFINEMENT — PRELIMINARY`.

- Internal causal mechanism: đã có evidence mạnh trong controlled benchmark.
- Novelty: chỉ còn ở tổ hợp hẹp, confidence trung bình.
- External validity: yếu.
- Reproducibility trong 12 tuần: tốt cho core controlled study; chưa đạt cho external benchmark.

## Bước tiếp theo duy nhất

Artifact gate đã thực hiện: EnvTrustBench `FAIL` vì không public executable cases; ProvenanceGuard artifact `PASS` kỹ thuật nhưng chỉ `PARTIAL` fit. Bước tiếp theo là manual-audit 12 Agent-SafetyBench/WorkBench cases trước khi viết adaptation code. Xem [[journal/2026-09-15-external-validity-artifact-gate]].

## Related

- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]]
- [[journal/2026-09-15-adversarial-prior-art-provenance-metadata]]
