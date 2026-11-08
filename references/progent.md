---
title: "Progent: Securing AI Agents with Privilege Control"
category: references
tags: [paper, ai-agents, authorization, least-privilege, runtime-policy]
sources:
  - https://arxiv.org/abs/2504.11703
  - https://github.com/sunblaze-ucb/progent
summary: "Progent sinh policy tool/argument từ task, cập nhật theo execution context và buộc mọi privilege expansion phải được approver chấp thuận."
provenance: {extracted: 0.94, inferred: 0.05, ambiguous: 0.01}
base_confidence: 0.94
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# Progent

## Problem

Progent bảo vệ generic tool-using agent trước indirect prompt injection và hành động vượt thẩm quyền. Đây là **authorization runtime**, không phải chỉ là sandbox: policy biểu diễn allow/forbid ở mức tool name và typed arguments; mọi call không khớp allow rule bị chặn.

## Method và permission model

**FACT:** LLM tạo policy ban đầu từ user task. Sau mỗi tool return, một updater đề xuất policy mới từ task context, observation và policy trước đó. SMT solver xác định update là narrowing hay expansion. Narrowing được áp dụng tự động; expansion cần approver cấu hình (auto deny, auto approve, hoặc human review). Tác giả gọi guarantee này là *monotonic confinement*. Quyền có granularity tool và argument, không phải path-level filesystem. [[concepts/least-privilege-tool-use]]

## Dynamic behavior, evidence và human interaction

Có thay đổi policy trong runtime, gồm mở rộng và thu hẹp. Evidence là task ban đầu, tool return và policy hiện hành; expansion không được tự động biện minh bởi failure signal riêng. Human review kiểm tra policy ban đầu và mọi expansion trong cấu hình Manual Approval. Paper báo cáo chỉ 6% policy updates cần approval trong AgentDojo, nhưng đây không phải thử nghiệm tối ưu hoá risk tier hay human-load policy.

## Metrics / results

Trên AgentDojo, attack success rate giảm từ 39.9% xuống 1.0%; trên ASB giảm từ 70.3% xuống 3.9%, trong khi paper báo cáo utility được duy trì. Các baseline approver gồm Disable Update, Auto-Deny, Auto-Approve và Manual Approval. Đây là counterexample trực tiếp cho broad GAP-A/C/D.

## Assumptions và limitations

- User query là benign; observation sau đó có thể bị attacker kiểm soát. **FACT**
- Không bảo vệ hành vi xấu vẫn nằm trong least privilege của user task, hoặc text-only attack. **Author-stated.**
- Policy được LLM sinh; độ đúng semantic của permission boundary không được chấm bằng ground-truth minimal set như AuthBench. **INFERENCE.**
- Không dùng dependency/call/build graph của repository để suy ra file-level capability. **FACT về setting; INFERENCE về khoảng trống.**

## Artifact availability

Code và reproduction scripts được paper công bố tại https://github.com/sunblaze-ucb/progent. Paper là arXiv v3; cần kiểm tra license của repository trước khi tái sử dụng. Benchmark evaluation dùng AgentDojo và ASB; không cần huấn luyện cho core framework nhưng có model/API calls.

## Liên hệ

- [[synthesis/Agent Capability and Permission Control]]
- [[synthesis/Prior-Art Threat - Agent Capability Control]]
- [[synthesis/Preliminary Gap - Progressive Capability Expansion]]
