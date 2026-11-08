---
title: "Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures"
category: synthesis
tags: [research-gap, ai-agents, verification, tool-failure, reliability]
sources:
  - "projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03.md"
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "https://arxiv.org/abs/2603.02345"
  - "https://proceedings.mlr.press/v267/kim25e.html"
  - "https://doi.org/10.1109/TSE.1986.6312924"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_robustness_gate"
summary: >-
  PRELIMINARY gap: controlled main gate pass, nhưng robustness gate fail khi 25% provenance labels sai; chỉ claim accurate/conservatively incomplete metadata còn sống.
provenance:
  extracted: 0.43
  inferred: 0.52
  ambiguous: 0.05
base_confidence: 0.71
lifecycle: draft
lifecycle_changed: 2026-09-13
tier: core
created: 2026-09-13T00:00:00Z
updated: 2026-10-03T21:46:13+07:00
---

# PRELIMINARY Gap — Provenance-aware verification dưới correlated tool failures

> [!important] Trạng thái hiện hành — 2026-10-03
> `SURVIVES WITH REFINEMENT — PRELIMINARY`, không confirmed novelty. Paper v0.4 là controlled characterization của **refund authorization decisions**, không new algorithm hoặc executed-transaction safety. Hypothesis/variables/baselines phía dưới giữ hồ sơ discovery ban đầu, **không** current measured endpoints. Working RQ/H1 ở [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]; citation limits ở [[projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03]]. Không reproduce RIVA hoặc chạy head-to-head: “RIVA-style” dưới đây chỉ historical inspiration, không implementation-equivalent baseline. Main benefit gần by-construction với accurate metadata; targeted valid-refund correctness vẫn `0/50` ở hai policies; live-agent effect chưa đo được và đã dừng scaling.

## Gap statement

Các method cross-tool verification hiện có, điển hình là RIVA, dùng nhiều distinct diagnostic paths nhưng chưa đo xem các path có thật sự độc lập về data source/failure mechanism hay không. Chưa tìm thấy evaluation so sánh fixed-`K` cross-validation với selector chọn evidence từ distinct failure domains dưới controlled common-mode silent corruptions và cùng tool-call budget.

## Evidence

- RIVA cải thiện reliability bằng cross-validation nhưng dựa trên independence intuition.
- RIVA cũng cho thấy tăng `K` có thể làm performance collapse khi verification paths khan hiếm.
- Knight–Leveson (1986) cho thấy independence assumption trong multiversion programming không tự động đúng.
- `Correlated Errors in Large Language Models` cho thấy shared architecture/provider liên quan đến correlated errors; đây là analogous evidence, không phải direct tool evidence.

## Vì sao current methods chưa đủ?

Distinct tool names hoặc commands chỉ cho biết interface khác nhau. Chúng không cho biết output được lấy từ database, cache, API provider hoặc telemetry collector nào. Majority/cross-validation có thể biến một shared-source error thành false confidence.

## Candidate hypothesis

### H1 — English

When unsafe acceptance is more costly than abstention, provenance-aware selection of corroborating tools from distinct failure domains reduces expected decision loss under common-mode silent tool-output failures compared with fixed-K and random-K selection at a matched tool-call budget.

### Diễn giải

Khi nhiều tool có thể cùng sai vì chia sẻ backend và việc tin nhầm gây hậu quả lớn, selector ưu tiên evidence từ failure domains khác nhau được kỳ vọng giảm tổng loss. Hypothesis không nói policy này luôn tốt hơn: abstention quá đắt có thể đảo ngược kết quả.

## Variables và baselines

- Independent variables: fault regime (`none`, `independent`, `common-mode`), selector (`single`, `fixed-K`, `random-K`, `provenance-aware`, `oracle`), budget `K`.
- Dependent variables: detection precision/recall/F1, false-alarm rate, undetected-corruption rate, task success khi có live agent, extra tool calls, latency.
- Baselines: trust first tool; RIVA-style fixed `K=2`; random `K=2` matched budget; oracle independent-source selector.

## Ground truth

Canonical environment state quyết định value đúng. Fault injector lưu `source_id`, `dependency_group`, corruption type và affected calls. Ground truth là **by construction**, không dùng LLM judge để quyết định tool output đúng/sai.

## Minimum viable experiment

Mở rộng `trajectory-judge` bằng redundant read interfaces và source-dependency map; inject cùng một plausible wrong value vào toàn bộ tool thuộc một group. Chạy four selectors trên 20–30 task templates, ba fault regimes và nhiều seeds. External validation trên subset `tau2-bench` chỉ thực hiện sau pilot.

## Expected contribution

1. Một controlled fault model cho independent vs common-mode silent tool corruptions.
2. Evidence thực nghiệm về khi nào fixed-`K` cross-validation thất bại.
3. Một provenance-aware selector đơn giản và cost-matched comparison.

## Threats to validity

- Source dependency graph do benchmark định nghĩa có thể quá sạch so với production.
- Redundant tools thêm vào synthetic environment có thể thiếu realism.
- Nếu policy chỉ đọc metadata rồi chọn group khác, method có thể bị xem là engineering hiển nhiên; contribution phải đến từ rigorous characterization, controlled baselines và generalization.
- Small local model có thể fail vì reasoning, che mất effect của verification.

## What could invalidate this gap?

- Tìm thấy paper đã inject correlated/shared-backend tool corruptions và dùng dependency-aware verifier selection.
- RIVA implementation thực tế đã track underlying source dependencies dù paper không mô tả.
- Fixed-`K` và provenance-aware không khác nhau khi matched budget.
- Benchmark không thể tạo redundant sources có ecological validity.
- Effect chỉ tồn tại trong scripted agent nhưng mất trên live tool-using agents.

## Three-month feasibility

**Có điều kiện.** Core experiment không cần training và có thể chạy offline. Scope phải giới hạn ở read-only facts, 2–3 dependency groups và tối đa hai domains. Nếu đến cuối tuần 2 không tạo được ≥10 task với meaningful redundant sources, bỏ gap thay vì tiếp tục mở rộng benchmark.

## Status

`SURVIVES WITH REFINEMENT — PRELIMINARY`; không phải confirmed novelty.

## Exploratory pilot update

Pilot 600 paired episodes cho thấy mechanism tồn tại nhưng đồng thời làm gap hẹp hơn:

- provenance-aware giảm common-mode unsafe accept từ `34%` xuống `0%` so với fixed-K;
- đổi lại abstention tăng lên `64%`;
- so với random-K, difference nhỏ hơn và cluster-bootstrap CI chạm `0`;
- expected winner thay đổi theo relative abstention cost.

Do đó contribution tiềm năng không phải “provenance luôn tốt”, mà là đo và tối ưu **unsafe-acceptance–abstention trade-off** dưới correlated faults. Evidence hiện chưa đủ để nâng status.

## 30-task adversarial update

Holdout 30 task làm gap hẹp thêm:

- Accurate provenance giảm common-mode unsafe acceptance so với random-K với CI không chạm zero.
- Expected decision loss chỉ tốt hơn random-K rõ ở normalized abstention cost `0.10`; tại `0.25` CI đã chạm zero.
- Wrong metadata làm true-source diversity và safety gain suy giảm; ở `wrong_50`, policy gần như random-K.
- Independent-fault comparison không cho thấy advantage, đúng với scoped hypothesis.
- Partial local-model check cho thấy selector đúng chưa đủ: 0.5B không thực hiện abstention, còn 1.5B có false abstention trong clean tasks.

**RESEARCH GAP CANDIDATE:** Phần còn sống không phải một selector đơn giản, mà là rigorous characterization của ba-way interaction giữa correlated faults, provenance quality và relative abstention cost, kèm externally enforced runtime decision. Đây vẫn có nguy cơ bị xem là application của common-mode/N-version principles nếu không có realistic live-agent evidence.

## Full live-agent adversarial update

Full gate không xác nhận gap. Trên 36 episodes, provenance có một positive example rõ (`INS-00032`) nhưng cũng có counterexample (`INS-00033`) nơi agent bỏ qua eligibility verification rồi refund sai. Prompt-only self-verification không lần nào dùng hai distinct interfaces, còn enforced policy chỉ có `4/6` eligibility coverage dưới fault.

**INFERENCE:** “Chọn independent source tốt hơn” chưa đủ thành một agent method nếu điểm kiểm tra là optional. Candidate chỉ còn hợp lý khi runtime bắt buộc verification ở action boundary trước side effect.

**OPEN QUESTION:** Mandatory action-boundary verification có giữ được clean utility và tạo difference ổn định giữa provenance-independent và random-source corroboration hay không?

**Status:** `SURVIVES WITH REFINEMENT — PRELIMINARY`, nhưng gate hiện tại là `FAIL EXPERIMENTAL VALIDITY`; không nâng confidence và không gọi là externally validated.

## Main-study adversarial update

Preregistered deterministic gate đã `PASS`: provenance giảm targeted common-mode unsafe refund từ `0.200` xuống `0.000` so với random-K, 95% CI của paired difference `[-0.273, -0.127]`, không giảm clean correctness, và effect xuất hiện ở bốn difficulty strata. Independent negative control không cho thấy advantage rõ.

Tuy nhiên main result đồng thời làm lộ novelty threat mạnh nhất: random-K chỉ thất bại ở toàn bộ `30` attempts mà nó chọn cùng `operational_db`; provenance tránh đúng trường hợp này nhờ benchmark cung cấp accurate dependency labels. Do đó **method behavior đã được chứng minh**, nhưng **research contribution chưa được chứng minh**. Nếu không bổ sung realistic/uncertain provenance hoặc second environment, reviewer có thể xem kết quả là hệ quả hiển nhiên của common-mode fault model.

**Status:** `SURVIVES WITH REFINEMENT — PRELIMINARY`. Confidence tăng đối với internal causal claim, không tăng tương ứng đối với novelty và external validity.

## Imperfect-provenance result

Robustness gate cố phá hai giả định của main study: provenance metadata hoàn hảo và independent source không bao giờ nhận cùng corruption. Kết quả tổng thể `FAIL ROBUSTNESS`.

- Accurate metadata vẫn tạo measurable safety gain khi cross-domain leakage tới `0.50` trong sample này.
- Missing `25%` labels vẫn pass condition tại leakage `0.10`; selector fallback `29%` trong refund attempts.
- Wrong `25%` labels không pass condition tại leakage `0.10`: CI chạm zero.
- Mixed `25% missing + 25% wrong` không khác random một cách đáng tin cậy ở bất kỳ leakage level nào.

**RESEARCH IMPLICATION:** Claim “provenance-aware verification robust với imperfect metadata” bị bác bỏ. Claim còn sống là hẹp hơn: known-accurate hoặc conservatively incomplete dependency metadata có thể hỗ trợ source selection dưới controlled common-mode failure.

**OPEN QUESTION:** Có thể xác minh/calibrate provenance metadata đủ tin cậy trước khi dùng nó cho safety decision không? Đây chưa phải gap mới cho tới khi prior-art search riêng được thực hiện.

**Status:** `SURVIVES WITH REFINEMENT — PRELIMINARY`, nhưng scope bị thu hẹp thêm; không được rescue bằng cách đổi threshold hậu kiểm.

## Adversarial prior-art update — provenance metadata và source selection

Search riêng đã tìm thấy direct threats cho các claim rộng:

- [[references/tea-cxa]] đã học tool expertise và chọn response nên tin khi tools mâu thuẫn.
- [[references/provenanceguard-misalignment-provenance-analysis]] đã dùng provenance để chặn proposed tool call trước execution.
- [[references/provenanceguard-source-aware-factuality]] đã làm source-aware verification cho MCP traces.
- [[references/grade-agent-dependency-execution]] và [[references/agentflow-agent-dependency-graphs]] đã derive/grade dependency structure.

Do đó novelty không thể là “dynamic trust selection”, “provenance-aware action gating” hay “dependency validation” nói chung. Chưa tìm thấy direct work kết hợp failure-domain-independent corroboration, targeted common-mode silent tool failures, mandatory irreversible-action boundary và matched `K=2` comparison.

**RESEARCH IMPLICATION:** Exact RQ sống sót ở phạm vi hẹp, nhưng metadata validation không nên được dùng để rescue gap: nó là một bài toán riêng, có prior art mạnh và ground truth khó cho project 12 tuần.

**Status:** `SURVIVES WITH REFINEMENT — PRELIMINARY`; novelty confidence ở mức trung bình, external validity vẫn yếu. Xem [[synthesis/Prior-Art Threat - Provenance Metadata and Source Selection]].

## Related

- [[synthesis/Research - Correlated Silent Tool Failures and Verification]]
- [[synthesis/Candidate RQ - Provenance-Aware Verification under Correlated Tool Failures]]
- [[references/riva]]
- [[journal/2026-09-14-correlated-tool-verification-next-gate]]
- [[journal/2026-09-14-full-live-agent-verification-gate]]
- [[journal/2026-09-15-adversarial-prior-art-provenance-metadata]]
