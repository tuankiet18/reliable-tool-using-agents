---
title: "AgentForesight: Online Auditing for Early Failure Prediction in Multi-Agent Systems"
category: references
tags: [paper, benchmark, ai-agents, failure-detection, multi-agent]
sources:
  - "https://arxiv.org/abs/2605.08715"
  - "https://github.com/ZBox1005/AgentForesight"
  - "https://huggingface.co/datasets/ZBox008003/AFTraj"
source_url: https://arxiv.org/abs/2605.08715
summary: >-
  Online auditor nhìn từng trajectory prefix, báo continue/alarm và localize decisive error; AFTraj-2K là dataset công khai khả thi cho phân tích không tốn API.
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.94
lifecycle: draft
lifecycle_changed: 2026-09-12
tier: core
created: 2026-09-12T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# AgentForesight: Online Auditing for Early Failure Prediction in Multi-Agent Systems

## Problem và setting

AgentForesight chuyển failure attribution hậu kiểm thành online auditing: ở mỗi step, auditor chỉ thấy current prefix và phải chọn `CONTINUE` hoặc `ALARM` tại decisive error sớm nhất. Setting chính là multi-agent trong Coding, Math và Agentic web/QA.

## Dataset và fault construction

AFTraj-2K có 2,276 trajectories: 1,162 safe và 1,114 unsafe. Safe runs được kiểm tra outcome, integrity và coherence. Unsafe set kết hợp organic failure với controlled fault injection; Coding faults gồm `code_bug`, `verification_skip`, `verdict_misread`; Agentic faults có `tool_injection`, `prompt_injection`, `verification_shortcut` và các lỗi verdict.

Injected trajectories được replay để giữ downstream propagation thật, và chỉ giữ nếu outcome chuyển sang failure. Decisive error step được gán by construction hoặc qua nhiều proposer/verifier call.

## Method và result

AgentForesight-7B dùng coarse-to-fine RL để học cả loại lỗi, vị trí và agent chịu trách nhiệm. Paper báo `66.44 Exact-F1`, cao hơn strongest proprietary baseline `19.88` điểm, và transfer sang Who&When.

## Artifact và tính phù hợp 12 tuần

- Dataset và inference code public, MIT license theo repository.
- Checkpoint 7B được hứa release sau paper acceptance; training gốc dùng `2× NVIDIA H200`, không phù hợp để tái huấn luyện trong project này.
- Dataset có thể dùng cho analysis/baseline không cần API; đây là lựa chọn tốt hơn tự tạo 20–30 task nếu mục tiêu chỉ là học và kiểm tra evaluation protocol.

## Limitation và novelty impact

- Auditor phải chạy ở mọi prefix.
- Coverage chưa gồm long-horizon embodied/scientific discovery.
- Fault catalog có cả silent intermediate errors và tool/verification faults; external benchmark transfer cũng đã được đo.

**Kết luận:** prior art trực tiếp cho prefix-based early failure detection và decisive-step localization. Nó không phải lý do để làm lại một classifier nhỏ trên cùng bài toán.

## Related

- [[synthesis/Research - Early Failure Detection in Tool-Using Agents]]
- [[references/real-time-detection-and-repair-agent-failures]]

