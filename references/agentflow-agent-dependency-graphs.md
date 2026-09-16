---
title: "AgentFlow: Building Agent Dependency Graphs for Static Analysis of Agent Programs"
category: reference
tags: [ai-agents, static-analysis, dependency, security, prior-art]
sources:
  - "https://arxiv.org/abs/2607.01640"
created: 2026-09-15T15:34:48+07:00
updated: 2026-09-15T15:34:48+07:00
summary: >-
  AgentFlow dùng static analysis tạo Agent Dependency Graph từ source code của agent programs; có thể suy ra structural metadata nhưng không suy ra shared runtime failure domains.
---

# AgentFlow: Building Agent Dependency Graphs for Static Analysis of Agent Programs

## Problem và method

Agent programs kết hợp host-language code với framework semantics về models, tools, memory và orchestration. AgentFlow dùng static analysis để tạo `Agent Dependency Graph` gồm component, control-flow và data-flow edges.

## Results

Paper triển khai cho năm agent frameworks và đánh giá trên `AgentZoo` gồm 5,399 programs; ADG hỗ trợ Agent BOM và phát hiện 238 prompt-to-tool risks.

## Giới hạn liên quan RQ hiện tại

- Đây là counterexample cho claim rộng rằng dependency metadata không thể được derive tự động.
- Static graph thường over-approximate và biểu diễn dependency trong program, không chứng minh hai tool adapters có cùng database/cache/provider hay cùng correlated failure mechanism lúc chạy.
- Không dùng graph để chọn verification source và không đo unsafe action dưới silent output corruption.

## Phân loại

`NO — adjacent only` đối với exact RQ; `PARTIAL` đối với câu hỏi phụ “metadata có thể derive/validate thế nào?”.

## Related

- [[references/grade-agent-dependency-execution]]
- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]]

