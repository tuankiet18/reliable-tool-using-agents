---
title: "Correlated Errors in Large Language Models"
category: references
tags: [paper, reliability, verification, ensembles, failure-correlation]
sources:
  - "https://proceedings.mlr.press/v267/kim25e.html"
  - "https://arxiv.org/abs/2506.07962"
summary: >-
  ICML 2025 cho thấy model diversity không bảo đảm error independence; đây là evidence nền tảng cho common-mode verification risk nhưng không nghiên cứu tool outputs.
provenance:
  extracted: 0.96
  inferred: 0.03
  ambiguous: 0.01
base_confidence: 0.97
lifecycle: draft
lifecycle_changed: 2026-09-13
tier: supporting
created: 2026-09-13T00:00:00Z
updated: 2026-09-13T00:00:00Z
---

# Correlated Errors in Large Language Models

## Problem và setting

Paper ICML 2025 kiểm tra giả định rằng nhiều model khác nhau tạo ra independent evidence. Nghiên cứu hơn 350 LLM trên leaderboard data và resume screening.

## Main results

Trên một leaderboard dataset, khi hai model đều sai, chúng chọn cùng đáp án sai khoảng `60%` số trường hợp. Shared architecture và provider là các yếu tố liên quan tới error correlation; model lớn và chính xác hơn vẫn có correlated errors cao.

## Limitation đối với project này

Đối tượng là model predictions, không phải runtime tool outputs hay tool provenance. Vì vậy paper chỉ hỗ trợ nguyên lý “diversity bề ngoài không đồng nghĩa independence”, không phải direct prior art cho method đề xuất.

## Kết nối nền tảng

Knight và Leveson (1986) đã thực nghiệm phản bác giả định independence đơn giản trong multiversion programming. Hai nguồn cùng cảnh báo rằng redundancy chỉ có ích khi failure mechanisms đủ độc lập.

## Related

- [[references/riva]]
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]]

