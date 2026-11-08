---
title: "Preliminary Gap: Progressive Capability Expansion"
category: synthesis
tags: [research-gap, preliminary, authorization, runtime-policy]
sources:
  - https://arxiv.org/abs/2504.11703
  - https://arxiv.org/abs/2606.20023
  - https://arxiv.org/abs/2607.27267
summary: "REJECTED: Progent đã cập nhật policy runtime và kiểm soát expansion/narrowing; ToolPrivBench đã chấm escalation sau transient failure."
provenance: {extracted: 0.94, inferred: 0.05, ambiguous: 0.01}
base_confidence: 0.94
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# REJECTED — Progressive Capability Expansion

## Claim bị bác bỏ

“Bắt đầu hẹp, mở rộng dần theo runtime evidence, rồi thu hẹp/revoke” là broad direction đã có core components trực tiếp.

## Evidence

[[references/progent]] tạo policy theo task, update mỗi bước theo tool return, SMT phân loại expansion/narrowing, và chỉ cho expansion sau approval. [[references/fava]] duy trì authorization graph từ runtime dataflow/context. [[references/toolprivbench]] chấm escalation sau transient failure và huấn luyện policy chịu lỗi thay vì vội dùng tool quyền cao.

## Kết luận

**REJECTED.** Chưa xác minh toàn bộ combination của TTL/revocation token, nhưng thêm temporal implementation feature không đủ thành research gap khi central policy lifecycle đã được nghiên cứu trực tiếp.
