---
title: "Claim–Evidence Ledger — Failure-Domain-Aware Verification Paper"
category: project
tags: [paper-draft, evidence, reproducibility, research-methods, verification]
sources:
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "journal/2026-09-15-action-boundary-main-study.md"
  - "journal/2026-09-15-imperfect-provenance-robustness-gate.md"
  - "synthesis/Prior-Art Threat: Provenance Metadata and Source Selection.md"
created: 2026-09-15T17:15:00+07:00
updated: 2026-09-15T17:15:00+07:00
summary: >-
  Ledger nối từng claim của living paper với evidence, epistemic status, phạm vi được phép viết và evidence còn thiếu.
lifecycle: draft
---

# Claim–Evidence Ledger

Mục đích của ledger là ngăn paper mạnh hóa claim theo thời gian. Khi có experiment hoặc prior art mới, cập nhật ledger trước rồi mới sửa [[projects/reliable-tool-using-ai-agents/paper/paper-draft]].

## Active claims

| ID | Claim | Evidence | Status | Phạm vi được phép viết | Evidence còn thiếu |
|---|---|---|---|---|---|
| C1 | Tool-interface diversity không bảo đảm failure independence. | Knight–Leveson; correlated LLM errors; constructed shared-backend counterexample | `SUPPORTED PRINCIPLE` | Nói như risk/assumption problem, không nói prevalence của production tool failures | empirical production tool-dependency data |
| C2 | Random-K có thể xác nhận sai khi primary và corroborator cùng failure domain. | 30/30 same-domain random attempts unsafe trong main study | `FACT — CONTROLLED` | Chỉ trong targeted controlled topology | second environment |
| C3 | Provenance-K giảm unsafe refund hơn random-K dưới targeted common-mode fault. | Δ `-0.200`, 95% CI `[-0.273,-0.127]` | `SUPPORTED — CONTROLLED` | Phải kèm accurate metadata, mandatory boundary và matched `K=2` | external validation |
| C4 | Provenance-K giữ clean correctness trong main benchmark. | both `1.000`, difference `0.000` | `SUPPORTED — CONTROLLED` | Không generalize thành “no utility cost” ở mọi domain | larger/second clean workload |
| C5 | Provenance-K không có material advantage dưới independent faults. | unsafe Δ `+0.0067`, CI `[-0.020,0.033]` | `SUPPORTED NEGATIVE CONTROL` | “No evidence of advantage in this study” | more tasks nếu muốn equivalence claim |
| C6 | Wrong provenance metadata có thể phá safety advantage. | wrong-25/leak-.10 CI upper bound `0.000`; robustness gate fail | `SUPPORTED LIMITATION` | Dùng “advantage was not reliably retained”, không nói always harmful | other noise mechanisms |
| C7 | Missing labels ít nguy hiểm hơn wrong labels trong current design. | missing-25 passes; fallback visible | `INFERENCE` | Chỉ giải thích mechanism plausible, không universal hierarchy | preregistered direct comparison |
| C8 | Prompt-only self-verification không đủ để bảo đảm action-boundary coverage. | 36-episode live gate: compliance 0; coverage 50–67% | `FACT — SMALL LOCAL MODEL` | Giới hạn vào local Qwen2.5-1.5B gate | capable models/external scaffolds |
| C9 | Exact combined RQ chưa có direct prior-art match trong search hiện tại. | three-round adversarial search | `PRELIMINARY NEGATIVE SEARCH` | “We did not identify”, không “no prior work exists” | citation chaining và supervisor review |
| C10 | Core controlled experiment reproducible không cần API/GPU. | deterministic rerun hashes; tests/invariants pass | `FACT` | Áp dụng core artifact | independent machine reproduction |

## Rejected or prohibited claims

| Claim không được dùng | Vì sao |
|---|---|
| “This is the first provenance-aware agent guardrail.” | ProvenanceGuard direct counterexample. |
| “No previous work selects which tool output to trust.” | TEA-CXA direct counterexample. |
| “No prior work models or validates agent dependencies.” | GRADE, AgentFlow và EDGE là counterexamples. |
| “The method is robust to imperfect provenance metadata.” | Post-main robustness gate failed. |
| “The method generalizes to realistic environments.” | Chưa có executable external validation. |
| “Two different tools provide independent evidence.” | Đây chính là assumption bị nghiên cứu phản bác. |
| “Provenance-K always improves expected utility.” | Utility phụ thuộc abstention/escalation cost và fault regime. |
| “Full live-agent experiment validated the method.” | Live gate failed experimental validity. |
| “EnvTrustBench reproduced the external result.” | Chỉ aggregate CSV được tái tính; cases/runners không public. |

## Evidence hierarchy

1. **Confirmatory controlled evidence:** frozen 1,350-episode main study.
2. **Protocol-defined post-main evidence:** 3,750-episode robustness gate.
3. **Exploratory evidence:** 600-episode pilot, 3,600-episode characterization, 108-episode mechanism gate.
4. **Weak/diagnostic evidence:** 36-episode local live-agent gate.
5. **External literature evidence:** dùng để motivate hoặc bound novelty, không thay thế experiment của project.

## Update rule

Mỗi lần thêm result:

1. ghi result và protocol chronology vào research journal;
2. thêm hoặc sửa một row trong ledger;
3. kiểm tra wording trong Abstract, Introduction, Discussion và Conclusion;
4. nếu claim bị yếu đi, giữ contradictory result và thu hẹp wording;
5. chỉ nâng `PRELIMINARY` sau prior-art và reproducibility gate tương ứng.

## Open claims requiring work

| ID | Open claim | Gate cần thiết |
|---|---|---|
| O1 | Effect tồn tại trên task semantics ngoài refund workflow. | 12-case Agent-SafetyBench/WorkBench-derived secondary pilot hoặc executable external benchmark. |
| O2 | Failure-domain metadata có thể được cung cấp chính xác trong thực tế. | scope/assumption justification; không biến thành RQ thứ hai. |
| O3 | Safety gain đáng đổi lấy false blocks/escalations. | preregister cost sensitivity hoặc domain-grounded cost ratios. |
| O4 | Effect xuất hiện với capable live agents. | small, stable live-agent validation sau khi action-boundary environment ổn định. |

## Related

- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]
- [[journal/2026-09-15-external-validity-artifact-gate]]
- [[synthesis/Protocol: Action-Boundary Provenance Verification Main Study]]

