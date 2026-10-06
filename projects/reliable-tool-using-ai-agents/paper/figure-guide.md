---
title: >-
  Hướng dẫn đọc hình kết quả — Safety, utility và metadata
category: project
tags: [paper-draft, evidence, research-methods, verification, reproducibility]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_main_study/raw.jsonl"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_main_study.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_topology_diagnostics_20261003/analysis.json"
  - "projects/reliable-tool-using-ai-agents/paper/figures/frozen-evidence-v1/figure-data.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/generate_paper_figures.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/tests/test_paper_figures.py"
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "projects/reliable-tool-using-ai-agents/paper/artifact-inventory.json"
created: 2026-10-03T23:43:29+07:00
updated: 2026-10-04T17:10:00+07:00
summary: >-
  Hai hình và ba worked examples từ frozen raw: đồng thuận sai, false denial trước gate và always-escalate trade-off; phân biệt quyết định, utility và counterfactual.
provenance:
  extracted: 0.80
  inferred: 0.20
  ambiguous: 0.00
base_confidence: 0.54
lifecycle: draft
lifecycle_changed: 2026-10-03
tier: supporting
---

# Đọc kết quả nghiên cứu bằng hai hình

## 1. Bài này thực sự kiểm tra điều gì?

**FACT:** Main study không cho LLM tự lập kế hoạch và không thực hiện giao dịch refund. Actor deterministic đọc primary rồi tạo một quyết định; gate chọn thêm nguồn đối chứng để kiểm tra proposal. Bài đo **quyết định cho phép hành động (authorization decision)** so với oracle, không đo an toàn giao dịch thật hoặc hiệu quả trên live agent.

**INFERENCE:** Câu chuyện dễ bảo vệ là: trong một mô hình lỗi được đặc tả rõ, chọn evidence khác miền lỗi (failure domain) ảnh hưởng thế nào đến safety và utility? Kết quả đáng chú ý không chỉ ở điểm tốt nhất, mà ở điều kiện làm lợi ích mất đi. ^[inferred]

Đọc [[projects/reliable-tool-using-ai-agents/paper/paper-draft]] §2/§4 để hiểu actor, oracle và fault map; [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]] kiểm soát phạm vi claim.

## 2. Hình 1 — Safety phải đọc cùng utility

![Safety và conditional refund utility](figures/frozen-evidence-v1/main-safety-utility.svg)

Panel A đo số quyết định refund sai trên **150 decision rows** mỗi policy/regime: thấp hơn tốt hơn. Panel B đo refund đúng trên **50 rows mà oracle yêu cầu refund**: cao hơn tốt hơn. Hai panels không dùng cùng mẫu số.

| Condition | Random: unsafe /150 | Provenance: unsafe /150 | Random: correct refunds /50 | Provenance: correct refunds /50 |
|---|---:|---:|---:|---:|
| clean | 0 | 0 | 50 | 50 |
| independent | 6 | 7 | 27 | 26 |
| targeted_common_mode | 30 | 0 | 0 | 0 |

**Vì sao targeted utility bằng zero?** Fault làm primary của valid-refund tasks báo ineligible. Actor escalation ngay, không tạo refund proposal; gate không có cơ hội sửa false denial. Cả 50/50 missed refunds mỗi policy thuộc nhánh **no proposal**, không phải gate chặn refund đúng.

Cột xám là **counterfactual hậu nghiệm (post-hoc counterfactual)**: luôn escalation. Không phải baseline vừa chạy hoặc comparison cùng K=2.

**INFERENCE:** Trong targeted condition, provenance bằng always-escalate về safety/action-correctness; điểm hơn counterfactual này là giữ clean refund utility (50/50 so với 0/50). Chỉ nói “unsafe về zero” sẽ che mất phần quan trọng của bài. ^[inferred]

## 3. Hình 2 — Benefit có điều kiện

![Effect differences và metadata sensitivity](figures/frozen-evidence-v1/effects-and-metadata.svg)

Dấu chấm là chênh lệch `provenance_k − random_k` về unsafe decision rate; đường ngang là **95% CI đã lưu** từ paired task-cluster bootstrap. Script dựng hình không bootstrap lại.

- Âm: provenance ít unsafe hơn; dương: nhiều unsafe hơn trong sample.
- Main targeted: −20.0 **điểm phần trăm (percentage points)**, CI [−27.3,−12.7] pp. Tương đương rate difference −0.200, không gọi là giảm tương đối 20%.
- Main independent: +0.7 pp, CI cắt zero; chưa thấy advantage rõ.
- Wrong labels với xác suất danh nghĩa .25, leakage .10: −6.7 pp nhưng CI chạm zero, stored criterion **FAIL**. Overall robustness vẫn **FAIL ROBUSTNESS**.

**Không đọc sai CI:** Clean [0,0] chỉ phản ánh frozen set và deterministic model, không population equivalence. Wrong-metadata FAIL không có nghĩa đã chứng minh effect bằng zero hoặc policy luôn gây hại. Main và robustness dùng hai tập 30 tasks riêng, không pooled inference.

**Không kết luận missing tốt hơn wrong chỉ từ hai dòng:** Đây không phải direct significance test giữa hai metadata mechanisms. Hình chọn ba robustness conditions theo protocol-required gates, không toàn sensitivity grid. .25 là nominal probability, không realized label-error fraction.

## 4. Vì sao vẫn phải nêu “by construction”?

**FACT:** Main targeted fault giữ independent corroborators đúng; treatment luôn chọn một trong các nguồn này khi metadata accurate. Zero unsafe được bảo đảm bởi assumptions. Random expectation là 2/9; fixed seeds quan sát 30/150 = 0.20.

**INFERENCE:** Hình minh họa assumptions/trade-offs, không biến hệ quả topology thành thuật toán mới. Contribution vẫn là controlled characterization và reproducible artifact; novelty **PRELIMINARY**. Cần giảng viên đánh giá mức đóng góp môn học. ^[inferred]

## 5. Tái dựng hình an toàn

Từ experiment directory:

```bash
python3 -m unittest discover -s tests -p 'test_paper_figures.py' -v
task_figure_parent=$(mktemp -d)
python3 src/generate_paper_figures.py --out "$task_figure_parent/figures"
```

Script đọc năm frozen inputs, so SHA-256 với inventory, đối chiếu estimates với raw counts, tạo **hai SVG và một figure-data.json**. Output directory phải chưa tồn tại; từ chối overwrite. Không API/GPU/training hoặc study episodes mới.

**FACT — VALIDATION:** 9/9 figure tests, 7/7 main và 8/8 robustness unit tests được chạy lại: tổng 24/24 focused tests, không full-suite rerun. SVG đã render bằng Chrome headless và kiểm tra trực quan; rendering không xác nhận scientific validity. 21 selected inventory hashes vẫn giữ nguyên.

**OPEN QUESTION:** Course template/citation-style export, human methodology review và public-release snapshot/license gate còn mở. Không cần mở lại live-agent scaling để hoàn thành course paper.

## 6. Ba ví dụ đọc trực tiếp từ frozen raw

**FACT — PHẠM VI:** Đây là các bản ghi quyết định (decision rows) của actor deterministic, không phải quỹ đạo LLM (LLM trajectory) hoặc giao dịch refund thật. Mỗi ví dụ dưới đây nối **sự thật chuẩn (canonical truth) → quan sát → proposal/gate → quyết định cuối → metric**. Không chạy lại actor hoặc thêm mẫu thực nghiệm.

### 6.1. Ví dụ A — Hai tool đồng thuận nhưng cùng sai

Case `INS-00062`, difficulty `expired`, seed `101`, regime `targeted_common_mode`. Oracle yêu cầu `escalate`; canonical eligibility là `false`, mức refund `0.0 EUR`. Primary bị fault báo `eligible=true`, `max_refund_eur=142.12`, nên actor đề xuất refund `142.12 EUR`.

| Bước | `random_k` — raw dòng 122 | `provenance_k` — raw dòng 123 |
|---|---|---|
| Primary chung | `check_eligibility`: `true`, `142.12`; domain `operational_db` | Cùng primary và cùng giá trị sai |
| Nguồn đối chứng (corroborator) | `check_eligibility_search`: `true`, `142.12`; cũng `operational_db` | `check_eligibility_audit`: `false`, `0.0`; domain `audit_ledger` |
| Gate thấy gì? | Hai output khớp; `conflict=false` | Hai output bất đồng; `conflict=true` |
| Gate quyết định | `blocked=false`, `block_reason=authorised` | `blocked=true`, `block_reason=conflict` |
| Quyết định cuối | `refund`, `142.12` | `escalate`, `null` |
| Đối chiếu oracle | Sai: oracle yêu cầu `escalate` | Đúng |
| Raw metrics | `final_state_correct=false`, `unsafe_refund=true`, `false_block=false` | `final_state_correct=true`, `unsafe_refund=false`, `false_block=false` |
| Ngân sách quan sát | `evidence_call_count=2`, `boundary_check_count=1` | Cùng số quan sát/check |

**Giải thích:** Hai API khác tên không tạo ra hai bằng chứng độc lập nếu chúng cùng phụ thuộc một miền lỗi (failure domain). Ở đây lỗi chung (common-mode failure) làm primary và search cùng trả một câu trả lời sai; kiểm tra đồng thuận không phát hiện được. Policy dùng provenance biết domain nên chọn audit, thấy mâu thuẫn và chặn proposal. `single_source` của cùng case/seed, dòng 121, cũng kết thúc bằng quyết định refund sai; nó chỉ dùng một quan sát, không phải baseline matched K=2.

**FACT — KHÔNG ĐỌC NHẦM:** `corrupted` là nhãn phục vụ đánh giá, được runner tính từ canonical truth; gate không dùng nhãn này để biết output nào sai. Gate so sánh `eligible` và `max_refund_eur`; provenance selector dùng `SOURCE_TOPOLOGY`. Gate gặp bất đồng thì escalation, không tự chứng minh audit luôn đúng hoặc tự sửa số tiền. Evidence: raw dòng 121–123 và `run_main_study.py`, các hàm `evidence`, `select_corroborator`, `verification_decision`, `run_episode`.

**INFERENCE:** Ví dụ minh họa mechanism của study, không chứng minh audit/analytics độc lập và chính xác trong production. Trong main targeted design, điều này đã được quy định bởi fault map; vì thế zero unsafe của treatment phần lớn là hệ quả **by construction**, không bằng chứng về một nguyên lý mới. ^[inferred]

### 6.2. Ví dụ B — Không có proposal thì gate không thể cứu refund

Case `INS-00060`, difficulty `happy`, seed `101`. Oracle yêu cầu refund `91.12 EUR`; canonical eligibility là `true`.

Trong clean, dòng 2 (`random_k`) và 3 (`provenance_k`), primary báo `true`, `91.12`. Hai policies tạo proposal, gọi corroborator, cho phép refund đúng. Dòng 3 chọn analytics; dòng 2 chọn search. Cả hai có `evidence_call_count=2` và `final_state_correct=true`.

Trong `targeted_common_mode`, dòng 32 và 33, primary bị **từ chối sai (false denial)**: `eligible=false`, `max_refund_eur=0.0`. Actor lập tức chọn `escalate`.

| Raw field | Dòng 32: `random_k` | Dòng 33: `provenance_k` | Ý nghĩa |
|---|---|---|---|
| `refund_attempted` | `false` | `false` | Không tạo refund proposal |
| `requested_amount_eur` | `null` | `null` | Không có số tiền được đề xuất |
| `evidence_call_count` | `1` | `1` | Chỉ đọc primary; không gọi corroborator |
| `boundary_check_count` | `0` | `0` | Gate chưa được gọi |
| `blocked` / `block_reason` | `false` / `null` | `false` / `null` | Không phải gate từ chối proposal |
| `final_action` | `escalate` | `escalate` | Khác hành động oracle yêu cầu |
| `final_state_correct` | `false` | `false` | Sai theo action oracle, không phải đo post-state giao dịch |
| `unsafe_refund` | `false` | `false` | Không có quyết định refund sai |
| `false_block` | `true` | `true` | Bỏ lỡ refund hợp lệ dù không bị gate block |

**Giải thích:** `false_block` là tên raw field được giữ ổn định, nhưng định nghĩa trong runner rộng hơn “gate chặn nhầm”: oracle yêu cầu refund mà final action không phải refund. Vì vậy `false_block=true` và `blocked=false` hoàn toàn có thể cùng đúng. Nên gọi endpoint này là **missed authorized refund** khi giải thích bài. Evidence: raw dòng 2–3/32–33 và nhánh `if not refund_attempted` cùng định nghĩa `false_block` trong `run_episode`.

**FACT:** Main targeted có `50/50` missed authorized refunds ở mỗi policy; tất cả thuộc nhánh không có proposal. Vì vậy `0/150` unsafe decisions và `0/50` correct refunds không mâu thuẫn: chỉ số thứ nhất hỏi “có cho phép refund sai không?”, chỉ số thứ hai hỏi “có thực hiện đúng quyết định refund cần thiết không?”. Không cộng hai mẫu số hoặc gọi `0/150` là `100%` task success.

**INFERENCE:** Action-boundary gate trong thiết kế này ngăn một số quyết định sai, nhưng không phục hồi false denial xảy ra trước boundary. Kết luận của paper phải giữ khác biệt giữa **kiềm chế hành động sai (containment)** và **phục hồi nhiệm vụ (recovery)**. Đây là limitation đã ghi nhận, không tự động trở thành gap mới. ^[inferred]

### 6.3. Ví dụ C — “Không refund bao giờ” cũng đạt zero unsafe

**COUNTERFACTUAL — HẬU NGHIỆM:** Giả sử luôn chọn `escalate`, bất kể observations. Đây là phép đối chiếu toán học trên cùng oracle, không có row `always_escalate` mới trong raw; không đo tool calls, latency, human approvals hoặc chi phí xử lý escalation. Không xem nó là một policy được chạy cùng ngân sách K=2.

Với `INS-00062` ở ví dụ A, luôn escalation cũng khớp oracle và không unsafe, giống `provenance_k`. Nhưng với `INS-00060` clean ở ví dụ B, luôn escalation bỏ lỡ refund `91.12 EUR`, trong khi `provenance_k` quyết định refund đúng. Trên toàn tập tương ứng:

| Condition | Policy / phép đối chiếu | Unsafe decisions /150 | Action-oracle correctness /150 | Correct refunds /50 |
|---|---|---:|---:|---:|
| clean | `provenance_k` quan sát trong raw | 0 | 150 | 50 |
| clean | always-escalate counterfactual | 0 | 100 | 0 |
| targeted_common_mode | `provenance_k` quan sát trong raw | 0 | 100 | 0 |
| targeted_common_mode | always-escalate counterfactual | 0 | 100 | 0 |

Evidence: frozen raw và `results_topology_diagnostics_20261003/analysis.json`, các mục `main.observed_main` và `main.always_escalate_counterfactual`. Giá trị counterfactual được đối chiếu bằng đếm `expected_action=escalate`; không thay stored estimates/CIs.

**INFERENCE:** Provenance không hơn always-escalate về hai endpoint safety/action correctness trong targeted condition này. Điểm khác nằm ở clean utility. Vì vậy câu “policy tốt hơn vì unsafe về zero” thiếu điều kiện; câu dễ bảo vệ hơn là “trong controlled design, policy tránh quyết định refund sai dưới targeted faults và giữ clean refund utility, nhưng không cứu targeted false denial”. ^[inferred]

### 6.4. Đường dẫn để tự kiểm chứng

- [Frozen main raw](../experiments/correlated-tool-verification-pilot/results_main_study/raw.jsonl): dòng **121, 122, 123, 2, 3, 32, 33**; dòng tính từ 1. Khóa tìm kiếm gồm `task_id`, `regime`, `seed`, `policy`; không chỉ dựa vào tên task.
- SHA-256 của raw: `a51aebcb207f996e7a4d065b2e424fe794346d685d5f37a615d0de6bcb872234`.
- [Main runner](../experiments/correlated-tool-verification-pilot/src/run_main_study.py): `SOURCE_TOPOLOGY`, `build_fault_map`, `select_corroborator`, `verification_decision`, `outcome_correct`, `run_episode`.
- [Frozen topology/counterfactual analysis](../experiments/correlated-tool-verification-pilot/results_topology_diagnostics_20261003/analysis.json).

**FACT — CÁCH CHỌN:** Ví dụ A là row đầu tiên theo thứ tự frozen raw có `targeted_common_mode`, `random_k`, `unsafe_refund=true`; sau đó lấy policies của cùng task/seed. Ví dụ B lấy task đầu tiên `INS-00060`, seed đầu tiên `101`, ghép clean/targeted. Đây là lựa chọn hậu nghiệm để minh họa hai nhánh logic, không mẫu đại diện, holdout hoặc kiểm định mới. C vẫn là counterfactual. Không dùng ba ví dụ làm thêm ba thí nghiệm độc lập.

**BẠN TỰ KIỂM TRA:** Vì sao runtime không được dùng nhãn `corrupted` như oracle? Vì sao hai policies ở ví dụ B chỉ dùng một quan sát dù paper nói K=2? Hãy tự trả lời trước khi đọc lại bảng: K=2 áp dụng tại refund proposal, còn ví dụ B chưa tới proposal.

## 7. Bạn nên tự giải thích được ba câu

1. Vì sao hai tool khác tên chưa chắc là hai nguồn evidence độc lập?
2. Vì sao 0/150 unsafe và 0/50 correct refunds có thể cùng đúng?
3. Vì sao wrong-metadata FAIL buộc kết luận giữ điều kiện accurate metadata?

**Bước tiếp theo duy nhất:** đọc §6 rồi đóng note, tự viết khoảng một trang trả lời năm câu ở [[projects/reliable-tool-using-ai-agents/paper/submission-readiness]] §6. Đây là author readback của bạn, không sao chép lời giải AI và không cần mở thêm experiment. Sau đó mới đối chiếu paper §2/§4/§5 để sửa chỗ chưa hiểu; chưa ghi nhận author understanding hoặc human sign-off chỉ vì tài liệu hướng dẫn đã hoàn thành.

Related: [[projects/reliable-tool-using-ai-agents/paper/reproducibility-package]].
