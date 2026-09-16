---
title: >-
  Seed Papers and Benchmarks for Reliable Tool-Using Agents
category: references
tags: [reading-list, ai-agents, reliability, benchmark, research]
sources: [https://arxiv.org/abs/2406.12045, https://arxiv.org/abs/2408.04682, https://arxiv.org/abs/2406.13352, https://arxiv.org/abs/2404.07972]
summary: >-
  Danh mục ưu tiên gồm 21 paper và benchmark cho các vòng bằng chứng tiếp theo, phân theo hướng độ tin cậy; chưa coi là bằng chứng trước khi đọc sâu.
provenance:
  extracted: 0.65
  inferred: 0.30
  ambiguous: 0.05
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: core
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# Paper và benchmark seed cho AI Agent dùng tool đáng tin cậy

`Seed Papers and Benchmarks for Reliable Tool-Using Agents`

Đây là hàng đợi đọc, không phải tập claim đã được chấp nhận. Mục `P0` cần đọc tiếp vì chúng kiểm tra trực tiếp gap candidate hoặc xác lập nền thực nghiệm khả thi.

| Ưu tiên | Hướng | Paper / benchmark | Lý do nằm trong phạm vi | Trạng thái |
|---|---|---|---|---|
| P0 | Recovery | [[references/failing-tools]] | Controlled runtime faults and recovery | partial note; verify artifacts |
| P0 | Recovery | [[references/agenttether]] | Diagnosis-guided repair on τ-bench | partial note |
| P0 | Detection | Efficient Forecasting of Task Failures in LLM Agents through Adaptive Fault Injection | Partial-trace failure forecasting | fetch final/version and code |
| P0 | Diagnosis | [[references/hintbench]] | Detection vs localization gap | partial note |
| P0 | Reflection | [[references/benchtrace]] | Tests diagnosis and transfer of reflection | partial note |
| P0 | Verification | [[references/tau-bench]] | Goal-state success and pass^k | partial note |
| P0 | Tool failure | [[references/toolsandbox]] | Stateful dependencies/milestones | partial note |
| P0 | Security | [[references/miniscope]] | Least-privilege enforcement | partial note |
| P0 | Security | When Lower Privileges Suffice / ToolPrivBench | Transient-failure privilege escalation | fetch paper/code |
| P0 | Coding security | Do Coding Agents Understand Least-Privilege Authorization? / AuthBench | Permission-boundary inference | fetch paper/code |
| P1 | Verification | Plan Verification for LLM-Based Embodied Task Completion Agents | Planner–judge iteration | read for verifier design |
| P1 | Observability | AgentDebugX | Detect–attribute–recover–rerun tooling | inspect artifact/cost |
| P1 | Security | [[references/agentdojo]] | Dynamic prompt-injection benchmark | partial note |
| P1 | Long horizon | [[references/osworld]] | Executable computer tasks | partial note; likely costly |
| P1 | Coding | SWE-bench Verified | Reproducible code-task substrate | assess contamination/cost |
| P1 | Coding | SWE-Bench Pro | Long-horizon software tasks | inspect availability |
| P1 | Coding | SWE-Sharp-Bench | C#/.NET-aligned benchmark | inspect release/access |
| P2 | Agent generality | AgentBench | Foundational multi-environment agent benchmark | context only |
| P2 | Tool calling | Berkeley Function Calling Leaderboard (BFCL) | Function-call correctness breadth | context only |
| P2 | Planning | PlanBench | Foundational planning/replanning probe | conceptual baseline |
| P2 | Recovery | Reflexion | Historical self-reflection baseline | baseline only |

## Quy tắc chọn ở vòng tiếp theo

Đọc các nguồn P0 theo cặp có thể bác bỏ cùng một candidate: detection + recovery; tool failure + recovery policy; authorization + transient-failure escalation. Chỉ nâng một nguồn thành full claim sau khi kiểm tra version cuối, benchmark artifact và evaluation setup.
