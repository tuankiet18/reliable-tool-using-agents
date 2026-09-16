---
title: >-
  Failing Tools: Benchmarking LLM Agent Recovery Under Runtime Tool Failures
category: references
tags: [paper, benchmark, ai-agents, recovery, tool-failure]
sources: [https://openreview.net/pdf/2be5795add6ec19f401efc71c99e69f5dea50e1c.pdf]
source_url: https://openreview.net/pdf/2be5795add6ec19f401efc71c99e69f5dea50e1c.pdf
summary: >-
  Benchmark đang review, chèn lỗi service thực tế và phân biệt lỗi tạm thời/kéo dài để đánh giá recovery trajectory.
provenance:
  extracted: 0.87
  inferred: 0.08
  ambiguous: 0.05
base_confidence: 1.00
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: core
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# Failing Tools

> [!tldr] Đây là benchmark ứng viên giá trị cao vì đo recovery thay vì tool calling lý tưởng; tình trạng xuất bản và artifact vẫn phải xác minh.

## Vấn đề và lý do quan trọng

Function-calling benchmark lý tưởng không kiểm tra agent nhận ra, suy luận và phục hồi từ tool suy giảm như thế nào.

## Setting và phương pháp

Paper mô tả service API mô phỏng với outage, stale output, schema inconsistency và silent failure. Lỗi có thể tạm thời hoặc kéo dài; staged tool disclosure kiểm soát thời điểm fallback tool được nhìn thấy.

## Metric và kết quả chính

Phần tài liệu đã trích xuất xác lập được đánh giá recovery có kiểm soát, nhưng chưa đủ bảng số liệu đã xác minh. **OPEN QUESTION:** phải lấy manuscript cuối, repository, license, số task và metric chính xác trước khi chọn làm benchmark dự án.

## Giả định và hạn chế

- Fault được chèn, dù đại diện cho production, vẫn có thể khác incident service thật. ^[inferred]
- Nguồn ở vòng đầu là PDF anonymous đang review, nên claim còn provisional đến khi metadata/artifact được xác minh. ^[ambiguous]

## Paper này chưa giải quyết gì

Phần trích xuất hiện có chưa xác lập policy chọn action đã hiệu chỉnh có tốt hơn recovery cố định qua các điều kiện fault persistence và tác dụng phụ hay không.

## Liên hệ với research này

- [[concepts/agent-recovery-policy]]
- [[synthesis/Preliminary Gap: Selective Recovery Routing]]
- [[synthesis/Deep Comparison: Recovery Routing Anchor Works]]

## Sources

- <https://openreview.net/pdf/2be5795add6ec19f401efc71c99e69f5dea50e1c.pdf>
