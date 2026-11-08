---
title: "GRADE: Graph Representation of LLM Agent Dependency and Execution"
category: reference
tags: [ai-agents, observability, failure-detection, dependency, prior-art]
sources:
  - "https://arxiv.org/abs/2606.22741"
  - "https://github.com/yzhao062/grade"
created: 2026-09-15T15:34:48+07:00
updated: 2026-09-15T15:34:48+07:00
summary: >-
  GRADE biểu diễn execution và dependency edges, ghi rõ edge là observed/declared/inferred; trực tiếp đe dọa claim rằng dependency metadata chưa được kiểm định.
---

# GRADE: Graph Representation of LLM Agent Dependency and Execution

## Problem và method

Execution trace cho biết bước nào đã chạy nhưng thường không ghi bước đó phụ thuộc state/evidence nào. GRADE biểu diễn agent run bằng execution edges và dependency edges; mỗi dependency edge được đánh dấu theo evidence quality: `observed`, `declared` hoặc `inferred`.

## Evidence

Paper đánh giá trên sáu corpora gồm tool-use, coding và web agents. Dependency features hỗ trợ failure prediction và execution layer hỗ trợ localization. Đáng chú ý, paper dùng controls để kiểm tra liệu inferred attachments có thực sự chứa structure hữu ích; một số inferred features transfer kém hoặc collapse.

## Artifact

Code công khai tại `yzhao062/grade`, license MIT; core stack tương đối nhẹ (`Python`, `networkx`), dù tái lập toàn bộ corpora/model results vẫn có thể tốn chi phí.

## Liên quan RQ hiện tại

- Broad claim “agent dependency metadata luôn được nhận như ground truth và chưa ai grade/validate” bị bác bỏ.
- GRADE phân tích **step dependency**, không phải backend/source failure-domain equivalence.
- Nó dùng graph cho prediction/localization, không chọn corroborator trước irreversible action và không đánh giá common-mode tool corruption.

## Phân loại

`PARTIAL`: prior art mạnh cho metadata provenance/quality, adjacent chứ chưa same problem.

## Related

- [[synthesis/Prior-Art Threat - Provenance Metadata and Source Selection]]
- [[references/agentflow-agent-dependency-graphs]]

