---
title: "Automata from Agent Traces: Failure and Next-Step Prediction"
category: references
tags: [paper, ai-agents, failure-detection, runtime-monitoring, automata]
sources:
  - "https://arxiv.org/abs/2608.23670"
  - "https://seonglae-agentstategraph.hf.space/"
source_url: https://arxiv.org/abs/2608.23670
summary: >-
  Dùng finite-state machine tổng hợp từ nhiều trace để dự đoán next step và failure từ partial trace; đánh giá trên 12 public datasets.
provenance:
  extracted: 0.89
  inferred: 0.08
  ambiguous: 0.03
base_confidence: 0.91
lifecycle: draft
lifecycle_changed: 2026-09-12
tier: supporting
created: 2026-09-12T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# Automata from Agent Traces: Failure and Next-Step Prediction

## Problem và method

Paper gom execution traces thành một finite-state machine (FSM) chung, rồi dùng state/topology features cho next-step prediction và failure prediction. Monitor online xếp hạng risk từ partial trace và có thể early-stop trước completion.

## Evidence

Trên 12 public datasets, paper báo FSM chỉ có 7–43 states và replay held-out data với fitness ít nhất `0.997`. Failure predictor đạt held-out AUROC tối đa `0.941`; tại 50% trajectory, FSM features đạt khoảng 92% full-trace AUROC. Cross-model transfer trung bình được báo cáo `0.786` so với self-domain `0.877` trên các `τ²` suites.

## Hạn chế và artifact

- Broader cross-architecture/domain transfer vẫn là future work.
- Paper dùng trajectory outcomes và corpus topology, không tập trung riêng vào controlled tool-service faults.
- Project page công khai; repository/code chính thức chưa được xác minh trong search pass này.

## Novelty impact

Kết quả trực tiếp bác bỏ claim “dùng partial trajectory structure để dự đoán failure/early stop” là mới. Nếu nghiên cứu tiếp, cần một điều kiện failure và nguồn evidence mà FSM/prefix methods chưa quan sát được.

## Related

- [[synthesis/Research: Early Failure Detection in Tool-Using Agents]]
- [[references/prefixguard]]

