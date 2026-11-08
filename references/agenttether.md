---
title: >-
  AgentTether: Graph-Guided Diagnosis and Runtime Intervention for Reliable LLM Agent Operation
category: references
tags: [paper, ai-agents, diagnosis, recovery, runtime-monitoring]
sources: [https://arxiv.org/abs/2607.06273]
source_url: https://arxiv.org/abs/2607.06273
summary: >-
  Framework 2026 mô hình hóa agent run bằng transition graph có phụ thuộc, chẩn đoán critical subtrajectory và hướng dẫn rerun bằng repair memory.
provenance:
  extracted: 0.84
  inferred: 0.16
  ambiguous: 0.00
base_confidence: 1.00
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# AgentTether

> [!tldr] AgentTether là bằng chứng diagnosis-guided rerun có thể tốt hơn blind retry, nhưng đánh giá được báo cáo là repair sau thất bại trên benchmark/model cụ thể.

## Vấn đề và lý do quan trọng

Lỗi bề mặt có thể xuất hiện sau nguyên nhân thật; blind retry thiếu diagnosis và self-reflection có thể không đặt correction trên bằng chứng.

## Phương pháp

Run được chuyển thành Transition Units và Critical Transition Graph. Normal-behavior model kết hợp run-local graph detector định vị subtrajectory; framework biến diagnosis thành guidance theo phạm vi và có thể giữ Repair Memory qua rerun.

## Dataset / metric / kết quả chính

Trên 261 task τ-bench với Qwen3.7-max, paper báo cáo sửa được 49/83 Banking task thất bại ban đầu (59.04%); trong setting Banking cross-model, báo cáo 56/86 (65.12%). Paper cũng báo cáo ít turn/token hơn. Đây là kết quả do paper báo cáo, chưa được tái lập độc lập.

## Hạn chế và phê bình cho research này

- Đánh giá được báo cáo bắt đầu từ failed run; thời điểm can thiệp online và calibration cần đánh giá riêng. ^[inferred]
- Phương pháp phụ thuộc graph/model đủ nhiều nên tái lập trong ba tháng có thể rủi ro cao. ^[inferred]

## Paper này chưa giải quyết gì

Paper chưa xác lập recovery router tối thiểu, model-agnostic cho tool fault tạm thời so với kéo dài đã biết.

## Liên hệ với research này

- [[concepts/agent-observability-and-runtime-monitoring]]
- [[concepts/agent-recovery-policy]]
- [[synthesis/Preliminary Gap - Selective Recovery Routing]]
- [[synthesis/Deep Comparison - Recovery Routing Anchor Works]]

## Sources

- <https://arxiv.org/abs/2607.06273>
