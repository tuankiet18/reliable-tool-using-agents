---
title: >-
  ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities
category: references
tags: [paper, benchmark, ai-agents, tool-use, stateful]
sources: [https://arxiv.org/abs/2408.04682]
source_url: https://arxiv.org/abs/2408.04682
summary: >-
  An Apple benchmark for stateful and conversational tool use with implicit tool dependencies and milestone-aware evaluation.
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
base_confidence: 1.00
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# ToolSandbox

> [!tldr] ToolSandbox đưa state dependence, thông tin thiếu và milestone trên quỹ đạo bất kỳ vào môi trường tool-use tái lập được.

## Vấn đề, setting và phương pháp

Đánh giá trước đây thường stateless, single-turn hoặc off-policy. ToolSandbox cung cấp stateful tool, phụ thuộc state ngầm, user simulator và đánh giá milestone trung gian/cuối động.

## Kết quả chính

Tác giả báo cáo khoảng cách giữa proprietary/open-source model; task state dependency, canonicalization và insufficient information vẫn khó với model mạnh.

## Hạn chế và phê bình cho research này

- Paper nhấn mạnh statefulness không lý tưởng, nhưng abstract chưa xác lập taxonomy runtime tool fault có kiểm soát như silent write hay temporary outage. ^[inferred]
- Đây chủ yếu là môi trường đánh giá, không phải recovery controller.

## Liên hệ với research này

- [[concepts/reliable-tool-using-agent-lifecycle]]
- [[references/tau-bench]]
- [[synthesis/Preliminary Gap - Selective Recovery Routing]]

## Sources

- <https://arxiv.org/abs/2408.04682>
