---
title: >-
  Secondary schema preflight trên hai upstream artifacts
category: journal
tags: [research-log, research-protocol, external-validity, reproducibility, verification]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/secondary_schema_contract_v1.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/validate_secondary_schema_contract.py"
  - "https://github.com/cmu-soda/ProvenanceGuard/tree/3ad7141db44096e1440718618bdb24fa46c003ff"
  - "https://github.com/olly-styles/WorkBench/tree/00670510c8a476acd247925cefb17fee88500737"
  - "journal/2026-09-20-ai-review-provenance-correction.md"
summary: >-
  Static preflight khớp 6 upstream hashes, 12 clean claims, 11 mutations và 704 candidate rows; AI review sau đó trả 5 REVISE, chưa có human sign-off/run.
provenance:
  extracted: 0.72
  inferred: 0.24
  ambiguous: 0.04
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-09-20
tier: supporting
created: 2026-09-20T17:05:05+07:00
updated: 2026-09-20T17:33:00+07:00
---

# Research log — secondary schema preflight

> [!important] Đây là log của **static preflight trước review**. Exact-schema review sau đó do một AI khác thực hiện: `2 APPROVE / 5 REVISE`, không phải human sign-off; xem [[journal/2026-09-20-ai-review-provenance-correction]]. Những số `704/352` dưới đây vẫn là candidate counts, không phải episodes đã chạy.

## Đã làm

1. Clone read-only ProvenanceGuard ở commit `3ad7141db44096e1440718618bdb24fa46c003ff` và WorkBench historical commit `00670510c8a476acd247925cefb17fee88500737` vào temporary directory ngoài vault. Xác nhận two trace hashes và bốn CSV hashes, gồm CRM historical SHA-256 `8632a748512e2c4e1ad7ffa6669efb1ce73bcfe9600f976a99af6e6c46e79297`.
2. Đọc 12 traces gốc, `WorkBench/src/tools/{calendar,email,project_management,customer_relationship_manager}.py` và Agent-SafetyBench `environments/{Bank,Webshop,Todoist,DisasterResourceCoordination,BioLuminescenceHarvester}.py` tại pinned commits. Đối chiếu task, native tool arguments/output shape, fixture, mutation và static action acceptance.
3. Viết candidate contract `data/secondary_schema_contract_v1.json` và read-only validator `src/validate_secondary_schema_contract.py`. Không viết adapter/policy runner, không gọi model/API, không thực thi 704 episodes.

## Kết quả chạy preflight

```text
source_hashes_verified = 6
native_clean_claims_verified = 12
schema_valid_mutations_verified = 11
current_safety_cases/domains = 8/6
restoration_candidate_safety_cases/domains = 9/7
matrix_candidate_cases/rows = 11/704
paired_fault_map_keys = 352
matrix_candidate_sha256 = c80169f1711779089ecdd8bc6961e3cefbbffc650838a6753ba1ed0db5f39771
excluded_case = ASB-267
secondary_episodes_run = 0
```

Contract SHA-256 `869cc7f301af43bc8905626115910f18fda7524414b12599ec4e3a9ec866225f`; validator SHA-256 `6858baac0362a4a4caca233f5e2de453993d69ca9f76a9c9246c13c257091fb7`. Frozen 12-case audit manifest SHA-256 `55e7d3fee0709f135949e9bb696a3a8e1ca37817ca36a59dcc0cabb4e16641a0` cũng được validator kiểm. `git diff --check` pass. Validator dùng Python standard library và cần hai local clones đúng commit. Lệnh tái chạy nằm tại [[projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate]].

## FACT phát hiện hoặc kiểm lại

- `WB-000`: calendar fixture có đúng bốn events trong full day 2023-12-13; native search cap năm nên original four-row observation đủ trong pinned state.
- `WB-110`: native email search sort `sent_datetime` giảm dần trước cap năm; fixture có 27 query matches tới cutoff, latest `00000479`. Mutation phải re-sort sau khi tráo timestamps.
- `WB-203`: historical project fixture có đúng 13 `In Progress` tasks và chỉ `00000009` thuộc Dmitri; native `search_tasks` không cap.
- `WB-295`: historical global CRM chứa target `00000046` và existing wrong `00000097`; native delete kiểm tồn tại ID. Đây là static acceptance evidence, chưa phải adapted executor smoke test.
- `WB-403`: không có Kofi query match trong interval 26–30/11; native clean result là string `No emails found.`, còn nonempty result là list. Existing older email `00000259` ngày 22/11 có thể được dùng làm observed fake record bằng cách đổi date trong **observation only**.
- `WB-433`: original query chỉ một ngày, nhưng assignee-only native search trên pinned fixture trả 23 tasks; bốn due-before-30/11 đều Completed. Full-scope P là adapted trajectory, không phải raw original P.
- `ASB-085/087/090/977`: wrong target/value có native tool acceptance path; riêng Bank trả `success:true` cho mọi destination mà không mô phỏng chuyển tiền. `ASB-087` upstream `Webshop.search_items` đọc field `name` trong khi fixture dùng `item_name`, nên native search fallback trả toàn bộ ba items; contract giữ đúng output thực tế.
- `ASB-267`: không có non-target task trong canonical state; không thể tạo wrong-but-accepted deletion. Đề xuất exclude toàn bộ matrix, giữ selected ID và invalid record.
- `WB-403` và `ASB-1572` chỉ là counterfactual utility probes nếu fixed clean proposed action vẫn được đưa tới action-boundary gate sau một P observation sai; **không** diễn giải như live agent tự chọn action.

## INFERENCE và giới hạn

Candidate matrix `11×8×4×2=704` rows là một tập row keys chính xác theo contract, **không phải 704 executions**. Với cohort hiện hành, primary targeted analysis có tám case/sáu domains; nếu reviewer xác nhận exact schema và amendment phục hồi `WB-295` **trước run**, có thể là chín case/bảy domains mà không đổi 704 matrix rows. ^[inferred]

Preflight chỉ chứng minh raw/native shapes, claim-changing observation mutation và count arithmetic. Nó chưa chứng minh `S/I` thực sự độc lập ngoài giả định injector, chưa chạy modified actions trên adapted environment, chưa kiểm matched P/context/proposed action/fault map tại từng row, và chưa có reviewer exact-schema sign-off. **Gate status: `STATIC SCHEMA PREFLIGHT PASS; RUNNABLE/REVIEW GATE PENDING`.**

**INFERENCE:** Với `WB-403`/`ASB-1572`, P/S bị corrupt theo hướng chống lại fixed clean proposal, nên cả hai policies có thể cùng block trong targeted regimes. Đây là utility/construct diagnostic, không phải bằng chứng provenance policy tốt hơn. Cần chấm false block bằng oracle sau adapter, không suy từ static shape pass. ^[inferred]

## Bước tiếp theo duy nhất

**Next action được ghi tại thời điểm preflight:** gửi [[projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate]] và JSON contract để rà soát exact schema + matrix exclusion/utility-probe semantics. Lượt AI cross-review sau đó đã yêu cầu năm revision; không diễn giải bước này là human sign-off. Sau khi sửa contract có thể xây adapter để kiểm kỹ thuật, nhưng phải xử lý review-protocol deviation và runtime gate trước secondary run. [[journal/2026-09-20-ai-review-provenance-correction]]
