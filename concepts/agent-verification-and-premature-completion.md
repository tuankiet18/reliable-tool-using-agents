---
title: >-
  Agent Verification and Premature Completion
category: concepts
tags: [ai-agents, verification, reliability, evaluation]
sources: [https://arxiv.org/abs/2404.07972, https://arxiv.org/abs/2406.12045, https://arxiv.org/abs/2509.02761]
summary: >-
  Phân biệt giữa việc agent tự báo hoàn thành và goal state được xác minh độc lập, gồm cả lỗi silent write và quỹ đạo chưa hoàn tất.
provenance:
  extracted: 0.70
  inferred: 0.30
  ambiguous: 0.00
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# Xác minh agent và kết thúc nhiệm vụ quá sớm

`Agent Verification and Premature Completion`

**FACT:** τ-bench so sánh trạng thái database cuối với goal state đã gán nhãn. OSWorld cung cấp hàm đánh giá dựa trên thực thi cho từng tác vụ. Cả hai mạnh hơn việc chấp nhận lời khẳng định bằng ngôn ngữ tự nhiên của agent.

**INFERENCE:** “Kết thúc nhiệm vụ quá sớm” (premature task completion) nên được định nghĩa vận hành là agent dừng trước khi validator goal state độc lập pass, thay vì nhận xét chủ quan khi đọc trace. ^[inferred]

## Dạng lỗi

- báo thành công sau tool error hoặc silent write failure;
- nhầm hoàn thành một phần là hoàn thành toàn bộ;
- hành động cục bộ đúng nhưng ràng buộc toàn cục chưa đạt;
- retry sau tool action không idempotent, tạo tác dụng phụ trùng lặp.

## Liên quan

- [[concepts/reliable-tool-using-agent-lifecycle]]
- [[concepts/agent-recovery-policy]]
