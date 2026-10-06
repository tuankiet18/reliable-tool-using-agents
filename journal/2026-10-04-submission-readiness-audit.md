---
title: "2026-10-04 — Final claim audit và course submission readiness"
category: journal
tags: [research-log, paper-draft, evidence, reproducibility, research-methods]
sources:
  - "projects/reliable-tool-using-ai-agents/paper/submission-readiness.md"
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger.md"
  - "projects/reliable-tool-using-ai-agents/paper/artifact-inventory.json"
  - "projects/reliable-tool-using-ai-agents/paper/reproducibility-package.md"
  - "projects/reliable-tool-using-ai-agents/paper/supplementary-appendix.md"
  - "projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03.md"
created: 2026-10-04T11:15:00+07:00
updated: 2026-10-04T11:15:00+07:00
summary: >-
  v0.8 sửa version/chronology và tách submission gates; counts/hashes giữ nguyên. Không study/model/analyzer rerun, novelty upgrade hoặc human sign-off.
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.00
base_confidence: 0.59
lifecycle: draft
lifecycle_changed: 2026-10-04
tier: supporting
---

# Claim audit trước khi hoàn thiện bản nộp

## Mục tiêu và cách kiểm

Tiếp tục next action từ v0.7: đọc toàn manuscript, ledger, appendix, package và figure guide; đối chiếu headline counts với frozen raw/stored inference, không search rộng hoặc chạy thêm episodes. Dùng `content-research-writer` cho lập luận và `wiki-update` cho vault tracking. Đây là AI-assisted documentation audit, không independent scientific review.

## FACT — Evidence được đối chiếu

- Main raw có 1,350 decision rows: targeted unsafe random 30/150, provenance 0/150; clean correctness 150/150 và correct refunds 50/50 mỗi policy; targeted correct refunds 0/50. Independent unsafe 6/150 vs 7/150. Stored targeted Δ −0.200, CI [−0.273,−0.127]. Không bootstrap lại.
- Robustness raw có 3,750 decision rows; stored decision vẫn FAIL ROBUSTNESS ở wrong_25/leakage .10 condition. Không sửa gate vì upper CI làm tròn về zero.
- Secondary raw có 1,056 rows; đếm lại targeted-25 đúng 59/96 vs 24/96 unsafe, utility false blocks 9/24 vs 18/24. Giữ cohort/exclusions và project-defined topology.
- Live raw có 16 episodes; stored pair audit giữ 0/4 matched unsafe-capable pairs. Không dùng zero unsafe làm treatment-effect evidence.
- 21 selected inventory files giữ SHA-256. Inventory không complete dependency lock hoặc current committed snapshot.

## FACT — Sửa gì và không sửa gì?

Paper v0.8 sửa “lượt này tái phân tích” thành historical v0.5/ngày 2026-10-03; gọi robustness là decision rows. Appendix bỏ stale v0.5 heading và bổ sung chronology v0.6–v0.8. Project overview đồng bộ version/next action. Ledger C30 và evidence-tier labels giữ internal pre-specified scope, không independent registry.

[[projects/reliable-tool-using-ai-agents/paper/submission-readiness]] tách course checklist, public-release checklist và scientific limits. Không thay RQ/H1, estimates/CIs, raw/scripts, source-reading claims hoặc figures. Không rerun unit tests/analyzers, thêm model/API/GPU calls, commit/push hoặc cấp license.

Historical 8-output local reanalysis/24 focused tests vẫn được ghi theo ngày/lượt đã thực hiện; audit này không trình bày chúng như checks mới. Một read-only inspection ban đầu giả định inference JSON là object nhưng thực tế là list; đã sửa inspection và đọc được nguồn. Đây không lỗi analyzer, dữ liệu hoặc unit test.

## INFERENCE — Kết luận và giới hạn

**FACT — FINAL CHECKS:** 9/9 research-page frontmatters, local sources/path-qualified wikilinks và embedded images hợp lệ; summaries không quá 200 ký tự. 15 unique cited/defined IDs khớp bibliography. RQ/H1 parity 3/3; 21 selected inventory hashes và ba figure hashes không đổi. Abstract, Introduction, Background, Methods, Discussion, Threats và Conclusion giữ section hashes; Related Work/bibliography cũng giữ nguyên. Results chỉ đổi chronology/decision-row wording, không numerical results. `git diff --check` đạt; không full-vault lint hoặc unit-test rerun.

Manuscript có thể dùng để tác giả/giảng viên review một controlled characterization study. Chưa được kết luận submission-ready/accept-ready: cần author understanding, format/export và đánh giá contribution. MAJOR REVISION/PRELIMINARY vẫn giữ; wording rõ hơn không làm topology độc lập hoặc nâng external validity.

**OPEN QUESTION:** Giảng viên chấp nhận phạm vi contribution này theo rubric môn học hay muốn thay đổi gì? Không giả định giảng viên sẽ audit case/oracle. Public license/snapshot/dependency issues là gate riêng nếu redistribution, không lý do sửa scientific outcomes.

## Bước tiếp theo duy nhất

Tác giả dùng paper §2/§4/§5 và [[projects/reliable-tool-using-ai-agents/paper/figure-guide]] viết explanation một trang trả lời năm câu trong readiness note. Sau khi understanding và format đã rõ mới final export; không mở live-agent scaling để cứu effect.
