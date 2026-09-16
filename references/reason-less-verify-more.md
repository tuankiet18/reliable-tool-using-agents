---
title: "Reason Less, Verify More: Deterministic Gates Recover a Silent Policy-Violation Failure Mode in Tool-Using LLM Agents"
category: references
tags: [paper, ai-agents, verification, tool-use, reliability]
sources: ["https://arxiv.org/abs/2607.07405"]
summary: >-
  Bốn deterministic pre-execution gates ngăn silent wrong-state writes trong tau2-bench airline, nhưng chỉ xử lý policy decidable từ current state và chưa giải quyết unreliable read sources.
provenance:
  extracted: 0.94
  inferred: 0.04
  ambiguous: 0.02
base_confidence: 0.95
lifecycle: draft
lifecycle_changed: 2026-09-13
tier: supporting
created: 2026-09-13T00:00:00Z
updated: 2026-09-13T00:00:00Z
---

# Reason Less, Verify More: Deterministic Gates Recover a Silent Policy-Violation Failure Mode in Tool-Using LLM Agents

## Problem

Trong policy-permissive environment, write tool có thể chấp nhận syntactically valid action dù action vi phạm policy. Agent tưởng task đã xong nhưng final state sai.

## Method và results

Bốn deterministic read-only gate kiểm tra proposed write và current state trước execution. Trên `tau2-bench` airline với gpt-4o-mini, paper báo success tăng từ `29.6%` lên `42.0%`; trên 26/50 task nơi gate thực sự fire, mức tăng là `+19.2pp`.

## Limitations

- Một positive domain; một gate tạo phần lớn gain.
- Gate ngăn action nhưng không bảo đảm agent recover.
- Chỉ áp dụng khi policy có thể quyết định từ state quan sát được.
- Không kiểm tra trường hợp current state/tool read chính nó đã bị silent corruption.
- Code chỉ được hứa release khi publication; artifact hiện `UNVERIFIED`.

## Research implication

Generic state-invariant gate không còn là novelty. Nhưng paper vô tình làm rõ trust boundary: nếu gate và agent đọc cùng corrupted source, deterministic rule cũng có thể xác nhận sai.

## Related

- [[references/tau-bench]]
- [[synthesis/Research: Correlated Silent Tool Failures and Verification]]

