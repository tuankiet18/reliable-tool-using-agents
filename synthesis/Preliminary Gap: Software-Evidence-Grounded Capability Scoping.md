---
title: "Preliminary Gap: Software-Evidence-Grounded Capability Scoping"
category: synthesis
tags: [research-gap, preliminary, coding-agents, authorization, program-analysis]
sources:
  - https://arxiv.org/abs/2605.14859
  - https://arxiv.org/abs/2606.25189
  - https://arxiv.org/abs/2607.27267
summary: "PRELIMINARY / SURVIVES WITH REFINEMENT: chưa xác minh prior art đo liệu evidence software độc lập cải thiện tight task-scoped scope cho coding agent."
provenance: {extracted: 0.62, inferred: 0.28, ambiguous: 0.10}
base_confidence: 0.68
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: supporting
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# PRELIMINARY — Software-Evidence-Grounded Capability Scoping

## Gap statement hẹp

**HYPOTHESIS, chưa xác minh:** Với coding task, kết hợp evidence tĩnh có thể kiểm tra được (repository dependency/build/test graph) với task text sẽ sinh hoặc audit file-level R/W/X scope *tighter* hơn task-only inference, trong khi giữ utility trên cùng reference execution.

Đây **không** phải claim về “dynamic permissions”, sandbox hay policy engine.

## Strongest counterexamples

- [[references/authbench]] đã task-infer file R/W/X policy và STD forward-simulates toolchain. Nó là overlap trực tiếp ở output/metric, nhưng paper không mô tả imports, call graph, build graph hay test dependency là evidence độc lập.
- [[references/actplane]] dùng project/task context để cụ thể hoá OS policy và enforce cross-event actions; không tối ưu permission scope hay chấm permission precision/recall.
- [[references/fava]] xây graph của dataflow/dependency/context để runtime authorize; không đánh giá repository static analysis hay canonical minimum file scope.

## Why current methods may be insufficient

**INFERENCE:** AuthBench cho thấy task-only LLM policy sinh đồng thời under-grant và over-grant. Nhưng chưa có bằng chứng đầy đủ rằng program analysis giải được lỗi này; dependency graph có thể over-approximate, thiếu reflection/code generation, hoặc mở rộng scope quá mức.

## What could invalidate it

1. Một full-text / artifact hiện có đã dùng repository dependency/build/test analysis để infer hoặc audit minimal agent filesystem authority và đo bằng executable ground truth.
2. Pilot trên AuthBench-style tasks cho thấy software evidence không tăng precision/utility so với STD hay chỉ tăng access rộng hơn.
3. Không xây được reference execution / counterfactual removal oracle một cách tái lập trong 12 tuần.

## Minimum viable experiment (chỉ sau pilot)

20 coding tasks có Dockerized environment và reference trajectory; tạo candidate scope từ task-only baseline và task + static evidence; chạy counterfactual deny/removal để chấm utility, permission precision/recall against reviewed oracle, và sensitive exposure. Không nên gọi đây là research project nếu phải tự xây large benchmark.

## Three-month feasibility

**Medium-low.** Không cần train model, nhưng artifact/ground truth là gate. Trạng thái: **SURVIVES WITH REFINEMENT — PRELIMINARY**, không đủ mạnh để đề xuất RQ chính thức.
