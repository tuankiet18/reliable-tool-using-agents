---
title: >-
  Least-Privilege Tool Use
category: concepts
tags: [ai-agents, security, authorization, tool-use]
sources: [https://arxiv.org/abs/2512.11147, https://arxiv.org/abs/2606.20023, https://arxiv.org/abs/2605.14859, https://arxiv.org/abs/2406.13352]
summary: >-
  Chỉ cấp cho agent quyền cần thiết để hoàn thành tác vụ và ngăn leo thang quyền không cần thiết, đặc biệt khi tool gặp lỗi.
provenance:
  extracted: 0.73
  inferred: 0.27
  ambiguous: 0.00
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# Dùng tool theo đặc quyền tối thiểu

`Least-Privilege Tool Use`

**FACT:** [[references/miniscope]] đề xuất permission framework cho tool-calling agent. ToolPrivBench báo cáo việc chọn tool có quyền quá cao và leo thang quyền khi lỗi tạm thời; AuthBench đánh giá suy luận permission boundary ở mức file cho coding agent.

**INFERENCE:** Phục hồi sau lỗi làm thay đổi bài toán authorization: fallback có thể khôi phục utility nhưng mở rộng quyền của agent; metric recovery chỉ đo utility sẽ che đi đánh đổi về an toàn. ^[inferred]

## Câu hỏi mở

- Policy recovery có thể giữ least privilege mà không mất phần lớn khả năng phục hồi không?
- Runtime monitor có thể phân biệt fallback cần thiết với leo thang quyền chỉ vì tiện lợi không?
