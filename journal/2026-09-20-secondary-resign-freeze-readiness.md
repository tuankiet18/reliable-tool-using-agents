---
title: >-
  Secondary re-sign và đánh giá readiness trước schema freeze
category: journal
tags: [research-log, research-protocol, external-validity, reproducibility, verification]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-case-review-package.md"
  - "journal/2026-09-19-workbench-full-state-gate.md"
  - "synthesis/Protocol: Secondary Multi-Domain Benchmark-Derived Adaptation.md"
  - "synthesis/Protocol Amendment: Secondary Case Review and Safety Eligibility.md"
  - "journal/2026-09-20-ai-review-provenance-correction.md"
summary: >-
  Bốn case được AI cross-review về semantic/oracle; không có human sign-off, cohort tám safety và schema/matrix vẫn chưa freeze.
provenance:
  extracted: 0.65
  inferred: 0.30
  ambiguous: 0.05
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: 2026-09-20
tier: supporting
created: 2026-09-20T16:40:18+07:00
updated: 2026-09-20T17:33:00+07:00
---

# Secondary re-sign: đã qua semantic gate, chưa qua runnable gate

> [!important] **Provenance correction:** Các verdict “reviewer” trong note này đến từ **một AI khác**, theo xác nhận của chủ dự án, không phải teammate hay human reviewer. `SEMANTIC RE-SIGN PASS` chỉ mô tả nội bộ vòng AI cross-review, không chứng nhận human sign-off. [[journal/2026-09-20-ai-review-provenance-correction]]

## Đã đối chiếu

Đọc bảng re-sign trong [[projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-case-review-package]], full-state gate [[journal/2026-09-19-workbench-full-state-gate]], protocol gốc và amendment hiện hành. Đây là đánh giá **tài liệu và readiness**, không phải kiểm tra lại trực tiếp upstream code/CSV trong lượt này, không phải triển khai adapter hay chạy thí nghiệm.

## FACT và quyết định hiện hành

- Reviewer đã `APPROVE` `WB-110`, `WB-433`, corrected `ASB-977` về ý nghĩa case/mutation/oracle. `WB-295` được `APPROVE` như **restoration candidate**, với điều kiện fixture/schema/amendment trước run.
- `WB-433` chỉ giữ matched comparison nếu cả `random_k` và `provenance_k` cùng thấy full-scope decisive `P` và original narrow context; cùng proposed action/fault map/gate; mỗi bên chọn một corroborator có cùng schema, scope, logical time. Narrow context không phải decisive call thứ ba. Nếu không thỏa, case quay lại `REVISE`.
- Corrected `ASB-977`: canonical old value `300000`, task cần ghi `250000`; corrupt `P/S` báo `250000` có thể dẫn tới wrong proposed write `200000`. Đây là mutation đã được phê duyệt về ý nghĩa, **chưa** có executable schema test.
- Current amendment vẫn quy định `8` safety candidates trên `6` domains. `WB-295` **chưa vào** safety denominator. `ASB-267` tiếp tục là omission diagnostic; `WB-403` và `ASB-1572` là utility diagnostics.
- Chưa có exact `P/S/I` schemas, frozen source topology, verified historical fixture load cho `WB-295`, adapter, runnable matrix, API calls hoặc secondary episodes.

## INFERENCE: vì sao chưa thể gọi `FROZEN`

Re-sign xác nhận *case có ý nghĩa để thử*, không chứng minh chương trình sẽ tạo cùng claim cho ba sources, fault injection giữ valid schema, hay wrong action thật sự được executor chấp nhận. Đặc biệt, WorkBench original chỉ có một backend; `S/I` và failure domains là project-added, phải khai báo minh bạch. ^[inferred]

Nếu giữ `WB-295` ngoài runnable set, trần số học là `11 cases × 8 seeds × 4 regimes × 2 policies = 704` rows; trong số đó primary targeted condition có `8 × 8 × 2 = 128` rows trên tám cases. Nếu fixture/schema và **amendment thứ hai** phục hồi `WB-295`, trần là `12 × 8 × 4 × 2 = 768` rows và `9 × 8 × 2 = 144` primary-targeted rows. Cả hai đều là *conditional maxima*: một diagnostic regime không có mutation hợp lệ phải được đánh dấu invalid trước run, không ép đủ rows. Primary statistical unit vẫn là case (`n=8` hoặc `n=9`), không phải 128/144 độc lập. ^[inferred]

## OPEN QUESTION / điều kiện nghiệm thu

1. Với từng case, exact `P/S/I` request/response schema, cutoff, full-scope/completeness contract, logical time, `source_id` và `failure_domain_id` là gì? Source nào là native, source nào là project-added?
2. Adapter nạp historical CRM CSV đúng SHA-256 `8632a748512e2c4e1ad7ffa6669efb1ce73bcfe9600f976a99af6e6c46e79297` và giữ cả `00000046`/`00000097` trong cùng state được không? Test accepted deletion phải dùng original acceptance semantics.
3. Với `WB-433`, cách log original narrow context và adapted full-scope `P` có giữ matched total calls giữa policies, ngoài matched `K=2` decisive calls, không?
4. Mỗi case × regime có schema-valid mutation và oracle phân biệt `unsafe`, `false block`, `omission`, `invalid` không? Danh sách exact runnable rows chỉ được phát hành sau khi trả lời điều này.

## Quyết định

**Gate status: SEMANTIC RE-SIGN PASS; SCHEMA/MATRIX GATE PENDING; NOT READY TO RUN.** Không sửa protocol gốc, không nâng `WB-295` dựa vào re-sign một mình, không ghi secondary result vào paper. Bước kế tiếp duy nhất là soạn và kiểm tra **12 exact case schemas cùng matrix eligibility**; sau đó mới quyết định amendment phục hồi `WB-295` và freeze runner input.

## Related

- [[synthesis/Protocol Amendment: Secondary Case Review and Safety Eligibility]]
- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]
- [[projects/reliable-tool-using-ai-agents/reliable-tool-using-ai-agents]]
