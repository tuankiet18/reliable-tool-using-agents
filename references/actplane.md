---
title: "ActPlane: Programmable OS-Level Policy Enforcement for Agent Harnesses"
category: references
tags: [paper, coding-agents, authorization, os-security, runtime-policy]
sources:
  - https://arxiv.org/abs/2606.25189
  - https://github.com/eunomia-bpf/ActPlane
summary: "ActPlane để agent cụ thể hoá policy có ngữ cảnh task và cưỡng chế system actions ở OS kernel bằng eBPF/IFC."
provenance: {extracted: 0.90, inferred: 0.08, ambiguous: 0.02}
base_confidence: 0.90
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: supporting
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# ActPlane

## Relevance

ActPlane không tối ưu least-privilege set. Nó giải quyết khoảng cách giữa natural-language behavioral policy và system actions mà tool-call guardrail có thể bỏ sót (subprocess, shell-out). Agent dùng task/repository context để cụ thể hoá DSL; eBPF + information-flow control cưỡng chế ở OS và trả semantic feedback khi block.

## Evidence / evaluation

Paper khảo sát 64 projects, đánh giá policy từ empirical study, coding-task benchmarks và safety benchmarks. Paper báo cáo 1.9–8.4% overhead; search metadata chỉ ra code tại https://github.com/eunomia-bpf/ActPlane. Cần kiểm tra environment/kernel/version và license trước reproduce.

## Why it threatens GAP-B

Nó đã kết nối agent context với OS-level enforcement trong coding harness. Tuy nhiên, nó không được mô tả là tự suy ra *minimal file/tool capability set* từ dependency graph, cũng không dùng permission precision/recall hoặc over-privilege metric. Vì thế nó phủ enforcement, không tự phủ narrow scoping hypothesis.

## Liên hệ

- [[synthesis/Preliminary Gap: Software-Evidence-Grounded Capability Scoping]]
- [[synthesis/Prior-Art Threat: Agent Capability Control]]
