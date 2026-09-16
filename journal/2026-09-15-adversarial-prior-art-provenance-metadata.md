---
title: "Adversarial prior-art search — Provenance metadata and source selection"
category: journal
tags: [research-log, prior-art, provenance, verification, novelty]
sources:
  - "https://arxiv.org/abs/2602.21517"
  - "https://arxiv.org/abs/2606.18037"
  - "https://arxiv.org/abs/2607.01236"
  - "https://arxiv.org/abs/2605.08828"
  - "https://arxiv.org/abs/2606.22741"
  - "https://arxiv.org/abs/2607.01640"
  - "https://aclanthology.org/2024.findings-emnlp.978/"
created: 2026-09-15T15:34:48+07:00
updated: 2026-09-15T15:34:48+07:00
summary: >-
  Ba-round adversarial search thu hẹp novelty của provenance-aware verification; exact controlled RQ sống sót nhưng metadata validation không nên trở thành RQ mới.
---

# Research log — adversarial prior art cho provenance metadata

## Mục tiêu

Cố bác bỏ open question sau robustness gate: prior work đã validate/calibrate provenance metadata hoặc chọn evidence source theo trust/uncertainty đủ gần exact RQ hay chưa?

## Đã tìm gì

Ba vòng search bao phủ:

1. Broad discovery: `tool trust`, `source-aware verification`, `provenance agent`, `uncertainty calibration`, `environmental evidence`.
2. Gap filling: `dependency graph`, `static analysis`, `counterfactual dependency validation`, MCP provenance và action guardrails.
3. Contradiction/adversarial: tìm direct combination của common-mode/correlated tool faults, failure-domain metadata, independent corroborator selection và irreversible action gating.

Nguồn ưu tiên gồm arXiv full text, ACL Anthology, OpenReview và official GitHub repositories.

## Đã học được gì

- `FACT:` TEA-CXA đã học dynamic tool trust và chọn response trong conflict; broad tool-response selection không mới.
- `FACT:` hai paper khác nhau cùng dùng tên `ProvenanceGuard`. Một paper kiểm tra source attribution trong MCP answers; paper ASE 2026 kiểm tra justification provenance trước tool execution.
- `FACT:` GRADE, EDGE và AgentFlow đã nghiên cứu derivation hoặc validation của dependency structure.
- `FACT:` EnvTrustBench đã benchmark false paths do stale/wrong/malicious environmental evidence.
- `INFERENCE:` Không work nào tìm được kết hợp failure-domain independence, targeted common-mode silent corruption, mandatory irreversible-action boundary và matched-budget source selection.
- `HYPOTHESIS:` Exact controlled effect vẫn có research value nếu được external validation; nó không đủ novelty nếu chỉ lặp lại synthetic topology.

## Negative evidence không được bỏ

TEA-CXA và ProvenanceGuard làm mất quyền claim “first dynamic trust selection” hoặc “first provenance-aware action gate”. GRADE làm mất quyền claim “first uncertainty-aware dependency metadata”. Đây là giới hạn thật, không phải paper chỉ adjacent nên có thể bỏ qua.

## Uncertainties

- Negative search không chứng minh absence hoàn toàn.
- Một số 2026 artifacts chưa release code/data đầy đủ.
- `failure domain` trong production có thể khó quan sát hơn source/tool IDs.
- EnvTrustBench public release có thể chưa đủ để chạy end-to-end.

## Decision

Giữ canonical RQ và status `SURVIVES WITH REFINEMENT — PRELIMINARY`. Không biến metadata validation thành RQ mới trong project 12 tuần.

## Next action

Chỉ làm một việc tiếp theo: [[references/envtrustbench|artifact gate cho EnvTrustBench]] để quyết định external validation có khả thi hay không.

## Related

- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]]
- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]

