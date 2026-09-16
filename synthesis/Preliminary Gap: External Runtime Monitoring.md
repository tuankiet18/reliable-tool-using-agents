---
title: >-
  Preliminary Gap: External Runtime Monitoring for Early Intervention
category: synthesis
tags: [research-gap, preliminary, ai-agents, monitoring, failure-detection]
sources: [https://openreview.net/pdf/f81b4d72b4ac58cbc7ec781bdc3f8e3c705d4650.pdf, https://arxiv.org/abs/2604.13954, https://arxiv.org/abs/2607.18754]
summary: >-
  REJECTED: external trace monitoring và online failure warning đã có nhiều direct prior art năm 2026; chỉ còn open question hẹp về task-grounded semantic verification.
provenance:
  extracted: 0.48
  inferred: 0.44
  ambiguous: 0.08
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-12T00:00:00Z
---

# REJECTED Gap: external runtime monitoring để can thiệp sớm

> [!danger] **Gap status: REJECTED.** Không tiếp tục coi broad external runtime monitoring/early failure detection là thesis gap.

## Evidence bác bỏ

- Adaptive Fault Injection dự báo terminal failure từ partial execution trace và đánh giá cross-policy theo paper.
- PrefixGuard học online warning monitor từ terminal outcomes, đo false-alarm/lead-time và không cần runtime LLM.
- AgentForesight so external specialized auditor với self-reflection trên cùng Qwen2.5-7B backbone; paper báo `66.44` so với `23.38` Exact-F1.
- AgentTrajectorySentinel dùng telemetry-only one-class monitor, cost-aware escalation và rollback/rerun; public artifact đã chạy local CPU.
- Weakly Supervised Early Alerting và Automata from Agent Traces đã nghiên cứu accuracy–earliness/early stopping từ partial trace.

## Trả lời open question cũ

**FACT:** So sánh hoàn toàn matched về latency/accuracy trong riêng tool-service-fault setting chưa được thấy ở mọi paper. Nhưng AgentForesight đã có same-backbone comparison, còn AgentTrajectorySentinel đo trực tiếp latency và judge-call burden. Phần còn thiếu quá hẹp để cứu broad gap trong project 12 tuần.

## Điều có thể còn mở

**OPEN QUESTION — không phải gap đã xác lập:** telemetry-only monitor không thể nhận biết tool output sai về ngữ nghĩa nhưng vẫn đúng schema và có vẻ hợp lý nếu không có external reference. Có thể cần task-grounded invariant/state verification. Phải search lane này riêng trước khi đưa ra RQ.

## Quyết định

Không xây thêm external trajectory classifier hoặc local 20–30-task failure-prediction harness. Dùng [[references/agentforesight]] và [[references/real-time-detection-and-repair-agent-failures]] để học/reproduce; chuyển novelty search sang [[synthesis/Research: Early Failure Detection in Tool-Using Agents]].
