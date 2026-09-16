---
title: "Do Coding Agents Understand Least-Privilege Authorization?"
category: references
tags: [paper, benchmark, coding-agents, authorization, least-privilege]
sources: [https://arxiv.org/abs/2605.14859]
summary: "AuthBench biến task-scoped file permission inference thành bài toán benchmark 120 terminal tasks với nhãn do người rà soát và validator thực thi."
provenance: {extracted: 0.95, inferred: 0.04, ambiguous: 0.01}
base_confidence: 0.95
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# Do Coding Agents Understand Least-Privilege Authorization?

## Problem

Paper định nghĩa **permission-boundary inference**: từ instruction và terminal environment, sinh whitelist POSIX read/write/execute theo path pattern *trước khi agent thực thi*. Mục tiêu là policy vừa đủ cho task (sufficiency) nhưng không mở bề mặt nhạy cảm không cần thiết (tightness).

## Benchmark, ground truth và metrics

**FACT:** AuthBench có 120 realistic terminal tasks (80 standard, 40 sensitive), lấy từ Terminal-Bench, SWE-Bench và OpenThoughts-TBLite; có human-reviewed permission specification cùng executable validator cho task utility và attack outcome. Metrics gồm task success rate (TSR), sensitive exposure rate (SER), attack success rate (ASR) và permission-axis F1.

Nhãn $S_{gold}$ là **static required-permission proxy được calibrate theo safe oracle execution**, không phải minimum policy phổ quát cho mọi execution agent. Đây là giới hạn trực tiếp của ground truth, do chính appendix nêu rõ.

## Method / main results

Sufficiency-Tightness Decomposition (STD) trước hết forward-simulate task/toolchain để lấy coverage policy, sau đó audit từng entry theo task grounding và sensitivity. Các model vừa under-grant execution-chain permissions vừa over-grant unused/sensitive permissions; tăng reasoning không giải quyết đồng thời hai lỗi. STD tăng sensitive-task TSR tối đa 15.8% trên tightness-biased models, giảm ASR trên các model thử nghiệm và tăng execute-axis F1 tối đa 16.7% ở standard tasks.

## What it does not solve

- Không có runtime expansion/revocation sau khi execution bắt đầu.
- Không so sánh bằng static program analysis như imports, call graph, build graph hoặc test dependency để suy ra scope.
- Paper trang arXiv không nêu artifact code/data public; phải coi reproducibility là **UNVERIFIED** cho tới khi tìm được repository chính thức.

## Research implication

AuthBench là counterexample trực tiếp cho broad **GAP-A — Task-Aware Permission Inference**. Nó đồng thời là benchmark tốt nhất hiện có để kiểm tra một variant coding-agent, nhưng proxy ground truth và không có dynamic phase khiến nó không tự chứng minh một nghiên cứu mới về runtime capability lifecycle.

## Liên hệ

- [[synthesis/Agent Capability and Permission Control]]
- [[synthesis/Preliminary Gap: Task-Aware Permission Inference]]
- [[synthesis/Preliminary Gap: Software-Evidence-Grounded Capability Scoping]]
