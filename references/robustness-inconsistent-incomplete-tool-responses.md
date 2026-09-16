---
title: "Robustness Analysis of Agentic AI to Inconsistent and Incomplete Tool Responses"
category: references
tags: [paper, ai-agents, tool-failure, failure-detection, verification]
sources: ["https://arxiv.org/abs/2608.22676"]
summary: >-
  Pilot study phân biệt incomplete và schema-valid inconsistent tool returns ngay tại return boundary bằng likelihood và next-action distributions, nhưng chưa chạy agent end-to-end hay nghiên cứu correlated failures.
provenance:
  extracted: 0.93
  inferred: 0.05
  ambiguous: 0.02
base_confidence: 0.94
lifecycle: draft
lifecycle_changed: 2026-09-13
tier: core
created: 2026-09-13T00:00:00Z
updated: 2026-09-13T00:00:00Z
---

# Robustness Analysis of Agentic AI to Inconsistent and Incomplete Tool Responses

## Problem

Paper hỏi liệu agent có biểu hiện tín hiệu khác nhau ngay khi nhận incomplete return hoặc well-formed false return hay không. Đây là bước **recognition/diagnosis**, không phải recovery policy.

## Method và signals

Tác giả inject fault vào retail customer-service setting và đọc hai signal từ Qwen3-8B:

1. likelihood của tool return dưới schema-only so với full trajectory prefix;
2. probability distribution trên 17 legal next actions.

## Main result

Incomplete returns có tín hiệu rõ trong schema likelihood. Inconsistent returns khó hơn: contradiction trực tiếp với value đã xuất hiện trong context có thể thấy được, còn contradiction cần suy luận qua domain policy thì yếu. Next-action distribution phản ánh mức fault ảnh hưởng quyết định kế tiếp hơn là phản ánh đúng fault family.

## Limitations

- Chỉ là qualitative pilot ở một decision point, không chạy agent tới final outcome.
- Một model, một domain, một số fault case nhỏ.
- Không có recovery intervention, cross-tool verification hay correlated/common-mode failure.
- Plausible wrong output không mâu thuẫn với prefix có thể không quan sát được bằng các signal này.

## Research implication

Paper bác bỏ claim “schema-valid wrong output chưa từng được nghiên cứu”. Tuy nhiên nó không trả lời cách chọn independent evidence source để verify khi nhiều tool có thể cùng sai.

## Related

- [[synthesis/Research: Early Failure Detection in Tool-Using Agents]]
- [[synthesis/Research: Correlated Silent Tool Failures and Verification]]

