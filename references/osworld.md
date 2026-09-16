---
title: >-
  OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments
category: references
tags: [paper, benchmark, ai-agents, long-horizon, verification]
sources: [https://arxiv.org/abs/2404.07972]
source_url: https://arxiv.org/abs/2404.07972
summary: >-
  Benchmark thực thi năm 2024 gồm 369 task máy tính thật và evaluator theo task, cho thấy khoảng cách lớn về hiệu năng agent multimodal mở.
provenance:
  extracted: 0.92
  inferred: 0.08
  ambiguous: 0.00
base_confidence: 1.00
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# OSWorld

> [!tldr] OSWorld có tương tác OS thật và kiểm tra hoàn thành dựa trên thực thi, nhưng gánh nặng GUI/multimodal có lẽ quá cao cho nghiên cứu độ tin cậy 12 tuần đầu tiên.

## Setting và phương pháp đánh giá

369 task thực tế trên các hệ điều hành máy tính, có initial-state setup, task evaluator dựa trên thực thi và VM isolation/reset.

## Kết quả chính

Paper báo cáo hiệu năng baseline từ 0,99% đến 12,24%; workflow nhiều app đặc biệt khó. Các lỗi được nêu gồm grounding, hành động lặp, cửa sổ bất ngờ và kiến thức UI hạn chế.

## Hạn chế và phê bình cho research này

- GUI perception là yếu tố gây nhiễu lớn nếu RQ là recovery policy thay vì multimodal grounding. ^[inferred]
- Nó có lẽ kém tiết kiệm hơn API benchmark cho việc chèn lỗi có kiểm soát. ^[inferred]

## Liên hệ với research này

- [[concepts/agent-verification-and-premature-completion]]
- [[concepts/reliable-tool-using-agent-lifecycle]]

## Sources

- <https://arxiv.org/abs/2404.07972>
