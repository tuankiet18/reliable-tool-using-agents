---
title: "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents"
category: references
tags: [paper, ai-agents, false-success, verification, failure-detection]
sources: ["https://arxiv.org/abs/2606.09863"]
source_url: https://arxiv.org/abs/2606.09863
summary: >-
  Phân tích false success trên tau2-bench và AppWorld; lightweight task-disjoint detector vượt LLM judges nhưng cross-domain vẫn cần calibration.
provenance:
  extracted: 0.93
  inferred: 0.05
  ambiguous: 0.02
base_confidence: 0.94
lifecycle: draft
lifecycle_changed: 2026-09-12
tier: supporting
created: 2026-09-12T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents

## Problem

Agent tuyên bố đã hoàn thành nhưng environment state cho thấy task thất bại—một dạng **thất bại im lặng (silent failure)** hay `false success`.

## Setting và ground truth

Paper phân tích 9,876 `tau2-bench` trajectories từ 8 model families và 1,879 AppWorld trajectories từ 4 model families. Nhãn dùng text-independent environment ground truth, không tin vào lời tự báo của agent.

## Main results

Paper báo false success chiếm `45–48%` failures trong single-control `tau2-bench` domains, `3%` ở dual-control telecom và `75.8%` trong AppWorld self-assessing trajectories có explicit status claims. Không LLM judge configuration nào vượt AUROC `0.65` trên `tau2-bench` hoặc `0.54` trên AppWorld. TF-IDF detector đạt task-disjoint AUROC `0.83` và `0.95`, với latency thấp hơn khoảng 3,300×.

## Limitation và research implication

Đây chủ yếu là false-success detection/triage gần hoặc sau completion, không phải controlled tool-output corruption prediction trước onset. Cross-domain transfer giảm và cần calibration.

**Kết luận:** “silent failure chưa được nghiên cứu” là claim sai. Phần có thể còn mở phải cụ thể hơn: schema-valid tool value sai về semantics tại runtime và không có text/state completion cue.

## Related

- [[concepts/agent-verification-and-premature-completion]]
- [[synthesis/Research - Early Failure Detection in Tool-Using Agents]]

