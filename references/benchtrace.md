---
title: >-
  BenchTrace: A Benchmark for Testing Reflection Ability and Controlled Evolution in LLM Agents
category: references
tags: [paper, benchmark, ai-agents, reflection, diagnosis]
sources: [https://arxiv.org/abs/2605.29225]
source_url: https://arxiv.org/abs/2605.29225
summary: >-
  Benchmark episode có nhãn năm 2026, kiểm tra nhận diện lỗi và việc reflection có chuyển thành hành vi tránh lỗi qua các task hay không.
provenance:
  extracted: 0.91
  inferred: 0.09
  ambiguous: 0.00
base_confidence: 1.00
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# BenchTrace

> [!tldr] BenchTrace thách thức giả định reflection luôn tạo recovery tổng quát: diagnosis là nút thắt và episode nhiễu tích lũy có thể gây negative transfer.

## Dataset / metric

1.821 annotated episode trên sáu task. Reflection Evaluation kiểm tra nhận diện qua câu hỏi mục tiêu; Evolution Evaluation dùng failure avoidance rate (FAR).

## Kết quả chính

Paper báo cáo end-to-end reflection pass rate dưới 30% cho Qwen3-32B và GPT-4.1; chỉ reflection hoàn toàn đúng tương quan mạnh với FAR cao hơn. Paper báo cáo forgetting khi episode nhiễu và generalization qua context hạn chế.

## Paper này chưa giải quyết gì

Paper không so sánh runtime recovery-action policy trong điều kiện tool failure được kiểm soát.

## Liên hệ với research này

- [[concepts/agent-recovery-policy]]
- [[synthesis/Preliminary Gap: Selective Recovery Routing]]

## Sources

- <https://arxiv.org/abs/2605.29225>
