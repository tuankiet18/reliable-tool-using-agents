---
title: "Research: Early Failure Detection in Tool-Using Agents"
category: synthesis
tags: [ai-agents, failure-detection, runtime-monitoring, prior-art, research]
sources:
  - "https://openreview.net/forum?id=d3Qq4weuwz"
  - "https://arxiv.org/abs/2605.06455"
  - "https://arxiv.org/abs/2605.08715"
  - "https://arxiv.org/abs/2606.05414"
  - "https://arxiv.org/abs/2608.02464"
  - "https://arxiv.org/abs/2608.23670"
  - "https://openreview.net/pdf?id=lqNDwH3zTG"
  - "https://arxiv.org/abs/2606.09863"
  - "https://arxiv.org/abs/2609.00038"
summary: >-
  Adversarial novelty gate bác bỏ broad early-failure-detection topic; trả lời experimental open questions và xác định semantic runtime verification là lane cần search tiếp, chưa phải gap.
provenance:
  extracted: 0.82
  inferred: 0.15
  ambiguous: 0.03
base_confidence: 0.91
lifecycle: draft
lifecycle_changed: 2026-09-12
tier: core
created: 2026-09-12T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# Early failure detection trong tool-using agents

> [!important] **Kết luận novelty gate: REJECTED.** Đề tài rộng “dùng execution trajectory để dự đoán sớm final task failure dưới controlled tool failures” đã có prior art trực tiếp, đa dạng và một artifact tái lập được. Không triển khai harness 20–30 task như contribution mới.

## 1. Bài toán là gì?

Tại mỗi thời điểm `t`, monitor chỉ được thấy phần quỹ đạo đã xảy ra `τ≤t` và ước lượng liệu agent cuối cùng có fail hay không. Đây là **dự báo lỗi sớm (early failure prediction)**, khác với:

- failure detection sau explicit exception: “tool vừa báo lỗi”;
- post-hoc diagnosis: phân tích sau khi trajectory kết thúc;
- recovery routing: chọn retry/replan/fallback sau khi có tín hiệu.

## 2. Trả lời các open question

### OQ1 — Nên chọn experimental domain nào?

**Trả lời trước novelty gate:** file/data-processing tool tasks là lựa chọn hợp hoàn cảnh hơn coding agents vì local, deterministic, không cần paid API và dễ tạo outcome oracle.

**Trả lời sau novelty gate:** không nên tự xây domain này để tuyên bố novelty. Để học/reproduce, dùng AFTraj-2K hoặc committed traces của AgentTrajectorySentinel. Nếu sau này có gap mới về semantic verification, AppWorld hoặc một tập local data-processing task có reference state mới là domain phù hợp.

### OQ2 — Prediction point nên định nghĩa thế nào?

Monitor nên chạy tại **mỗi observed prefix/step** và phát alert lần đầu khi risk vượt threshold. Đánh giá bằng first-alert recall, false-alarm rate và lead time. Có thể báo thêm kết quả tại fixed checkpoints `k=2,3,4`.

Không dùng “50% độ dài cuối trajectory” làm feature hoặc trigger online vì final length thuộc tương lai. PrefixGuard cho thấy `t+T` là một oracle confound rất mạnh.

### OQ3 — Nhãn positive là gì?

Cần tách ba nhãn:

1. `fault_exposed`: trajectory đã bị injection;
2. `fault_onset_step`: step bắt đầu perturbation;
3. `terminal_task_failure`: final state/outcome sai.

Positive cho forecasting phải dựa vào `terminal_task_failure`; injection onset chỉ dùng để đo lead time. Một injected fault có thể được agent phục hồi nên **fault exposure không đồng nghĩa task failure**. Ground truth tốt nhất là reference-state scorer hoặc continuation rollout được verify.

### OQ4 — Detector được nhìn thấy tín hiệu gì?

Chỉ dùng agent-visible evidence tại prefix: tool name/arguments/output, status/error, latency, state delta, retry/loop count và task context đã có. Không cho nhìn fault injector metadata, future step, expected answer hoặc final trajectory length.

Nếu explicit error đã xuất hiện, kết quả sau đó là failure detection/recovery prediction, không phải dự báo trước tool failure. Với schema-valid silent wrong output, telemetry có thể không đủ; phải có task-grounded invariant hoặc external reference.

### OQ5 — Baseline tối thiểu là gì?

- error flag / retry-count rule;
- step-position và task-prior controls;
- TF-IDF + logistic regression trên visible prefix;
- memoryless Mahalanobis/delta-Mahalanobis;
- agent self-assessment hoặc LLM judge khi có ngân sách, phải tính latency/token cost;
- oracle dùng onset/future chỉ để đo upper bound, không được tính là deployable baseline.

### OQ6 — Benchmark nào phù hợp nhất hiện tại?

**AFTraj-2K** phù hợp nhất để học và phân tích offline: public, 2,276 trajectories, có safe/unsafe và decisive-error step, bao phủ Coding/Math/Agentic, không cần paid API. **AgentTrajectorySentinel** là artifact tốt nhất để reproduce monitor/fault-injection pipeline local CPU.

ToolBench-X chỉ giữ làm secondary stress test vì pilot đã phát hiện data validity, signal semantics, trace export, license và free-tier throughput confounds.

### OQ7 — External monitor có tốt hơn self-assessment ở latency/chi phí tương đương không?

**FACT:** AgentForesight báo external specialized auditor tốt hơn self-reflection cùng Qwen2.5-7B backbone (`66.44` so với `23.38` Exact-F1 trong paper). AgentTrajectorySentinel không so cùng accuracy/capacity với LLM judge nhưng chứng minh một monitor khoảng `200 µs/step` và cost-aware escalation dùng ít judge calls hơn judge-every-step.

**Kết luận:** câu hỏi rộng đã được trả lời một phần đáng kể; không đủ để làm novelty claim. So sánh hoàn toàn matched về latency/capacity trong riêng realistic tool-service faults có thể chưa đầy đủ, nhưng đây là refinement nhỏ và measurement-heavy, không phải lựa chọn tốt nhất cho người mới trong 12 tuần.

## 3. Prior-art threat matrix

| Work | Partial trace online? | Controlled/observed failures | Silent/ambiguous failure | Transfer | Cost/earliness | Public artifact |
|---|---:|---:|---:|---:|---:|---:|
| Adaptive Fault Injection | ✓ | ✓ adaptive injection + rollout labels | △ không tập trung riêng silent tool output | ✓ across agent policies theo paper | ✓ low-cost forecaster | ? chưa xác minh code |
| PrefixGuard | ✓ | ✓ terminal outcomes trên 4 benchmarks | △ chỉ failure có visible prefix evidence | △ cross-benchmark diagnostics | ✓ FAR, lead time, no runtime LLM | ? |
| AgentForesight / AFTraj-2K | ✓ | ✓ organic + injected decisive errors | ✓ có silent intermediate error | ✓ Who&When | △ per-step 7B cost | ✓ data/code; checkpoint pending |
| Weakly Supervised Early Alerting | ✓ | ✓ five benchmark families | △ sparse/delayed evidence | △ domain-specific refit có thể cần | ✓ accuracy–earliness policy | △ promised release |
| AgentTrajectorySentinel | ✓ | ✓ five injected classes + real traces | ✓ context corruption/silent abort; △ plausible wrong value | ✓ ranking; ✗ cold calibration | ✓ ~200 µs, judge-call cost | ✓ code/data/tests |
| Automata from Agent Traces | ✓ | ✓ public trace outcomes | △ không riêng tool corruption | ✓ cross-model on `τ²`; broader open | ✓ early stop | △ project page, code unverified |
| Predicting Web-Agent Failure Risk from Trajectory Prefixes | ✓ | ✓ 3,364 web trajectories | △ web risk, không riêng silent tool fault | ✓ across website regimes | ✓ false-cut budget | ? anonymous submission |
| False Success / trajectory-judge | △ chủ yếu full trajectory | ✓ environment/oracle labels | ✓ explicit silent/loud strata | ✓ task/model split một phần | ✓ judge cost/calibration | ✓ trajectory-judge |

Legend: `✓` rõ ràng; `△` một phần; `✗` không hỗ trợ; `?` chưa đủ evidence.

## 4. Thử bác bỏ gap

### Claim 1 — Partial trajectory prediction chưa được nghiên cứu

**REJECTED:** tất cả các work chính ở trên làm trực tiếp.

### Claim 2 — Controlled tool failures tạo novelty

**REJECTED:** Adaptive Fault Injection, AgentForesight và AgentTrajectorySentinel đều inject/construct failures và xác minh downstream effect.

### Claim 3 — Early stopping/accuracy trade-off chưa được nghiên cứu

**REJECTED:** PrefixGuard đo FAR/lead time; weakly supervised alerting tối ưu Pareto frontier; Automata thực hiện early stopping.

### Claim 4 — Cross-model/cross-domain generalization chưa được đo

**WEAK:** đã có external benchmark, cross-corpus và cross-model tests. Tuy nhiên cold deployment transfer còn kém và nhiều method cần calibration/refit.

### Claim 5 — Silent failures chưa được xử lý

**SURVIVES ONLY AS AN OPEN QUESTION:** silent abort, goal drift, context corruption và false success đã được nghiên cứu. Trường hợp khó còn lại là tool trả **schema-valid, plausible nhưng semantically wrong value** mà không có anomaly telemetry. AgentTrajectorySentinel nói rõ trường hợp này không quan sát được nếu không có external reference.

## 5. Gap status và quyết định plan

**Broad gap:** `REJECTED`.

**Narrow candidate:** `PRELIMINARY OPEN QUESTION`, chưa phải research gap:

> Liệu lightweight task-grounded invariants có phát hiện runtime schema-valid silent tool-output corruption trên unseen tool environments mà không cần failure labels cho từng deployment hay không?

Candidate này đổi trọng tâm từ generic trajectory classification sang **xác minh ngữ nghĩa lúc chạy (runtime semantic verification)**. Cần adversarial prior-art search riêng trong runtime verification, data validation, agent verifiers và tool-output consistency trước khi tạo RQ.

### Kết quả thực hiện plan

| Plan item | Trạng thái | Lý do |
|---|---|---|
| 1. Formalize problem | Hoàn thành | Đã định nghĩa prefix, labels, visible signals và leakage rules. |
| 2. Deep prior-art search | Hoàn thành | Tìm thấy nhiều direct 2026 prior art. |
| 3. Novelty gate | Hoàn thành — `REJECTED` | Broad topic đã bị phủ. |
| 4. Chốt RQ | Không thực hiện | Gate không cho phép tạo RQ yếu. |
| 5–9. Xây 20–30 task harness và chạy API pilot | Hủy theo gate | Sẽ lặp direct prior art, tốn thời gian/API và không tạo contribution. |
| 10. Feasibility decision | Hoàn thành | Artifact public/CPU khả thi để reproduce; topic rộng không khả thi về novelty. |

## 6. Research Question

**Chưa chốt Research Question.** Không nên đổi open question hẹp thành RQ trước khi search prior art cho semantic verification.

## 7. Bước tiếp theo duy nhất

Thực hiện một adversarial prior-art search có phạm vi hẹp cho: **task-grounded runtime verification of schema-valid silent tool outputs**, đặc biệt xem methods có dùng reference execution, invariants, state transition checks hoặc cross-tool consistency để phát hiện sớm hay chưa.

## Related

- [[references/real-time-detection-and-repair-agent-failures]]
- [[references/prefixguard]]
- [[references/agentforesight]]
- [[references/weakly-supervised-early-failure-alerting]]
- [[references/automata-from-agent-traces]]
- [[references/from-confident-closing-to-silent-failure]]
- [[references/trajectory-judge]]
- [[references/toolbench-x]]
- [[synthesis/Preliminary Gap: External Runtime Monitoring]]
