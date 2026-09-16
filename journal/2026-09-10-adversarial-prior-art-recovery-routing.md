---
title: >-
  Nhật ký nghiên cứu — Adversarial prior-art search cho Selective Recovery Routing
category: journal
tags: [research-log, prior-art, ai-agents, recovery, tool-failure]
sources: [https://arxiv.org/abs/2608.11977, https://arxiv.org/abs/2606.01416, https://arxiv.org/abs/2606.25819, https://arxiv.org/abs/2607.06273]
summary: >-
  Adversarial search bác bỏ broad Selective Recovery Routing gap vì có prior art trực tiếp; ghi lại bằng chứng, artifact gate và quyết định không tạo RQ.
provenance:
  extracted: 0.82
  inferred: 0.13
  ambiguous: 0.05
base_confidence: 0.93
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: supporting
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# Nhật ký nghiên cứu — Adversarial prior-art search cho Selective Recovery Routing

## Đã kiểm tra

- Đọc sâu Failing Tools, Efficient Forecasting of Task Failures in LLM Agents through Adaptive Fault Injection và AgentTether theo failure model, observable signal, timing, action space, baseline, metric và artifact.
- Tìm kiếm adversarial theo các họ từ khóa `retry vs replan`, `recovery policy`, `strategy-aware tool use`, `runtime intervention`, `rollback`, `verifier-guided recovery`, `human escalation` và `tool environment unreliability`.
- Kiểm tra full HTML của Retry, Switch, or Abstain?, AgentTether, Self-Healing Agentic Orchestrators, ToolBench-X repository/dataset và các nguồn rollback lân cận.

## Kết quả

**REJECTED:** broad gap không còn phù hợp. Retry, Switch, or Abstain? có S1 retry, S2 switch và S3 abstain/escalate, BTM runtime context, DAPO RL, strategy-level metric, cross-benchmark evaluation. Self-Healing Agentic Orchestrators là counterexample bổ sung cho bounded, verifier-guided controller so với retry-only/full replanning.

## Quyết định về RQ

Không tạo candidate Research Question. Làm RQ theo broad claim sẽ có novelty threat quá lớn và dễ trở thành reproduction/engineering variation của BENCH2ROBUST.

## Artifact gate

- Failing Tools và Adaptive Fault Injection: chưa xác minh được code/data/license chính thức.
- AgentTether: arXiv đầy đủ nhưng chưa thấy official implementation; API/multi-model cost cao.
- ToolBench-X: code/data public và có local runtime, nhưng dataset license hạn chế modification/dissemination; phù hợp pilot sau khi làm rõ license, không phải nền cho broad novelty.

## Điều còn mở nhưng không kết luận là gap

Chưa thấy benchmark public đồng thời: chấm correct human escalation, phạt non-idempotent side effect, có goal-state verification và cho phép auditable no-training controller. Đây chỉ là điều kiện hẹp để kiểm tra ở tương lai.

## Bước tiếp theo duy nhất

Quay lại landscape và chọn **một** gap candidate khác—ưu tiên failure-aware least privilege hoặc completion verification—rồi thực hiện adversarial prior-art search tương tự trước khi đề xuất RQ.

