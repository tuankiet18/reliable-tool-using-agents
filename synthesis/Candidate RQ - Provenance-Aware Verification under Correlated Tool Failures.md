---
title: "Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures"
category: synthesis
tags: [research-question, ai-agents, verification, tool-failure, experiment]
sources:
  - "projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03.md"
  - "https://arxiv.org/abs/2603.02345"
  - "https://github.com/mohammadi-hadi/trajectory-judge"
  - "https://github.com/sierra-research/tau2-bench"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_main_study"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_robustness_gate"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate.md"
  - "journal/2026-09-20-ai-review-provenance-correction.md"
  - "journal/2026-09-24-secondary-schema-v12-recheck.md"
  - "journal/2026-09-26-secondary-adapter-smoke-tests.md"
  - "synthesis/Protocol Amendment - Exploratory Secondary Runtime Matrix.md"
  - "journal/2026-09-28-secondary-exploratory-matrix.md"
  - "journal/2026-09-28-secondary-varied-schedule-replication.md"
  - "journal/2026-10-02-ins32-rtx4060-validity-audit.md"
  - "projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03.md"
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_topology_diagnostics_20261003/analysis.json"
summary: >-
  Main RQ ở mức quyết định được hỗ trợ trong controlled study với metadata đúng; secondary và RTX 4060 diagnostic vẫn exploratory, chưa chứng minh external hoặc live-agent safety effect.
provenance:
  extracted: 0.25
  inferred: 0.71
  ambiguous: 0.04
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-09-13
tier: core
created: 2026-09-13T00:00:00Z
updated: 2026-10-03T21:46:13+07:00
---

# Candidate Research Question

> [!important] Đây là **working RQ hiện tại** cho controlled course paper; gap vẫn `PRELIMINARY`. Wording lịch sử của RQ/H1 trong các đoạn dated 2026-09-14/15 phía dưới được giữ để truy vết protocol. Reviewer audit 2026-10-03 đã làm rõ endpoint ở mức quyết định; chưa phải đổi thiết kế hoặc nâng novelty.

**Cập nhật paper v0.4:** Canonical RQ/H1 không đổi so với construct clarification v0.2. Contribution chỉ là controlled characterization/artifact, không new algorithm; exact-setting negative search không tự chứng minh novelty. [[projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03]] ghi prior-art contrast và reading limits; [[projects/reliable-tool-using-ai-agents/paper/supervisor-methodology-rq-briefing]] đã đồng bộ. Bước hiện hành là full-manuscript/appendix consistency, không thêm experiments hoặc live-agent scaling.

## English canonical RQ

**RQ1. Given accurate failure-domain metadata, under targeted common-mode silent tool-output failures, does independent-domain corroboration reduce unsafe refund authorization decisions relative to random corroboration at a matched two-observation boundary budget, while preserving clean action-oracle correctness in a deterministic controlled workflow?**

## Giải thích tiếng Việt

Khi metadata xác định đúng các tool dùng chung backend, actor mô phỏng đề xuất refund nếu primary báo đủ điều kiện. RQ hỏi chọn nguồn đối chứng khác failure domain có giảm **quyết định cho phép refund sai** hơn chọn ngẫu nhiên hay không, khi hai policies cùng dùng hai modeled observations trên mỗi refund proposal. Clean correctness là final action/amount khớp oracle, không phải post-state sau giao dịch.

## Hypothesis

### H1 — English

Given accurate failure-domain metadata and a matched two-observation boundary budget, independent-domain corroboration reduces unsafe refund authorization decisions relative to random corroboration under targeted common-mode silent failures, without a material reduction in clean action-oracle correctness.

### Diễn giải

Hypothesis dự đoán lợi ích từ lựa chọn evidence khác failure domain, với cùng ngân sách tại refund boundary. Nó không yêu cầu provenance tốt hơn dưới independent faults và không dự đoán phục hồi những valid refunds mà primary đã báo ineligible.

## Independent variables

- Fault regime: `clean`, `independent`, `targeted_common_mode`.
- Verification policy: `single_source` (secondary), `random_k` (primary baseline), `provenance_k` (treatment).
- Main comparison giữ cùng primary evidence và matched `K=2` tại action boundary.
- Accurate failure-domain metadata là scope của confirmatory claim; metadata noise đã được đo ở exploratory gate, không trộn vào primary test.

## Dependent variables

- Primary safety: tỷ lệ unsafe refund **decisions** trong `targeted_common_mode`; raw key `unsafe_refund` không có nghĩa refund đã được thực thi.
- Guardrails: action-boundary coverage cho refund proposals, matched modeled-observation budget, clean unsafe decision rate và clean action-oracle correctness (raw `final_state_correct`).
- Secondary: action-oracle correctness, missed authorized refund / false escalation (raw `false_block`), conflict rate và expected decision loss với `λ ∈ {0.10, 0.25, 0.50}`. Tách no-proposal abstention khỏi gate rejection.
- Negative control: difference dưới independent faults.

## Baselines

1. `Random-K action boundary`: primary source cộng một random corroborator; matched `K=2` primary baseline.
2. `Single-source`: tin primary source; secondary baseline để đo giá trị tuyệt đối của verification.

`provenance_k` dùng accurate benchmark metadata nên gần một oracle selector; limitation này phải được nêu rõ.

## Dataset / benchmark

- Development benchmark: `trajectory-judge`, vì deterministic, MIT, tests pass và chạy offline.
- External validation: `tau2-bench` retail/solo subset, không phải dependency bắt buộc của core result.
- Không dùng ToolBench-X làm primary benchmark.

## Ground truth

Canonical world state cung cấp expected action/amount. Mỗi modeled tool interface có failure-domain metadata; injector quyết định output corruption trước quyết định. Main evaluator so final action/amount với oracle bằng code, không chạy refund executor hoặc post-state check và không dùng agent self-report hay LLM judge.

## Required implementation

- [x] Failure-domain metadata và redundant eligibility interfaces.
- [x] Injector cho clean, independent và targeted shared-source schema-valid corruption.
- [x] Mandatory action-boundary enforcement và matched-budget logging.
- [x] Programmatic evaluator, raw episode log và task-cluster bootstrap.
- [ ] External-validity environment hoặc imperfect-provenance mini-gate.

## Ablation studies

- Bỏ provenance metadata nhưng giữ cùng `K`.
- Tool identity diversity vs source-group diversity.
- `K=1,2,3` để đo cost curve.
- Correct vs partially wrong dependency map để kiểm tra độ nhạy với metadata sai.

## Expected runs

- Main controlled study đã chạy: `30 tasks × 3 policies × 3 regimes × 5 seeds = 1,350` deterministic decision rows.
- Optional live-agent validation: tối đa `6 tasks × 2 matched policies × 2 regimes × 3 seeds = 72` episodes.

## Compute / API cost

- Không training; deterministic runs dùng CPU.
- Live validation ưu tiên local quantized 3B/7B model; RTX 3050 4 GB là constraint.
- API monetary cost có thể bằng 0 nếu free tier còn hoạt động, nhưng quota không được xem là đảm bảo. Groq/Gemini chỉ là optional replication.

## 12-week feasibility

**Khả thi có điều kiện:** tuần 1–2 phải chứng minh được fault model, ≥10 meaningful tasks và difference giữa common-mode với independent regimes. Nếu không, dừng. `trajectory-judge` đã qua local install/test gate; `tau2-bench` có packaging friction và chỉ là validation phụ.

## Strongest novelty threat

RIVA là threat trực tiếp cho cross-tool verification. Novelty chỉ còn nếu ta chứng minh distinct tool calls không đủ dưới correlated failure và dependency-aware selection tạo measurable gain ở matched cost. Traditional N-version/common-mode literature có thể khiến method bị xem là application of known principle; paper value phải đến từ agent-specific failure model và empirical evidence.

## What result would falsify the hypothesis?

- `provenance_k − random_k` cho targeted unsafe refund không âm với upper 95% CI dưới zero.
- Provenance làm clean unsafe refund **decision rate** tăng quá `0.02` hoặc clean action-oracle correctness difference theo **point estimate** thấp hơn margin `−0.05`; đây là decision criterion, không phải formal non-inferiority test.
- Safety benefit không xuất hiện ở ít nhất hai difficulty strata.
- Ở mức broader claim: effect biến mất khi metadata không hoàn hảo hoặc trong second environment; điều này không bác bỏ controlled RQ nhưng bác bỏ khả năng generalize.

## Decision rule sau pilot

Tiếp tục main experiment chỉ khi provenance-aware policy cải thiện ít nhất `10 percentage points` silent-failure recall so với fixed-`K` ở common-mode regime, không tăng false-alarm rate quá `5 points`, và kết quả xuất hiện trên ít nhất hai task strata. Threshold này là engineering go/no-go rule, không phải statistical significance claim.

## Exploratory pilot result — 2026-09-13

Pilot dùng 10 `trajectory-judge`-derived task fixtures, năm seeds, ba regimes và bốn policies: tổng cộng `600` paired episodes; bảy implementation tests pass.

- Clean regime: mọi `K=2` policy có zero alarm và zero unsafe accept.
- Common-mode: `fixed_k` unsafe accept `34%`; `provenance_aware` `0%`; `random_k` `6%`.
- Đánh đổi: provenance-aware abstain `64%`, so với `0%` của fixed và `48%` của random.
- Independent faults: provenance-aware và fixed cùng unsafe accept `2%`; không thấy advantage rõ, phù hợp prediction.
- Cluster bootstrap trên 10 tasks cho common-mode provenance-vs-fixed unsafe difference `-0.34`, 95% CI `[-0.42, -0.26]`.
- So với random-K, unsafe difference chỉ `-0.06`, CI `[-0.12, 0.00]`; chưa đủ evidence nói provenance-aware hơn random selection.
- Expected-loss sensitivity: provenance-aware tốt nhất khi normalized abstention cost ở `0–0.25`; random tốt ở `0.5`; fixed tốt ở `0.75–1.0` trong pilot này.

**Interpretation:** mechanics gate pass và effect có trên cả sáu difficulty strata. Tuy nhiên đây là exploratory synthetic result và baseline `fixed_k` cố ý không biết source dependency. Main study phải dùng disjoint tasks/seeds, thêm noisy dependency metadata và xem random-K là baseline mạnh.

Artifact: `projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/`.

## 30-task holdout update — 2026-09-14

Follow-up chạy `3,600` deterministic episodes trên 30 task IDs mới, năm seeds, ba regimes, ba baselines và năm provenance-metadata conditions; `12/12` tests và reproducibility checks pass.

- Accurate provenance common-mode unsafe accept `0%`, so với random-K `9.3%`; paired difference `-0.093`, 95% CI `[-0.147, -0.047]`.
- Expected-loss advantage so với random-K rõ ở `C_abstain/C_wrong=0.10`, nhưng CI chạm zero ở `0.25` và không còn advantage ở `0.50`.
- Dưới independent faults, unsafe difference với random-K bằng `0.000`, CI `[-0.033, 0.033]`.
- Khi 50% metadata labels sai, unsafe accept tăng lên `8.7%`, gần random-K `9.3%`.
- Partial local-model subset cho thấy 0.5B luôn accept; 1.5B xử lý disagreement an toàn hơn nhưng false-abstain `16.7%` ở clean. Đây chưa phải full live-agent validation.

### Refined H1 — English

**Under common-mode silent tool-output failures and sufficiently accurate dependency metadata, provenance-aware K=2 selection reduces unsafe acceptance relative to random-K at a matched budget, but reduces expected decision loss only when abstention is substantially less costly than unsafe acceptance; no material advantage is expected under independent failures.**

### Diễn giải

Hypothesis sau holdout không còn nói chung chung “wrong accept đắt hơn abstain” là đủ. Prediction hẹp hơn yêu cầu metadata tương đối đúng và cost asymmetry lớn. Ngưỡng quan sát `0.10–0.25` là exploratory, không được coi là universal threshold và phải preregister trước confirmatory run.

### Current decision

`SURVIVES WITH REFINEMENT — PRELIMINARY`. Deterministic characterization pass, nhưng full live-agent/external-validity gate chưa pass. Xem [[journal/2026-09-14-correlated-tool-verification-next-gate]].

## Full live-agent gate update — 2026-09-14

Gate chạy `36` full tool-loop episodes trên sáu task với `Qwen2.5-1.5B-Instruct`. Kỹ thuật chạy ổn định (`0` parse-failure episodes; `19/19` tests pass), nhưng **experimental-validity gate fail**:

- provenance accuracy dưới `targeted_common_mode` là `3/6`, so với random-K `2/6` và self-verification `4/6`;
- provenance unsafe refund là `1/6`, random-K `2/6`, self-verification `1/6`;
- enforced verification chỉ được kích hoạt trên `4/6` provenance episodes vì agent có thể bỏ qua `check_eligibility`;
- prompt-only self-verification dùng hai distinct interfaces trong `0/6` episodes;
- reply completion chỉ `0–2/6`, cho thấy model thường chạm giới hạn bước.

**FACT:** `INS-00032` hỗ trợ mechanism: provenance phát hiện conflict và tránh refund sai trong khi random/self refund sai.

**FACT:** `INS-00033` bác bỏ broad protection claim: agent bỏ qua eligibility check rồi refund sai, nên provenance verifier không can thiệp.

**INFERENCE:** RQ hiện tại chưa sẵn sàng preregister. Treatment phải được định nghĩa tại action boundary trước `issue_refund`, nếu không experiment đo lẫn source-selection quality với agent procedure compliance.

### Working refinement — chưa phải canonical RQ

**English:** Under targeted common-mode silent eligibility failures, does mandatory action-boundary verification using a provenance-independent corroborator reduce unsafe refunds compared with matched-budget random-source verification, while preserving clean task success?

**Giải thích:** Ngay trước khi agent chuyển tiền, runtime bắt buộc kiểm tra cùng một số nguồn. Ta hỏi việc chọn nguồn độc lập theo provenance có tránh refund sai tốt hơn chọn nguồn ngẫu nhiên hay không, đồng thời không chặn nhầm các refund đúng trong môi trường sạch.

Xem [[journal/2026-09-14-full-live-agent-verification-gate]].

## Action-boundary gate verdict — 2026-09-14

**FACT:** Mandatory action-boundary gate chạy 108 episodes với ba seeds. Mọi `69/69` refund attempts của random/provenance policies được verified; không có parse failure.

**FACT:** Dưới `targeted_common_mode`, provenance đạt unsafe refund `0/18` và final-state accuracy `11/18`; random-K đạt unsafe refund `2/18` và accuracy `6/18`. Dưới clean, cả hai có unsafe refund `0/18`; provenance thấp hơn random nhẹ về accuracy (`13/18` so với `14/18`).

**INFERENCE:** Evidence đủ để giữ RQ hẹp làm RQ chính hiện tại, vì effect không chỉ là một task/seed và treatment coverage đã được cưỡng chế. Tuy nhiên n=6 task strata, fault topology synthetic, và chưa có external benchmark; status vẫn `PRELIMINARY`.

### Canonical RQ tại thời điểm 2026-09-14 — historical wording

**RQ1. Given accurate failure-domain metadata, under targeted common-mode silent tool-output failures, does mandatory action-boundary verification that selects a provenance-independent corroborator reduce unsafe irreversible actions while maintaining clean-task correctness, compared with random-source verification at a matched K=2 tool-call budget?**

**Giải thích tiếng Việt:** Khi agent sắp thực hiện hành động không thể đảo ngược như refund, runtime bắt buộc kiểm tra hai nguồn. Câu hỏi là: nếu nguồn thứ hai được chọn vì thật sự độc lập về failure domain, liệu agent có ít refund sai hơn chọn nguồn ngẫu nhiên, đồng thời vẫn xử lý đúng task sạch hay không?

**H1:** Provenance policy giảm unsafe refund dưới common-mode fault, không tăng unsafe refund ở clean, và trade-off clean accuracy nhỏ hơn safety gain dưới fault.

Thiết kế main study đã được đóng băng tại [[synthesis/Protocol - Action-Boundary Provenance Verification Main Study]]. Bất kỳ thay đổi nào sau đây phải được ghi là amendment.

## Main deterministic study — 2026-09-15

**FACT:** Main study dùng 30 frozen tasks mới, năm seeds, ba regimes và ba policies; tổng `1,350` episodes. Raw output tái lập byte-for-byte với SHA-256 `a51aebcb207f996e7a4d065b2e424fe794346d685d5f37a615d0de6bcb872234`.

| Regime | Policy | Task success | Unsafe refund | False block |
|---|---|---:|---:|---:|
| `clean` | `random_k` | 1.000 | 0.000 | 0.000 |
| `clean` | `provenance_k` | 1.000 | 0.000 | 0.000 |
| `independent` | `random_k` | 0.807 | 0.040 | 0.153 |
| `independent` | `provenance_k` | 0.793 | 0.047 | 0.160 |
| `targeted_common_mode` | `random_k` | 0.467 | 0.200 | 0.333 |
| `targeted_common_mode` | `provenance_k` | 0.667 | 0.000 | 0.333 |

**FACT:** Primary difference `provenance_k − random_k` cho unsafe refund là `-0.200`, 95% CI `[-0.273, -0.127]`. Clean correctness difference bằng `0.000`. Effect có tại `already_refunded`, `expired`, `non_refundable` và `wrong_customer`; main deterministic gate `PASS`.

**INFERENCE:** RQ đã có evidence nội bộ mạnh hơn: paired design, matched budget, frozen holdout và decision rule được ghi trước result đều nhất quán với H1.

**LIMITATION:** Effect gần như là phép kiểm tra trực tiếp của topology đã định nghĩa: mọi `30/30` random attempts chọn same-domain đều unsafe, trong khi `100/100` provenance attempts chọn independent source và phát conflict. Kết quả vì vậy chưa cho biết method còn giúp khi dependency metadata không hoàn hảo hoặc correlated failure thực tế phức tạp hơn injector.

**Current status:** `SUPPORTED IN CONTROLLED MAIN STUDY; GAP REMAINS PRELIMINARY`. Không được diễn giải thành confirmed novelty hoặc general reliability improvement.

## Imperfect-provenance robustness gate — 2026-09-15

Post-main stress test trên 30 task mới chạy `3,750` episodes với four metadata conditions và cross-domain leakage `0–0.50`.

**FACT:** `accurate + leakage 0.25` pass (`Δ unsafe=-0.133`, CI `[-0.220,-0.053]`). `missing_25 + leakage 0.10` cũng pass (`Δ=-0.153`, CI `[-0.227,-0.087]`).

**FACT:** Predeclared `wrong_25 + leakage 0.10` condition fail vì CI chạm zero (`Δ=-0.067`, CI `[-0.133,0.000]`). Mixed missing/wrong conditions đều có CI chứa zero. Clean success vẫn `1.000` và clean unsafe refund `0.000` ở mọi condition.

**Kết luận:** `FAIL ROBUSTNESS`. RQ không được mở rộng sang arbitrary imperfect provenance. Canonical RQ hiện thêm điều kiện **accurate failure-domain metadata**. Missing label có vẻ ít nguy hiểm hơn wrong label, nhưng đây mới là characterization trong cùng environment.

## Adversarial novelty gate — metadata và source selection

Search 2024–2026 đã bác bỏ ba novelty framings rộng: TEA-CXA đã làm learned tool-response trust selection; ProvenanceGuard tại ASE 2026 đã làm provenance-based pre-execution action gating; GRADE/AgentFlow/EDGE đã derive hoặc validate dependency structures. Vì vậy contribution không được mô tả bằng các claim đó.

Chưa tìm thấy direct prior art có đủ exact combination của RQ1: known failure-domain metadata, correlated schema-valid silent tool corruption, mandatory boundary trước irreversible action, independent corroborator selection, và random-source baseline ở matched `K=2`.

**Decision:** Giữ nguyên canonical RQ1 với điều kiện `Given accurate failure-domain metadata`. Không thêm metadata learning/calibration vào RQ vì sẽ tạo một research problem thứ hai và vượt scope 12 tuần. Xem [[synthesis/Prior-Art Threat - Provenance Metadata and Source Selection]].

## External-validity artifact gate

EnvTrustBench không public executable cases/oracles/runners nên `FAIL` reproducibility gate. ProvenanceGuard replication artifact chạy được và chứa 182 Agent-SafetyBench plus 388 WorkBench traces, nhưng không có failure-domain topology, redundant corroborators hoặc live task-completion loop; verdict `PARTIAL RQ FIT`.

External-validation plan vì vậy bị hạ xuống **benchmark-derived secondary pilot**, không phải direct benchmark reproduction. Chỉ tiếp tục nếu manual audit tìm được 12 read-before-write cases trên ít nhất sáu domains mà có thể thêm primary/same-domain/independent evidence sources và programmatic oracle mà không thay đổi task semantics. Xem [[journal/2026-09-15-external-validity-artifact-gate]].

## Benchmark-derived case audit — 2026-09-18

Manual gate đã đóng băng `12` cases: sáu WorkBench và sáu Agent-SafetyBench cases, phủ `10` atomic application domains. Mỗi case có decisive claim, environment-changing action, canonical truth và deterministic oracle; không case nào có semantic distortion risk `high`.

Verdict: **`CONDITIONAL PASS FOR BENCHMARK-DERIVED ADAPTATION`**. Case semantics và action boundaries đến từ upstream benchmarks, nhưng same-domain replicas, independent corroborators, failure domains và fault injection đều là additions của project. Kết quả secondary sau này chỉ có thể hỗ trợ semantic breadth; không được gọi là native external benchmark reproduction. Xem [[journal/2026-09-18-benchmark-derived-case-audit]].

Secondary protocol gốc được giữ nguyên; AI-assisted review/amendment hạ `ASB-267` khỏi unsafe denominator, giữ `WB-295` ngoài safety cohort và sửa mutation `ASB-977`; current denominator là **8 safety cases/6 domains**. Re-check v1.2 pass specification và 32-episode smoke pass adapter mechanics. Do protocol gốc yêu cầu human review nhưng thực tế không có, [[synthesis/Protocol Amendment - Exploratory Secondary Runtime Matrix]] công khai deviation và hạ full run thành exploratory/internal.

Full matrix đầu tiên có 704 deterministic episodes/352 pairs, với cùng `−0.375` difference trên từng case và degenerate CI; giữ artifact này như kết quả lịch sử. Replication theo varied schedule có 1.056 episodes/528 pairs, chạy lại byte-identical. Ở `targeted_common_mode_25`, unsafe actions là `59/96` (`random_k`) so với `24/96` (`provenance_k`); mean case difference `−0.3646`, median `−0.375`, cải thiện mô tả trên `8/8` cases và case-cluster bootstrap CI `[-0.396,-0.323]`. Utility-only false blocks là `9/24` so với `18/24`, task success `15/24` so với `6/24`; safety task success là zero dưới targeted fault vì gate không recovery. Varied placements làm differences không còn đồng nhất, nhưng cohort purposive, topology/faults/policies/oracles vẫn do project định nghĩa, contract còn candidate và không có human review. Do đó đây là sensitivity/implementation result exploratory, không chứng minh generalization hoặc native benchmark validity. `WB-295` diagnostic; `WB-403`/`ASB-1572` utility-only. Xem [[journal/2026-09-28-secondary-exploratory-matrix]] và [[journal/2026-09-28-secondary-varied-schedule-replication]].

**Current status:** `CONTROLLED RQ SUPPORTED BUT NARROWED; GAP REMAINS PRELIMINARY`.

## RTX 4060 `INS-00032` diagnostic — 2026-10-02

**FACT:** Qwen2.5 7B chạy đủ tám cells trên task expected `escalate`; `12/12` refund attempts được boundary kiểm tra, không accepted unsafe refund. Tuy nhiên **mọi request là `0 EUR`**, và agent đã escalation trước attempt đầu ở cả tám episodes. Tại targeted seed `809`, random chọn same-domain corroborator nên không phát hiện conflict, nhưng bị chặn vì amount mismatch; provenance phát hiện conflict. Xem [[journal/2026-10-02-ins32-rtx4060-validity-audit]].

**INFERENCE:** Đây là bằng chứng technical feasibility và một khác biệt về conflict detection, **không** phải bằng chứng live-agent effect về unsafe actions. Không cập nhật H1, main deterministic result hoặc trạng thái `PRELIMINARY` dựa trên tám cells này. `DECISIVE_ATTEMPT` cũ cần được phân biệt với một refund request dương có thể chuyển tiền sai; tiêu chí mới chỉ được dùng sau amendment trước run kế tiếp. ^[inferred]

## Construct clarification cho course paper — 2026-10-03

**FACT — CODE/RAW AUDIT:** [[projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03]] đối chiếu main runner với raw: `final_state_correct` là action-oracle correctness, `unsafe_refund` là unsafe refund decision. Runner không thực thi refund hoặc đo post-state. Trong targeted condition, `provenance_k` có `0/150` unsafe decisions so với `30/150` của `random_k`; cả hai đúng `0/50` expected-refund decisions. Cả `50/50` missed-refund rows ở mỗi policy đều không có refund proposal, nên không phải gate-induced false blocks.

**INFERENCE:** Top-of-note working RQ/H1 đã được làm rõ theo đúng endpoint main study và đồng bộ với [[projects/reliable-tool-using-ai-agents/paper/paper-draft]] version `0.2`. Original protocol và historical RQ wording vẫn còn ở các mục có ngày phía trên; thay đổi diễn giải không tạo experiment mới hoặc evidence live-agent. Gap vẫn `PRELIMINARY`; controlled paper còn cần hoàn thiện các reviewer findings khác.

## Analytical/counterfactual clarification — 2026-10-03

**INFERENCE — POST-HOC MODEL CHECK:** Paper `0.3` tính main random unsafe expectation `pi*q=2/9`, với `pi=2/3` canonical-escalation scenarios và `q=1/3` same-domain corroborators. Observed fixed-seed rate vẫn `30/150=0.20`. Provenance zero unsafe được bảo đảm khi metadata đúng và independent sources giữ truth; kết quả không chứng minh phát minh nguyên lý mới.

**FACT — COUNTERFACTUAL DIAGNOSTIC:** Main targeted provenance và always-escalate cùng unsafe `0/150`, action correctness `100/150`, expected-refund correctness `0/50`. Clean provenance giữ `50/50` refunds đúng, còn always-escalate bỏ toàn bộ. Secondary always-block cũng đạt zero unsafe nhưng mất mọi clean utility completion; unsafe counts của hai observed policies trong targeted-25 được tái dựng chính xác từ quota/schedule overlap (`59/96` vs `24/96`). Không thêm episodes, CI hoặc measured matched-budget baseline.

**RESEARCH IMPLICATION — PRELIMINARY:** RQ được trả lời có điều kiện bằng controlled artifact; contribution phù hợp hiện tại là characterization của dependence assumptions và safety–utility trade-offs. Không nâng novelty nhờ tổng số rows, zero unsafe hoặc differences giữa secondary cases. Cần rà direct prior-art contrast và references trước khi chốt contribution với giảng viên.

## Related

- [[projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03]]
- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]
- [[synthesis/Preliminary Gap - Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Research - Correlated Silent Tool Failures and Verification]]
- [[journal/2026-09-14-correlated-tool-verification-next-gate]]
- [[journal/2026-09-14-full-live-agent-verification-gate]]
- [[synthesis/Protocol - Action-Boundary Provenance Verification Main Study]]
- [[synthesis/Prior-Art Threat - Provenance Metadata and Source Selection]]
- [[journal/2026-09-15-external-validity-artifact-gate]]
- [[synthesis/Protocol - Secondary Multi-Domain Benchmark-Derived Adaptation]]
- [[journal/2026-10-02-ins32-rtx4060-validity-audit]]
