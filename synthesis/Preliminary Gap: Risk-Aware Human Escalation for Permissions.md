---
title: "Preliminary Gap: Risk-Aware Human Escalation for Permissions"
category: synthesis
tags: [research-gap, preliminary, authorization, human-in-the-loop, security]
sources:
  - https://arxiv.org/abs/2504.11703
  - https://arxiv.org/abs/2606.20023
  - https://arxiv.org/abs/2606.02668
summary: "WEAK / PRELIMINARY: approval cho privilege expansion đã có trong Progent; chưa có evidence đủ cho một khoảng trống nhỏ và đo được về risk-tier routing."
provenance: {extracted: 0.76, inferred: 0.16, ambiguous: 0.08}
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: supporting
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# WEAK — Risk-Aware Human Escalation for Permissions

## Counterexample

[[references/progent]] có explicit approver module với Manual Approval cho initial policy và mọi expansion; nó đo các cấu hình auto-deny/auto-approve/manual và báo cáo approval frequency. Human gate theo risk/irreversibility cũng là pattern kỹ thuật phổ biến, không phải novelty tự thân.

## Chỗ chưa được chứng minh

**OPEN QUESTION:** Một routing policy có risk score, irreversibility và confidence/evidence để tối ưu *safety–utility–approval burden* có được đánh giá công bằng trên benchmark public hay chưa? Search pass chưa xác minh paper/benchmark trực tiếp; vì vậy không được nâng thành gap mạnh.

## Why weak

Không có ground truth đáng tin cho “khi nào human review thật sự thay đổi outcome”, và user-study/human approvals khó kiểm soát trong 12 tuần. `What You Approve Is What Executes` còn cho thấy consent UI integrity là vấn đề độc lập, có thể làm scope phình ra.

## Kết luận

**WEAK — PRELIMINARY.** Không phù hợp làm hướng chính hiện tại.
