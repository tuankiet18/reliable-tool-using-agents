---
title: >-
  Preliminary Gap: Failure-Aware Least-Privilege Recovery
category: synthesis
tags: [research-gap, preliminary, ai-agents, authorization, recovery]
sources: [https://arxiv.org/abs/2512.11147, https://arxiv.org/abs/2606.20023, https://arxiv.org/abs/2605.14859]
summary: >-
  REJECTED: ToolPrivBench đã trực tiếp đánh giá privilege escalation sau transient failure và phương án mitigation.
provenance:
  extracted: 0.53
  inferred: 0.40
  ambiguous: 0.07
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# REJECTED — recovery có xét least privilege khi lỗi xảy ra

**FACT:** [[references/toolprivbench]] trực tiếp đo transient failure làm tăng escalation sang tool quyền cao, cho phép retry/switch/escalate/stop, và đánh giá privilege-aware post-training. [[references/progent]] cũng quản lý policy expansion theo runtime observation.

**KẾT LUẬN:** Broad claim “failure-aware least-privilege recovery” không còn là research gap; ToolPrivBench phủ đúng risk escalation sau transient failure. Một đổi tên policy hay thêm static permission layer không đủ tạo khác biệt.

**Điều còn hạn chế của ToolPrivBench:** simulation, tool độc lập đủ dùng, 5 turns và không có real side effects. Đây là limitation evaluation, **không tự tạo gap** cho 12-week project.

Xem [[synthesis/Prior-Art Threat: Agent Capability Control]] và [[synthesis/Preliminary Gap: Progressive Capability Expansion]].
