---
title: >-
  τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains
category: references
tags: [paper, benchmark, ai-agents, tool-use, reliability]
relationships:
  - target: "[[concepts/reliable-tool-using-agent-lifecycle]]"
    type: implements
sources: [https://arxiv.org/abs/2406.12045]
source_url: https://arxiv.org/abs/2406.12045
summary: >-
  Benchmark tool-agent-user có state và policy; goal-state evaluation cùng pass^k qua nhiều lần chạy làm lộ hành vi thiếu ổn định của agent.
provenance:
  extracted: 0.92
  inferred: 0.08
  ambiguous: 0.00
base_confidence: 1.00
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: core
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains

> [!tldr] Testbed API-agent tái sử dụng được, trong đó database state cuối—không phải agent tự báo—quyết định success; nhiều lần chạy đo độ tin cậy.

## Vấn đề và lý do quan trọng

Đánh giá tool agent trước đây thường bỏ qua trao đổi với người dùng và policy theo domain. τ-bench đánh giá agent trong hội thoại động với user mô phỏng, domain API, database và policy guideline.

## Setting và phương pháp

Domain kiểu retail và airline; agent hội thoại, truy xuất thông tin policy và gọi tool. Evaluator so sánh database state cuối với goal state đã gán nhãn. `pass^k` đo agent có pass toàn bộ k lần thử độc lập hay không.

## Baseline và kết quả chính

Paper báo cáo GPT-4o thành công dưới 50% task và retail `pass^8` dưới 25%. Các con số do paper báo cáo này cho thấy cần đo tính ổn định, không chỉ success của một lần chạy.

## Giả định và hạn chế

- User/domain/API mô phỏng có thể không đại diện cho tool outage hay hiệu ứng production không thể đảo ngược. ^[inferred]
- Chấm final state mạnh để xác minh hoàn thành, nhưng tự nó không attribution lỗi hay chỉ ra recovery. ^[inferred]

## Paper này chưa giải quyết gì

Paper không chèn lỗi độ tin cậy của tool có kiểm soát, cũng không đánh giá policy retry so với replan.

## Liên hệ với research này

- [[concepts/reliable-tool-using-agent-lifecycle]]
- [[concepts/agent-verification-and-premature-completion]]
- [[concepts/agent-recovery-policy]]

## Sources

- <https://arxiv.org/abs/2406.12045>
