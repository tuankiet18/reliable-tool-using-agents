---
title: "Failure-Domain-Aware Verification for Tool-Using AI Agents under Correlated Silent Tool Failures"
category: project
tags: [ai-agents, paper-draft, verification, tool-failure, reliability]
sources:
  - "synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures.md"
  - "synthesis/Protocol: Action-Boundary Provenance Verification Main Study.md"
  - "journal/2026-09-15-action-boundary-main-study.md"
  - "journal/2026-09-15-imperfect-provenance-robustness-gate.md"
  - "journal/2026-09-15-external-validity-artifact-gate.md"
  - "journal/2026-09-18-benchmark-derived-case-audit.md"
  - "journal/2026-09-20-secondary-schema-preflight.md"
  - "journal/2026-09-20-ai-review-provenance-correction.md"
  - "journal/2026-09-24-secondary-schema-v12-recheck.md"
  - "journal/2026-09-26-secondary-adapter-smoke-tests.md"
  - "synthesis/Protocol Amendment: Exploratory Secondary Runtime Matrix.md"
  - "journal/2026-09-28-secondary-exploratory-matrix.md"
  - "synthesis/Protocol: Secondary Varied-Schedule Replication.md"
  - "journal/2026-09-28-secondary-varied-schedule-replication.md"
  - "https://arxiv.org/abs/2603.02345"
  - "https://proceedings.mlr.press/v267/kim25e.html"
created: 2026-09-15T17:15:00+07:00
updated: 2026-09-28T14:27:00+07:00
summary: >-
  Living paper draft cho controlled study về mandatory action-boundary verification chọn corroborator độc lập theo failure domain dưới correlated silent tool failures.
lifecycle: draft
paper_status: living-draft
version: "0.1"
---

# Failure-Domain-Aware Verification for Tool-Using AI Agents under Correlated Silent Tool Failures

> [!important] **Living paper — version 0.1.** Nội dung tiếng Việt giúp kiểm tra reasoning và evidence. Title, Research Question và Hypothesis dùng English canonical wording. Đây chưa phải submission-ready English manuscript. Abstract, contribution claims và conclusion chưa được đóng băng.

## Abstract — PROVISIONAL

AI agent dùng tool có thể nhận phản hồi sai nhưng vẫn đúng schema và không phát sinh exception. Một cách phòng vệ phổ biến là gọi thêm tool để kiểm tra chéo. Tuy nhiên, hai tool có tên và API khác nhau vẫn có thể dùng chung database replica, cache, provider hoặc telemetry pipeline; khi shared dependency sai, các tool có thể đồng thuận trên cùng một kết quả sai. Nghiên cứu này khảo sát xác minh dựa trên miền lỗi (failure-domain-aware verification) ngay trước hành động không thể đảo ngược. Trong controlled support workflow, runtime bắt buộc dùng primary observation và một corroborator ở cùng ngân sách `K=2`. Treatment chọn corroborator thuộc failure domain khác primary; baseline chọn ngẫu nhiên trong các tool interfaces khác tên. Main deterministic study gồm 1,350 episodes trên 30 frozen tasks. Dưới targeted common-mode silent failures, treatment giảm unsafe refund từ `0.200` xuống `0.000`, với paired task-cluster bootstrap difference `-0.200`, 95% CI `[-0.273,-0.127]`; clean correctness của cả hai policy là `1.000`. Tuy nhiên, post-main robustness study gồm 3,750 episodes cho thấy advantage không còn đủ chắc chắn khi `25%` failure-domain labels bị gán sai. Kết quả hỗ trợ causal claim trong controlled setting với accurate metadata, nhưng chưa chứng minh external validity hoặc production readiness.

**Keywords:** tool-using AI agents; runtime verification; correlated failures; common-mode failures; provenance; action boundary; agent reliability.

## 1. Introduction

Các large language model agents ngày càng được phép gọi API, đọc database, sửa file, gửi email hoặc tạo transaction. Trong vòng lặp `plan → tool call → observation → next action`, agent thường xem tool output như evidence về trạng thái bên ngoài. Nếu tool trả exception, lỗi tương đối dễ nhận biết. Nguy hiểm hơn là **lỗi công cụ im lặng (silent tool failure)**: call thành công về mặt giao thức và output đúng schema, nhưng nội dung sai hoặc stale.

Một hướng xử lý tự nhiên là kiểm tra chéo qua nhiều tool. RIVA cho thấy nhiều diagnostic paths có thể tăng reliability khi observability tools trả erroneous output [[references/riva]]. Tuy nhiên, số lượng tool interfaces không đồng nghĩa với số lượng nguồn evidence độc lập. `get_order_status` và `search_order_history` có thể cùng đọc một `operational_db` replica. Nếu replica đó bị corrupt, hai calls khác tên có thể trả cùng một kết quả sai và tạo false confidence.

Rủi ro này liên quan đến **lỗi chung nguyên nhân (common-mode failure)** trong dependable systems. Knight và Leveson cho thấy diverse implementations không tự động bảo đảm statistical independence; nghiên cứu gần đây về hơn 350 LLMs cũng quan sát substantial correlated errors và liên hệ chúng với shared architecture/provider [[references/correlated-errors-in-large-language-models]]. Evidence này không trực tiếp chứng minh tool outputs có correlated failures, nhưng phản bác giả định đơn giản rằng diversity bề ngoài đủ tạo independence.

Vấn đề đặc biệt quan trọng trước **hành động không thể đảo ngược hoặc có side effect lớn (irreversible action)**. Nếu agent chỉ trả lời sai bằng text, hậu quả có thể sửa được. Nếu agent gọi `issue_refund`, xóa resource hoặc gửi dữ liệu nhạy cảm, lỗi đã chuyển từ belief sai thành state change thực tế. Vì vậy nghiên cứu này đặt verification tại **ranh giới hành động (action boundary)**: runtime intercepts proposed write và yêu cầu corroboration trước execution.

Nghiên cứu không claim rằng provenance-aware guardrail hoặc tool trust selection là hoàn toàn mới. TEA-CXA đã học query-dependent tool expertise để chọn response nên tin [[references/tea-cxa]]. ProvenanceGuard đã kiểm tra claim–source attribution trong MCP traces [[references/provenanceguard-source-aware-factuality]], và một work khác cùng tên đã dùng provenance để chặn misaligned tool calls trước execution [[references/provenanceguard-misalignment-provenance-analysis]]. Phần được khảo sát ở đây hẹp hơn: liệu **failure-domain-independent corroboration** có giảm unsafe actions hơn random-source corroboration dưới controlled correlated silent faults, với cùng tool-call budget hay không.

### 1.1 Research Question

#### English canonical RQ

**RQ1. Given accurate failure-domain metadata, under targeted common-mode silent tool-output failures, does mandatory action-boundary verification that selects a provenance-independent corroborator reduce unsafe irreversible actions while maintaining clean-task correctness, compared with random-source verification at a matched K=2 tool-call budget?**

#### Giải thích tiếng Việt

Khi runtime biết chính xác tool nào dùng chung failure domain, việc chọn một nguồn kiểm chứng thật sự độc lập có giảm hành động nguy hiểm hơn chọn ngẫu nhiên một tool khác tên hay không? Hai policy phải dùng đúng cùng hai evidence calls để lợi ích không đến từ việc treatment tốn nhiều tài nguyên hơn.

### 1.2 Hypothesis

#### H1 — English

**Given accurate failure-domain metadata and a matched K=2 verification budget, provenance-independent corroboration reduces unsafe refunds relative to random-source corroboration under targeted common-mode silent failures, without a material reduction in clean final-state correctness.**

#### Diễn giải

Treatment được kỳ vọng tốt hơn đúng trong trường hợp shared-source corruption. Không dự đoán treatment tốt hơn dưới independent faults. Hypothesis cũng không áp dụng khi failure-domain metadata bị gán sai.

### 1.3 Provisional contributions

Các contribution sau chỉ được giữ nếu final audit và external-validity decision không làm thay đổi evidence:

1. Một controlled fault model phân biệt independent và targeted common-mode schema-valid tool corruptions.
2. Một matched-budget comparison giữa random tool-interface diversity và failure-domain-independent corroboration tại action boundary.
3. Empirical characterization cho thấy safety gain với accurate metadata, cùng negative result rằng wrong metadata có thể phá gain.
4. Một reproducible deterministic artifact với frozen tasks, raw episode logs, invariants và task-cluster bootstrap analysis.

Không claim “first provenance-aware verifier”, “first agent guardrail” hoặc “first learned tool trust method”.

## 2. Background and Problem Formulation

### 2.1 Tool, source và failure domain

- **Tool interface:** function mà agent có thể gọi, ví dụ `check_eligibility_replica`.
- **Data source:** backend cung cấp dữ liệu, ví dụ một operational database replica.
- **Failure domain:** nhóm components có thể cùng sai do shared dependency hoặc common cause.

Hai tool interfaces có thể khác tên nhưng thuộc cùng failure domain. Ngược lại, hai interfaces cùng cung cấp eligibility information có thể lấy từ operational database và independent audit ledger.

### 2.2 Failure regimes

- `clean`: mọi observation phản ánh canonical state.
- `independent`: một tool observation có thể bị corrupt độc lập.
- `targeted_common_mode`: primary source và mọi same-domain replicas nhận cùng schema-valid wrong value.

Fault injector chỉ thay đổi eligibility evidence. Canonical world state và evaluator không bị sửa.

### 2.3 Action-boundary verification

Ngay trước `issue_refund`, runtime thực hiện:

```text
proposed irreversible action
        ↓
primary eligibility evidence
        +
one corroborating evidence source
        ↓
agree and authorize exact amount?
   yes → allow action
   no  → block and escalate
```

Verification là mandatory runtime enforcement, không phụ thuộc agent tự nhớ phải kiểm tra. Quyết định cuối dùng deterministic rule; LLM không tự chấm độ đúng của evidence.

### 2.4 Policies

- `single_source`: tin primary evidence; secondary baseline.
- `random_k`: primary cộng một random corroborator trong các interfaces còn lại.
- `provenance_k`: primary cộng một corroborator thuộc failure domain khác theo metadata.

Main comparison là `random_k` với `provenance_k`. Cả hai có `K=2`, cùng primary source và đúng một corroborator tại mỗi refund attempt.

### 2.5 Outcomes

Primary safety outcome là **unsafe refund**: refund được thực hiện khi expected action không phải refund hoặc amount khác canonical authorised amount. Clean-task utility được đo bằng final-state correctness. Secondary outcomes gồm false block, escalation, conflict, extra tool calls và expected decision loss.

## 3. Related Work

### 3.1 Tool failure detection và recovery

Research về unreliable tools đã phân biệt transient/persistent failures, controlled fault injection, failure forecasting và recovery. Tuy nhiên, recovery-action routing nói chung đã có direct prior art và không phải contribution của paper này. [[references/robustness-inconsistent-incomplete-tool-responses]] cho thấy incomplete responses dễ nhận biết hơn schema-valid inconsistent responses, nhưng không chạy recovery policy hay correlated-failure experiment.

### 3.2 Runtime verification và postconditions

`Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures` dùng postcondition verification, verify-before-retry và idempotency để giảm duplicate side effects [[references/verified-tool-calls-non-atomic-failures]]. `Reason Less, Verify More` dùng deterministic pre-write gates để ngăn silent policy violations [[references/reason-less-verify-more]]. Hai work xác lập giá trị của runtime verification, nhưng không giải quyết trường hợp verifier và agent cùng tin một corrupted read source.

### 3.3 Cross-tool verification

RIVA là prior art gần nhất. RIVA tạo ít nhất `K` diagnostic paths và cross-validate kết quả để phát hiện configuration drift khi observability tools có thể sai [[references/riva]]. Paper báo accuracy tăng từ `27.3%` với ReAct lên `50.0%` dưới erroneous tool responses. Tuy nhiên, RIVA dựa trên trực giác rằng independent tools khó cùng sai, không mô hình hóa shared failure domains. Kết quả `K=3` có thể collapse khi không đủ diagnostic paths cũng cho thấy thêm verification không tự động cải thiện reliability.

### 3.4 Tool trust và uncertainty-aware selection

TEA-CXA dùng reinforcement learning để học practical trustworthiness của medical tools theo query type; khi outputs conflict, agent học response nào nên tin [[references/tea-cxa]]. ProbeCal hiệu chỉnh expected effectiveness của tool-use prompts và execution traces. Do đó broad claim về dynamic/uncertainty-aware tool selection đã bị prior art phủ. Khác biệt của nghiên cứu hiện tại là explicit common-mode fault topology, no-training selector và matched action-safety comparison.

### 3.5 Provenance-aware agent verification

`ProvenanceGuard: Source-Aware Factuality Verification for MCP-Based LLM Agents` kiểm tra claim có được đúng source hỗ trợ hay không, nhưng không chứng minh source đúng ngoài đời hoặc độc lập về failure mechanism [[references/provenanceguard-source-aware-factuality]]. `Safeguarding LLM Agents from Misalignment through Provenance Analysis` intercepts proposed tool calls và kiểm tra justification provenance từ query, tool documentation, history và plan [[references/provenanceguard-misalignment-provenance-analysis]]. Nó bảo vệ user-intent alignment, không bảo vệ truthfulness khi context/tool observation bị common-mode corruption.

GRADE và AgentFlow cho thấy dependency structure có thể được biểu diễn, derive hoặc grade [[references/grade-agent-dependency-execution]] [[references/agentflow-agent-dependency-graphs]]. Vì vậy paper này giả định accurate failure-domain metadata thay vì claim giải quyết metadata discovery.

### 3.6 Environmental evidence benchmarks

EnvTrustBench báo agents thường đi theo false path khi files, logs, APIs hoặc command outputs bị stale, wrong hoặc malicious [[references/envtrustbench]]. Public aggregate data cho phép tái tính `3,206/3,850 = 83.27%`, nhưng release hiện không có executable cases/oracles/runners. Agent-SafetyBench và WorkBench artifacts trong ProvenanceGuard có traces và action labels, nhưng không có redundant evidence sources hay correlated-fault model [[journal/2026-09-15-external-validity-artifact-gate]].

## 4. Methodology

### 4.1 Experimental environment

Controlled experiment mở rộng deterministic support-desk environment từ `trajectory-judge` [[references/trajectory-judge]]. Environment có canonical customer, order, refund-policy và eligibility state. Redundant eligibility interfaces được ánh xạ vào `operational_db`, `analytics_replica` và `audit_ledger` failure domains.

Upstream `trajectory-judge` commit được ghi là `d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5`. Project artifact nằm tại `projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/`.

### 4.2 Frozen main-study design

- 30 tasks: `INS-00060`–`INS-00089`.
- Six difficulty strata; five tasks mỗi stratum.
- Five seeds: `101`, `211`, `307`, `401`, `503`.
- Three regimes: `clean`, `independent`, `targeted_common_mode`.
- Three policies: `single_source`, `random_k`, `provenance_k`.
- Total: `1,350` deterministic episodes.

Task manifest được tạo trước main harness, không trùng task IDs đã dùng ở pilots, với SHA-256 `a122dda63a40ab8db43d1af2a6a7019ca561c4c9e533db0e798fe9470e88cfa6`.

### 4.3 Ground truth

Canonical environment state quyết định expected action và authorised refund amount. Fault map ghi corruption regime và affected failure domain. Evaluator chấm programmatically; không dùng LLM-as-a-judge hoặc agent self-report.

### 4.4 Analysis

Primary unit of inference là task. Năm seed episodes được cluster theo task. Paired difference giữa `provenance_k` và `random_k` được ước lượng bằng task-cluster bootstrap với 10,000 resamples; report point estimate và two-sided 95% confidence interval.

Confirmatory gate yêu cầu:

1. boundary coverage `1.000` và matched `K=2` invariants;
2. common-mode unsafe-refund difference âm với upper 95% CI dưới zero;
3. clean unsafe refund không tăng quá `0.02`;
4. clean correctness không giảm quá margin `0.05`;
5. safety benefit xuất hiện ở ít nhất hai difficulty strata.

### 4.5 Evidence chronology

| Stage | Vai trò | Episodes | Có preregistered không? |
|---|---|---:|---|
| Exploratory pilot | kiểm tra mechanics và tìm baseline mạnh | 600 | Không |
| 30-task next gate | characterization/noisy-metadata exploration | 3,600 | Một phần |
| Full live-agent gate | kiểm tra agent compliance | 36 | Gate phụ |
| Action-boundary mechanism gate | sửa vị trí enforcement | 108 | Exploratory |
| Main deterministic study | primary confirmatory test | 1,350 | Có |
| Imperfect-provenance robustness | post-main stress test | 3,750 | Protocol amendment trước run |

Không dùng exploratory thresholds như universal conclusions. Không trình bày post-main robustness analysis như primary confirmatory evidence.

## 5. Results

### 5.1 Exploratory findings

Trong 600-episode pilot, `provenance_aware` giảm common-mode unsafe acceptance từ `0.34` của fixed-K xuống `0.00`, nhưng abstention tăng từ `0.00` lên `0.64`. So với random-K, difference chỉ `-0.06` với CI `[-0.12,0.00]`. Kết quả này làm random-K trở thành primary baseline và cho thấy phải đo safety–abstention trade-off.

Full live-agent gate gồm 36 episodes không tạo valid comparative evidence: prompt-only self-verification compliance bằng zero, enforced verification coverage chỉ `50–67%`, và reply completion thấp. Negative result này dẫn tới mandatory action-boundary enforcement thay vì yêu cầu agent tự kiểm tra.

### 5.2 Main deterministic study

Tất cả 29 tests, static checks và experiment invariants pass. Reproduction rerun tạo cùng raw-data SHA-256 `a51aebcb207f996e7a4d065b2e424fe794346d685d5f37a615d0de6bcb872234`.

| Regime | Policy | Final-state correctness | Unsafe refund | False block | Conflict |
|---|---|---:|---:|---:|---:|
| `clean` | `random_k` | 1.000 | 0.000 | 0.000 | 0.000 |
| `clean` | `provenance_k` | 1.000 | 0.000 | 0.000 | 0.000 |
| `independent` | `random_k` | 0.807 | 0.040 | 0.153 | 0.193 |
| `independent` | `provenance_k` | 0.793 | 0.047 | 0.160 | 0.193 |
| `targeted_common_mode` | `random_k` | 0.467 | 0.200 | 0.333 | 0.467 |
| `targeted_common_mode` | `provenance_k` | 0.667 | 0.000 | 0.333 | 0.667 |

Trong targeted common-mode regime:

- unsafe-refund difference `provenance_k − random_k = -0.200`;
- 95% CI `[-0.273,-0.127]`;
- safety benefit xuất hiện ở `4/6` difficulty strata.

Clean correctness difference là `0.000`, CI `[0.000,0.000]`. Independent-fault negative control không cho thấy advantage: unsafe-refund difference `+0.0067`, CI `[-0.020,0.033]`.

Main deterministic gate do đó `PASS` theo toàn bộ criteria đã ghi trước.

### 5.3 Mechanism analysis

Trong 100 targeted-common-mode refund attempts của random-K, policy chọn corroborator cùng `operational_db` 30 lần; cả `30/30` dẫn tới unsafe refund. Provenance-K chọn independent domain trong `100/100` attempts và phát conflict trong `100/100`.

Đây là evidence mạnh cho internal causal mechanism, nhưng cũng cho thấy effect được tạo trực tiếp bởi controlled topology. Task semantics đóng vai trò nhỏ hơn source-selection structure trong primary result.

### 5.4 Imperfect-provenance robustness

Post-main study dùng 30 tasks mới, năm seeds, four metadata conditions và cross-domain leakage `0–0.50`, tổng `3,750` episodes.

| Condition | Provenance unsafe | Random unsafe | Difference | 95% CI | Gate |
|---|---:|---:|---:|---:|---|
| accurate, leakage `.25` | .193 | .327 | -.133 | [-.220,-.053] | PASS |
| missing `.25`, leakage `.10` | .100 | .253 | -.153 | [-.227,-.087] | PASS |
| wrong `.25`, leakage `.10` | .187 | .253 | -.067 | [-.133,.000] | **FAIL** |

Overall robustness gate `FAIL` vì cả ba required conditions phải pass. Missing labels tạo uncertainty nhìn thấy được và cho phép fallback; wrong labels tạo false confidence. Vì vậy canonical RQ được thu hẹp thành `Given accurate failure-domain metadata`.

### 5.5 External-validity artifact gate

EnvTrustBench không public executable cases. ProvenanceGuard replication artifact setup thành công, load được 182 Agent-SafetyBench và 388 WorkBench traces, đồng thời chạy được ba analysis notebooks offline. Tuy nhiên các datasets không có failure-domain topology hoặc redundant corroborators. Hiện chưa có direct external validation.

Follow-up case audit đã đóng băng 12 read-before-write cases từ hai artifacts, gồm sáu WorkBench và sáu Agent-SafetyBench cases trên 10 atomic application domains. Các case giữ nguyên user goal, original action boundary và có programmatic oracle, nhưng same-domain replica, independent corroborator và fault topology đều phải được project bổ sung. Vì vậy audit chỉ pass feasibility cho một **benchmark-derived secondary adaptation**; nó chưa tạo thêm experimental evidence và không thay đổi kết luận “chưa có direct external validation”.

AI-assisted semantic cross-review và static schema preflight sau audit đã thu hẹp kế hoạch: tám safety cases hiện hành trên sáu domains, `WB-295` là restoration diagnostic ngoài denominator, `ASB-267` là `INVALID_NOT_RUN`. Exact-schema AI cross-review trả `2 APPROVE / 5 REVISE`, **không phải human sign-off**. Specification re-check v1.2 pass typed P/S/I materialization, trace-bound actions, structured oracle assertions, `WB-433` hashes và negative tests; smoke test 32 episodes chỉ xác nhận adapter mechanics. Protocol amendment đã công khai deviation và giới hạn mọi secondary runtime result thành exploratory/internal. Ma trận 704-row đầu tiên có unsafe `40/64` (`random_k`) vs `16/64` (`provenance_k`), nhưng cùng `−0.375` ở cả tám case và CI suy biến. Đây là kết quả lịch sử, được giữ nguyên để truy vết chứ không dùng thay cho varied-schedule analysis [[journal/2026-09-28-secondary-exploratory-matrix]].

### 5.6 Secondary exploratory runtime matrix — không confirmatory

Một replication exploratory mới giữ nguyên cohort/contract nhưng thay lịch chọn source và fault theo `case_id × seed × purpose`. Lịch 11 case × 12 seed × 4 regime × 2 policy có 1.056 rows/528 matched pairs và được khóa trước runtime (schedule SHA-256 `f630cb0a34276c23462d838eb23113ea2e4d6c4270958b292db25d26ce725469`). Ở `targeted_common_mode_25`, unsafe accepted actions là `59/96` (`random_k`) so với `24/96` (`provenance_k`). Mean paired rate difference trên tám safety cases là `−0.3646`, median `−0.375`, advantage mô tả ở `8/8` cases; từng case nằm trong khoảng `−0.250` đến `−0.417`. Case-cluster bootstrap percentile 95% CI là `[-0.396,-0.323]`, nhưng chỉ resample tám cases được chọn có chủ đích; hai domains có case lặp nên bootstrap theo case chưa mô hình hóa hết phụ thuộc trong domain. Đây không phải population-level inference. Utility-only false blocks là `9/24` (`random_k`) và `18/24` (`provenance_k`), trong khi utility task success là `15/24` và `6/24`. Clean safety/utility success là 100% cho cả hai. Ở targeted common-mode regimes, safety task success là `0/96` cho cả hai: gate block/allow nhưng không sửa proposal. Raw output được chạy hai lần byte-identical; ma trận cũ vẫn không đổi. Kết quả cho thấy schedule overlap từng phần giải thích khác biệt giữa cases, nhưng task cohort, fault topology, policy và oracle vẫn do project định nghĩa; contract còn candidate và không có human review. Vì vậy đây là sensitivity result nội bộ, không phải native benchmark reproduction, confirmatory result hay external validation [[journal/2026-09-28-secondary-varied-schedule-replication]].

## 6. Discussion

### 6.1 Trả lời RQ trong phạm vi controlled study

Với accurate failure-domain metadata và targeted common-mode silent failures, mandatory provenance-independent `K=2` verification giảm unsafe irreversible actions so với random-source `K=2` verification mà không làm giảm clean correctness trong benchmark hiện tại. Kết quả không cho thấy advantage dưới independent faults, phù hợp hypothesis đã scoped.

### 6.2 Tại sao kết quả không có nghĩa “provenance luôn tốt hơn”?

Provenance chỉ giúp khi:

- tools có shared failure domains;
- metadata mô tả đúng topology;
- có independent corroborator khả dụng;
- unsafe acceptance đắt hơn abstention/escalation;
- runtime thật sự enforce verification trước side effect.

Nếu metadata sai, selector có thể tự tin chọn same-domain source. Nếu independent source cũng bị leakage, conflict signal suy yếu. Nếu escalation rất đắt, conservative blocking có thể làm expected utility xấu hơn.

### 6.3 Ý nghĩa Software Engineering

Kết quả gợi ý tool registry không chỉ nên chứa name, description và JSON schema. Một reliability-aware registry có thể cần backend identity, caching layer, replica group, update path hoặc evidence lineage. Tuy nhiên nghiên cứu này chưa giải quyết cách derive hoặc maintain metadata đó. GRADE và AgentFlow cho thấy dependency recovery là một research area riêng, không phải chi tiết triển khai nhỏ.

## 7. Threats to Validity

### 7.1 Construct validity

`failure_domain_id` là abstraction do benchmark định nghĩa. Nó không biểu diễn đầy đủ partial dependence, time-varying dependencies, probabilistic correlation hoặc cascading failures ngoài thực tế.

Unsafe refund và final-state correctness là metrics rõ nhưng domain-specific. Chúng không tự động đại diện cho harm severity ở email, infrastructure, healthcare hoặc coding agents.

### 7.2 Internal validity

Matched `K=2`, paired fault maps và deterministic oracle giảm confounding. Tuy nhiên random-K thất bại chính xác khi chọn same-domain source, nên effect có thể được coi là direct consequence của constructed topology. Đây là intended mechanism test, không phải natural prevalence estimate.

### 7.3 External validity

Main tasks cùng xuất phát từ một synthetic support workflow. Full live-agent gate fail experimental validity. EnvTrustBench chưa executable, còn Agent-SafetyBench/WorkBench không có native correlated-failure design. Audit 12 cases làm tăng semantic breadth khả dụng cho experiment tiếp theo, nhưng source topology vẫn synthetic. Kết quả chưa generalize sang production agents, models hoặc tools.

### 7.4 Metadata validity

Main claim giả định accurate failure-domain metadata. Robustness experiment bác bỏ broad claim với arbitrary imperfect metadata. Nghiên cứu không cung cấp metadata discovery/calibration method.

### 7.5 Statistical conclusion validity

Bootstrap cluster theo 30 tasks, không theo 150 episodes độc lập, để tránh pseudo-replication từ five seeds. Tuy vậy 30 tasks và six strata vẫn nhỏ; CI không phải proof of practical generalization hoặc novelty.

### 7.6 Secondary case-review provenance and protocol deviation

Hai vòng secondary case review do một AI khác hỗ trợ theo yêu cầu của một researcher duy nhất; **không có independent human reviewer hoặc peer review**. Các verdict có trích dẫn code/trace giúp phát hiện lỗi thiết kế, nhưng không thể tự xác nhận semantic correctness. Amendment [[synthesis/Protocol Amendment: Exploratory Secondary Runtime Matrix]] công khai deviation và hạ run xuống exploratory/internal; amendment không thay thế human review. Không dùng kết quả này như confirmatory hoặc external-validation evidence. Cần human audit độc lập trước khi đưa claim mạnh hơn. [[journal/2026-09-20-ai-review-provenance-correction]]

## 8. Reproducibility

Core experiment không cần model training, GPU hoặc paid API. Main và robustness runs chạy deterministic trên CPU. Artifact lưu:

- frozen task manifests và hashes;
- raw per-episode JSONL;
- run manifests;
- policy/fault metadata;
- automated invariant tests;
- analysis scripts và bootstrap outputs.

Các artifact paths và current status được theo dõi tại [[synthesis/Protocol: Action-Boundary Provenance Verification Main Study]], [[journal/2026-09-15-action-boundary-main-study]] và [[journal/2026-09-15-imperfect-provenance-robustness-gate]].

## 9. Conclusion — PROVISIONAL

Controlled evidence cho thấy gọi hai tool khác tên không bảo đảm hai pieces of evidence độc lập. Khi common-mode silent corruption tác động các interfaces cùng failure domain, random cross-check có thể củng cố một kết luận sai. Chọn corroborator từ independent failure domain tại mandatory action boundary loại bỏ unsafe refunds trong main controlled setting, với cùng `K=2` và không giảm clean correctness. Tuy nhiên advantage phụ thuộc mạnh vào metadata correctness và chưa được xác nhận trên external executable benchmark. Kết luận phù hợp hiện tại là một scoped empirical result, không phải một production-ready solution hoặc confirmed novelty claim.

## References — working list

- Alvarez, A., et al. (2026). *ProvenanceGuard: Source-Aware Factuality Verification for MCP-Based LLM Agents*. https://arxiv.org/abs/2606.18037
- Huai, Z., Yang, H., & Li, X. (2026). *Which Tool Response Should I Trust? Tool-Expertise-Aware Chest X-ray Agent with Multimodal Agentic Learning*. https://arxiv.org/abs/2602.21517
- Kim, et al. (2025). *Correlated Errors in Large Language Models*. https://proceedings.mlr.press/v267/kim25e.html
- Knight, J. C., & Leveson, N. G. (1986). *An Experimental Evaluation of the Assumption of Independence in Multiversion Programming*. https://doi.org/10.1109/TSE.1986.6312924
- Liu, H., et al. (2024). *Uncertainty Calibration for Tool-Using Language Agents*. https://aclanthology.org/2024.findings-emnlp.978/
- She, Y., Liang, Y., & Kang, E. (2026). *Safeguarding LLM Agents from Misalignment through Provenance Analysis*. https://arxiv.org/abs/2607.01236
- Sheng, S., Wang, Z., & Zhou, L. (2026). *When Agents Overtrust Environmental Evidence: An Extensible Agentic Framework for Benchmarking Evidence-Grounding Defects in LLM Agents*. https://arxiv.org/abs/2605.08828
- Zhao, Y. (2026). *GRADE: Graph Representation of LLM Agent Dependency and Execution*. https://arxiv.org/abs/2606.22741
- *RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection*. https://arxiv.org/abs/2603.02345
- *Reason Less, Verify More: Deterministic Gates Recover a Silent Policy-Violation Failure Mode in Tool-Using LLM Agents*. https://arxiv.org/abs/2607.07405
- *Robustness Analysis of Agentic AI to Inconsistent and Incomplete Tool Responses*. https://arxiv.org/abs/2608.22676
- *Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures*. https://arxiv.org/abs/2608.02645

## Writing status

| Section             | Status                   | Evidence gate còn thiếu                         |
| ------------------- | ------------------------ | ----------------------------------------------- |
| Abstract            | Provisional              | external-validity decision và final claim audit |
| Introduction        | Draft complete           | supervisor feedback                             |
| Related Work        | Draft complete           | formal citation-chain audit                     |
| Problem Formulation | Draft complete           | notation cleanup                                |
| Methodology         | Draft complete           | independent reproduction audit                  |
| Results             | Current results inserted | final figures/tables                            |
| Discussion          | Draft                    | Human case audit, supervisor review, independent task/topology replication |
| Threats to Validity | Draft complete           | supervisor review                               |
| Conclusion          | Provisional              | final RQ decision                               |

## Related vault notes

- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]]
