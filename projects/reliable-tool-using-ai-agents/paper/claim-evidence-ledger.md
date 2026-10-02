---
title: "Claim–Evidence Ledger — Failure-Domain-Aware Verification Paper"
category: project
tags: [paper-draft, evidence, reproducibility, research-methods, verification]
sources:
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "journal/2026-09-15-action-boundary-main-study.md"
  - "journal/2026-09-15-imperfect-provenance-robustness-gate.md"
  - "synthesis/Prior-Art Threat: Provenance Metadata and Source Selection.md"
  - "journal/2026-09-18-benchmark-derived-case-audit.md"
  - "synthesis/Protocol: Secondary Multi-Domain Benchmark-Derived Adaptation.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate.md"
  - "journal/2026-09-20-ai-review-provenance-correction.md"
  - "journal/2026-09-24-secondary-schema-v12-recheck.md"
  - "journal/2026-09-26-secondary-adapter-smoke-tests.md"
  - "synthesis/Protocol Amendment: Exploratory Secondary Runtime Matrix.md"
  - "journal/2026-09-28-secondary-exploratory-matrix.md"
  - "synthesis/Protocol: Secondary Varied-Schedule Replication.md"
  - "journal/2026-09-28-secondary-varied-schedule-replication.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_secondary_varied/analysis-summary.json"
  - "journal/2026-09-30-rtx4060-live-agent-diagnostic.md"
  - "synthesis/Protocol Amendment: Exploratory RTX 4060 Safety Diagnostic.md"
  - "journal/2026-09-30-live-agent-safety-preflight.md"
  - "journal/2026-10-01-live-agent-diagnostic-instrumentation.md"
  - "journal/2026-10-02-ins32-rtx4060-validity-audit.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_live_agent_ins32_rtx4060_20261002/raw.jsonl"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_live_agent_ins30_rtx4060_20260930/raw.jsonl"
  - "synthesis/protocol-prospective-live-agent-opportunity-gate.md"
  - "journal/2026-10-02-live-agent-opportunity-preflight.md"
created: 2026-09-15T17:15:00+07:00
updated: 2026-10-02T01:59:00+07:00
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
| C11 | Đã audit 12 benchmark-derived cases trên nhiều domain; không phải cả 12 đều phù hợp primary experiment. | Frozen audit: 6 WorkBench + 6 Agent-SafetyBench cases; AI-assisted semantic cross-review, static schema preflight và exploratory runtime matrix | `FACT — CASE AUDIT / EXPLORATORY RUN` | Nói 12 selected IDs, 11 runnable matrix cases và `ASB-267` omission-only exclusion; không gọi là external validation hoặc human-reviewed cohort | human audit các case/oracles và task/topology replication độc lập |
| C12 | Secondary adaptation chạy hai deterministic matrices theo amendment exploratory vì không có human review; không được xem là confirmatory/external validation. | [[synthesis/Protocol: Secondary Multi-Domain Benchmark-Derived Adaptation]]; [[synthesis/Protocol Amendment: Secondary Case Review and Safety Eligibility]]; [[synthesis/Protocol Amendment: Exploratory Secondary Runtime Matrix]]; [[synthesis/Protocol: Secondary Varied-Schedule Replication]]; [[projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate]]; [[journal/2026-09-28-secondary-exploratory-matrix]]; [[journal/2026-09-28-secondary-varied-schedule-replication]] | `FACT — EXPLORATORY INTERNAL RUN` | Được nói ma trận gốc 704 và varied-schedule 1,056 rows đều rerun byte-identical; nêu solo researcher/AI-assisted review, project-defined topology, contract candidate và giới hạn diễn giải | human audit; independent topology/task selection; live-agent evaluation |
| C13 | Lịch secondary matrix ban đầu tạo advantage mô tả cho `provenance_k` trong targeted common-mode + 25% leakage, đồng thời tăng utility false blocks. | Historical raw 704-row SHA `d07e929b9c932866046d28ee8f77476e800f5a80f4a41b363036f90e815b94f7`; [[journal/2026-09-28-secondary-exploratory-matrix]] | `FACT — EXPLORATORY / BY-CONSTRUCTION; SUPERSEDED SCHEDULE` | Chỉ nêu như kết quả lịch sử: `40/64` vs `16/64`, cùng `−0.375` ở mọi case, CI suy biến; không dùng làm kết quả varied-schedule mới | human review; independent task/topology selection; non-deterministic/live agent |
| C14 | Với lịch chọn nguồn/leakage thay đổi theo case nhưng giữ các tần suất 6/12 và 3/12 đã định trước, `provenance_k` có unsafe accepted-action rate thấp hơn `random_k` trên cả tám safety cases của adaptation hiện tại; utility false blocks cao hơn. | Varied raw 1,056-row SHA `40a419491011308dcce04db477c4a98dbda2e543d2db531b0a4fb07c08b43c35`; schedule SHA `f630cb0a34276c23462d838eb23113ea2e4d6c4270958b292db25d26ce725469`; [[journal/2026-09-28-secondary-varied-schedule-replication]] | `FACT — EXPLORATORY INTERNAL REPLICATION` | Nêu denominator theo case `n=12`: `random_k` unsafe `6–8/12`, `provenance_k` `3/12`; mean case Δ `−0.3646`, case-cluster bootstrap `[-0.396,-0.323]` mô tả cho 8 purposive cases và chưa account đầy đủ phụ thuộc trong 2 domains có case lặp; utility false blocks `9/24` vs `18/24`; clean success hai policy 100%. Không generalize sang population/benchmark gốc/agent thật. | human case/oracle audit; independent tasks/topology and domain-cluster sensitivity; valid live-agent test; another independent replication |
| C15 | Local Qwen2.5 7B đã thực thi action-boundary loop trên RTX 4060, nhưng diagnostic này chưa đo safety advantage của provenance selector. | `INS-00030`, seed 701, sáu raw rows SHA `59921cc274a2c27e91d7aed43dbdf6d9903a4d94ecc409006b2e72df1b2155d7`; cả năm artifacts khôi phục đúng hash tại `results_live_agent_ins30_rtx4060_20260930/`; [[journal/2026-09-30-rtx4060-live-agent-diagnostic]]. | `FACT — RE-AUDITABLE DIAGNOSTIC; NO EFFECT EVIDENCE` | Nêu `3/3` clean final states, `6/6` enforced refund attempts được gate kiểm tra, `3/3` targeted final states sai; chỉ một task có fault gây false denial thay vì cho phép refund trái phép, cả hai enforced policies đều chặn, hai clean trajectories có refund lặp rồi escalation. Không dùng `0/6` unsafe làm chứng cứ safety. | valid live-agent safety opportunity |
| C16 | `INS-00032` có canonical escalation và targeted fault tạo **static** false-positive refund opportunity; seed `809` phân biệt source selectors, nhưng 7B không tạo positive-amount refund request. | Task SHA `f587ec9afa9ce5ffe55d49e60379e1ed7f6602c9f956d889a8b82e056e985ec9`; old action-boundary raw SHA `15c9788948ac9f94d43d9caadb5f70d406b362e76b04b09f447a8dd122be99f8`; [[journal/2026-09-30-live-agent-safety-preflight]]; [[journal/2026-10-02-ins32-rtx4060-validity-audit]] | `FACT — OFFLINE OPPORTUNITY; LIVE EFFECT NOT TESTED` | Nêu ground truth/fault/source mapping và hậu nghiệm của seed `809`; phân biệt cơ hội trong môi trường với hành động thật của agent. | task/model tạo unsafe-capable live attempt; independent cases |
| C17 | Instrumentation chọn đủ tám cell và tách process outcomes khỏi final-state outcomes; đã chạy trên Windows, nhưng đây là measurement readiness, không phải policy-effect evidence. | Runner/analyzer/tests; `58/58` tests Linux ở phiên trước, `21/21` tests Windows theo báo cáo máy chạy, `62/62` tests Linux sau khi thêm strict opportunity gate; [[journal/2026-10-01-live-agent-diagnostic-instrumentation]]; [[journal/2026-10-02-live-agent-opportunity-preflight]] | `FACT — IMPLEMENTATION / DIAGNOSTIC` | Được nói old Windows dry-run và tám raw rows hợp lệ; code mới chưa được chạy trên Windows, không suy ra safety advantage từ coverage. | Windows preflight code mới và task tạo matched positive-amount attempt |
| C18 | Qwen2.5 7B/RTX 4060 chạy đủ tám `INS-00032` cells, `12/12` refund attempts được gate kiểm tra, nhưng không đo được effect của source selector vì mọi request đều `0 EUR` sau khi đã escalation. | Raw SHA `a39fcf684661d339f2ca457f8be9210b73918c37f3b6364111bad344afda1abd`; summary SHA `2fa7b630c4439870e631e2d8ec632716587e2a13dd0473d2deaa1616aa1074c6`; audit SHA `ee17e08563db332588606c26785f814c816b4b67dd5852568685670f806b326a`; [[journal/2026-10-02-ins32-rtx4060-validity-audit]] | `FACT — EXPLORATORY DIAGNOSTIC; POLICY-EFFECT VALIDITY FAIL` | Nêu `8/8` final state, `0/8` unsafe, 21 escalation calls và conflict detection difference chỉ như mô tả trace; không dùng các tỷ lệ này làm effect estimate hoặc live validation. | prospective unsafe-capable opportunity criterion; case không lộ canonical answer trước fault; independent replication |
| C19 | Một cổng prospective nghiêm ngặt đã được định nghĩa và static preflight 16-cell/4-task có topology phân biệt selectors; **chưa có model run mới**. | [[synthesis/protocol-prospective-live-agent-opportunity-gate]]; [[journal/2026-10-02-live-agent-opportunity-preflight]]; code mới ghi `boundary_events`; `62/62` local tests. | `FACT — PROTOCOL / STATIC PREFLIGHT ONLY` | Được nói bốn oracle `escalate`, seed 1111 source mapping và điều kiện `BOUNDARY_UNSAFE_CAPABLE`; không nói 7B sẽ tạo opportunity hoặc policy thắng. | Windows dry-run và 16-cell exploratory result, matched-pair audit |

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
| “RTX 4060/Qwen2.5 7B diagnostic validated the safety advantage.” | Một task `INS-00030` chủ yếu thử false denial dưới targeted fault thay vì false-positive refund; random và provenance đều chặn, còn clean process có refund lặp và post-success escalation. |
| “Tám episode INS-00032/Qwen2.5 7B chứng minh provenance policy giảm unsafe refund.” | Cả 12 refund requests là `0 EUR` sau escalation; seed `809` random không thấy conflict nhưng vẫn bị chặn vì amount mismatch. `DECISIVE_ATTEMPT` cũ chỉ nghĩa là có call, chưa chắc có cơ hội chuyển tiền sai. |
| “EnvTrustBench reproduced the external result.” | Chỉ aggregate CSV được tái tính; cases/runners không public. |

## Evidence hierarchy

1. **Confirmatory controlled evidence:** frozen 1,350-episode main study.
2. **Protocol-defined post-main evidence:** 3,750-episode robustness gate.
3. **Exploratory evidence:** 600-episode pilot, 3,600-episode characterization, 108-episode mechanism gate.
4. **Weak/diagnostic evidence:** 36-episode Qwen2.5-1.5B gate, sáu-episode RTX 4060 `INS-00030` và tám-episode RTX 4060 `INS-00032`; các lượt RTX chứng minh feasibility/measurement nhưng chưa đạt policy-effect validity.
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
| O1 | Effect tồn tại ngoài refund workflow khi fault schedules không lặp cấu trúc đồng nhất. | Varied-schedule adaptation còn advantage mô tả ở 8/8 case với differences không còn đồng nhất; tuy nhiên case cohort purposive, topology/mutations do project định nghĩa, lịch deterministic và hai case utility-only. Cần human audit và independent task/topology replication; chưa có live-agent validation. |
| O2 | Failure-domain metadata có thể được cung cấp chính xác trong thực tế. | scope/assumption justification; không biến thành RQ thứ hai. |
| O3 | Safety gain đáng đổi lấy false blocks/escalations. | preregister cost sensitivity hoặc domain-grounded cost ratios. |
| O4 | Effect xuất hiện với capable live agents. | `INS-00030` thử false denial; `INS-00032` có false-positive fault nhưng 7B đã escalation trước mọi refund attempt và chỉ yêu cầu `0 EUR`. Protocol prospective 16-cell đã khóa strict opportunity và boundary evidence logging nhưng **chưa chạy**; cần matched positive-amount pre-escalation pair trước khi coi là policy-effect diagnostic. Agent-visible fault exposure là yêu cầu riêng nếu muốn claim lỗi tool đã gây quyết định sai. |

## Related

- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]
- [[journal/2026-09-15-external-validity-artifact-gate]]
- [[synthesis/Protocol: Secondary Multi-Domain Benchmark-Derived Adaptation]]
- [[synthesis/Protocol: Action-Boundary Provenance Verification Main Study]]
