---
title: "Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures"
category: references
tags: [paper, software-engineering, tool-failure, verification, reliability]
sources: ["https://arxiv.org/abs/2608.02645"]
summary: >-
  Verification-aware wrapper dùng postcondition, verify-before-retry và idempotency để giảm duplicate side effects dưới non-atomic failures; postcondition vẫn phải được thiết kế theo domain.
provenance:
  extracted: 0.91
  inferred: 0.07
  ambiguous: 0.02
base_confidence: 0.92
lifecycle: draft
lifecycle_changed: 2026-09-13
tier: supporting
created: 2026-09-13T00:00:00Z
updated: 2026-09-13T00:00:00Z
---

# Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures

## Problem

Tool call ngoài thực tế không luôn atomic: request có thể đã được dispatch nhưng client timeout, state có thể cập nhật một phần hoặc update chưa nhìn thấy ngay. Retry mù có thể tạo duplicate side effects.

## Method

Paper thêm wrapper gồm:

- postcondition verification trên state sau call;
- verify-before-retry;
- idempotency key.

Verifier trả `true`, `false` hoặc `unknown`, sau đó wrapper quyết định có retry hay không.

## Evaluation và limitation

Evaluation dùng hai simulated workflows với injected non-atomic failures và cho thấy duplicate actions giảm trong khi task success tương đương. Tuy nhiên postcondition chứa domain knowledge và không tự suy ra được chỉ từ API signature; paper cũng không lựa chọn evidence source theo provenance hoặc kiểm tra common-mode wrong returns.

## Research implication

Paper là prior art trực tiếp cho state/postcondition verification. Vì vậy RQ mới không được tuyên bố “thêm postcondition vào tool call”; điểm phân biệt phải nằm ở **dependency-aware evidence selection under correlated silent failures**.

## Related

- [[concepts/agent-verification-and-premature-completion]]
- [[synthesis/Research - Correlated Silent Tool Failures and Verification]]

