---
title: "When Evidence is Sparse: Weakly Supervised Early Failure Alerting in Dialogs and LLM-Agent Trajectories"
category: references
tags: [paper, ai-agents, failure-detection, weak-supervision, early-stopping]
sources: ["https://arxiv.org/abs/2606.05414"]
source_url: https://arxiv.org/abs/2606.05414
summary: >-
  Học early alert từ trajectory-level outcome khi failure evidence thưa và xuất hiện muộn; tối ưu trực tiếp trade-off accuracy–earliness.
provenance:
  extracted: 0.91
  inferred: 0.07
  ambiguous: 0.02
base_confidence: 0.92
lifecycle: draft
lifecycle_changed: 2026-09-12
tier: core
created: 2026-09-12T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# When Evidence is Sparse: Weakly Supervised Early Failure Alerting in Dialogs and LLM-Agent Trajectories

## Problem

Trong nhiều dataset chỉ có nhãn success/failure cho toàn trajectory, nhưng monitor phải cảnh báo từ partial history. Gán terminal failure label cho mọi prefix tạo label noise vì bằng chứng thực sự thường thưa và đến muộn.

## Method

Attention-based multiple-instance learner tìm turn chứa failure evidence từ trajectory label. `α-STOP` là stopping policy nhận preference để chọn điểm trên trade-off accuracy–earliness mà không train lại cho từng operating point.

## Evidence

Trên năm benchmark gồm AppWorld và ALFWorld, paper báo failure evidence chỉ tập trung ở `4.7–11.3%` số turn và lần đầu xuất hiện trung bình sau `59.0–83.6%` trajectory. Hệ thống cải thiện Pareto-frontier hypervolume `3–42%` so với state-of-the-art trigger policies.

## Limitations và research implication

- New deployment domain có thể cần refit lightweight heads.
- Turn relevance được LLM judge đánh giá hồi cứu, không phải causal ground truth.
- Code/prompts/splits được hứa release khi publication; public artifact chưa được xác minh trong pass này.

**Kết luận:** trade-off “cảnh báo sớm hay chính xác” và weak terminal labels đã được nghiên cứu trực tiếp. Đây không còn là novelty claim phù hợp cho undergraduate project.

## Related

- [[synthesis/Research - Early Failure Detection in Tool-Using Agents]]
- [[references/prefixguard]]

