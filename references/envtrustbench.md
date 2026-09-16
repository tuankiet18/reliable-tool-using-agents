---
title: "When Agents Overtrust Environmental Evidence: An Extensible Agentic Framework for Benchmarking Evidence-Grounding Defects in LLM Agents"
category: reference
tags: [ai-agents, benchmark, verification, tool-failure, prior-art]
sources:
  - "https://arxiv.org/abs/2605.08828"
  - "https://github.com/EnvTrustBench/EnvTrustBench"
created: 2026-09-15T15:34:48+07:00
updated: 2026-09-15T16:27:33+07:00
summary: >-
  EnvTrustBench đo việc agent tin sai evidence từ file, log, API và command output; rất phù hợp làm external-validity gate nhưng artifact công khai hiện chưa đủ cho reproduction đầy đủ.
---

# When Agents Overtrust Environmental Evidence: An Extensible Agentic Framework for Benchmarking Evidence-Grounding Defects in LLM Agents

## Problem

Agent có thể coi environmental evidence bị stale, sai hoặc malicious là đủ căn cứ để hành động và đi theo false path. Paper gọi lỗi này là evidence-grounding defect.

## Benchmark

Mỗi case có initial workspace, evidence configuration, task objective, true environment state, correct/false path, verification opportunity và machine oracle. Báo cáo hiện có 55 cases thuộc 11 scenarios, 14 model–scaffold stacks và 3,850 accepted runs; aggregate false-path/environmental-misgrounding rate là `83.3%`.

## Liên quan RQ hiện tại

- Đây là evidence trực tiếp rằng incorrect tool/environment observations là realistic reliability problem.
- Trajectory và final state được chấm bằng oracle, phù hợp hơn LLM judge.
- Benchmark không mô hình hóa redundant sources theo failure domain, không inject shared-backend common-mode faults và không so sánh source-selection policies.

## Artifact gate — result

Gate tại commit `0763e9cf3da33076c103f69bf049172752c0bad5` đã `FAIL`. GitHub repository dùng MIT license; Hugging Face dataset card ghi `cc-by-nc-nd-4.0`. Cả hai chỉ public project docs và aggregate results. Full Git history không chứa case generator, oracle implementation, executable `W0/E0/q/Omega`, raw traces hay runner.

Public CSV đủ để tái tính `3,206/3,850 = 83.27%`, khớp `83.3%` sau rounding. Nó không đủ để chạy một official machine-oracle case.

## Research implication

EnvTrustBench vẫn là motivation tốt, nhưng bị loại khỏi vai trò executable external benchmark tại thời điểm này. Không tự dựng lại case từ hình minh họa rồi gọi đó là reproduction. Xem [[journal/2026-09-15-external-validity-artifact-gate]].

## Related

- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]]
- [[synthesis/Research: Correlated Silent Tool Failures and Verification]]
