---
title: "Rà soát paper theo góc nhìn reviewer khó tính — 2026-10-03"
category: project
tags: [paper-draft, evidence, research-methods, verification, reproducibility]
sources:
  - "journal/2026-10-05-main-study-influence-audit.md"
  - "journal/2026-10-04-clean-environment-core-reproduction.md"
  - "journal/2026-10-04-pre-action-prior-art-audit.md"
  - "projects/reliable-tool-using-ai-agents/paper/figure-guide.md"
  - "projects/reliable-tool-using-ai-agents/paper/reproducibility-package.md"
  - "projects/reliable-tool-using-ai-agents/paper/supplementary-appendix.md"
  - "projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03.md"
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_main_study.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_main_study.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_main_study/raw.jsonl"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_main_study/inference.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_robustness_gate.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/generate_secondary_varied_schedule.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_secondary_varied.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_secondary_varied/analysis-summary.json"
  - "synthesis/Protocol - Action-Boundary Provenance Verification Main Study.md"
  - "journal/2026-09-28-secondary-varied-schedule-replication.md"
  - "journal/2026-10-03-live-agent-opportunity-diagnostic.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_topology_diagnostics.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_topology_diagnostics_20261003/analysis.json"
  - "https://arxiv.org/html/2603.02345"
  - "https://arxiv.org/html/2607.01236v2"
  - "https://arxiv.org/abs/2606.18037"
  - "https://arxiv.org/abs/2602.21517"
created: 2026-10-03T15:30:38+07:00
updated: 2026-10-05T08:15:00+07:00
summary: >-
  MAJOR REVISION: construct, utility và novelty cần bounded claims; v0.7 cập nhật prior art nhưng không đóng scientific limitations hoặc human review gate.
lifecycle: draft
---

# Rà soát paper như một reviewer khó tính

## 1. Kết luận và phạm vi review

**Verdict: MAJOR REVISION.** Draft cần sửa đáng kể trước khi nộp. Các số liệu chính tái kiểm tra được, nhưng một số tên metric và câu diễn giải mạnh hơn điều code thực sự đo.

Theo quyết định của tác giả, đầu ra hiện tại là **controlled empirical study cho môn học**, không bắt buộc kết quả trên agent thật hoặc submission hội nghị. Không có yêu cầu phải cứu live-agent experiment để hoàn thành paper này. Nếu định submission nghiên cứu, mức novelty và sức nặng của empirical contribution vẫn là rủi ro lớn; review này không dự đoán acceptance của venue cụ thể.

Đây là **AI-assisted reviewer-style audit** cho một solo researcher, không phải independent human review, giảng viên sign-off hay peer review. Không chạy thêm model, thay protocol, sửa raw data hoặc sửa manuscript trong lượt review này.

Snapshot: Git HEAD `18bcf40e92755a6fed05ec2cdacb5cf863cd7410`, kèm các thay đổi chưa commit đã có trước review. `paper-draft.md` được rà có SHA-256 `ff0c330b5c71f7b2844cb32509c0d901386ba1c6928155bf75fd42eec2bc4b33`. Số dòng dưới đây chỉ áp dụng cho snapshot đó, không phải permalink tới một working-tree revision đã commit.

### Điểm tốt cần giữ

- Có so sánh paired, primary observation/fault map chung và ngân sách đối chứng giống nhau ở action boundary.
- Có independent-fault negative control, robustness với metadata sai và evidence bất lợi được giữ lại.
- Raw artifacts, task manifest, scripts và hash cho phép kiểm tra kết quả; không chỉ có biểu đồ tổng hợp.
- Secondary adaptation và live-agent diagnostic đã công khai giới hạn, không được dùng để giả lập external validation.
- Phạm vi controlled study phù hợp điều kiện thời gian/chi phí hiện tại. Vấn đề cần sửa trước tiên là **claim–measurement alignment**, không phải mua API hoặc chạy thêm GPU.

## 2. Các finding cần xử lý

`P0` = sai lệch giữa claim và phép đo, phải sửa trước khi nộp. `P1` = ảnh hưởng mạnh đến lập luận/diễn giải. `P2` = chất lượng trình bày và khả năng tái lập.

| ID | Mức | Finding và bằng chứng | Cách sửa tối thiểu / điều kiện đóng finding |
|---|---|---|---|
| R1 | P0 | Draft §2.5, dòng 131, gọi outcome là refund “được thực hiện” và “final-state correctness”. `run_main_study.py:126–132,135–197` chỉ tạo action/amount rồi so với oracle; `World` ở dòng 200–225 chỉ cấp canonical eligibility. Không có thực thi `issue_refund` hay kiểm tra post-state trong main run. | Đổi cách gọi trong prose/table sang **action-oracle correctness** và **unsafe refund decision**; mô tả rõ simulated authorization. Giữ raw key cũ, có bảng mapping. Không coi đây là final-state evaluation của agent thật. |
| R2 | P0 | `false_block` tại `run_main_study.py:171` là mọi expected-refund task kết thúc không refund. Nó gồm cả trường hợp actor không tạo proposal. Trong targeted regime, cả hai policy có 50 false blocks nhưng cả 50 đều **không có refund attempt**, không phải gate chặn proposal đúng. | Đổi tên aggregate thành **missed authorized refund / false escalation**; phân biệt no-proposal abstention và gate-induced false block bằng `refund_attempted`, `blocked`. Không đổi nhãn raw âm thầm. |
| R3 | P1 | Draft dòng 38,165–186 nói deterministic nhưng chưa diễn đạt đủ rõ actor: primary báo eligible thì request đúng amount primary; ngược lại escalate ngay. Có 1.350 grid rows, không phải 1.350 LLM trajectories hoặc 1.350 nhiệm vụ độc lập. | Thêm actor pseudocode, đơn vị experimental row = task × seed × regime × policy. Nêu 30 task instances sinh từ sáu strata và không gọi LLM trong main/robustness. |
| R4 | P1 | Main table dòng 221–228 thiếu utility phân tầng dưới faults. Targeted regime có action correctness 70/150 vs 100/150 nhưng **cả hai chỉ đúng 0/50 task cần refund**. Correct escalation góp toàn bộ correctness của provenance. | Báo cả conditional correctness của expected-refund và expected-escalation tasks; nói rõ containment không recovery. Không viết “preserves task completion under failures”. |
| R5 | P1 | Source topology và fault map bảo đảm nguồn khác domain trả truth trong main targeted regime (`run_main_study.py:17–22,57–93`). Safety advantage là hệ quả có thể tính trước của thiết kế. Đây không phải bằng chứng tự phát rằng một thuật toán mới hiểu agent tốt hơn. | Thêm analytical sanity check ở §4; đóng góp là đo/đặc tả điều kiện của mechanism và giới hạn metadata, không phải phát minh nguyên lý independent corroboration. |
| R6 | P1 | Bảng main bỏ `single_source` dù raw đã có; paper không bàn always-abstain. Tuy nhiên **always-block diagnostic đã có** trong `analyze_secondary_varied.py:145–156`. | Hiển thị single-source, đưa always-block diagnostic vào phần safety–utility. Nêu diagnostic là counterfactual, ngoài matched K=2, pooled cả hai policy; không gọi đó là experiment baseline mới. |
| R7 | P1 | Bootstrap theo task tốt hơn coi seeds độc lập, nhưng 30 task từ fixed strata không đại diện production. Clean CI `[0,0]` phản ánh model/sample. Gate `clean_success_noninferior_point_margin_0_05` tại `analyze_main_study.py:210–216` kiểm tra **point estimate**, không một formal non-inferiority test. | Xác định estimand và phạm vi task-cluster bootstrap; mô tả “pre-specified point-margin criterion”. Không suy CI suy biến thành chứng minh population equality. |
| R8 | P1 | Protocol expected loss có call-cost term; `analyze_main_study.py:175–185` chỉ dùng unsafe + λ × false_block. `evidence_call_count` là số modeled observations, không latency/token/API measurement. | Ghi đúng executed analysis và protocol deviation; ở cặp K=2, call-count contribution triệt tiêu khi cùng attempt schedule, không phải đã đo overhead thực tế. Giữ λ là sensitivity giả định, không economics thực tế. |
| R9 | P1 | Main topology cố định; secondary varied schedule dùng quota 6/12 same-domain selections, 3/12 leakage và 4/4/4 fault locations (`generate_secondary_varied_schedule.py:45–53,61–76`). Đây không phải observed real fault distribution. Baseline secondary có hai corroborators, main có ba. | Mô tả quota/hash schedule, denominator và khác biệt baseline; gọi secondary là semantic adaptation/schedule sensitivity, không independent topology replication hay native benchmark performance. |
| R10 | P1 | Exact-combination novelty vẫn PRELIMINARY. RIVA đã đặt vấn đề kiểm tra bằng tools được cho là independent; ProvenanceGuard và TEA-CXA chặn claims rộng. Draft dòng 145–155 có nguy cơ tạo đối thủ quá yếu nếu nói prior work “không bảo vệ” thay vì không evaluate setting này. | Dùng comparison theo threat model, oracle, dependence assumption, outcomes; không claim prior methods chắc chắn thất bại khi chưa chạy. Giữ novelty ở contribution thực nghiệm hẹp. |
| R11 | P2 | “Preregistered” hiện có internal journal/hash; initial Git commit chứa cả study và results. Không có independent timestamp từ registry trong artifact đã rà. Wrong-25 là xác suất làm sai label, không cam kết realized 25%. CI chạm 0 không chứng minh effect bằng 0. | Gọi internal pre-specified protocol, công khai chronology và evidence timestamp giới hạn; báo nominal vs realized corruption; viết “did not reliably retain advantage”, không “proved no effect”. |
| R12 | P2 | References dòng 345–356 thiếu AgentFlow được nêu trong text, một số authors/venue thiếu; Results có nhiều debugging chronology. Writing status còn để external/live gates như điều kiện hoàn thiện mặc dù course scope đã chọn. | Chuẩn hóa citation IDs/metadata, đưa chronology/schema debug sang appendix; cập nhật checklist theo controlled-paper scope. Supplement liệt kê environment, upstream pins, licenses, reproduction commands và artifact inventory. |

Không finding nào ở trên đòi hỏi đổi outcome sau khi xem kết quả. Sửa prose/metric dictionary là đính chính construct; nếu về sau đổi executor hoặc endpoint, phải mở study riêng và giữ study cũ.

## 3. Kiểm tra lại số liệu: những gì paper phải nói rõ

**FACT — RECOMPUTED FROM FROZEN RAW:** Đọc lại `results_main_study/raw.jsonl`, không chạy lại runner. Mỗi regime/policy có 150 rows = 30 tasks × 5 seeds; gồm 50 expected-refund và 100 expected-escalation rows.

| Regime | Policy | Action-oracle correctness /150 | Unsafe refund decisions /150 | Refund proposals | Correct expected-refund outcomes /50 | Missed authorized refunds /50 | Trong số missed: no proposal / gate block |
|---|---|---:|---:|---:|---:|---:|---:|
| clean | random_k | 150 | 0 | 50 | 50 | 0 | 0 / 0 |
| clean | provenance_k | 150 | 0 | 50 | 50 | 0 | 0 / 0 |
| independent | random_k | 121 | 6 | 62 | 27 | 23 | 13 / 10 |
| independent | provenance_k | 119 | 7 | 62 | 26 | 24 | 13 / 11 |
| targeted_common_mode | random_k | 70 | 30 | 100 | 0 | 50 | 50 / 0 |
| targeted_common_mode | provenance_k | 100 | 0 | 100 | 0 | 50 | 50 / 0 |

Ví dụ cách đọc hàng cuối: provenance không authorize refund sai trong 150 modeled decisions. Nó escalate đúng 100 trường hợp phải escalate, nhưng cũng escalate sai cả 50 trường hợp đáng ra phải refund. Đây là **safety containment**, không phải agent đã khôi phục và hoàn thành 2/3 nghiệp vụ refund.

Các số `30/150 = 20%` và `0/150 = 0%` vẫn đúng. Nếu đổi denominator sang refund attempts, chúng là `30/100 = 30%` và `0/100 = 0%`. Không trộn denominator trong Abstract, table hoặc slides. Report số lần và mẫu số trước, tỷ lệ sau.

`single_source` cũng đã có trong raw: clean correct `150/150`, unsafe `0/150`; independent correct `112/150`, unsafe `25/150`; targeted correct `0/150`, unsafe `100/150`. Baseline này cho thấy giá trị chung của verification, còn random-vs-provenance mới tách source-selection mechanism.

### Metric dictionary đề xuất

| Raw key hiện có | Tên dùng trong main/robustness paper | Đo được / không đo được |
|---|---|---|
| final_state_correct | action-oracle correctness | Action/amount khớp expected action/amount; **không** kiểm tra state mutation sau refund. |
| unsafe_refund | unsafe refund decision | Simulated final decision là refund sai action/amount; **không** quan sát giao dịch thực hoặc real harm. |
| false_block | missed authorized refund / false escalation | Expected refund nhưng final action không refund; gồm cả actor abstention và gate block. |
| blocked | runtime gate rejection | Gate từ chối proposal; chỉ là false block nếu proposal đáng ra hợp lệ. |
| evidence_call_count | modeled evidence-call count | Số evidence entries; **không** token usage, network requests hay latency. |

Mapping này chỉ áp dụng cho runners đã rà. Live-agent và secondary có executor/oracle khác; phải mô tả endpoint riêng, không đổi tên tất cả `final_state` keys một cách máy móc.

## 4. Reviewer hỏi: kết quả có gần như được bảo đảm bởi thiết kế không?

**INFERENCE — ANALYTICAL SANITY CHECK:** Trong main targeted regime:

- Canonical escalation chiếm π = 20/30 = 2/3 task instances.
- Fault biến primary của các task này thành eligible sai. Một trong ba corroborators của random-K chia sẻ domain với primary, nên xác suất chọn nguồn cùng hỏng là q = 1/3.
- Expected unsafe decision rate của random-K theo selector model là πq = 2/9 ≈ 22,2%; observed fixed-seed rate là 30/150 = 20%.
- Provenance-K luôn chọn một corroborator khác domain; targeted model làm các nguồn này luôn đúng. Vì vậy expected unsafe decision rate bằng 0 trong mô hình này.
- Các task canonical refund bị primary báo ineligible, actor không tạo proposal, nên gate không được dùng để sửa false denial.

Điều này **không làm kết quả sai**, nhưng làm yếu novelty nếu contribution chỉ là “nguồn độc lập giúp tránh lỗi tương quan”. Reviewer có thể hỏi: “Tại sao cần 1.350 rows để chứng minh điều đã suy ra từ topology?” Câu trả lời phù hợp là experimental characterization của assumptions, metadata sensitivity và safety–utility trade-off, không phải tăng số rows để biến một hệ quả thiết kế thành discovery.

Nên thêm công thức expected rate rồi đối chiếu observed finite-seed rate. Đây là phân tích hậu nghiệm trong review, không được ghi như hypothesis đã đăng ký trước.

### Trivial baseline: always escalate / always block

**INFERENCE — POST-HOC COUNTERFACTUAL, NOT A NEW RUN:** Nếu main actor luôn chọn escalate, oracle của cùng 150 rows cho unsafe = 0, action correctness = 100/150 và correct expected-refund = 0/50 ở cả clean lẫn targeted. Dưới targeted, provenance có đúng các endpoint này; dưới clean, provenance giữ `150/150` thay vì `100/150`. Do đó lợi ích vượt always-escalate nằm ở **giữ clean utility**, không ở phục hồi valid refunds dưới targeted fault.

**FACT — EXISTING SECONDARY DIAGNOSTIC:** Secondary summary đã có always-block counterfactual. Clean: chặn `264/264` clean proposals. Targeted-25: chặn `48/48` clean proposals và 192 wrong safety proposals. Đây là số **pooled rows từ cả hai policies**, không 264 task instances độc lập và không một baseline vừa chạy mới. Diagnostic nằm ngoài primary matched-K=2 comparison. Cần giải thích denominator hoặc chuẩn hóa theo từng policy trước khi đặt cạnh utility `9/24` và `18/24`.

Không cần lập tức implement baseline mới chỉ để có những số đã suy ra hoặc đã lưu. Nếu muốn một comparison thực nghiệm mới, khóa trước protocol và metric riêng.

## 5. Novelty và related work: điểm reviewer dễ tấn công

**FACT — PRIOR ART:** RIVA mô tả kiểm chứng nhận định bằng nhiều tools được xem là independent; vì vậy không được mô tả họ đơn giản là “đếm tool khác tên”. Điểm có thể so sánh là cách định nghĩa/kiểm tra shared-backend failure domains và controlled common-mode evaluation, không phải tuyên bố RIVA hoàn toàn bỏ qua independence. [RIVA full text](https://arxiv.org/html/2603.02345).

**FACT — PRIOR ART:** *Safeguarding LLM Agents from Misalignment through Provenance Analysis* kiểm tra grounding của hành động theo task/docs/history. Từ setting đó có thể nói paper không evaluate thí nghiệm correlated silent backend failures của mình; không thể suy ra mọi implementation của họ chắc chắn không bảo vệ trong setting này. [ProvenanceGuard full text](https://arxiv.org/html/2607.01236v2).

Hai work tên ProvenanceGuard phải được phân biệt bằng tên đầy đủ/citation ID; *ProvenanceGuard: Source-Aware Factuality Verification for MCP-Based LLM Agents* là work khác. TEA-CXA cũng trực tiếp đe dọa claim rộng về lựa chọn tool response đáng tin. [Source-aware ProvenanceGuard](https://arxiv.org/abs/2606.18037), [TEA-CXA](https://arxiv.org/abs/2602.21517).

**INFERENCE:** Contribution dễ bảo vệ nhất hiện tại là một artifact và controlled characterization của failure-domain-aware boundary authorization, gồm negative controls và metadata sensitivity. Broad algorithmic novelty chưa mạnh. Không nên thêm “first”, “novel framework” hoặc tuyên bố không có prior art chỉ vì chưa tìm được exact combination.

Việc kiểm tra nguồn trong lượt này chỉ nhắm metadata/claim quan trọng, không phải một systematic literature review mới. DOI Knight–Leveson resolve nhưng full text từ publisher không đọc được trong lượt này; không gán thêm quantitative claims từ full text chưa kiểm tra. Prior-art search trước đó vẫn **PRELIMINARY**.

## 6. Methodology, thống kê và reproducibility

### Cần viết rõ trong Methods

1. Tool outputs là gì, các trường có kiểu nào, canonical eligibility lấy từ đâu; action oracle tách biệt observed evidence.
2. Actor deterministic đọc **chỉ primary** để tạo proposal. Gate không replan, regenerate action hoặc chọn amount mới.
3. Failure domain là modeled dependency group. Main registry được cung cấp đúng trước run, không được tự suy ra từ repository hoặc deployment.
4. Targeted corruption tác động primary/search cùng domain; các independent sources giữ truth. Independent regime dùng per-interface Bernoulli faults. Đây là stress conditions, không measured production prevalence.
5. K=2 là **hai modeled evidence observations trên mỗi refund proposal**, không hai calls cho mọi task và không tính toàn bộ agent workflow.
6. Số seeds, cách chọn corroborator, paired fault schedule; lý do bootstrap theo task và giới hạn sáu strata/fixed task generator.
7. Main/robustness đo decision-level endpoints; secondary/live sử dụng những oracle/executor riêng. Không cộng tất cả rows thành một thống kê chung.

### CI và pass/fail

Giữ main estimate `−0.200` và CI `[-0.273,-0.127]` như kết quả task-cluster bootstrap của frozen study. Không gọi đây là CI cho production tool-using agents. Số rows lớn hơn số task clusters không tạo thêm task diversity.

Clean CI `[0,0]` và clean `150/150` đúng trong current model/sample, không chứng minh tác động clean bằng zero ở mọi task. “PASS main gate” là đạt operational criteria đã ghi, không chứng minh novelty hoặc external validity.

Wrong metadata condition không giữ được criterion CI-upper < 0 là một robustness failure theo protocol; không đồng nghĩa đã chứng minh effect = 0, always harmful hoặc worst-case security. `wrong_25` phải phân biệt xác suất label noise 0,25 với realized error fraction.

Protocol có công thức cost rộng hơn analyzer. Vì hai primary policies có cùng primary và cùng attempt indicator, modeled additional-call count bằng nhau ở main comparison; chênh lệch call-cost term sẽ bằng 0 nếu cùng unit cost. Nhưng chưa có empirical latency/token/monetary-cost claim, và không thể bỏ term khi so với single-source mà không giải thích.

### Reproducibility chưa đồng nghĩa validity

Byte-identical rerun kiểm tra artifact consistency, không kiểm tra xem construct đã đặt tên đúng, fault model thực tế hay oracle độc lập. `load_cases` xác nhận goal/difficulty drift nhưng không trực tiếp enforce Git commit của upstream; paper phải hướng dẫn kiểm tra pin trước chạy, không chỉ tin manifest ghi một commit.

Protocol/journal cho thấy chronology nội bộ tác giả đã ghi. Hash xác nhận nội dung, không chứng minh độc lập thời điểm viết trước results. Nếu chưa có timestamp/registry bên ngoài, dùng “internally pre-specified protocol” và công khai limitation thay vì implied public preregistration.

## 7. Rà theo từng phần manuscript

| Phần | Đánh giá | Sửa ưu tiên |
|---|---|---|
| Title | Quá dễ được hiểu là general agent evaluation. | Gắn “controlled study” hoặc “decision-level”; không phải bắt buộc đổi hướng đề tài. |
| Abstract | Có số liệu, nhưng endpoint và phạm vi actor chưa đủ chính xác. | Nêu deterministic actor, modeled authorization, n/mẫu số, utility dưới faults, metadata assumption. |
| Introduction | Motivation hợp lý; ví dụ thực tế mạnh hơn setting đã đo. | Tách motivating harms khỏi experimentally observed decisions; nêu core question là evidence dependence. |
| Related Work | Có direct threats, chưa thành so sánh literature theo axes. | Ưu tiên RIVA/ProvenanceGuard/TEA-CXA; recovery background rút gọn; không suy “không evaluate” thành “không thể bảo vệ”. |
| Problem Formulation | Gate rõ nhưng actor/fault mathematics chưa đầy đủ. | Pseudocode actor + topology diagram + analytical expected unsafe rate. |
| Methods | Chưa phân biệt tốt simulation và executing environment. | Metric dictionary, task generator/strata, modeled-call budget, paired selection/fault schedule. |
| Results | Main estimate tái kiểm tra được; bỏ qua conditional utility và baseline có sẵn. | Counts/denominators, single-source, no-proposal vs gate-block, always-block diagnostic; không tổng hợp trái setting. |
| Discussion | Có limitations tốt, nhưng dễ nâng containment thành completion. | Nêu targeted valid-refund outcomes 0/50; metadata fragility; utility trade-off ở secondary. |
| Threats to Validity | Đã có nhiều caveats, thiếu construct mismatch vừa phát hiện. | Đưa R1/R2 vào construct validity, topology guarantee và task-template dependence vào internal/statistical validity. |
| Reproducibility | Artifact mạnh hơn prose hiện tại. | Một reproduction recipe pinned, rõ files/versions/license/commands/checksums, API/GPU = 0 cho core. |
| Conclusion | “Loại bỏ unsafe refunds” quá mạnh nếu không phân biệt decision/state. | “Observed zero unsafe refund decisions in this controlled setting”; không đưa live effect hoặc production guarantee. |

Lịch sử sửa UTF-8, Windows checkout, schema review và chọn seed sau khi xem trace nên để supplementary chronology. Main paper không cần kể toàn bộ hành trình dự án.

## 8. Wording đề xuất — chưa thay canonical RQ hoặc draft

### Title — proposed

*A Controlled Study of Failure-Domain-Aware Action Authorization under Correlated Silent Tool-Output Failures*

### RQ — English, proposed wording clarification

Given accurate failure-domain metadata, does independent-domain corroboration reduce unsafe refund authorization decisions relative to random corroboration at a matched two-observation boundary budget, while preserving clean action-oracle correctness in a deterministic controlled workflow?

### Giải thích tiếng Việt

Trong workflow mô phỏng với actor deterministic và metadata đúng, chọn nguồn đối chứng khác failure domain có giảm quyết định cho phép refund sai so với chọn nguồn ngẫu nhiên, khi cả hai dùng cùng hai observations tại boundary, mà vẫn giữ quyết định đúng ở điều kiện clean hay không?

Đây là **đề xuất làm rõ đúng construct đã đo**, không kết quả mới hoặc quyết định nâng novelty. RQ vẫn **PRELIMINARY** cho đến khi tác giả/giảng viên duyệt wording và contribution.

### Methods — đoạn đề xuất

Main study là decision-level simulation, không chạy LLM agent hoặc thực thi giao dịch refund. Một actor deterministic tạo refund proposal với amount lấy từ primary output nếu output báo eligible; ngược lại actor chọn escalation. Verification gate kiểm tra proposal bằng primary và một corroborator. Chúng tôi so sánh final action/amount với canonical oracle. Vì không cập nhật World state sau refund, endpoint này được gọi là action-oracle correctness, không phải final-state correctness.

### Results/Conclusion — đoạn đề xuất

Trong targeted common-mode condition, random corroboration cho 30 unsafe refund decisions trên 150 rows, so với 0/150 ở independent-domain corroboration; paired task-cluster bootstrap difference là −0.200, 95% CI [−0.273, −0.127]. Cả hai đúng 150/150 clean decisions. Tuy nhiên cả hai chỉ đúng 0/50 expected-refund outcomes dưới targeted faults: gate ngăn harmful authorization chứ không phục hồi nhiệm vụ refund. Đây là kết quả có điều kiện trên synthetic topology và accurate metadata, không bằng chứng về real transaction safety hoặc hiệu quả trên live agents.

## 9. Kế hoạch sửa bài tối thiểu

| Thứ tự | Công việc | Cần experiment mới? | Xong khi |
|---|---|---|---|
| 1 | Sửa R1/R2 ở Abstract, Outcomes, Methods, bảng chính và Conclusion; thêm metric dictionary. | Không | Không còn claim state execution từ main/robustness hoặc gọi no-proposal abstention là gate false block. |
| 2 | Thêm actor/topology và analytical sanity check; bảng counts + conditional utility + single-source. | Không; tái tính frozen raw đã có | Người đọc suy được expected rate và thấy 0/50 targeted valid-refund outcomes. |
| 3 | Diễn giải always-block diagnostic có sẵn, sửa statistic/cost/protocol wording. | Không | Denominators, diagnostic status, point-margin criterion và nominal metadata noise rõ. |
| 4 | Thu hẹp contributions/related-work contrast; đưa secondary và negative live validity vào đúng scope. | Không | Không first/production/generalization claim; topology và oracle không bị che bằng tổng số episodes. |
| 5 | Chuẩn hóa references, appendix/reproduction recipe; kiểm tra toàn văn và gửi giảng viên methodology/RQ/contribution. | Không | Citation complete, claim–evidence audit pass, course-paper checklist rõ. |

Ước lượng lập kế hoạch: khoảng 2–3 buổi tập trung để sửa nội dung, cộng một buổi kiểm tra citations/artifact; không phải cam kết thời gian. Hỏi giảng viên về **mức contribution phù hợp môn học**, không yêu cầu thầy xác nhận mọi case/oracle.

**Bước tiếp theo tại thời điểm review:** sửa manuscript theo R1/R2 trước, dùng wording decision-level và metric dictionary, rồi kiểm tra Abstract–Methods–Results–Conclusion có cùng một endpoint hay chưa.

### Trạng thái xử lý — 2026-10-03, paper v0.2

**FACT — EDITORIAL CHANGE:** R1/R2 đã được xử lý trong [[projects/reliable-tool-using-ai-agents/paper/paper-draft]] version `0.2`: Abstract, RQ/H1, Outcomes, Methods, bảng Results, Discussion, Threats và Conclusion dùng action-oracle correctness/unsafe refund decisions; bảng mới tách no-proposal abstention khỏi gate rejection. Raw keys và kết quả thực nghiệm giữ nguyên. [[synthesis/Candidate RQ - Provenance-Aware Verification under Correlated Tool Failures]] đã đồng bộ working wording; dated historical RQ và protocol vẫn giữ nguyên.

**OPEN QUESTION — tại thời điểm v0.2:** Chưa đóng R5–R12. Bước tiếp theo sau sửa construct là làm rõ analytical expectation từ source topology và safety–utility baseline có sẵn, rồi kiểm tra novelty/citations. MAJOR REVISION vẫn là verdict cho toàn draft; cập nhật này không phải reviewer sign-off.

### Trạng thái xử lý — 2026-10-03, paper v0.3

**FACT — POST_HOC ANALYSIS / EDITORIAL CHANGE:** Script `analyze_topology_diagnostics.py` xác minh sáu frozen input hashes và tái dựng chính xác unsafe counts của cả tám secondary safety cases; không chạy episodes hoặc model calls mới. Paper §4.6/§5.3/§5.6 bổ sung:

- **R5:** topology/actor cho main random expectation `2/9` và provenance zero unsafe by construction; observed random vẫn `30/150`, không thay point estimate/CI bằng kỳ vọng.
- **R6:** single-source giữ trong bảng chính; always-escalate counterfactual cho main và always-block diagnostic có sẵn được chuẩn hóa theo unique secondary scenario, không measured matched-K=2 baselines. Main targeted provenance bằng always-escalate; clean utility tạo khác biệt.
- **R9, phần mechanism:** khác biệt main/secondary corroborator pools và quota-overlap được viết rõ. Secondary targeted-25 counts `59/96` vs `24/96` suy được đầy đủ từ schedule; không independent semantic generalization.
- **R8, phần cost interpretation:** §6.2 ghi proxy loss hậu nghiệm và break-even ratios, không actual API/latency/human cost hoặc economic optimality.

Đây là phản hồi nội bộ cho findings, **không independent reviewer sign-off**. Không đánh dấu toàn bộ R5–R12 đã đóng; statistics/protocol chronology, novelty comparison, citation metadata và manuscript structure còn phải rà toàn văn. Contribution hiện nên là controlled characterization và reproducible artifact có giới hạn, không phát minh nguyên lý independent corroboration.

**Bước tiếp theo tại thời điểm v0.3:** kiểm tra contribution/related-work contrast với direct prior art và chuẩn hóa references. Kết quả lượt sửa này được ghi ở cập nhật v0.4 dưới đây; không tiếp tục live-agent scaling.

### Trạng thái xử lý — 2026-10-03, paper v0.4

**FACT — EDITORIAL / SOURCE AUDIT:** [[projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03]] ghi coverage của 14 citation IDs; không phải 14 full-paper deep reads. Contributions thu hẹp thành controlled comparison, conditional characterization và artifact. RIVA contrast nhận diện alternative verification paths; provenance/verification contrasts dùng **evaluated setting**, không unsupported claim rằng systems chắc chắn thất bại. Thêm AgentFlow bibliography và AgentOS adjacent threat với metadata/README-only limitation. Không head-to-head, không experiment mới.

- **R10:** broad novelty/strawman wording đã sửa; substantive novelty và contribution sufficiency vẫn cần human methodology review. Exact feature conjunction không là contribution tự thân.
- **R12 — citations/scope:** IDs, authors, versions và venue status được đối chiếu; missing pagination không tự điền. Supervisor briefing đã đồng bộ decision-level RQ/H1 và controlled course scope. Citation-style export, appendix/reproduction recipe và full-manuscript structure còn mở.
- Không đánh dấu toàn bộ findings `CLOSED`; verdict **MAJOR REVISION** giữ nguyên, chưa independent reviewer sign-off. Raw hashes và measured outcomes không đổi.

**Bước tiếp theo hiện hành:** final whole-manuscript consistency/structure pass, tách chronology và khóa reproducibility inventory trước giảng viên review; không mở rộng experiments.

### Trạng thái xử lý — 2026-10-03, paper v0.5

**FACT — EDITORIAL / LOCAL REANALYSIS:** Whole-manuscript pass giữ decision-level endpoints và unchanged RQ/H1. Discovery/schema/Windows chronology chuyển sang [[projects/reliable-tool-using-ai-agents/paper/supplementary-appendix]], negative live result vẫn trong main paper. §4.5/R11 làm rõ internal pre-specified chronology, không independent preregistration. §8/R12 nối [[projects/reliable-tool-using-ai-agents/paper/reproducibility-package]] và 21-file SHA-256 inventory; 8 selected analysis outputs byte-identical trong local temporary directory.

R12 structure/recipe đã có draft; chưa citation-style export, course template/figures, committed release snapshot, fresh-machine generation hoặc public license gate. Pinned WorkBench tree thiếu root license file; không mặc nhiên chuyển indirect MIT attribution thành independently verified redistribution clearance. Giữ **MAJOR REVISION**, không human sign-off. Scientific limitations R5/R7/R9/R10 về constructed topology, population inference và contribution không thể đóng chỉ bằng sửa prose.

**Bước tiếp theo tại thời điểm v0.5:** tác giả đọc paper và appendix, gửi đồng bộ briefing cho giảng viên review RQ/methodology/contribution; nhận feedback rồi final format/figures. Không thêm experiments để tăng row count hoặc tiếp tục live scaling.

### Trạng thái xử lý — 2026-10-03, paper v0.6

**FACT — DERIVED FIGURES:** Hai SVG từ frozen evidence đặt safety cạnh conditional refund utility, và tách main CI khỏi post-main metadata stress conditions. [[projects/reliable-tool-using-ai-agents/paper/figure-guide]] giải thích denominators, pp, counterfactual, no-proposal losses và wrong-metadata FAIL. Generator đối chiếu năm input hashes và raw estimates/stored CIs; 24/24 focused unit tests đạt (9 figures + 7 main + 8 robustness), không full suite.

Không thay RQ/H1, raw, estimates, CIs hoặc thêm study episodes/API calls. Rendering và tests không đóng scientific limitations về constructed topology/population/novelty. **MAJOR REVISION / PRELIMINARY** và human feedback gate giữ nguyên. Course-template layout/citation export/author proofreading còn mở.

**Bước tiếp theo hiện hành:** tác giả dùng hai hình để tự giải thích trade-off, rồi giảng viên review methodology/RQ/contribution; không mở live scaling để cứu effect.

### Trạng thái xử lý — 2026-10-04, paper v0.7

**FACT — RELATED-WORK INTEGRATION:** §3.2/§3.7 và references có artifact-level AGOS26 contrast, qualitative LBYL26 scope và 15 citation IDs với explicit reading limits. Numerical results từ nguồn còn ambiguity không được dùng. Journal/citation ledger/briefing đã đồng bộ; RQ/H1, Methods, Results và frozen figures không đổi. Không experiment mới hoặc head-to-head.

**R10/R12:** prior-art framing/citation coverage được sửa thêm; chưa chứng minh novelty, contribution sufficiency, public-release readiness hoặc full-paper AgentOS comparison. Không đánh dấu findings `CLOSED`; **MAJOR REVISION / PRELIMINARY** và human review gate giữ nguyên.

**Bước tiếp theo hiện hành:** final claim–evidence audit giữa manuscript, appendix và package, rồi submission-readiness checklist. Course formatting, author understanding, human feedback và licensing/snapshot còn mở; không tăng episode count để che các blockers này.

### Trạng thái xử lý — 2026-10-04, paper v0.8

**FACT — CLAIM ALIGNMENT, NOT SIGN-OFF:** [[projects/reliable-tool-using-ai-agents/paper/submission-readiness]] đối chiếu toàn manuscript với ledger/appendix/package và stored evidence. Sửa stale version labels, reanalysis chronology và reader-facing decision-row labels; không đổi scientific values hoặc câu hỏi. Course checklist tách khỏi optional public-release/external-claim gates. Không chạy study episodes, model/API calls, unit tests hoặc bootstrap mới.

R12 documentation alignment đã có pass trong phạm vi audit; author understanding, template/citation export và supervisor assessment còn mở. R5/R7/R9/R10 scientific limits được giữ, không đánh dấu CLOSED vì prose đã rõ. **MAJOR REVISION / PRELIMINARY** vẫn là AI-assisted assessment, không hội nghị verdict hoặc human approval.

**Bước tiếp theo hiện hành:** tác giả viết explanation một trang trả lời năm câu trong readiness note trước final export. Không yêu cầu giảng viên review từng case/oracle hoặc tiếp tục live scaling.

## 10. Evidence integrity và liên kết

### Cập nhật reproducibility — 2026-10-04, paper v0.9

**FACT:** [[journal/2026-10-04-clean-environment-core-reproduction]] ghi fresh upstream clone/base install và core replay trong venv mới cùng host: main/robustness raw, manifests và sáu analysis JSONs khớp 10/10 selected files; 15 focused tests đạt. R12 setup evidence mạnh hơn local reanalysis-only; chưa complete dependency/build lock, secondary/fresh-machine/independent reproduction. Không thêm independent samples hoặc live-agent effect; MAJOR REVISION/PRELIMINARY và scientific findings vẫn giữ.

### Bổ sung R7 — 2026-10-05, post-hoc influence audit

[[journal/2026-10-05-main-study-influence-audit]] tính 123 deletion summaries trên frozen main raw: targeted Δ giữ âm qua 30 task, 5 seed và 6 stratum deletions; independent stratum-deletion Δ từ −0.80 đến +1.60 pp. Appendix §F/ledger C32 ghi phạm vi mô tả. Không thêm CI, mẫu độc lập hoặc thay point-margin gate. Targeted sign vẫn bị ràng buộc bởi zero unsafe by construction; stratum deletion đổi task composition. Vì vậy chỉ bổ sung evidence về mức tập trung của kết quả, **R7 về population/statistical scope vẫn mở**. Manuscript v0.9 giữ nguyên, không reviewer/human sign-off.

Hashes kiểm tra lại trong audit:

- Main raw: `a51aebcb207f996e7a4d065b2e424fe794346d685d5f37a615d0de6bcb872234`.
- Robustness raw: `f22e7f29c97a89eda20bdb57f9e59fa43581adb3d3b6475ee40e926492ab1982`.
- Secondary varied raw: `40a419491011308dcce04db477c4a98dbda2e543d2db531b0a4fb07c08b43c35`.

Review không phát hiện số main raw bị đổi so với hashes lịch sử. Finding mới là **cách định nghĩa/diễn giải**, không cáo buộc data fabrication. Không sửa code, raw artifacts hoặc canonical protocol trong lượt này.

Related:

- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
- [[projects/reliable-tool-using-ai-agents/reliable-tool-using-ai-agents]]
- [[synthesis/Candidate RQ - Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Prior-Art Threat - Provenance Metadata and Source Selection]]
- [[synthesis/Protocol - Action-Boundary Provenance Verification Main Study]]
- [[journal/2026-09-28-secondary-varied-schedule-replication]]
- [[journal/2026-10-03-live-agent-opportunity-diagnostic]]
