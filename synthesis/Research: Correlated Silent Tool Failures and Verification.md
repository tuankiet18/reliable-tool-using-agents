---
title: "Research: Correlated Silent Tool Failures and Verification"
category: synthesis
tags: [ai-agents, verification, tool-failure, prior-art, research]
sources:
  - "https://arxiv.org/abs/2603.02345"
  - "https://arxiv.org/abs/2608.22676"
  - "https://arxiv.org/abs/2608.02645"
  - "https://arxiv.org/abs/2607.07405"
  - "https://arxiv.org/abs/2503.18666"
  - "https://proceedings.mlr.press/v267/kim25e.html"
  - "https://doi.org/10.1109/TSE.1986.6312924"
  - "https://github.com/sierra-research/tau2-bench"
  - "https://github.com/mohammadi-hadi/trajectory-judge"
summary: >-
  Adversarial prior-art search loại generic runtime semantic verification nhưng giữ lại một PRELIMINARY gap hẹp: verification không xét dependency/provenance có thể thất bại khi nhiều tool cùng chịu common-mode silent corruption.
provenance:
  extracted: 0.78
  inferred: 0.19
  ambiguous: 0.03
base_confidence: 0.87
lifecycle: draft
lifecycle_changed: 2026-09-13
tier: core
created: 2026-09-13T00:00:00Z
updated: 2026-09-13T00:00:00Z
---

# Correlated silent tool failures và runtime verification

## Kết luận ngắn

> [!important] **Gap status: SURVIVES WITH REFINEMENT — PRELIMINARY.** Generic semantic verification đã đông prior art. Phần còn sống sót là ảnh hưởng của **lỗi chung nguyên nhân (common-mode failure)** lên cross-tool verification, và liệu chọn evidence theo provenance/failure domain có tốt hơn chỉ đếm số tool khác nhau hay không.

## 1. Bài toán sau khi thu hẹp

Giả sử agent hỏi hai tool:

- `get_order_status`;
- `search_order_history`.

Hai tên và API khác nhau, nhưng cả hai đều đọc cùng một stale database replica. Nếu replica sai, hai tool có thể trả cùng một status sai. Majority vote hoặc fixed-`K` cross-validation sẽ thấy “hai nguồn đồng ý” và tăng confidence sai.

Điểm cần phân biệt:

- **tool diversity:** tool name/call khác nhau;
- **evidence independence:** dữ liệu đến từ failure domain khác nhau;
- **provenance-aware verification:** chọn corroborating tool dựa trên dependency/source metadata, không chỉ dựa trên tool identity.

## 2. Prior art đã giải quyết gì?

### Runtime rules và state gates

`AgentSpec`, `Reason Less, Verify More`, GuardAgent và ShieldAgent đã có runtime policy/rule enforcement. `Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures` đã có postcondition verification, verify-before-retry và idempotency. Vì vậy “thêm verifier/gate/postcondition” là claim đã bị phủ.

### Schema-valid inconsistent returns

`Robustness Analysis of Agentic AI to Inconsistent and Incomplete Tool Responses` đã inject well-formed inconsistent returns và đọc likelihood/next-action signals ngay tại return boundary. Vì vậy “nghiên cứu schema-valid wrong output” cũng không còn đủ mới.

### Cross-tool verification

RIVA đã dùng `K` diagnostic paths, tool history và cross-validation để chịu erroneous tool output. Đây là prior art gần nhất và là novelty threat mạnh nhất.

## 3. Ma trận prior art

| Dimension | RIVA | Robustness Analysis | Verified Tool Calls | Reason Less | AgentSpec |
|---|---:|---:|---:|---:|---:|
| schema-valid/silent wrong output | ✓ | ✓ | △ | ✓ wrong-state write | △ |
| runtime intervention | ✓ | ✗ single decision analysis | ✓ | ✓ pre-write | ✓ |
| cross-tool corroboration | ✓ | ✗ | ✗ | ✗ | ✗ |
| state/postcondition check | △ IaC spec | ✗ | ✓ | ✓ | ✓/△ rule-dependent |
| fixed verification budget | ✓ `K` | ✗ | △ | ✓ gates | ✗ |
| models tool dependencies | ✗ | ✗ | ✗ | ✗ | ✗ |
| correlated/common-mode tool faults | ✗ | ✗ | ✗ | ✗ | ✗ |
| provenance-aware verifier selection | ✗ | ✗ | ✗ | ✗ | ✗ |
| task-success metric | ✓ | ✗ | ✓ | ✓ | △ safety/compliance |
| verification/tool-call cost | ✓ steps/tokens | ✗ | ✓ executions | △ latency | ✓ latency |
| public code | ? RIVA code | ? | ? | ? promised | ✓ |

Legend: `✓` supported; `△` partial; `✗` absent; `?` insufficient evidence.

## 4. Adversarial novelty test

### Claim: chưa ai dùng verification cho silent tool failures

**REJECTED.** RIVA, deterministic gates và verified tool wrappers là direct counterexamples.

### Claim: chưa ai dùng nhiều tool để kiểm tra chéo

**REJECTED.** RIVA làm trực tiếp.

### Claim: nhiều tool khác nhau tạo independent evidence

**REJECTED như một assumption chung.** RIVA nêu independence như trực giác thiết kế nhưng không đo nó. Knight–Leveson cho thấy multiversion software có coincident failures; `Correlated Errors in Large Language Models` cho thấy diversity bề ngoài cũng không bảo đảm independent errors ở model ensembles.

### Claim hẹp: dependency-aware source selection dưới correlated tool failure

**SURVIVES WITH REFINEMENT — PRELIMINARY.** Qua ba vòng search bằng các cụm `correlated tool failures`, `common-mode`, `shared backend`, `failure domain`, `source diversity`, `provenance-aware verification` và `metamorphic tool verification`, chưa tìm thấy paper tool-agent nào vừa:

1. inject silent faults theo shared dependency/failure domain;
2. so sánh fixed-`K` tool-name diversity với dependency-aware source selection;
3. đo detection/utility trên cùng tool-call budget.

Đây không phải bằng chứng về confirmed novelty; chỉ là chưa tìm thấy counterexample đủ gần.

## 5. Contradiction tạo gap

- **FACT — RIVA:** cross-validation nhiều diagnostic path cải thiện accuracy khi một số tool sai.
- **FACT — RIVA:** method giả định nhiều independent tools khó cùng sai một cách.
- **FACT — RIVA:** `K=3` có thể collapse vì không đủ diagnostic paths; thêm verification không luôn tốt hơn.
- **FACT — software diversity / LLM ensembles:** các implementation/model khác nhau vẫn có correlated errors.
- **INFERENCE:** tool identity không phải proxy đáng tin cho evidence independence.
- **HYPOTHESIS:** chọn verifier từ distinct failure domains sẽ tốt hơn fixed-`K` dưới common-mode faults, với cùng số tool call.

## 6. Reproducibility gate

### `trajectory-judge`

- Public, MIT, Python `>=3.12`, deterministic world và fault injection.
- Local check ngày 2026-09-13: clone thành công; `uv sync --extra dev`; **188 tests pass**; mock run tạo `17` trajectories và judge toàn bộ không cần API.
- Điểm yếu: chỉ một support-desk domain; hiện chưa có redundant data sources. Ta phải thêm một layer nhỏ mô tả source group và correlated corruptions.

### `tau2-bench`

- Public, MIT, 114 retail task, 50 airline task và final-state evaluator.
- Local check: core `uv sync --locked` thành công, data đọc được.
- Reproducibility concern: test collection sau `--extra dev` fail vì core import path cần `websockets` thuộc optional voice extra. Đây là packaging/dependency issue, không chứng minh benchmark unusable nhưng tăng setup risk.
- Full agent run cần agent LLM và thường cần user-simulator LLM; solo mode có thể giảm một nửa API dependence.

### Hardware và cost

- Máy hiện tại: RTX 3050 Laptop 4 GB VRAM, 16 GB RAM; phù hợp model local khoảng 3B/7B quantized hơn là 14B full-speed.
- Không cần GPU training. Deterministic fault-generation và metric pipeline chạy CPU.
- API free tier không phải resource đảm bảo; thiết kế chính không được phụ thuộc vào throughput của Groq/Gemini.

## 7. Benchmark strategy phù hợp 12 tuần

1. Phát triển fault model và metric trên `trajectory-judge`, dùng canonical world state làm oracle.
2. Tạo 2–3 logical tool interfaces cho cùng fact nhưng gán dependency group rõ ràng; inject independent và shared-source corruption by construction.
3. So sánh các verification selectors ở matched tool-call budget.
4. Chỉ sau khi pilot có effect, external validation trên subset 15–30 `tau2-bench` retail/solo tasks.

Không xây benchmark lớn mới, không train model và không dùng AIOpsLab làm dependency chính.

## 8. Quyết định

**Tiếp tục nhưng chỉ với formulation hẹp.** Exploratory 10-task pilot đã xác nhận fault-model mechanics: provenance-aware giảm unsafe acceptance dưới common-mode faults nhưng tăng abstention mạnh; random-K là baseline khó hơn fixed-K. Vì vậy RQ đã được sửa thành expected-decision-loss trade-off tại [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]].

## Related

- [[references/riva]]
- [[references/robustness-inconsistent-incomplete-tool-responses]]
- [[references/verified-tool-calls-non-atomic-failures]]
- [[references/reason-less-verify-more]]
- [[references/correlated-errors-in-large-language-models]]
- [[references/trajectory-judge]]
- [[references/tau-bench]]
