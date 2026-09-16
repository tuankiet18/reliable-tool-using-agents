---
title: "ToolGuardian: Declarative Security for AI Agent-Tool Interactions"
category: references
tags: [paper, ai-agents, authorization, mcp, security]
sources: [https://arxiv.org/abs/2607.21835]
summary: "ToolGuardian kết hợp vetting tool bằng description/syscall/mock/source evidence với task-aware runtime authorization qua ASP."
provenance: {extracted: 0.88, inferred: 0.07, ambiguous: 0.05}
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: supporting
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# ToolGuardian

## Problem / evidence model

ToolGuardian bảo vệ agent-tool interaction trước tool bên thứ ba có interface lành tính nhưng implementation nguy hiểm. Nó dùng progressive characterization: tool description, system-call trace, mock execution/effect và source analysis; sau đó ASP policy layer suy luận capability, effect, task context và multi-tool composition.

## Relevance và limitation

Paper đánh giá 16 MCP-style tools (8 malicious variants) và 20 runtime scenarios; báo cáo deny-class F1 0.86 khi vetting. Đây là counterexample cho claim chung “dùng source/software evidence để task-aware authorize tool”. Nhưng nó phân tích *tool implementation*, không phải dependency/build/test evidence của repository để derive minimal coding-agent file authority; không báo cáo permission precision/recall hay task completion dưới minimal path policy.

Artifact URL/license: **UNVERIFIED** trong full-text metadata đã kiểm tra.

## Liên hệ

- [[synthesis/Prior-Art Threat: Agent Capability Control]]
- [[synthesis/Preliminary Gap: Software-Evidence-Grounded Capability Scoping]]
