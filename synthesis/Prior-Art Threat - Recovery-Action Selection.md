---
title: >-
  Prior-Art Threat Analysis: Recovery-Action Selection
category: synthesis
tags: [ai-agents, recovery, prior-art, novelty, tool-failure]
sources: [https://arxiv.org/abs/2608.11977, https://arxiv.org/abs/2606.01416, https://arxiv.org/abs/2606.25819, https://arxiv.org/abs/2607.06273, https://arxiv.org/abs/2603.20625]
summary: >-
  Phân tích phản biện prior art cho thấy broad Selective Recovery Routing gap bị đe dọa trực tiếp bởi Retry, Switch, or Abstain và Self-Healing Agentic Orchestrators.
provenance:
  extracted: 0.81
  inferred: 0.14
  ambiguous: 0.05
base_confidence: 0.93
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# Prior-Art Threat Analysis: Recovery-Action Selection

## Kết luận phản biện

**REJECTED cho broad gap.** Claim rằng literature chưa nghiên cứu dynamic selection giữa retry, fallback/switch và escalation/stop dưới runtime tool failure không còn đứng vững sau khi kiểm tra [[references/retry-switch-or-abstain]]. Paper này gần như trùng khớp phần lõi: controlled error injection, retry/switch/abstain scenario, runtime recovery context, learned policy, strategy-level metric và cross-benchmark evaluation.

## Prior-art threat table

| Paper                                                               | Year | Setting                                                          | Recovery choices                                               | Dynamic selection?                                 | Inputs/signals                                                         | Cost-aware?                                        | Same problem?                                    |
| ------------------------------------------------------------------- | ---: | ---------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------ |
| [[references/retry-switch-or-abstain]]                              | 2026 | Multi-turn API/tool agents                                       | retry, switch/fallback, abstain/escalate                       | **Có:** BTM + RL policy                            | Tool error/output, fallback map, constraints, recoverability summaries | △ token/episode efficiency; không side-effect cost | **YES**                                          |
| Self-Healing Agentic Orchestrators                                  | 2026 | Controlled tool-augmented orchestrator + compact live model loop | targeted recovery action dưới budget; verifier-guided recovery | **Có:** maps observable fault class to action      | Runtime status, tool output, verifier                                  | ✓ budget sweep/cost proxy                          | **YES** về controller, nhưng benchmark synthetic |
| ToolBench-X                                                         | 2026 | Executable multi-step tool agents                                | retry, fallback, verify, cross-check                           | △ targeted hints, không controller tách biệt       | Hazard/tool output, deferred hint                                      | △ inference budget analysis                        | **PARTIAL**                                      |
| [[references/agenttether]]                                          | 2026 | τ-bench stateful tool agent                                      | rerun + guidance + guarded correction                          | △ correction strength/channel; không strategy menu | Full trace, CTG, detector, guidance                                    | ✓ tokens/turns/duration                            | **PARTIAL**                                      |
| ReflectAgent: Diagnose, Localize, and Rollback Errors in LLM Agents | 2026 | Agent trajectory repair                                          | diagnose/localize/rollback                                     | △ rollback-focused                                 | Step trace/feedback                                                    | ?                                                  | **PARTIAL**                                      |
| GA-Rollback                                                         | 2025 | Goal-driven/embodied agents                                      | rollback after assistant feedback                              | △ rollback-focused                                 | Actions, observations, feedback confidence                             | ?                                                  | **PARTIAL**                                      |
| ACRFence                                                            | 2026 | Checkpoint/retry with consequential external actions             | replay-or-fork fencing                                         | ✗ authorization safety, not recovery routing       | irreversible-effect ledger, authorization state                        | △ prevents duplicate harm                          | **NO**; critical side-effect constraint          |

## Vì sao hai paper đầu là threat trực tiếp

### Retry, Switch, or Abstain?

S1 buộc retry, S2 buộc switch, S3 quy định escalation khi không còn viable path. BTM cung cấp fallback map/recovery constraint tại runtime; RL được train theo curriculum có ba strategy. Paper không chỉ cho LLM “tự reflect”; nó phân tích S1 retry success, S2 switch success và premature escalation. Đây là overlap trực tiếp với broad research idea.

### Self-Healing Agentic Orchestrators

Abstract và full text mô tả bounded runtime control: observable failure signal → inferred failure class → targeted recovery action dưới budget → verification. Nó so sánh retry-only và full replanning ở matched recovery budget. Điểm yếu của threat này là controlled benchmark 100 task và live-model validation nhỏ; nhưng nó vẫn phá vỡ claim rộng rằng không có recovery-action controller.

## Cố gắng bác bỏ từng thành phần của claim cũ

| Thành phần claim             | Counterexample mạnh nhất                                                                                                 | Kết quả                                                                                                                     |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| dynamic selection            | Retry, Switch, or Abstain? dùng BTM + DAPO RL                                                                            | **Bị bác bỏ**                                                                                                               |
| multiple recovery actions    | S1 retry, S2 switch, S3 abstain/escalate                                                                                 | **Bị bác bỏ**                                                                                                               |
| runtime trajectory evidence  | BTM có tool/error observation + recoverability summaries; AgentTether dùng full trace                                    | **Bị bác bỏ**                                                                                                               |
| realistic tool failures      | Retry, Switch, or Abstain? có explicit/silent, transient/persistent injection; Failing Tools/ToolBench-X củng cố realism | **Bị bác bỏ ở mức benchmark**                                                                                               |
| cost / side-effect awareness | Self-Healing đo recovery budget; AgentTether đo token/turn; ACRFence nêu duplicate irreversible effect                   | **Chỉ còn phần hẹp:** chưa thấy một public benchmark đo *đồng thời* action routing, verified escalation và side-effect cost |

## Điểm khác biệt có thể còn lại — nhưng chưa đủ thành đề tài

**SURVIVING NARROW CONDITION (không phải gap đã chứng minh):** Đánh giá *không huấn luyện* một controller có thể kiểm toán (auditable), chọn `retry/switch/stop-escalate` theo history của trajectory và risk của action không idempotent, với goal-state verification và penalty cho side effect, trên benchmark public stateful API tool.

Điều này khác Retry, Switch, or Abstain? ở bốn điểm: không RL; calibration từ online trajectory history thay vì chủ yếu fallback map; evaluator thưởng đúng stop/escalation; và safety cost cho non-idempotent action. Tuy nhiên chưa có benchmark public hiện tại hội đủ các điều kiện này; do đó đây mới là hướng đọc tiếp, **không phải novelty claim**.

## Reproducibility gate

[[references/retry-switch-or-abstain]] là prior art nhưng không phải nền tái lập tốt: arXiv v1 không liên kết code; RL Qwen3-4B/8B cần GPU; S3 chưa có held-out metric cho correct abstention. ToolBench-X có GitHub, Hugging Face dataset (~31.5 MB) và script local/API, nhưng license chỉ cho academic research và cấm modify/disseminate; cần xin/đọc rõ điều khoản trước khi xây extension.

## Quyết định evidence-led

Không phát triển đề tài “Selective Recovery Routing under Runtime Tool Failures” dưới dạng broad idea. Nếu muốn giữ nhánh này, phải tìm benchmark công khai chấm đúng escalation và stateful side effect, rồi chứng minh narrow condition thực sự chưa được nghiên cứu—một rủi ro cao cho 12 tuần.

