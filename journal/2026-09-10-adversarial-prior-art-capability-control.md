---
title: "2026-09-10 — Adversarial prior-art search: capability control"
category: journal
tags: [research-log, prior-art, authorization, ai-agents]
sources:
  - https://arxiv.org/abs/2504.11703
  - https://arxiv.org/abs/2605.14859
  - https://arxiv.org/abs/2606.20023
  - https://arxiv.org/abs/2607.27267
summary: "Search adversarial bác bỏ task-aware inference và progressive expansion broad; software-evidence scoping còn điều kiện nhưng chưa đủ evidence."
provenance: {extracted: 0.85, inferred: 0.12, ambiguous: 0.03}
base_confidence: 0.90
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# Research log — Capability control adversarial search

## Đã tìm

Tìm theo `least privilege`, authorization, capability control, dynamic/progressive permissions, just-in-time access, human approval, coding-agent sandbox và software dependency evidence; ưu tiên 2024–2026. Đọc full HTML các paper AuthBench, Progent, ToolPrivBench, FAVA khi có; kiểm tra public repository/dataset của Progent và ToolPrivBench.

## Đã học được

- AuthBench trực tiếp formalize task-scoped file permission inference và có human-reviewed proxy + executable validation.
- Progent đã tạo/update policy runtime, formal-check expansion/narrowing, human approval và MCP integration.
- ToolPrivBench đã chấm privilege escalation sau transient failure; đây là lý do không được hồi sinh Failure-Aware Least-Privilege Recovery.
- FAVA và ActPlane cho thấy runtime/formal/OS enforcement là lane đông, không phải khoảng trống tính năng.

## Uncertainties

- AuthBench artifact public chưa được xác minh từ nguồn chính thức.
- FAVA artifact chưa thấy URL chính thức; coi là **UNVERIFIED**.
- Chưa xác minh exhaustively rằng không có paper dùng dependency/call/build/test graph để tạo và đánh giá minimal R/W/X scope; do đó GAP-B chỉ preliminary.
- “Minimum required permission” phụ thuộc execution agent; proxy phải nêu rõ oracle/reference trace.

## Next single action

Làm **artifact-and-method audit** cho AuthBench: tìm source/data/license, chạy hoặc đọc validator của 10–20 tasks, rồi xác định liệu permission labels có thể mở rộng bằng counterfactual removal và repository static evidence hay không. Không thiết kế hệ thống trước gate này.

## Status

GAP-A **REJECTED**; GAP-B **SURVIVES WITH REFINEMENT — PRELIMINARY**; GAP-C **REJECTED**; GAP-D **WEAK — PRELIMINARY**. Chưa tạo candidate RQ: evidence và reproducibility chưa đủ.
