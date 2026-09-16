---
title: "PrefixGuard: From LLM-Agent Traces to Online Failure-Warning Monitors"
category: references
tags: [paper, ai-agents, failure-detection, runtime-monitoring, trajectories]
sources: ["https://arxiv.org/abs/2605.06455"]
source_url: https://arxiv.org/abs/2605.06455
summary: >-
  PrefixGuard học lightweight online warning monitor từ terminal outcomes và typed StepView; chỉ ra ranking tốt chưa chắc tạo alert hữu ích ở false-alarm thấp.
provenance:
  extracted: 0.91
  inferred: 0.07
  ambiguous: 0.02
base_confidence: 0.93
lifecycle: draft
lifecycle_changed: 2026-09-12
tier: core
created: 2026-09-12T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# PrefixGuard: From LLM-Agent Traces to Online Failure-Warning Monitors

## Problem

Từ raw execution trace và terminal outcome, học một monitor nhẹ chạy trên mỗi prefix để cảnh báo trước khi task kết thúc, không cần gọi LLM judge lúc deployment.

## Method và setting

`StepView` biến trace khác nhau thành typed step; monitor học event abstraction và prefix risk. Paper đánh giá trên WebArena, `τ²-Bench`, SkillsBench và TerminalBench. Positive warning window mặc định là `H=3` step gần failure point.

## Main results và critique

Paper báo AUPRC lần lượt `0.900/0.710/0.533/0.557` cho các benchmark. Nhưng chính first-alert analysis cho thấy AUPRC cao không đảm bảo can thiệp được: tại calibration FAR khoảng 10%, WebArena chỉ có early recall `0.007`, trong khi `τ²-Bench` là `0.192` và TerminalBench `0.178`.

**FACT:** label `H=3` chỉ đánh dấu cửa sổ ngay trước failure; nó không cố gắng xác định root-cause step sớm hơn. `t+T` là oracle có future information và chỉ dùng để audit confound, không dùng deployment.

**Research implication:** Không được chọn “50% trajectory” hoặc dùng final length để tạo feature online. Nên đánh giá first alert, false-alarm rate và lead time tại mỗi prefix quan sát được.

## Limitations

- Chỉ sinh warning monitor, không phải complete intervention policy.
- Failure phải để lại evidence trong observed prefix; paper đưa ra observability ceiling cho giới hạn này.
- Fixed horizon và FAR caps là evaluation controls, không phải quy luật tự nhiên.
- Public code chưa được xác minh trong pass này.

## Related

- [[synthesis/Research: Early Failure Detection in Tool-Using Agents]]
- [[references/real-time-detection-and-repair-agent-failures]]

