---
title: >-
  MiniScope: A Least Privilege Framework for Authorizing Tool Calling Agents
category: references
tags: [paper, ai-agents, authorization, security, tool-use]
sources: [https://arxiv.org/abs/2512.11147]
source_url: https://arxiv.org/abs/2512.11147
summary: >-
  Framework 2025 tái dựng hierarchy quyền của tool và áp dụng least-privilege authorization kiểu mobile cho tool-calling agent; là prior art một phần cho progressive grants/confirmation.
provenance:
  extracted: 0.88
  inferred: 0.12
  ambiguous: 0.00
base_confidence: 1.00
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# MiniScope

> [!tldr] MiniScope minh họa authorization layer cụ thể cho tool agent không đáng tin cậy và báo cáo latency overhead thấp; đánh đổi security/utility khi runtime recovery cần đọc sâu hơn.

## Vấn đề, lý do quan trọng và phương pháp

Policy viết thủ công cần chuyên môn, còn confinement có LLM trong vòng lặp thiếu guarantee chặt chẽ. MiniScope tái dựng permission hierarchy giữa các tool call và kết hợp permission model kiểu mobile. Theo abstract, mục tiêu là minimize permissions mà vẫn cân bằng security, usability và operational cost.

## Dataset / metric / kết quả chính

Paper giới thiệu synthetic dataset từ mười ứng dụng thực tế và báo cáo latency overhead 1–6% so với vanilla tool calling, permission minimization cùng chi phí vận hành/tính toán tốt hơn LLM baseline.

## Dynamic behavior, human interaction và hạn chế

**FACT (metadata/full-text snippets đã kiểm tra):** MiniScope áp dụng confirmation ở tool call theo risk, do đó là prior art một phần cho progressive grants và human-in-the-loop. **?** Chưa đọc được artifact/repository chính thức để xác nhận đầy đủ policy update, expiration/revocation hoặc phép đo task-derived minimum authority; các mục này giữ trạng thái insufficient evidence.

## Hạn chế và phê bình cho research này

- Cách tạo task synthetic và chỉ mười ứng dụng có thể hạn chế generalization. ^[inferred]
- Không có evidence rằng paper đánh giá transient tool failure hoặc recovery-triggered privilege escalation; ToolPrivBench mới trực tiếp bao phủ condition này. ^[inferred]
- Artifact public/license chưa xác minh qua source chính thức. **UNVERIFIED.**

## Liên hệ với research này

- [[concepts/least-privilege-tool-use]]
- [[synthesis/Preliminary Gap: Failure-Aware Least Privilege]]
- [[synthesis/Prior-Art Threat: Agent Capability Control]]

## Sources

- <https://arxiv.org/abs/2512.11147>
