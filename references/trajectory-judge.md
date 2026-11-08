---
title: "trajectory-judge: What Outcome-Only LLM Judges Miss on Agent Trajectories"
category: references
tags: [paper, benchmark, ai-agents, failure-detection, verification]
sources:
  - "https://arxiv.org/abs/2609.00038"
  - "https://github.com/mohammadi-hadi/trajectory-judge"
  - "https://doi.org/10.5281/zenodo.21797926"
source_url: https://arxiv.org/abs/2609.00038
summary: >-
  Deterministic tool environment và single-fault injector tạo ground truth silent/loud; step-rubric judge bắt silent faults tốt hơn outcome-only judge nhưng tốn chi phí hơn.
provenance:
  extracted: 0.94
  inferred: 0.04
  ambiguous: 0.02
base_confidence: 0.95
lifecycle: draft
lifecycle_changed: 2026-09-12
tier: supporting
created: 2026-09-12T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# trajectory-judge: What Outcome-Only LLM Judges Miss on Agent Trajectories

## Problem và method

Outcome-only judge có thể bỏ qua trajectory “đạt đáp án đúng bằng quy trình sai”. Artifact dùng deterministic support-desk environment, scripted oracle policy và single-fault injector để biết chính xác fault type, step và outcome có sống sót hay không.

## Ground truth và metrics

400 trajectories gồm 100 clean, 175 silent faults và 125 loud faults. Judges được đo detection, localization, type F1, calibration, false alarms, latency và cost. Vì scripted oracle luôn đúng trước injection, ground truth được tạo by construction, không cần human annotation.

## Main results

Paper/repository báo outcome-only Qwen2.5-14B có silent recall `0.451`, loud recall `0.840` và false-alarm rate `0.330`. Step-rubric judge cùng model đạt silent recall `0.766`, loud recall `0.984`, không false alarm trong sample nhưng tốn khoảng 3× latency. Programmatic rules có zero false alarm nhưng coverage silent thấp (`0.429`).

## Artifact và giới hạn

- Public code/raw verdicts, MIT license, DOI; mock demo/test chạy không cần API, real judge dùng local Ollama.
- Synthetic support-desk và fault distribution không ước lượng prevalence ngoài thực tế.
- Đây là full-trajectory judge comparison, không trực tiếp giải quyết early prefix prediction.

## Research implication

Artifact này cung cấp pattern tốt cho ground truth: tách `fault present` khỏi `outcome survived`, stratify silent/loud và luôn có programmatic baseline. Nó cũng cho thấy chỉ gọi LLM judge không tự động giải quyết semantic process violations.

## Related

- [[synthesis/Research - Early Failure Detection in Tool-Using Agents]]
- [[references/from-confident-closing-to-silent-failure]]

