---
title: >-
  Secondary semantic review — reclassification before adapter
category: journal
tags: [research-log, research-protocol, external-validity, reproducibility, verification]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-case-review-package.md"
  - "synthesis/Protocol Amendment: Secondary Case Review and Safety Eligibility.md"
  - "journal/2026-09-20-ai-review-provenance-correction.md"
  - "https://github.com/cmu-soda/ProvenanceGuard/tree/3ad7141db44096e1440718618bdb24fa46c003ff"
summary: >-
  AI-assisted semantic cross-review chỉ ra hai case không phù hợp unsafe denominator và một mutation no-op; không có human review hoặc secondary run.
provenance:
  extracted: 0.54
  inferred: 0.42
  ambiguous: 0.04
base_confidence: 0.76
lifecycle: draft
lifecycle_changed: 2026-09-19
tier: core
created: 2026-09-19T11:12:05+07:00
updated: 2026-09-20T17:33:00+07:00
---

# Research log — secondary semantic review

> [!important] **Đính chính ngày 2026-09-20:** Chủ dự án xác nhận các verdict review case do **một AI khác** thực hiện theo yêu cầu, không phải teammate/human reviewer. Những kiểm tra code/trace ghi ở đây giữ nguyên; nhãn “sign-off” lịch sử không có nghĩa human sign-off. [[journal/2026-09-20-ai-review-provenance-correction]]

## Đã kiểm tra

Vault owner báo đã đối chiếu năm medium-risk cases với ProvenanceGuard commit `3ad7141db44096e1440718618bdb24fa46c003ff`, ghi sign-off trong [[projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-case-review-package]]. Ở lượt kiểm tra lại, local clone cùng commit có trace hashes khớp [[journal/2026-09-18-benchmark-derived-case-audit]]. Mình kiểm tra `parameters`, `labels.csv` và code của `Bank`, `Todoist`, `DisasterResourceCoordination`, `BioLuminescenceHarvester`; không chạy secondary episodes.

## Điều học được

- **FACT:** `ASB-267` có năm tasks, tất cả match `Test`; `Todoist.delete_task` reject ID không tồn tại. Case này không có wrong-but-accepted deletion từ canonical state gốc.
- **FACT:** `ASB-977` old mutation `350000→300000` tạo no-op trên report gốc; correction `250000→200000` tạo wrong value được `modify_report` ghi nhận. Upstream `boundary=1` cần được công khai trong discussion.
- **FACT:** `ASB-085` có distractor receiving accounts và `Bank.transfer_accounts` trả success; code không mô phỏng chuyển số dư. Endpoint phù hợp là accepted unsafe call, không phải observed fund loss.
- **FACT:** `WB-295` trace 295 có `parameters={}` và query chỉ trả một record. Records khác ở các WorkBench traces không chứng minh shared executable fixture. Tool descriptions không xác định acceptance của ID giả.
- **FACT:** `workbench_tool_descs.json` nói `email.search_emails` trả tối đa năm results và `WB-110` trả đúng năm; `WB-433` truyền `due_date="2023-11-29"`, là equality filter chứ không phải toàn bộ khoảng overdue. `calendar.search_events` cũng cap năm nhưng `WB-000` trả bốn events trong ngày.
- **INFERENCE:** Với đúng tám candidate safety cases trên sáu domains, thí nghiệm hiện chỉ đạt ngưỡng stop rule theo phép đếm; một case không qua semantic/schema gate sẽ buộc dừng. ^[inferred]

## Điều chưa chắc chắn

- `WB-000`, `WB-110`, `WB-433` chưa có frozen `S/I` full-scope snapshots để chứng minh `first`, `last`, và `no unfinished overdue`; đặc biệt `WB-110` chạm result cap, `WB-433` chỉ query một ngày.
- `WB-295` chưa có executable same-state CRM fixture; giữ ngoài unsafe denominator trừ khi chứng minh được.
- Chưa có exact runnable matrix, case-card/schema freeze, secondary adapter hoặc result. `768` là maximum planned, không phải lượt đã chạy.

## Quyết định và next action

Ghi [[synthesis/Protocol Amendment: Secondary Case Review and Safety Eligibility]] **trước code/results**, hạ `ASB-267` và tạm `WB-295` khỏi safety denominator, sửa `ASB-977`, giữ stop rule. Bước kế tiếp: thiết kế và freeze 12 case cards/schema cùng exact runnable matrix, cho reviewer re-sign các revision và completeness evidence; sau đó mới viết adapter.
