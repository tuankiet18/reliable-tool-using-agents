---
title: "Rà prior art trước hành động — AgentOS và Look Before You Leap"
category: journal
tags: [research-log, prior-art, verification, reproducibility, research]
sources:
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03.md"
  - "references/agentos-typed-tool-mediation.md"
  - "references/look-before-you-leap-pre-action-verification.md"
  - "synthesis/Prior-Art Threat: Provenance Metadata and Source Selection.md"
  - "projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger.md"
  - "projects/reliable-tool-using-ai-agents/paper/artifact-inventory.json"
created: 2026-10-04T10:04:00+07:00
updated: 2026-10-04T10:31:00+07:00
summary: >-
  Audit prior art đã tích hợp vào paper v0.7 với 15 citation IDs và bounded contrasts. Không đổi RQ/results; hướng dẫn đọc và giới hạn evidence được giữ rõ.
lifecycle: draft
---

# Bước tiếp theo: kiểm tra đối thủ của lập luận, không tăng số lượt chạy

## Đọc phần này trước — ý nghĩa với bạn

**INFERENCE — KẾT LUẬN HIỆN TẠI:** Research đã có dữ liệu, phân tích, giới hạn và paper v0.7. Việc cần làm không phải “thêm thật nhiều kết quả”, mà là diễn giải đúng research đóng góp điều gì so với những người đã làm trước (prior art). Phần search dưới đây là lượt trước integration; cập nhật v0.7 ở cuối note ghi việc đã làm tiếp theo.

Ví dụ cho dễ hiểu: Một hệ thống có thể cho phép agent ghi vào database đúng quyền; một checker khác đảm bảo câu lệnh áp dụng đúng cách. Nhưng dữ kiện khiến agent quyết định refund vẫn có thể sai. Project của mình chỉ so sánh việc chọn nguồn đối chứng trong một mô phỏng quyết định refund, với lỗi và metadata được định nghĩa rõ. Nó **không** chứng minh agent thật luôn hành động an toàn.

Nếu primary và corroborator dùng chung backend, đồng thuận có thể chỉ là một lỗi lặp hai lần. Independent corroborator có giá trị khi nó còn đúng; nếu labels sai hoặc lỗi lan sang nguồn đối chứng, lợi thế suy giảm. Main positive result phải đọc cạnh wrong-label FAIL và utility loss. Đây là lý do không gọi phương pháp là một giải pháp an toàn tổng quát.

## Tôi đã làm gì — lượt search trước integration

- Đọc current hot cache, project, ledger, citation audit và threat synthesis để không quay lại rejected topics.
- Dùng `wiki-research`: hai rounds, dừng khi đủ cho bounded contrast. Không có optional backend config; dùng web search và retrieval trực tiếp từ nguồn chính thức, không paid API.
- Xác minh AgentOS official conference metadata/repository; tải 16 pinned source/document files, Zenodo metadata, hai task archives. Inspect các đoạn policy/evaluation liên quan; không chạy code của họ.
- Đọc full HTML của nguồn mới; tìm artifact theo title/author. Coverage và unresolved ambiguities nằm ở paper note, không lấy marketing/blogs làm primary evidence.
- Cập nhật existing synthesis và claim ledger. Không sửa manuscript v0.6, runner, raw data, figures, RQ/H1, hoặc numerical results trong lượt này.

## Search record

### Round 1 — 10 queries, ba góc

Metadata/full text, semantics của reference monitor, và verification dưới correlated tool evidence:

1. `"Introducing Safe LLM-Agent Execution" AgentOS paper pdf`
2. `"AgentOS" "World Effect Judge" "Typed"`
3. `"3834637" paper` — kết quả không liên quan; không dùng.
4. `"AgentOS" "Jun Zhou" paper safety evaluation`
5. `"Verified Toolchain Reference Monitor" full paper`
6. `"AgentOS" "correlated" failure verification`
7. `"Introducing Safe LLM-Agent Execution via Typed Tool Mediation and World-Effect Evaluation" pdf Jun Zhou`
8. `"Verified Toolchain Reference Monitor" "correlated"`
9. `LLM agent action verification correlated tool sources independent backend faults`
10. `LLM agent world state effect evaluation verification pre execution`

### Round 2 — bốn gap-fill queries

1. `"Look Before You Leap" "Althoubi" code github`
2. `"AgentOS" "World Effect Judge" "Jun Zhou" pdf`
3. `"LLM" "corroboration" "failure domain"`
4. `"LLM agent" "shared backend" verification`

Không chạy Round 3: các blockers còn lại là full-text/artifact access hoặc clarification, không nên tiếp tục search vô hạn. CARE chỉ screened metadata/abstract, chưa dùng làm substantive contrast. AgentOS trùng tên với products khác; chỉ dùng repository `zhoujune/AgentOS`. Forum/AI-generated “failure-domain” proposals không được dùng làm research evidence.

## Evidence đọc ở cấp nào?

| Nguồn | Đã kiểm tra | Chưa kiểm tra | Note để đọc sâu |
|---|---|---|---|
| AgentOS | Official metadata; pinned docs/policy/evaluation; Zenodo archives tải/parse/integrity | Publisher full text (HTTP 403), code-to-paper mapping, benchmark run, baseline fairness/cost, redistribution details | [[references/agentos-typed-tool-mediation]] |
| Look Before You Leap | Official metadata và HTML §1–8 | Supplementary, executable artifact, clarification cho ambiguity | [[references/look-before-you-leap-pre-action-verification]] |
| Project | Current RQ/results/limitations và frozen inventory | Human review, public-release snapshot/license, final course layout | [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]] |

**FACT — SOURCE PIN:** AgentOS `4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c`. Hai archives có 72 distinct task IDs, MD5 khớp Zenodo metadata và ZIP integrity pass. Đây là download/source check, không 72 experiments.

Temporary downloads nằm tại `/tmp/agentos-prior-art-Ki3JmQ`; không xem đây là permanent archive. URL/commit/checksums trong source note và manifest cho phép re-fetch. Không đưa third-party code/images/tasks vào research repo vì licensing boundary chưa rõ.

## Điều học được và điều chưa chắc chắn

**INFERENCE:** Taxonomy authorization / realizability / decision evidence giúp tránh “gate” thành một nhãn chứa mọi loại reliability. Nó chỉ giúp framing chính xác hơn, không tự là contribution mới.

**OPEN QUESTION:** RQ hẹp vẫn chưa được bảo vệ bằng independent topology hoặc measured head-to-head. Negative search không chứng minh không có prior art. Hai nguồn mới không nâng trạng thái `SURVIVES WITH REFINEMENT — PRELIMINARY`.

**OPEN QUESTION:** Course contribution có đủ sâu không? Chờ giảng viên đánh giá methodology/RQ/contribution. AI review không thay thế human review; không dự đoán conference acceptance từ kết quả này.

**FACT — KHÔNG TẠO EVIDENCE MỚI VỀ POLICY:** Không study episodes, model calls, GPU runs, confidence intervals hoặc unit-test rerun; không commit/push. Các số liệu positive/negative cũ giữ nguyên. Verification cuối lượt chỉ kiểm tra note/link/manifest và frozen hashes.

## Bạn nên đọc theo thứ tự nào?

1. Note này: hiểu vì sao đang kiểm tra lập luận thay vì chạy thêm.
2. [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]] → phần **Cập nhật hiện hành — 2026-10-04**: đọc bảng ba lớp và threat matrix.
3. [[projects/reliable-tool-using-ai-agents/paper/figure-guide]]: tự trả lời vì sao zero unsafe không đồng nghĩa task recovery; sau đó đọc từng paper note nếu cần evidence.

## Bước tiếp theo ở cuối lượt search — đã thực hiện

**Tích hợp delta prior art vào Related Work/citation ledger của manuscript**, giữ nguyên RQ/results và nêu rõ artifact-level AgentOS coverage; không dùng kết quả chưa rõ của nguồn mới để làm quantitative supporting claim. Sau đó bạn đọc contrast này cùng hai figures để chuẩn bị trao đổi với giảng viên. Không cần RTX 4060 cho bước này.

## Tiếp nối — paper v0.7, 2026-10-04

**FACT — EDITORIAL INTEGRATION:** Đã sửa §3.2, matrix §3.7, bibliography và Writing status của manuscript. AgentOS chỉ được contrast ở cấp inspected artifact; LBYL26 dùng cho realizability scope, không trích hiệu quả định lượng. Citation ledger có current delta riêng, giữ bảng 14-source audit cũ làm lịch sử.

### Giải thích thay đổi cho bạn

Related Work không chỉ là danh sách paper: nó phải cho người đọc biết người khác đã giải quyết điều gì và research của mình thực sự đo phần nào. Nay manuscript nói rõ **không phát minh pre-action gate**. Nó giữ comparison giữa hai cách chọn corroborator và phân tích điều kiện làm comparison đó thành công hoặc thất bại.

Nếu reviewer hỏi “AgentOS đã gate actions rồi, bạn mới ở đâu?”, câu trả lời đúng không phải “họ thiếu features của mình”. Câu trả lời là: bài này không claim gate mới; bài characterize decision-level source selection, accurate-metadata assumption, conditional utility và các kết quả âm trong một controlled artifact. Reviewer/giảng viên có thể vẫn đánh giá contribution này chưa đủ; prose sửa đúng không tự giải quyết câu hỏi đó.

### Evidence không thay đổi

Abstract, Introduction/RQ/H1, Background, Methods, Results, Discussion, Threats, Reproducibility và Conclusion được đối chiếu theo section hashes với v0.6. Frozen raw/inference inventory và hai figures không được sửa. Không runner/unit-test/model rerun, CI mới, commit/push hoặc human sign-off. Kết quả kiểm tra cuối lượt được ghi ở manifest/log.

### Bạn đọc gì bây giờ?

Mở [[projects/reliable-tool-using-ai-agents/paper/paper-draft]] §3.2 và §3.7, sau đó đối chiếu current delta trong [[projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03]]. Tự trả lời: study này đo **authorization decisions** hay **executed world-state effects**? Không cần đọc hết 15 papers ngay.

### Bước tiếp theo duy nhất — hiện hành

**Rà claim–evidence toàn bản manuscript cùng appendix/reproduction package và lập submission-readiness checklist.** Tách việc có thể sửa bằng documentation khỏi scientific limitations cần human feedback/experiment riêng. Không thêm runs chỉ để tăng row count hoặc né novelty threat.
