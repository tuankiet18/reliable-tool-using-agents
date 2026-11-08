---
title: "RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection"
category: references
tags: [paper, ai-agents, verification, tool-failure, reliability]
sources:
  - "https://arxiv.org/abs/2603.02345"
  - "https://doi.org/10.1145/3805621.3807644"
  - "https://github.com/microsoft/AIOpsLab"
summary: >-
  RIVA dùng nhiều diagnostic path để cross-validate tool output sai; hiệu quả dựa trên giả định các tool kiểm chứng đủ độc lập, nhưng paper không mô hình hóa correlated/common-mode failures.
provenance:
  extracted: 0.91
  inferred: 0.07
  ambiguous: 0.02
base_confidence: 0.93
lifecycle: draft
lifecycle_changed: 2026-09-13
tier: core
created: 2026-09-13T00:00:00Z
updated: 2026-09-13T00:00:00Z
---

# RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection

## Problem

RIVA nghiên cứu xác minh configuration drift bằng LLM agent khi observability tool có thể chạy thành công nhưng trả dữ liệu sai hoặc gây hiểu nhầm. Đây là **silent tool failure**, không phải exception rõ ràng.

## Setting và method

Hệ thống gồm `Verifier Agent`, `Tool Generation Agent` và `Tool Call History`. Với mỗi property trong IaC specification, agent tạo ít nhất `K` diagnostic path khác nhau, gọi tool và cross-validate kết quả trước khi kết luận.

Paper mô phỏng unreliable tools bằng cách sửa `get_logs`, `read_traces` và `read_metrics` để trả empty string trong AIOpsLab. Baseline là ReAct agent.

## Main results

- Khi có erroneous tool responses, paper báo average task accuracy tăng từ `27.3%` với ReAct lên `50.0%` với RIVA.
- Khi tool đúng, RIVA đạt `43.8%`, so với khoảng `28%` của ReAct.
- `K=2` hữu ích; `K=3` có thể làm accuracy giảm về `0%` vì AIOpsLab không luôn cung cấp đủ ba diagnostic path khác nhau.

## Assumption quan trọng

Paper nêu trực tiếp trực giác cốt lõi: nhiều **independent tools** khó cùng fail theo cùng một cách. Tuy nhiên “khác tool call” chưa chứng minh “khác failure domain”. Hai wrapper khác nhau có thể cùng đọc một API, cache, database replica hoặc telemetry pipeline.

## Limitations

### Author-stated / thể hiện trực tiếp trong evaluation

- AIOpsLab giới hạn số diagnostic path; tăng `K` có thể làm hệ thống không kết luận được.
- Fault injection chủ yếu là empty output, chưa bao phủ schema-valid plausible false values.
- Hệ thống sinh tool call bằng LLM nên chi phí và số step tăng.

### Limitation tôi suy ra

- `INFERENCE`: evaluation không thay đổi mức tương quan giữa tool failures và không kiểm tra common-mode failure.
- `INFERENCE`: diversity được operationalize chủ yếu bằng distinct diagnostic paths, không bằng provenance/dependency của data source.

## Artifact availability

- Paper: EuroMLSys 2026, DOI đã xác minh.
- Benchmark: AIOpsLab public, MIT license.
- RIVA implementation riêng: chưa tìm thấy public repository sau search theo tên hệ thống, tác giả và `Tool Call History`; đánh dấu `UNVERIFIED`.
- AIOpsLab yêu cầu Kubernetes/Helm và microservice environment, tương đối nặng cho project 12 tuần.

## Research implication

RIVA là prior art trực tiếp chống lại mọi claim chung kiểu “dùng nhiều tool để verify”. Phần chưa được paper kiểm tra là liệu lợi ích này còn tồn tại khi các tool **correlated** vì chia sẻ cùng failure domain hay không.

## Related

- [[synthesis/Research - Correlated Silent Tool Failures and Verification]]
- [[synthesis/Preliminary Gap - Provenance-Aware Verification under Correlated Tool Failures]]
- [[references/failing-tools]]

