---
title: >-
  Preliminary Gap: Completion Verification Under Degraded Tools
category: synthesis
tags: [research-gap, preliminary, ai-agents, verification, tool-failure]
sources: [https://arxiv.org/abs/2406.12045, https://arxiv.org/abs/2404.07972, https://openreview.net/pdf/2be5795add6ec19f401efc71c99e69f5dea50e1c.pdf]
summary: >-
  WEAK broad gap: generic independent/state verification đã có direct prior art; phần common-mode source dependency được chuyển sang một gap hẹp riêng.
provenance:
  extracted: 0.60
  inferred: 0.34
  ambiguous: 0.06
base_confidence: 0.80
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-13T00:00:00Z
---

# PRELIMINARY Gap: xác minh hoàn thành khi tool suy giảm

> [!warning] **Status: WEAK.** Broad completion/state verification đã có RIVA, deterministic gates và verified tool-call wrappers. Không dùng note này làm RQ chính.

**FACT:** τ-bench và OSWorld dùng đánh giá goal state/thực thi bên ngoài. Failing Tools có silent failure và stale output.

**Candidate hypothesis:** Verifier nhỏ kiểm tra action làm đổi state trước khi chấp nhận `DONE` có thể giảm false completion hiệu quả hơn chỉ đánh giá ở cuối.

**Evidence mới:** RIVA cross-validate nhiều diagnostic path; `Reason Less, Verify More` dùng deterministic pre-write state gates; `Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures` dùng postconditions và verify-before-retry. Vì vậy generic verifier wrapper không đủ novelty.

**Kiểm tra bác bỏ:** Chỉ ra evaluator benchmark có sẵn không thể dùng online, hoặc tìm công trình tương đương đo cùng đánh đổi false-completion/chi phí.

**Phần được chuyển sang gap hẹp:** [[synthesis/Preliminary Gap - Provenance-Aware Verification under Correlated Tool Failures]] hỏi liệu các verifier có cùng backend/failure domain nên cùng xác nhận sai hay không.
