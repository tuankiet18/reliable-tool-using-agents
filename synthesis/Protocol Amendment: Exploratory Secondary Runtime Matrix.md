---
title: >-
  Protocol Amendment: Exploratory Secondary Runtime Matrix
category: synthesis
tags: [research-protocol, experiment, external-validity, verification, reproducibility]
sources:
  - "synthesis/Protocol: Secondary Multi-Domain Benchmark-Derived Adaptation.md"
  - "synthesis/Protocol Amendment: Secondary Case Review and Safety Eligibility.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/secondary_schema_contract_v1.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/validate_secondary_schema_contract.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_secondary_smoke_tests.py"
summary: >-
  Prospective amendment ghi protocol deviation, exploratory-only status và exact 704-row secondary runtime matrix trước khi chạy matrix đầy đủ.
provenance:
  extracted: 0.58
  inferred: 0.38
  ambiguous: 0.04
base_confidence: 0.62
lifecycle: draft
lifecycle_changed: 2026-09-28
tier: supporting
created: 2026-09-28T10:14:00+07:00
updated: 2026-09-28T10:14:00+07:00
---

# Amendment: chạy secondary matrix ở chế độ exploratory

> [!important] **Ghi trước khi chạy bất kỳ episode nào trong full matrix.** Amendment này không sửa ngược protocol frozen ngày 2026-09-19. Một smoke test kỹ thuật 32 episode đã được chạy trước amendment; điều đó được khai báo rõ và không được gọi là blinded, preregistered, hay evidence về hiệu quả. Full secondary outcomes chưa được xem tại thời điểm ghi amendment.

## Vì sao có amendment này?

Protocol gốc yêu cầu một reviewer thứ hai trước khi viết adapter. Thực tế, dự án do một sinh viên thực hiện một mình; semantic và exact-schema cross-review được một AI khác hỗ trợ. Không có teammate hoặc human reviewer. Đây là **protocol deviation**, không thể xóa bằng cách gọi AI review là peer review.

Chủ dự án muốn tiếp tục kiểm tra tính khả thi và độ nhất quán của mechanism trên các task benchmark-derived. Vì không có human review, matrix này được hạ cấp thành **exploratory internal adaptation**. Kết quả chỉ mô tả behavior trong simulator, contract và fault topology do project định nghĩa; không được dùng như external validation, benchmark reproduction, confirmatory evidence, hoặc bằng chứng độc lập về generalization. Trước khi đưa các số liệu này vào paper như kết quả chính, cần có human review thật hoặc một nghiên cứu xác nhận riêng.

## Những gì đã được quan sát trước amendment

- Static contract re-check v1.2 đã pass.
- Adapter smoke test đã chạy 32 episode trên tám current safety cases, hai regime (`clean`, `targeted_common_mode_0`) và một seed; rerun byte-identical. Kết quả này chỉ kiểm tra plumbing/action/oracle, không phải effect estimate.
- Chưa chạy bất kỳ episode nào trong full 704-row matrix; chưa xem secondary comparative outcomes.
- Các review verdict trước đây do AI hỗ trợ; không có external/human sign-off.

Do smoke test là thông tin đã quan sát, amendment không tuyên bố toàn bộ pipeline được freeze trước mọi execution. Chỉ các lựa chọn dưới đây được khóa trước full-matrix outcome.

## Cohort, scope và ma trận đã khóa

Candidate rows được sinh theo `candidate_matrix()` trong `validate_secondary_schema_contract.py` từ contract v1.2:

- 11 runnable IDs: `WB-000`, `WB-110`, `WB-203`, `WB-295`, `WB-403`, `WB-433`, `ASB-085`, `ASB-087`, `ASB-090`, `ASB-977`, `ASB-1572`.
- `ASB-267` giữ trạng thái `INVALID_NOT_RUN`, không có row trong matrix.
- 8 current safety cases: `WB-000`, `WB-110`, `WB-203`, `WB-433`, `ASB-085`, `ASB-087`, `ASB-090`, `ASB-977`. Đây là cohort duy nhất dùng cho primary unsafe-action analysis.
- `WB-295` chạy như `SAFETY_RESTORATION_PENDING_AMENDMENT` diagnostic; **không** cộng vào safety denominator.
- `WB-403` và `ASB-1572` là `UTILITY_ONLY`; chỉ report utility/conflict/false-block diagnostics, không đưa vào unsafe denominator.
- 8 seeds theo đúng thứ tự contract: `1103, 1201, 1301, 1409, 1511, 1601, 1709, 1801`.
- 4 regimes: `clean`, `independent_single_source`, `targeted_common_mode_0`, `targeted_common_mode_25`.
- 2 policies: `random_k`, `provenance_k`; mỗi cặp dùng cùng seed, case, regime, fault map, primary observation và proposed action. Mỗi policy nhận một decisive primary call và một corroborator (`K=2`).
- Exact total: `11 × 8 × 4 × 2 = 704` episode rows / 352 matched policy pairs. Analysis unit vẫn là case, không phải episode.
- Candidate matrix JSONL SHA-256 (same canonical hashing rule as static validator): `1b803d2e209bc82827989207f34cefde73630f60579a2ed0c701a87c8bfc2c59`.

Không thay case, seed, regime, selection schedule, fault map, action, oracle hay metric sau khi xem full-matrix outcome. Nếu runner phát hiện contract/oracle/invariant lỗi, dừng lại; mọi sửa đổi cần amendment mới và toàn bộ affected paired cells phải được rerun, đồng thời lưu lỗi gốc.

## Runtime rules

1. Chỉ chạy offline deterministic; không gọi LLM/API và không dùng GPU.
2. Materialize P/S/I theo fault map đã định trước. Các payload gửi policy không được chứa `source_id`, `failure_domain_id`, ground truth, injector labels hay oracle-only fields.
3. So sánh decisive claim giữa P và corroborator đã chọn. Nếu bằng nhau thì thực thi proposed action; nếu khác nhau thì `BLOCK`/no-op. Không thêm tool call thứ ba, không tự đổi target hoặc sửa action.
4. Mỗi action thực thi trên fresh canonical-state copy; assertion phải chạy trên hậu trạng thái. Không sửa canonical fixture hoặc evaluator để ép kết quả.
5. Với `WB-433`, giữ nguyên full-scope primary P và shared narrow context giống nhau ở cả hai policies; 2 decisive calls + 1 shared non-decisive context call, tổng 3 calls mỗi policy. Nếu hash hoặc số calls không khớp, pair invalid.
6. Ghi raw episode rows, exception, fault map, source claims/hashes, selected source, decision, action/execution, oracle assertions và tool-call counts. Không bỏ row lỗi âm thầm.

## Phân tích đã khóa

### Primary exploratory estimate

Trên 8 safety cases tại `targeted_common_mode_25`, tính mỗi case:

`difference_case = unsafe_rate(provenance_k) - unsafe_rate(random_k)`

Sau đó tính trung bình đều giữa 8 case và 10.000 case-cluster bootstrap resamples, seed phân tích cố định `20260928`, percentile 95% CI. Báo cáo numerator/denominator và từng case difference. CI này mô tả độ nhạy trong cohort nhỏ, không suy rộng tới population.

Giữ nguyên decision threshold đã sửa trong amendment trước đó: supportive exploratory pattern chỉ khi CI upper `< 0`, tối thiểu `6/8` case có point improvement, improvement xuất hiện ở ít nhất `4` domains và clean exact-correctness difference `provenance−random ≥ −0.05`, đồng thời tất cả invariants pass. Đạt ngưỡng không biến nghiên cứu thành confirmatory hoặc external validation.

### Metrics phải báo riêng

- Unsafe accepted action rate trên đúng 8 safety cases.
- False-block rate / exact task correctness, không gộp block an toàn với hoàn thành task.
- Clean exact correctness và clean false blocks.
- Kết quả từng regime, fault placement, từng case và từng domain.
- `WB-295` diagnostic riêng; utility-only diagnostics riêng.
- Số decisive/tool calls; invariant `K=2`, và WB-433 shared call được báo riêng.
- Episode execution errors và missing rows.

Không dùng số episode như sample size độc lập, không gộp harm khác loại thành một utility score mới, và không đổi outcome classification sau run.

## Điều kiện dừng và khả năng tái lập

- Cần checkout upstream đúng commits và hash fixture khớp contract. Nếu thiếu artifact, ghi blocker, không thay bằng phiên bản mới hơn.
- Chạy static validator, runner dry-plan/hash check, sau đó smoke regression trước full matrix.
- Full run dự kiến 704 episode local/offline; không cần API, tiền hoặc GPU. Runtime thực tế sẽ được ghi sau run.
- Sau run, chạy lại cùng lệnh để xác nhận output deterministic; nếu output không byte-identical, dừng phân tích cho tới khi giải thích được khác biệt.
- Nếu dưới 8 current safety cases hoặc dưới 6 domains còn hợp lệ, dừng primary analysis; không bổ sung case hậu nghiệm.

## Ý nghĩa đối với paper

> **Hạn chế bắt buộc:** Đây là AI-assisted, single-researcher, benchmark-derived exploratory experiment với topology và faults do project thêm. Không gọi là “independent review”, “peer reviewed”, “external validation”, “replication”, hay “generalizes across benchmarks”. Bất kỳ khác biệt nào quan sát được chỉ là bằng chứng về implementation/mechanism trong điều kiện mô phỏng này.

Ngay cả khi matrix hỗ trợ hypothesis, claim mạnh hơn cần independent human review các case, oracle và mutation, sau đó cần replication trên task/benchmark được khóa độc lập. Nếu matrix không hỗ trợ hypothesis, giữ nguyên kết quả âm tính/không kết luận; không chỉnh thiết kế để cứu hướng nghiên cứu.

## Liên kết

- [[synthesis/Protocol: Secondary Multi-Domain Benchmark-Derived Adaptation]] — protocol gốc, giữ nguyên.
- [[synthesis/Protocol Amendment: Secondary Case Review and Safety Eligibility]] — cohort eligibility và prior amendment.
- [[projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate]] — schema/adapter gate.
- [[journal/2026-09-26-secondary-adapter-smoke-tests]] — smoke test đã quan sát trước amendment.
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]] — claim control.
