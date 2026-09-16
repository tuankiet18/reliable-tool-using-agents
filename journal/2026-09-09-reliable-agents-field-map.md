---
title: >-
  Research Log — Reliable Tool-Using Agents Field Map
category: journal
tags: [research-log, ai-agents, reliability, field-map]
sources: [https://arxiv.org/abs/2406.12045, https://arxiv.org/abs/2408.04682, https://arxiv.org/abs/2607.06273, https://openreview.net/pdf/2be5795add6ec19f401efc71c99e69f5dea50e1c.pdf]
summary: >-
  Vòng nghiên cứu đầu ghi nhận vòng đời độ tin cậy, sáu hướng, 21 nguồn seed và bốn gap sơ bộ mà chưa chọn đề tài luận văn.
provenance:
  extracted: 0.72
  inferred: 0.23
  ambiguous: 0.05
base_confidence: 0.86
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# Nhật ký nghiên cứu — Bản đồ AI Agent dùng tool đáng tin cậy

## Đã tìm kiếm gì

- Benchmark tool-agent-user; tool use có state; runtime tool failure/recovery.
- Failure forecasting, trajectory localization, runtime monitoring và diagnosis-guided repair.
- Completion verification, computer/coding agent dài hạn, least privilege và benchmark security.

Nguồn ưu tiên là arXiv/OpenReview/trang conference gốc và repository chính thức. Blog sản phẩm hay leaderboard không được coi là bằng chứng nghiên cứu chính.

## Đã học được gì

- Goal-state/execution evaluator đã có ở τ-bench và OSWorld; agent tự báo hoàn thành là không đủ.
- Fault persistence quan trọng: lỗi tạm thời làm retry hợp lý hơn, lỗi kéo dài cần fallback/replanning hoặc dừng.
- Benchmark trajectory mới cho thấy năng lực giảm rõ từ phát hiện tổng quát sang localization/diagnosis ở cấp bước.
- Diagnosis-guided repair và least-privilege authorization là hướng mới đang được nghiên cứu tích cực, không phải vùng trống.

## Điều chưa chắc chắn

- Failing Tools được tìm thấy dưới dạng PDF anonymous đang review; cần xác minh metadata cuối, code, license, số task và metric.
- Literature check chưa toàn diện; không gap PRELIMINARY nào là khẳng định novelty đã được xác thực.
- Khả năng so sánh trực tiếp AgentTether, failure forecasting và external monitoring với lightweight router chưa được xác minh.

## Hành động tiếp theo

Đọc sâu Failing Tools, adaptive task-failure forecasting và AgentTether song song theo paper deep-dive template; lập bảng so sánh về thời điểm can thiệp, tín hiệu quan sát, không gian recovery action, benchmark fault, baseline và khả dụng của artifact.
