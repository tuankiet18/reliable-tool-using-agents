---
title: "FAVA: Formal Authorization for Verified Agents with Evidence-Backed Permission Graphs"
category: references
tags: [paper, ai-agents, authorization, runtime-monitoring, formal-methods]
sources: [https://arxiv.org/abs/2607.27267]
summary: "FAVA dùng Permission IR, evidence-backed graph và SMT authorization để kiểm tra capability trước mỗi effectful action."
provenance: {extracted: 0.88, inferred: 0.07, ambiguous: 0.05}
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# FAVA

## Problem / method

FAVA cho rằng static tool permission không đủ cho data flow và state runtime. LLM chuyển natural-language task thành Permission IR; deterministic lowering tạo permission graph chứa dependencies, data flows và contextual labels. Trước mỗi effectful action, SMT authorizer tính capability được phép hoặc trả counterexample trace; gateway enforcement quyết định allow/intercept.

## Dynamic behavior và least privilege

Graph append observation/evidence đơn điệu ở runtime; established constraint không bị bỏ âm thầm. Encoding yêu cầu capability cần thiết và *softly minimize* capability còn lại. Vì vậy đây là counterexample mạnh cho generic “runtime evidence + formal authorization”, nhưng không chứng minh task-minimal policy trong coding repository. Các evidence graph là dataflow/context graph, không được mô tả là import/call/build/test dependency graph.

## Evaluation / artifacts

Paper đánh giá OpenAgentSafety, OctoBench và ActPlane scenarios; báo cáo aggregate DCR 90.5%, initialization overhead 8.75% và runtime gateway 0.3%. Trên arXiv full text không thấy code URL hay dataset release của FAVA: **UNVERIFIED artifact availability**. Paper là preprint tháng 07/2026; các kết quả chưa được peer review.

## Limitation và implication

FAVA là prior art trực tiếp chống lại claim quá rộng về task-aware runtime authorization. Nó có thể là threat cho GAP-B, nhưng evidence của source-code semantics và ground-truth *necessary permissions* vẫn không được paper này đánh giá rõ ràng.

## Liên hệ

- [[synthesis/Agent Capability and Permission Control]]
- [[synthesis/Prior-Art Threat - Agent Capability Control]]
