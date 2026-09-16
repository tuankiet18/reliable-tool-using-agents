---
title: >-
  HINTBench: Horizon-agent Intrinsic Non-attack Trajectory Benchmark
category: references
tags: [paper, benchmark, ai-agents, diagnosis, long-horizon]
sources: [https://arxiv.org/abs/2604.13954]
source_url: https://arxiv.org/abs/2604.13954
summary: >-
  Benchmark trajectory 2026 cho detection, định vị bước và nhận diện chi tiết intrinsic non-attack risk ở agent dài hạn.
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
base_confidence: 1.00
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# HINTBench

> [!tldr] HINTBench tách việc gắn cờ trajectory rủi ro tương đối dễ khỏi việc khó hơn nhiều là định vị và chẩn đoán critical step.

## Vấn đề và lý do quan trọng

Đánh giá an toàn agent thường nhấn mạnh external attack, dù unsafe trajectory vẫn có thể xuất hiện trong setting lành tính và lan truyền trong thực thi dài.

## Dataset / benchmark

629 trajectory (523 risky, 106 safe), trung bình 33 bước, với task risk detection, risk-step localization và failure-type identification.

## Kết quả chính

Tác giả báo cáo LLM mạnh phát hiện rủi ro tốt ở cấp trajectory nhưng strict F1 vẫn dưới 35 cho risk-step localization; guard model transfer kém.

## Hạn chế và phê bình cho research này

- Đây là risk-auditing benchmark, không phải môi trường tool-failure recovery. ^[inferred]
- Task và risk taxonomy cần kiểm tra trước khi suy rộng kết quả sang độ tin cậy API-agent. ^[inferred]

## Liên hệ với research này

- [[concepts/agent-observability-and-runtime-monitoring]]
- [[synthesis/Preliminary Gap: External Runtime Monitoring]]

## Sources

- <https://arxiv.org/abs/2604.13954>
