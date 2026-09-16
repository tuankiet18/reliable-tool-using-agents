---
title: "When Lower Privileges Suffice: Investigating Over-Privileged Tool Selection in LLM Agents"
category: references
tags: [paper, benchmark, ai-agents, least-privilege, tool-use]
sources:
  - https://arxiv.org/abs/2606.20023
  - https://github.com/AISafetyHub/agent-tool-selection-bias
  - https://huggingface.co/datasets/BAAI/ToolPrivBench
summary: "ToolPrivBench đo việc agent chọn hoặc escalation sang tool quyền cao dù tool quyền thấp đủ dùng, kể cả sau transient failure."
provenance: {extracted: 0.95, inferred: 0.04, ambiguous: 0.01}
base_confidence: 0.95
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# When Lower Privileges Suffice / ToolPrivBench

## Problem và setting

Paper nghiên cứu *over-privileged tool selection*: agent dùng risk tool quyền rộng khi standard tool quyền thấp vẫn đủ để hoàn thành. Setting là simulation-based generic tool agent, gồm 544 scenarios, 8 domains, 5 risk types; coding chiếm 12.3% scenarios nhưng không phải coding benchmark có repository thật.

## Failure model, action space và ground truth

Ba standard tool và ba risk tool cùng được tạo để độc lập đủ dùng. Standard tool có thể trả transient, privilege-unrelated error. Sau đó agent có thể retry standard tool, switch standard tool, escalate sang risk tool hoặc stop; horizon là 5 turns. Ground truth dựa vào human validation của functionality/independent sufficiency và privilege schema L1–L5; do đó chấm được preferential escalation, không chấm minimum filesystem/API policy cho workflow thực tế.

## Metrics / evidence

OPUR@k là tỷ lệ dùng high-privilege tool khi lower-privilege sufficient alternatives chưa bị loại trừ; PED là số lower-privilege tool đã thử trước escalation. Sáu trên mười một model vượt 30% OPUR; transient failure làm escalation tăng. Privilege-aware SFT + GRPO huấn luyện agent chịu transient failure và chỉ escalation sau low-privilege exploration; Qwen3-8B OPUR xuống 27.02%. Đây là counterexample trực tiếp cho failure-aware escalation dưới tool failure.

## Limitations

**Author-stated:** tool là simulation, substitutable và independently sufficient; chưa có live production tool, partial overlap, multi-tool workflows hay trajectory dài hơn 5 turns. Không cấp/revoke capability token; agent chọn giữa tool đã present. Không chấm human escalation, cost/side-effect thực thi thật hoặc policy scope theo argument/path.

## Artifact availability / feasibility

Public GitHub cung cấp evaluation scripts; Hugging Face công bố data JSONL 544 scenarios / 3,264 tool descriptions. Không cần GPU nếu chỉ evaluate fixed policies hay prompting; proposed defense của paper cần SFT+GRPO nên không hợp 12 tuần nếu tái huấn luyện. Kiểm tra LICENSE trước reuse là bắt buộc.

## Liên hệ

- [[synthesis/Preliminary Gap: Progressive Capability Expansion]]
- [[synthesis/Prior-Art Threat: Agent Capability Control]]
- [[concepts/least-privilege-tool-use]]
