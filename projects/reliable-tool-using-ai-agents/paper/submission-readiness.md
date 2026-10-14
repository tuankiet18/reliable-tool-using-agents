---
title: "Sẵn sàng nộp bài — Claim–evidence audit và các gate còn mở"
category: project
tags: [paper-draft, evidence, research-methods, reproducibility, verification]
sources:
  - "journal/2026-10-05-main-study-influence-audit.md"
  - "journal/2026-10-04-clean-environment-core-reproduction.md"
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger.md"
  - "projects/reliable-tool-using-ai-agents/paper/supplementary-appendix.md"
  - "projects/reliable-tool-using-ai-agents/paper/reproducibility-package.md"
  - "projects/reliable-tool-using-ai-agents/paper/artifact-inventory.json"
  - "projects/reliable-tool-using-ai-agents/paper/figure-guide.md"
  - "projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03.md"
  - "projects/reliable-tool-using-ai-agents/paper/review/paper-review-v0.9-2026-10-05.pdf"
  - "projects/reliable-tool-using-ai-agents/paper/build_review_pdf.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_main_study/raw.jsonl"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_main_study/inference.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_robustness_gate/decision.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_secondary_varied/episodes.jsonl"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_secondary_varied/analysis-summary.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_live_agent_opportunity_16cells_rtx4060_20261003/matched_pair_audit.json"
created: 2026-10-04T11:15:00+07:00
updated: 2026-10-05T09:14:46+07:00
summary: >-
  Claim audit giữ kết quả có điều kiện; đã xuất PDF A4 review copy v0.9 gắn với source hash. Course template, author readback, supervisor feedback, snapshot và independent reproduction còn mở.
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.00
base_confidence: 0.59
lifecycle: draft
lifecycle_changed: 2026-10-04
tier: supporting
---

# Bài đang sẵn sàng đến mức nào?

**INFERENCE — READY FOR AUTHOR / SUPERVISOR REVIEW, NOT YET SUBMISSION READY:** Manuscript có một câu chuyện thực nghiệm hẹp, có raw và analysis để kiểm tra. Audit này chưa phát hiện chênh lệch ở các headline counts đã đối chiếu. Nhưng format nộp, tác giả tự kiểm tra lập luận và đánh giá contribution của giảng viên còn mở. Không thể suy ra điểm số hoặc khả năng accept từ việc file/hashes hợp lệ.

**Scope:** Controlled empirical course paper; không bắt buộc kết quả trên live agent theo quyết định của tác giả. Không triển khai hệ thống mới hoặc thêm study episodes trong audit này. Reviewer-style verdict **MAJOR REVISION** vẫn là lịch sử đánh giá AI-assisted, không quyết định của reviewer hội nghị và không human sign-off. Novelty vẫn **SURVIVES WITH REFINEMENT — PRELIMINARY**.

## 1. Bài nghiên cứu thực sự nói điều gì?

Hai tools khác tên có thể cùng đọc một backend sai. Study so sánh việc chọn corroborator ngẫu nhiên với chọn khác miền lỗi (failure domain), trong một mô hình refund có actor deterministic và metadata đã biết. Nó kiểm tra quyết định cho phép refund, không thực hiện giao dịch thật ở main/robustness.

**FACT — KẾT QUẢ CHÍNH:** Targeted faults: unsafe refund decisions `30/150` random, `0/150` provenance; clean action-oracle correctness `150/150` ở cả hai. Nhưng targeted correct refunds đều `0/50`: giảm quyết định sai không đồng nghĩa phục hồi nhiệm vụ. Benefit còn phụ thuộc metadata và availability của nguồn độc lập.

**INFERENCE — GIÁ TRỊ CÓ THỂ BẢO VỆ:** Đặc tả rõ assumptions, kiểm tra mechanism, phân tích safety–utility và cung cấp artifact kiểm tra lại được. Không giới thiệu nguyên lý independence mới, thuật toán agent mới hoặc guarantee production safety. Kết quả chính phần lớn suy được từ constructed topology; số rows lớn không khắc phục điều này.

RQ/H1 canonical nằm ở paper §1 và [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]. Không đổi RQ để làm kết quả trông mạnh hơn.

## 2. Claim–evidence coverage

`ALIGNED` nghĩa wording/endpoint/số liệu khớp trong các tài liệu và nguồn được kiểm, không nghĩa claim đã được external validation.

| Nhóm claim | Evidence và kiểm tra | Wording được giữ | Trạng thái |
|---|---|---|---|
| Main effect — C3/C4 | Raw 1,350 rows; mỗi policy/regime 150; stored Δ −0.200, CI [−0.273,−0.127], 30 task clusters | Decision-level, accurate metadata, deterministic actor; K=2 chỉ tại refund proposal | ALIGNED |
| Utility/abstention — C21/C23 | Clean correct refunds 50/50 mỗi policy; targeted 0/50; raw `refund_attempted` phân biệt no proposal | Containment, không recovery; `false_block` không chỉ gate-induced rejection | ALIGNED |
| Negative control — C5 | Independent: unsafe 6/150 random, 7/150 provenance; stored CI của Δ cắt zero | No evidence of advantage; không equivalence claim | ALIGNED |
| Analytical mechanism — C22/C24 | Frozen topology analysis: main expectation 2/9; secondary random 9−r, provenance 3 theo 12 seeds/case | Post-hoc characterization/by construction; không thay observed estimates | ALIGNED |
| Wrong metadata — C6 | Stored decision `FAIL ROBUSTNESS`; wrong_25/leakage .10 upper CI khoảng zero | Advantage không reliably retained; .25 là nominal probability | ALIGNED |
| Secondary — C12/C14 | 1,056 rows; targeted-25 unsafe 59/96 vs 24/96; utility false blocks 9/24 vs 18/24 | Exploratory project-defined adaptation; 8 safety cases, không native benchmark/external validation | ALIGNED |
| Live negative — C20 | Matched-pair audit: 0/4 unsafe-capable pairs; 16 episodes | Không live policy-effect estimate; giữ stop rule | ALIGNED |
| Prior art — C25/C26/C29 | 15 citation IDs; bounded reading scope ở §3/references | Không superiority/first method; AgentOS artifact-level, LBYL26 qualitative only | ALIGNED WITH OPEN COVERAGE |
| Reproduction — C27/C28/C31 | 21 input/3 figure hashes; historical reanalysis; v0.9 clean-venv core replay 10/10 files, 15 tests | Same-host replay, không independent reproduction hoặc complete wheel/build lock | ALIGNED WITH OPEN RELEASE GATES |

Mẫu số khác nhau phải được giữ khi export bảng/hình. Không gộp 1,350 main decisions, 3,750 robustness decisions, 1,056 adaptation rows và 16 live episodes thành một N để làm evidence mạnh hơn. Các CIs là stored values; audit này không bootstrap lại.

**Bổ sung sau audit — 2026-10-05:** [[journal/2026-10-05-main-study-influence-audit]] / appendix §F / ledger C32 ghi leave-one-task/seed/stratum-out sensitivity. Targeted sign giữ âm; independent đổi dấu theo composition. Đây là ranges hậu nghiệm, không CI/new samples hoặc evidence đóng statistical generalization. Main manuscript v0.9 giữ nguyên; các course/human gates dưới đây vẫn mở.

## 3. Lỗi tài liệu được sửa trong v0.8

| Finding | Sửa tối thiểu | Tác động khoa học |
|---|---|---|
| Appendix heading vẫn v0.5; thiếu lịch sử v0.6/v0.7 | Heading trung tính và amendment rows đến v0.8 | Không thay dữ liệu |
| Paper §5.2/§8 nói “lượt này tái phân tích” dù reanalysis ở v0.5 | Ghi ngày 2026-10-03 và phân biệt current read-only count/hash audit | Không fresh reanalysis/test claim |
| Robustness gọi 3,750 “episodes” dễ nhầm live agent | Đổi reader-facing paper/briefing/ledger sang decision rows; giữ raw keys/historical notes | Construct rõ hơn; không sửa raw |
| Project overview còn current version 0.6 và next action đã làm | Đồng bộ current v0.8 và đường đọc readiness | Không novelty upgrade |
| Package checklist trộn course hand-in và public release | Tách hai đích dưới đây | Không tự cấp permission/license hoặc đặt yêu cầu môn học mới |

Không gọi đây là giải quyết scientific findings về novelty, constructed topology, external validity hoặc human review. Các limitations được ghi nhận, không bị xóa sau editorial pass.

## 4. Checklist trước khi nộp bài môn học

### Đã có bằng chứng

- [x] v0.9: core setup/generation/analysis chạy trong clean venv trên cùng host; không nâng claim independent reproduction.
- [x] RQ/H1 cụ thể, decision-level và có conditions; không dùng broad rejected lane.
- [x] Actor/oracle/fault map, matched boundary budget và metric mapping được mô tả.
- [x] Safety trình bày cùng utility, negative control và wrong-metadata FAIL.
- [x] Secondary/live outcomes giữ đúng evidence tier và review provenance.
- [x] Hai frozen-data figures, readable references, appendix và reproduction recipe.
- [x] Bản PDF A4 24 trang để tác giả/giảng viên review; gồm manuscript đến References, supplementary appendix bắt đầu trang mới và internal-note index. Đây là layout-only copy từ paper source SHA-256 `0e9855c81f0d4d91bb78b3c51944954a191cf1368713f163f47b730469403087`; các trang đại diện và contact sheet toàn PDF đã được kiểm tra. Xem [[projects/reliable-tool-using-ai-agents/paper/review/paper-review-v0.9-2026-10-05.pdf]].
- [x] Headline counts/selected hashes được đối chiếu; không chỉnh expected hashes để pass.

### Còn cần hoàn thành

- [ ] **Tác giả:** tự giải thích được năm câu ở §6; đọc lại paper, không chỉ tóm tắt AI.
- [ ] **Tác giả/giảng viên:** xác nhận rubric, ngôn ngữ, deadline và template/độ dài thực tế. “Theo tiêu chuẩn” chưa đủ chọn venue/template cụ thể.
- [ ] **Giảng viên:** góp ý RQ, methodology và mức contribution phù hợp môn học. Chưa nhận được feedback được ghi trong hồ sơ; không giả định thầy sẽ audit case/oracle. Nếu chưa trả lời khi gần deadline, trình bày tình trạng này trung thực, không tự ghi APPROVED.
- [ ] **Sau khi biết format môn học:** tạo bản nộp đúng yêu cầu về độ dài, citation style, heading/figure format và ngôn ngữ. PDF review hiện tại chỉ là bản A4 trung tính, chưa phải course-template export.
- [ ] **Tác giả:** proofread bản export, ghi vai trò AI theo quy định môn học và khóa snapshot hand-in có thể nhận diện. Commit/push chỉ khi được yêu cầu; cũng có thể dùng archive với hashes, không coi HEAD của dirty tree là bản nộp.

**INFERENCE:** Với course scope đã chọn, không cần tiếp tục RTX runs chỉ để có thêm zero-unsafe rows. Independent human case review/fresh-machine generation là evidence cần nếu muốn claim mạnh hơn; không tự biến chúng thành requirement bắt buộc của môn học. Thiếu chúng phải được disclosure.

## 5. Checklist riêng cho public artifact / venue submission

- [ ] Project release license do tác giả chọn; upstream data/code/fixture notices được xác minh theo origin trước redistribution.
- [ ] Complete release snapshot và dependency/import closure; không chỉ selected inventory.
- [ ] Fresh-machine generation/reanalysis nếu muốn claim independent portability/reproduction.
- [ ] Human semantic audit hoặc thiết kế độc lập nếu muốn nâng secondary evidence.
- [ ] Contribution/venue fit được đánh giá riêng; hiện không có live effect/head-to-head hoặc production prevalence evidence.

Không có yêu cầu phải submit hội nghị/tạp chí. Bản môn học và một artifact public là hai sản phẩm khác nhau; không dùng tình trạng course hand-in để suy licensing clearance hoặc accept probability.

## 6. Năm câu tác giả cần tự trả lời

1. Tool khác tên nhưng chung backend gây lỗi đồng thuận sai thế nào? Minh họa bằng một refund proposal cụ thể.
2. Vì sao main `unsafe_refund` là quyết định, không phải giao dịch sai đã thực thi? Secondary khác endpoint ở điểm nào?
3. Vì sao 0/150 unsafe vẫn đi cùng 0/50 correct refunds, và always-escalate có thể bằng provenance ở targeted condition?
4. Vì sao zero unsafe của provenance phần lớn được bảo đảm bởi assumptions? Wrong metadata phá assumption nào?
5. Vì sao live run 16/16 final-state correct không validate policy effect khi matched unsafe-capable pairs là 0/4?

**Bước tiếp theo duy nhất:** Tác giả đọc paper §2/§4/§5 và figure-guide, rồi tự viết một explanation khoảng một trang trả lời năm câu này. Dùng nó để kiểm tra understanding trước export/giảng viên feedback; chưa cần chạy model hoặc search rộng thêm. Nếu câu trả lời mâu thuẫn raw, sửa lập luận chứ không chọn lại seed.

**Hỗ trợ đã có — 2026-10-04:** [[projects/reliable-tool-using-ai-agents/paper/figure-guide]] §6 có ba worked examples từ bảy frozen decision rows: `INS-00062` shared-domain wrong agreement, `INS-00060` no-proposal false denial và always-escalate counterfactual. Đây là lời giải mẫu có nguồn để học cơ chế, không phải bản tác giả tự giải thích; checkbox author understanding vẫn mở. Paper v0.9, RQ/H1 và kết quả không đổi.

## Related

- [[journal/2026-10-04-clean-environment-core-reproduction]]
- [[projects/reliable-tool-using-ai-agents/paper/supervisor-methodology-rq-briefing]]
- [[journal/2026-10-04-submission-readiness-audit]]
- [[projects/reliable-tool-using-ai-agents/reliable-tool-using-ai-agents]]
