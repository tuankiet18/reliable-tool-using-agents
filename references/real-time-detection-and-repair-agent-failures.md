---
title: Real-Time Detection and Repair of LLM Agent Failures
category: references
tags: [paper, ai-agents, failure-detection, runtime-monitoring, reproducibility]
sources:
  - "https://arxiv.org/abs/2608.02464"
  - "https://github.com/sunnydubey1111/agent-trajectory-sentinel"
  - "https://huggingface.co/datasets/sunnydubey1111/agent-trajectory-sentinel"
source_url: https://arxiv.org/abs/2608.02464
summary: >-
  Prior art trực tiếp cho online failure detection: monitor causal từ step telemetry, deterministic verification và rollback/rerun; artifact CPU-only đã được kiểm tra cục bộ.
provenance:
  extracted: 0.91
  inferred: 0.07
  ambiguous: 0.02
base_confidence: 0.95
lifecycle: draft
lifecycle_changed: 2026-09-12
tier: core
created: 2026-09-12T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# Real-Time Detection and Repair of LLM Agent Failures

> [!tldr] Đây là prior art đe dọa mạnh nhất đối với đề tài “early failure detection từ execution trajectory”. Paper đã làm online monitoring, controlled fault injection, cross-corpus evaluation, cost-aware escalation và đóng vòng bằng rollback/rerun.

## Problem

Agent có thể lệch hướng giữa episode: lặp, cascade tool error, goal drift, grounding loss hoặc hấp thụ context bị hỏng. Câu hỏi là có thể báo động tại **thời điểm bắt đầu lệch hướng** chỉ từ tín hiệu quan sát được, với chi phí thấp hơn một LLM judge ở mỗi step hay không.

## Setting, failure model và tín hiệu

- Agent/tool setting gồm synthetic generator và 12 real-agent corpora qua nhiều framework/model.
- Năm lớp injection chính: `goal_drift`, `looping`, `tool_cascade`, `grounding_loss`, `context_corruption`.
- Monitor chỉ nhìn step telemetry: embedding của output, aggregate log-probability/uncertainty và action metadata như loại action, latency, output length, error flag.
- Dự đoán là causal: score tại step `t` chỉ dùng `x_1..x_t`.

## Method

Lớp một là one-class Echo State Network kết hợp CUSUM, fit chỉ trên healthy trajectories. Lớp hai là deterministic verification: tính lại kết quả từ tool outputs và kiểm tra các call bắt buộc. Khi gate báo lỗi, hệ thống rollback rồi rerun.

## Baselines và metrics

Baselines gồm memoryless Mahalanobis, delta-Mahalanobis, Isolation Forest, linear autoregression và GRU/LSTM/TCN. Metrics gồm detection tại false-alarm budget, steps saved, AUROC, latency/step, judge calls, repair success và task success.

## Main results

**FACT — do paper/artifact báo cáo:** trên 2,823 committed episodes, monitor chính đạt detection `0.71` tại false-alarm budget `5%`, AUROC `0.872`, khoảng `200 µs/step`. Ranking không retrain đạt AUROC `0.745` trên AFTraj-2K và `0.779` trên ATBench. Rollback/rerun phục hồi `45%` failure so với `16%` resampling control, nâng task success `52% → 73%` với khoảng một model call bổ sung mỗi run.

## Silent failure và generalization

- Completion/coverage verification bắt `7/7` silent aborts trong setting của paper.
- `context_corruption` và `goal_drift` tạo failure không chỉ dựa vào explicit exception.
- Tuy nhiên, **giá trị sai nhưng hợp schema và vẫn hợp lý về mặt bề ngoài** không thể nhận ra chỉ từ telemetry theo giả định của paper; cần external reference hoặc task-grounded invariant.
- Cross-corpus ranking có chuyển giao, nhưng cold transfer giữa deployment/model không tốt: paper báo AUROC `0.527` khi chuyển thẳng so với `0.885` sau target-side healthy recalibration.

## Limitation quan trọng cho research này

**FACT:** injected label trong data card biểu thị *fault exposure/onset*, không đồng nghĩa final task failure; organic labels lại dựa trên outcome. Trộn hai loại label sẽ làm sai bài toán dự đoán.

**INFERENCE:** Khoảng trống còn lại, nếu có, không thể chỉ là “dùng trajectory để dự đoán sớm”. Nó phải thêm nguồn evidence mà paper này không có, ví dụ semantic consistency với environment/reference để bắt schema-valid silent corruption, đồng thời kiểm tra cross-deployment calibration.

## Artifact và kiểm tra cục bộ

- Code/data: public; `LICENSE` trong repository là Apache-2.0.
- Yêu cầu Python 3.13+; study chính CPU-only, sequence baselines cần PyTorch tùy chọn.
- Kiểm tra ngày 2026-09-12 tại commit `1b3e07fee53ae13407173c3ea932adb4a43e8230`:
  - targeted offline tests: `89 passed`, `6 skipped`, `3 failed` vì môi trường tối giản thiếu optional `langchain_core`/`sqlalchemy` và live Ollama;
  - `run_experiment --quick --seed 99173`: hoàn tất trong `16.6s` trên CPU;
  - claims ledger: `121/121` claim khớp artifact;
  - behavior snapshot không khớp publication snapshot do không cài optional neural baselines và không dùng exact lockfile. Vì vậy đây là **smoke reproduction**, không phải tái lập chính xác headline numbers.

## Kết luận đối với gap

Paper này trực tiếp bác bỏ novelty của broad external runtime monitoring và controlled-trajectory early failure detection. Không nên xây một 20–30-task harness để lặp lại phần đã được artifact này thực hiện ở quy mô hàng nghìn episode.

## Related

- [[synthesis/Research - Early Failure Detection in Tool-Using Agents]]
- [[synthesis/Preliminary Gap - External Runtime Monitoring]]
- [[references/adaptive-fault-injection-task-failure-forecasting]]
- [[references/agentforesight]]

