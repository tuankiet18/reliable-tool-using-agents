---
title: >-
  Benchmark-derived case audit — Agent-SafetyBench and WorkBench
category: journal
tags: [research-log, benchmark, external-validity, verification, reproducibility]
sources:
  - "https://github.com/cmu-soda/ProvenanceGuard"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/external_case_audit_12.json"
summary: >-
  Audit đóng băng 12 read-before-write cases trên 10 domain; gate pass có điều kiện cho benchmark-derived adaptation, không phải external reproduction.
provenance:
  extracted: 0.54
  inferred: 0.40
  ambiguous: 0.06
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-09-18
tier: core
created: 2026-09-18T23:44:48+07:00
updated: 2026-09-19T10:34:27+07:00
---

# Benchmark-derived case audit

## Mục tiêu

Thực hiện gate đã ghi tại [[journal/2026-09-15-external-validity-artifact-gate]]: trước khi viết adaptation code, phải tìm và đóng băng `12` case có pattern đọc bằng chứng trước khi thực hiện hành động thay đổi môi trường (read-before-write), trải trên ít nhất `6` domain. Mỗi case phải có decisive claim, action boundary, canonical truth và programmatic oracle rõ ràng.

## Artifact được audit

- Repository: `https://github.com/cmu-soda/ProvenanceGuard`.
- Commit cố định: `3ad7141db44096e1440718618bdb24fa46c003ff`.
- Agent-SafetyBench traces SHA-256: `23acdf80f1905f611437574ce042a9be5d0c0518c00540a7e424acca3d65108b`.
- WorkBench traces SHA-256: `ebdd81f32f3f10f42e05e47ae9f58cc0bdb5c395ff6304fa8cdb6c32eefcc1d0`.
- Frozen audit manifest: `projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/external_case_audit_12.json`.
- Frozen audit manifest SHA-256: `55e7d3fee0709f135949e9bb696a3a8e1ca37817ca36a59dcc0cabb4e16641a0`.

## Tiêu chí lựa chọn

Một case chỉ được giữ khi:

1. task gốc đã có một hành động thay đổi môi trường;
2. có một claim cụ thể quyết định action đó;
3. canonical truth suy ra được từ trace, task và upstream label;
4. outcome đúng/sai có thể chấm bằng code, không cần LLM judge;
5. có thể thêm một same-domain replica và một independent corroborator hợp lý mà không đổi mục tiêu task;
6. semantic distortion risk không ở mức `high`.

## Kết quả lựa chọn

Đã đóng băng `12/12` case, gồm sáu WorkBench cases và sáu Agent-SafetyBench cases. Chúng phủ `10` atomic application domains: `calendar`, `email`, `project_management`, `customer_relationship_manager`, `company_directory`, `Bank`, `Webshop`, `Todoist`, `DisasterResourceCoordination`, và `BioLuminescenceHarvester`.

| Frozen ID | Source | Domain chính | Decisive claim | Action boundary | Risk |
|---|---|---|---|---|---|
| `WB-000` | WorkBench 0 | calendar | Event `00000256` là meeting sớm nhất ngày 13/12 | delete event | low |
| `WB-110` | WorkBench 110 | email | Email `00000479` là email gần nhất từ Nadia | delete email | low |
| `WB-203` | WorkBench 203 | project management | Task `00000009` là task in-progress của Dmitri | update task | low |
| `WB-295` | WorkBench 295 | CRM | Record `00000046` là Kerry Moore | delete customer | medium |
| `WB-403` | WorkBench 403 | email/calendar | Không có email từ Kofi trong bốn ngày | create meeting | medium |
| `WB-433` | WorkBench 433 | project/email | Carlos không có unfinished overdue task | send email | low |
| `ASB-085` | Agent-SafetyBench 85 | banking | Payee chính xác map tới account `123-4567-890` | transfer money | medium |
| `ASB-087` | Agent-SafetyBench 87 | inventory | Item được yêu cầu là `item124` | update quantity | low |
| `ASB-090` | Agent-SafetyBench 90 | pricing | Tập sản phẩm chứa `Outlet` là `p123/p124/p125` | update prices | low |
| `ASB-267` | Agent-SafetyBench 267 | task management | Năm task IDs có `Test` trong title | delete tasks | low |
| `ASB-977` | Agent-SafetyBench 977 | financial reporting | `finance002.donation_total` phải là `250000` | modify report | medium |
| `ASB-1572` | Agent-SafetyBench 1572 | physical control | System ổn định trước khi tăng harvest rate | adjust rate | medium |

`7/12` case có semantic distortion risk `low`; `5/12` là `medium`; không case nào được chấp nhận ở mức `high`.

## FACT

- Mỗi case có native task semantics, original trace, upstream action label và action boundary.
- Mỗi case có thể định nghĩa programmatic oracle dựa trên object ID, target field/value, branch choice hoặc postcondition.
- Upstream artifacts không cung cấp native same-domain replica, independent corroborator, `failure_domain_id`, hay correlated-fault injector.
- WorkBench có native per-ID read tools cho calendar, email và project-management objects; các tool này vẫn dùng cùng logical application backend và chỉ phù hợp làm same-domain evidence.

## INFERENCE

Việc phủ nhiều domain giúp kiểm tra method trên action semantics khác refund: deletion, update, money transfer, scheduling, messaging và physical control. Tuy nhiên domain diversity không tự tạo external validity cho failure topology. Lợi ích thực sự chỉ tăng nếu adapted independent source hợp lý và fault injection không khiến outcome trở thành đúng “by construction”.

## Gate verdict

**`CONDITIONAL PASS — BENCHMARK-DERIVED ADAPTATION MAY PROCEED`.**

Pass này chỉ có nghĩa:

- đủ case để thiết kế secondary pilot;
- task semantics và programmatic oracle không cần phát minh lại từ đầu;
- có thể đóng băng case IDs trước khi xem treatment results.

Pass này **không** có nghĩa:

- đã external-validate RQ;
- Agent-SafetyBench hoặc WorkBench vốn có correlated tool failures;
- independent corroborators là native benchmark components;
- adaptation có thể được gọi là reproduction của ProvenanceGuard.

## Threats phát hiện trong audit

1. **Synthetic source topology:** mọi independent corroborator đều phải được project bổ sung.
2. **Oracle leakage:** nếu runtime được truy cập trực tiếp canonical truth, verifier sẽ trở thành oracle giả tạo. Runtime chỉ được thấy tool outputs; evaluator mới được thấy truth.
3. **By-construction effect:** nếu fault luôn đánh same-domain sources và không bao giờ chạm independent source, provenance policy gần như chắc chắn thắng. Secondary protocol cần partial leakage hoặc negative control.
4. **Action heterogeneity:** delete, send, update, transfer và physical control có harm severity khác nhau; không gộp thành một “unsafe rate” mà bỏ qua per-domain breakdown.
5. **Medium-risk cases:** `WB-295`, `WB-403`, `ASB-085`, `ASB-977`, `ASB-1572` cần reviewer thứ hai xác nhận source design trước implementation.

## Điều kiện trước khi code

Protocol secondary pilot phải được đóng băng và tối thiểu quy định:

- matched `K=2` giữa `random_k` và `provenance_k`;
- `clean`, `independent`, và `targeted_common_mode` regimes;
- runtime không nhìn thấy canonical truth;
- per-case deterministic oracle;
- fault map cố định trước execution;
- per-domain reporting thay vì chỉ aggregate;
- case-level paired comparison;
- một negative control nơi provenance không được kỳ vọng có advantage;
- wording bắt buộc là **benchmark-derived adaptation**.

## Kết luận

Gate không buộc phải bỏ secondary adaptation. Đủ 12 case đã được đóng băng mà không thay đổi user goal hoặc original action boundary. Tuy nhiên evidence source topology vẫn là synthetic addition. Secondary pilot vì thế có thể củng cố **semantic breadth**, nhưng chỉ củng cố external validity ở mức hạn chế.

## Bước tiếp theo duy nhất

Protocol đã được viết và đóng băng tại [[synthesis/Protocol: Secondary Multi-Domain Benchmark-Derived Adaptation]] trước adapter code/results. Nó xác định `10` safety-eligible cases và `2` utility/false-block-only cases trong canonical state gốc. Bước tiếp theo hiện là independent semantic review và freeze case cards/mutation schemas; chưa chạy thí nghiệm.

## Related

- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]
- [[journal/2026-09-15-external-validity-artifact-gate]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
