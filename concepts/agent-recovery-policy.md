---
title: >-
  Agent Recovery Policy
category: concepts
tags: [ai-agents, recovery, runtime-monitoring, decision-making]
sources: [https://openreview.net/pdf/2be5795add6ec19f401efc71c99e69f5dea50e1c.pdf, https://openreview.net/pdf/f81b4d72b4ac58cbc7ec781bdc3f8e3c705d4650.pdf, https://arxiv.org/abs/2607.06273]
summary: >-
  Cách chọn lúc chạy giữa tiếp tục, retry, replan, rollback, escalation và dừng khi agent gặp rủi ro trong quá trình thực thi.
provenance:
  extracted: 0.48
  inferred: 0.52
  ambiguous: 0.00
base_confidence: 0.83
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: core
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# Chính sách phục hồi của AI Agent

`Agent Recovery Policy`

**FACT:** Failing Tools phân biệt lỗi tool được chèn vào là tạm thời và kéo dài; vì vậy retry và chiến lược thay thế cần khác nhau. [[references/agenttether]] báo cáo rerun có hướng dẫn từ chẩn đoán trên τ-bench; bối cảnh của nó đánh giá run đã thất bại, không phải một action router online đã được hiệu chỉnh.

**HYPOTHESIS:** Một router nhỏ bên ngoài, dựa trên trace, có thể chọn hành động phục hồi hiệu quả hơn policy “retry N lần” hoặc “luôn replan” khi tool gặp lỗi được chèn vào.

## Từ vựng quyết định

- **Continue:** tiếp tục khi chưa có tín hiệu rủi ro đủ để hành động.
- **Retry:** thử lại khi lỗi có vẻ tạm thời, an toàn và thao tác có tính idempotent.
- **Replan/fallback:** lập kế hoạch lại/dùng phương án thay thế khi capability, điều kiện tiên quyết hoặc khả dụng lâu dài đã thay đổi.
- **Rollback:** hoàn tác trước khi retry một tác động không idempotent.
- **Escalate/stop:** chuyển cho người xử lý/dừng khi không thể xác minh mục tiêu an toàn, hoặc chạm giới hạn ngân sách/quyền.

Hành động phục hồi đúng phụ thuộc vào tính kéo dài của lỗi, tác dụng phụ, lựa chọn thay thế và ngân sách còn lại—không chỉ phụ thuộc tool call trước đó có trả error hay không. ^[inferred]

## Câu hỏi mở

- Which low-cost trace signals support this routing across models and tasks?
- Does early intervention improve success enough to pay for monitoring and recovery calls?
- How should abstention/escalation be scored alongside success?
