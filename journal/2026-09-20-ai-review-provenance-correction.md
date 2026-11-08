---
title: >-
  Đính chính provenance của secondary case review
category: journal
tags: [research-log, research-protocol, external-validity, verification, reproducibility]
sources:
  - "User clarification in conversation, 2026-09-20: solo research project; another AI performed the reviews"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-case-review-package.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate.md"
summary: >-
  Hai vòng secondary review do một AI khác hỗ trợ, không phải teammate hay human reviewer; các verdict hữu ích nhưng chưa là human validation hoặc runnable evidence.
provenance:
  extracted: 0.72
  inferred: 0.24
  ambiguous: 0.04
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-09-20
tier: supporting
created: 2026-09-20T17:33:00+07:00
updated: 2026-09-20T17:33:00+07:00
---

# Đính chính nguồn gốc review — 2026-09-20

## FACT — thông tin do chủ dự án xác nhận

- Đây là dự án research do **một người** thực hiện. Không có teammate nào đã review các case.
- Semantic case review và exact-schema re-sign được chủ dự án yêu cầu **một AI khác** thực hiện. Tên model, prompt và mức độ tách biệt context chưa được ghi lại; không tự suy đoán.
- Vì vậy, các quyết định `APPROVE/REVISE/REJECT` là kết quả **AI-assisted cross-review**, không phải independent human review, peer review hoặc human sign-off.
- Exact-schema pass vẫn là `2 APPROVE / 5 REVISE`; contract **chưa `FROZEN`**, ma trận `704` chỉ là candidate row keys và chưa có secondary episode.

## Tác động lên lập luận nghiên cứu

Các code/trace/fixture citations và năm blocker do AI tìm ra vẫn là những đề xuất kiểm tra cụ thể; provenance được đính chính **không tự bác bỏ** chúng. Nhưng verdict của AI không chứng minh tính đúng đắn độc lập: cần typed contract, deterministic assertions và smoke tests trên adapted executor trước khi dùng case như bằng chứng thực nghiệm. ^[inferred]

Protocol gốc tại [[synthesis/Protocol - Secondary Multi-Domain Benchmark-Derived Adaptation]] dự kiến một reviewer thứ hai trước adapter; review package ban đầu còn ghi rõ “teammate”. Điều đó **chưa diễn ra**. Không sửa ngược protocol gốc hoặc gọi AI review là đã hoàn thành human-review gate. Nếu nhóm muốn thay yêu cầu này bằng AI cross-review + executable checks, phải ghi một thay đổi protocol minh bạch **trước secondary run**; nếu có human review sau này, ghi riêng người, phạm vi và ngày. ^[inferred]

## Quy trình tiếp theo

1. Sửa năm mục `REVISE` ở mức đặc tả: typed `P/S/I`, policy-visible vs oracle-only data, typed actions/oracles, paired `P/context` cho `WB-433`, fixture binding cho `WB-295`.
2. Cho AI cross-review lại **bản đã sửa**, nhưng gọi đúng tên phương pháp; không coi việc này là human validation.
3. Sau adapter, chạy executor smoke tests và runtime paired invariants. Chỉ khi đó mới quyết định runnable gate; `WB-295` vẫn ngoài safety denominator cho tới amendment trước run.

## Related

- [[projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-case-review-package]]
- [[projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate]]
- [[synthesis/Protocol Amendment - Secondary Case Review and Safety Eligibility]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
