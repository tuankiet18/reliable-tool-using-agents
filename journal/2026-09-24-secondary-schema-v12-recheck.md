---
title: >-
  Secondary schema v1.2 specification re-check
category: journal
tags: [research-log, research-protocol, external-validity, verification, reproducibility]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/secondary_schema_contract_v1.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/validate_secondary_schema_contract.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate.md"
  - "journal/2026-09-20-ai-review-provenance-correction.md"
summary: >-
  Re-check phát hiện v1.1 còn tự khai báo hơn kiểm chứng; v1.2 thêm source materialization, trace-bound actions, structured oracles, real hashes và negative tests, đủ để sang adapter nhưng chưa freeze.
provenance:
  extracted: 0.78
  inferred: 0.19
  ambiguous: 0.03
base_confidence: 0.84
lifecycle: draft
lifecycle_changed: 2026-09-24
tier: supporting
created: 2026-09-24T11:52:03+07:00
updated: 2026-09-24T11:52:03+07:00
---

# Secondary schema v1.2 — specification re-check

## Mục tiêu

Kiểm tra xem contract v1.1 có thật sự giải quyết năm mục `REVISE`, thay vì chỉ thêm field rồi để validator tự xác nhận sự tồn tại. Đây là `AI-assisted implementation re-check`, không phải human review, không chạy adapter và không tạo secondary result.

## Phát hiện khi tấn công v1.1

1. `source_to_claim_map` được mô tả trong journal nhưng không tồn tại trong contract; validator chưa materialize và so sánh exact P/S/I payloads.
2. `typed_oracle` vẫn chủ yếu là câu tiếng Anh. Validator chỉ kiểm chuỗi không rỗng, nên chưa phải machine-readable oracle specification.
3. `clean_action_typed`/`fault_action_typed` chưa được đối chiếu với tool calls và argument runtime types trong original traces.
4. `WB-433` chỉ so hai reference strings giống nhau giữa policies; chưa khóa hash của full-scope P và narrow context thật.
5. `WB-295` đã pin fixture nhưng post-state declarations chưa được kiểm bằng phép biến đổi state tĩnh.

Vì vậy, nếu dừng ở validator v1.1 thì kết luận “5/5 addressed” là quá mạnh. Đây là lỗi kiểm chứng của validator, không phải secondary experimental result.

## Sửa đổi v1.2

- Thêm `source_claim_routing` và materialize P/S/I từ pinned native P: clean P/S/I phải cùng canonical hash; targeted P/S phải cùng fault claim, I giữ clean claim; leakage I phải mang fault claim.
- Cấm `source_id`, `failure_domain_id` và `oracle_only_fields` xuất hiện trong policy-visible payload.
- Đối chiếu clean typed actions trực tiếp với original trace tool calls; fault actions phải dùng tool signature, argument keys và runtime types tương thích.
- Bổ sung `clean_assertions` và `fault_assertions` có cấu trúc cho cả 12 cases. Validator kiểm subject, selector/path, operator và typed value.
- Kiểm nested schema của `ASB-977.entries[]` thay vì chỉ xác nhận đây là list các dict.
- Khóa `WB-433` full-scope P SHA-256 `19138c09b6a806451649407317c302a57a091100036565536846ddec6e1ba152` và narrow context SHA-256 `46a483b06fb700b40cad6d6f48a9207d9c38627d80371d71c3c45026ff6cfd95`; đưa hai hashes vào từng candidate pair.
- Mô phỏng xóa target/distractor trong pinned `WB-295` fixture để kiểm expected row count và retained/deleted IDs ở mức static.
- Thêm `--contract` để chạy regression/negative tests trên contract bị sửa mà không chạm source of truth.

## Kết quả validator

```json
{
  "status": "SCHEMA_CANDIDATE_NOT_FROZEN",
  "contract_version": "1.2-recheck-candidate",
  "source_hashes_verified": 6,
  "native_clean_claims_verified": 12,
  "schema_valid_mutations_verified": 11,
  "typed_field_schemas_verified": 12,
  "clean_action_trace_bindings_verified": 12,
  "machine_oracle_specs_verified": 12,
  "source_payload_contracts_verified": 12,
  "wb295_executor_binding_verified": true,
  "wb433_fairness_invariants_verified": true,
  "wb433_observation_hashes_verified": true,
  "matrix_candidate_rows": 704,
  "matrix_candidate_pairs": 352,
  "matrix_candidate_sha256": "1b803d2e209bc82827989207f34cefde73630f60579a2ed0c701a87c8bfc2c59",
  "secondary_episodes_run": 0
}
```

Contract SHA-256: `552ef2c689cae93494d68c9114482d1550f5bcfa4653e9bff8902d3b19cfed1a`.

Validator SHA-256: `42f11f0b91f736ecb8195713115ea011cb56357b1e936b5694556efb1d50e38c`.

## Negative tests

| Corruption được đưa vào contract copy | Kết quả mong đợi |
|---|---|
| Xóa `WB-000.clean_assertions` | `FAIL`: oracle assertions rỗng |
| Đổi `ASB-085.fault_action.amount` từ string `"30"` thành integer `30` | `FAIL`: argument type mismatch |
| Đổi `WB-433.p_observation_sha256` thành `bad` | `FAIL`: full-scope P hash mismatch |
| Gán `I.failure_domain_field = p_s_domain` | `FAIL`: independent-domain routing mismatch |

Cả bốn corrupted contracts đều bị validator reject. Điều này cung cấp bằng chứng rằng các check mới nhạy với regression đại diện, thay vì luôn pass theo dữ liệu tự khai báo.

## impl-validator verdict

**Overall: `WARN`.** Specification gate đủ rõ để bắt đầu deterministic adapter development. Contract vẫn `SCHEMA_CANDIDATE_NOT_FROZEN` vì chưa có action executor, post-state assertion engine, row-level runtime logs, matched-policy runtime invariants hoặc human review. `WB-295` vẫn ngoài safety denominator; `704` vẫn là candidate rows, `0` secondary episodes.

## Bước tiếp theo

Viết **adapter smoke-test slice nhỏ nhất** cho một WorkBench safety case (`WB-000`) và một Agent-SafetyBench safety case (`ASB-085`). Smoke test phải materialize P/S/I, inject targeted fault, chạy clean/fault typed actions trên fresh state copy, thực thi structured oracle assertions và xuất paired runtime log. Chưa chạy toàn bộ 704 rows.

## Related

- [[projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate]]
- [[journal/2026-09-20-secondary-schema-contract-revision]]
- [[journal/2026-09-20-ai-review-provenance-correction]]
- [[synthesis/Protocol Amendment: Secondary Case Review and Safety Eligibility]]
