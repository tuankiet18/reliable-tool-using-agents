---
title: "ProvenanceGuard: Source-Aware Factuality Verification for MCP-Based LLM Agents"
category: reference
tags: [ai-agents, verification, provenance, mcp, prior-art]
sources:
  - "https://arxiv.org/abs/2606.18037"
  - "https://github.com/aalvsz/provenanceguard"
created: 2026-09-15T15:34:48+07:00
updated: 2026-09-15T15:34:48+07:00
summary: >-
  Source-aware verifier cho MCP traces, phát hiện claim được gán sai nguồn; không đánh giá nguồn có đúng ngoài đời hay độc lập về failure domain.
---

# ProvenanceGuard: Source-Aware Factuality Verification for MCP-Based LLM Agents

## Problem

Một answer có thể được evidence pool hỗ trợ nhưng lại gán claim cho sai source. Paper gọi đây là `cross-source conflation`.

## Method và results

ProvenanceGuard giữ stable tool/source IDs, tách answer thành atomic claims, route từng claim về source-specific evidence, kiểm tra bằng NLI và token alignment, rồi đưa verdict ở claim và answer level. Trên 281 medical MCP-agent traces, paper báo held-out block F1 `0.802` và source accuracy `0.858`; ở multisource setting khó hơn, source-plus-relation accuracy giảm còn `0.229`.

## Giới hạn liên quan RQ hiện tại

- Đây là prior art trực tiếp cho **source-aware verification**.
- Nó kiểm tra claim có được source đã nêu hỗ trợ hay không; tác giả nói rõ không chứng minh source đúng về mặt clinical/scientific.
- System nhận source IDs có sẵn và fallback sang tool name khi thiếu; không xác minh source independence hoặc shared failure mechanism.
- Không inject correlated tool failures và không chọn một independent corroborator trước irreversible action.
- Repository công khai hiện chỉ có manuscript/citation; code và data chưa được release.

## Phân loại

`PARTIAL`: bác bỏ claim rộng “source-aware verification chưa được nghiên cứu”, nhưng không giải quyết RQ hẹp về correlated failure domains.

## Related

- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]]
- [[references/provenanceguard-misalignment-provenance-analysis]]

