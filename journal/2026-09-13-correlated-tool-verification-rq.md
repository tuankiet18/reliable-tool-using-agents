---
title: "2026-09-13 — Correlated Tool Verification RQ Gate"
category: journal
tags: [research-log, prior-art, verification, tool-failure, research-question]
sources:
  - "https://arxiv.org/abs/2603.02345"
  - "https://arxiv.org/abs/2608.22676"
  - "https://arxiv.org/abs/2608.02645"
  - "https://arxiv.org/abs/2607.07405"
  - "https://proceedings.mlr.press/v267/kim25e.html"
  - "https://github.com/sierra-research/tau2-bench"
  - "https://github.com/mohammadi-hadi/trajectory-judge"
summary: >-
  Ba vòng adversarial search bác bỏ generic semantic verification và tạo RQ hẹp về provenance-aware verification dưới common-mode silent tool faults; artifact gate xác nhận trajectory-judge khả thi hơn tau2-bench cho development.
provenance:
  extracted: 0.73
  inferred: 0.24
  ambiguous: 0.03
base_confidence: 0.86
lifecycle: draft
lifecycle_changed: 2026-09-13
tier: supporting
created: 2026-09-13T00:00:00Z
updated: 2026-09-13T00:00:00Z
---

# Research log — Correlated tool verification RQ gate

## Đã search

- Semantic validation, runtime enforcement, postcondition verification và policy gates.
- Schema-valid inconsistent/incomplete tool returns.
- Cross-tool corroboration, verifier diversity, adaptive/fixed `K`.
- `correlated`, `common-mode`, `shared backend`, `failure domain`, `source diversity`, `provenance-aware verification`.
- Foundational multiversion-programming independence và LLM error correlation.
- Official repositories, licenses và local setup của `trajectory-judge`, `tau2-bench`, AIOpsLab.

## Đã học được

- Generic runtime semantic verification không phải gap: RIVA, AgentSpec, deterministic gates và verified tool wrappers đã phủ nhiều phần.
- RIVA là direct prior art cho cross-tool verification nhưng không model dependency giữa tools.
- Correlated/common-mode failure là assumption break hợp lý từ software reliability, nhưng direct agent-tool evidence vẫn thiếu.
- `trajectory-judge` là artifact nhẹ nhất cho controlled ground truth; `tau2-bench` có realism và final-state scorer tốt hơn nhưng setup/API phức tạp hơn.

## Local artifact checks

- `trajectory-judge`: `uv sync --extra dev`; 188 tests pass; `uv run trajectory-judge run --n 20 --judges mock ...` tạo 17 applicable trajectories và hoàn tất offline.
- `make demo` tự gọi executable ngoài `uv run` nên fail trong fresh uv environment; CLI chạy đúng khi gọi qua `uv run`.
- `tau2-bench` v1.0.1: core install pass; data gồm 114 retail, 50 airline, 2,285 telecom tasks. Dev tests không collect được vì missing `websockets` từ optional voice import path.
- Hardware: RTX 3050 Laptop 4 GB VRAM, 16 GB RAM; không phù hợp phụ thuộc 14B model nhanh.

## Uncertainties

- Chưa có citation graph exhaustive từ tất cả paper trích dẫn RIVA vì paper rất mới.
- RIVA code riêng chưa tìm thấy; có thể implementation có source-tracking không mô tả trong paper.
- Cách tạo redundant sources trong support-desk domain phải đủ realistic, nếu không gap biến thành toy benchmark.
- Free API quotas thay đổi và không thể là nền tảng của feasibility claim.

## Decision

Chọn một candidate RQ duy nhất về provenance-aware corroborating-tool selection under common-mode silent faults. Giữ status `PRELIMINARY`; bước kế tiếp là preregistered 10-task fault-model pilot, chưa xây full system.

## Related

- [[synthesis/Research: Correlated Silent Tool Failures and Verification]]
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]

