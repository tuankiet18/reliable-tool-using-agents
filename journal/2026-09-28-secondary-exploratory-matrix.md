---
title: >-
  Full secondary exploratory matrix — benchmark-derived verification
category: journal
tags: [research-log, experiment, external-validity, verification, reproducibility]
sources:
  - "synthesis/Protocol Amendment - Exploratory Secondary Runtime Matrix.md"
  - "synthesis/Protocol Amendment - Secondary Case Review and Safety Eligibility.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/secondary_schema_contract_v1.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_secondary_matrix.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_secondary_matrix.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_secondary_matrix/episodes.jsonl"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_secondary_matrix/analysis-summary.json"
  - "https://github.com/cmu-soda/ProvenanceGuard/tree/3ad7141db44096e1440718618bdb24fa46c003ff"
  - "https://github.com/olly-styles/WorkBench/tree/00670510c8a476acd247925cefb17fee88500737"
summary: >-
  Chạy 704 episode offline thành công và lặp lại byte-identical; giảm unsafe action trong fault topology định trước nhưng CI suy biến vì lịch deterministic lặp y hệt trên mọi case.
provenance:
  extracted: 0.66
  inferred: 0.29
  ambiguous: 0.05
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: 2026-09-28
tier: supporting
created: 2026-09-28T10:20:00+07:00
updated: 2026-09-28T10:20:00+07:00
---

# Full secondary exploratory matrix — benchmark-derived verification

## Mục tiêu và ranh giới diễn giải

Thực thi secondary adaptation trên task semantics của WorkBench và Agent-SafetyBench để kiểm tra toàn bộ luồng materialize observation, so sánh P với corroborator, chặn hoặc cho phép action, chạy action trên state mới và chấm oracle. Đây **không phải** reproduction của benchmark gốc: P/S/I topology, failure-domain labels, fault schedule và policy runners đều do project bổ sung.

Trước full run, [[synthesis/Protocol Amendment - Exploratory Secondary Runtime Matrix]] đã công khai deviation: nghiên cứu do một người thực hiện, review trước đó chỉ có AI hỗ trợ, không có human/peer review. Smoke test 32 episode đã xảy ra trước amendment và được ghi rõ; không có full-matrix outcome nào được xem trước khi khóa lựa chọn hiện tại. Do đó kết quả này là **exploratory internal adaptation**, không phải confirmatory study hoặc external validation.

## Artifact và khả năng chạy lại

- Upstream ProvenanceGuard: commit `3ad7141db44096e1440718618bdb24fa46c003ff`.
- Historical WorkBench: commit `00670510c8a476acd247925cefb17fee88500737`.
- Contract v1.2 SHA-256: `552ef2c689cae93494d68c9114482d1550f5bcfa4653e9bff8902d3b19cfed1a`.
- Exact matrix: 11 runnable cases × 8 seeds × 4 regimes × 2 policies = **704 episodes / 352 matched pairs**; matrix SHA-256 `1b803d2e209bc82827989207f34cefde73630f60579a2ed0c701a87c8bfc2c59`.
- Safety denominator: 8 cases / 6 domains. `WB-295` được thực thi nhưng chỉ là restoration diagnostic; `WB-403` và `ASB-1572` là utility-only; `ASB-267` vẫn `INVALID_NOT_RUN`.
- Episodes JSONL SHA-256 (includes policy-visible P/corroborator payloads and evaluator-only P/S/I snapshots): `d07e929b9c932866046d28ee8f77476e800f5a80f4a41b363036f90e815b94f7`.
- Chạy lại full command cho cùng hash trên; chạy bằng Python/offline, không API, model call, chi phí token hoặc GPU.
- Static validator xác nhận 6 source hashes, 12 traces/claims/schema-oracles, 11 mutations, WB-295 fixture binding và WB-433 fairness hashes. Runner kiểm tra matched policies, K=2, fresh-state execution và oracle assertions. Smoke regression trước full run tiếp tục pass 32/32.

## Kết quả chính

Primary exploratory comparison tại `targeted_common_mode_25`, chỉ trên 8 safety cases:

| Policy | Unsafe action được tool chấp nhận | Tỷ lệ |
|---|---:|---:|
| `random_k` | 40 / 64 | 0.625 |
| `provenance_k` | 16 / 64 | 0.250 |

Chênh lệch trung bình theo case (`provenance_k − random_k`) là **−0.375** (giảm 37.5 điểm phần trăm trong simulator này). Mỗi trong 8 cases có cùng kết quả `5/8` so với `2/8`, nên mọi case-level difference đều `−0.375`; bootstrap 10.000 lần cho percentile CI suy biến `[-0.375, -0.375]`.

> [!warning] CI này **không** cho thấy độ bất định gần như bằng 0. Các case dùng cùng fault positions, cùng lịch selector deterministic và cùng hành vi gate; vì thế case outcomes lặp lại một cấu trúc được thiết kế sẵn. Đây là degenerate descriptive bootstrap, không phải population inference hay evidence về nhiều task độc lập.

## Kết quả theo regime

| Regime | Policy | Unsafe / safety rows | Task success / toàn matrix rows | False block ở 2 utility cases |
|---|---|---:|---:|---:|
| `clean` | `random_k` | 0/64 | 88/88 | 0/16 |
| `clean` | `provenance_k` | 0/64 | 88/88 | 0/16 |
| `independent_single_source` | `random_k` | 0/64 | 33/88 | 10/16 |
| `independent_single_source` | `provenance_k` | 0/64 | 33/88 | 10/16 |
| `targeted_common_mode_0` | `random_k` | 32/64 | 8/88 | 8/16 |
| `targeted_common_mode_0` | `provenance_k` | 0/64 | 0/88 | 16/16 |
| `targeted_common_mode_25` | `random_k` | 40/64 | 10/88 | 6/16 |
| `targeted_common_mode_25` | `provenance_k` | 16/64 | 4/88 | 12/16 |

`task success` là action clean được thực thi theo oracle. Trong targeted regimes, cả 8 safety tasks luôn nhận proposed action sai từ P; gate có thể ngăn unsafe action nhưng **không sửa được action để hoàn thành task**. Bởi vậy safety reduction không đồng nghĩa với agent recovery hoặc end-to-end task success. Các utility-only false blocks là phép đo riêng, không đưa vào unsafe denominator.

## Diễn giải

- **FACT:** Runtime pipeline thực thi được đủ 704 row, matched 352 pairs; clean regime đạt 88/88 task success ở cả hai policy; raw JSONL rerun byte-identical.
- **FACT:** Trong fault regimes, provenance policy có ít unsafe accepted actions hơn ở `targeted_common_mode_0` và `targeted_common_mode_25` theo đúng fault topology và selector schedule đã lập trình.
- **FACT:** Tại `targeted_common_mode_25`, lợi ích đó đi kèm nhiều utility-only false blocks hơn (`12/16` so với `6/16`) và không làm safety tasks hoàn thành; gate chặn, không recovery.
- **INFERENCE:** Kết quả cho thấy cơ chế source selection + disagreement gate được hiện thực hóa nhất quán ở sáu domain do project chọn. Vì mọi topology và mutation là synthetic/project-defined, không thể kết luận hiệu quả ở benchmark nguyên bản, agent thật hoặc production.
- **LIMITATION:** Tám case purposive nhỏ, fault schedule deterministic lặp giống nhau cho từng case, policy decision không do agent/LLM học ra, và oracle/executor vẫn chưa có human review độc lập.

## Ảnh hưởng đến RQ và paper

Không đổi canonical RQ hoặc nâng gap khỏi `PRELIMINARY`. Không thêm secondary result vào abstract/conclusion như bằng chứng generalization. Có thể báo cáo như *exploratory implementation/mechanism check* kèm số liệu theo từng regime, false-block trade-off và degenerate-CI caveat. Claim–evidence ledger cần ghi riêng trạng thái này.

Kết quả không chứng minh paper sẽ được accept. Nó làm artifact hoàn chỉnh hơn, nhưng điểm yếu chính hiện là novelty/độc lập của topology, ground truth/oracle do AI-assisted single researcher tự xây và thiếu live-agent behavior.

## Next action

Yêu cầu một reviewer con người (giảng viên hoặc sinh viên research có kinh nghiệm) audit độc lập 8 safety case cards, 2 utility probes, fault schedule, oracle semantics và raw result parser; nếu chưa có reviewer, dừng mở rộng benchmark và chuyển sang sửa thiết kế để có task/fault variation không lặp cùng một outcome trên mọi case.
