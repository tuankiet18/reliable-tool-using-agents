---
title: >-
  AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents
category: references
tags: [paper, benchmark, ai-agents, security, tool-use]
sources: [https://arxiv.org/abs/2406.13352, https://proceedings.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf]
source_url: https://arxiv.org/abs/2406.13352
summary: >-
  Dynamic benchmark NeurIPS 2024 kiểm tra tool agent dưới indirect prompt-injection attack, gồm 97 task và 629 security case.
provenance:
  extracted: 0.93
  inferred: 0.07
  ambiguous: 0.00
base_confidence: 1.00
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# AgentDojo

> [!tldr] AgentDojo cung cấp môi trường động hướng security khá trưởng thành, nhưng prompt injection chỉ là một nguồn làm tool agent thiếu tin cậy.

## Vấn đề, setting và dataset

Benchmark đánh giá agent đọc tool output không đáng tin cậy và có thể bị dẫn dắt thực thi task độc hại. Nó có 97 task thực tế, 629 security test case và attack/defense có thể mở rộng.

## Kết quả chính

Tác giả nhận thấy LLM state-of-the-art vẫn thất bại ở một số task lành tính và attack hiện có phá vỡ một số—không phải toàn bộ—security property.

## Paper này chưa giải quyết gì

Paper không nhắm tới tool fault tạm thời/kéo dài không đối kháng hoặc chọn recovery action.

## Liên hệ với research này

- [[concepts/least-privilege-tool-use]]
- [[synthesis/Preliminary Gap - Failure-Aware Least Privilege]]

## Sources

- <https://arxiv.org/abs/2406.13352>
