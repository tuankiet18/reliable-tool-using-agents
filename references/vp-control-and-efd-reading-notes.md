---
title: "Ghi chú đọc VP-Control và EFD — hai công trình gần nhất"
category: references
tags: [prior-art, provenance, verification, ai-agents, literature-review]
sources:
  - "https://arxiv.org/abs/2609.10969"
  - "https://arxiv.org/abs/2609.02925"
  - "https://arxiv.org/abs/2609.01873"
  - "journal/2026-10-06-prior-art-refresh-vp-control-and-efd.md"
created: 2026-10-16T17:00:00+07:00
updated: 2026-10-16T17:00:00+07:00
summary: >-
  Ý chính của VP-Control (commit gate, 2×2 model × nguồn, portfolio, live study) và EFD (epistemic fault domain, structural cut κE, DAQC), đọc toàn văn PDF ngày 2026-10-16; kèm quan hệ với paper của tác giả và câu tự kiểm tra.
provenance:
  extracted: 0.8
  inferred: 0.2
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: 2026-10-16
---

# Ghi chú đọc VP-Control và EFD

Claude đọc toàn văn PDF hai bài (qua `pdftotext`) ngày 2026-10-16; bài Bara chỉ đọc abstract. Số liệu dưới đây lấy nguyên từ bài gốc. **Tác giả nên tự đọc ít nhất abstract, phần Results và phần Limitations của mỗi bài** để tự trả lời được các câu ở cuối trang.

## 1. VP-Control (Zheng, Li, Yao, Long, 2026; arXiv:2609.10969)

*Engineering Reliable Commit Gates for Agentic AI: Cost-Aware Verification Portfolios under Common-Mode Data Failures.*

### Bài toán

Agent sắp thực hiện một hành động thay đổi trạng thái (restart job, đổi quyền truy cập, migrate schema). Trước đó có một **commit gate** quyết định commit, block hay defer (chuyển cho người). Gate có nhiều cách kiểm tra:
- hỏi lại một model khác;
- đọc một nguồn khác;
- chạy guard trong transaction;
- hỏi người.

Mỗi cách có chi phí và điểm yếu riêng. Quy tắc quen thuộc "thêm một verifier nữa" âm thầm giả định bằng chứng độc lập. Nhưng nếu hai interface cùng đọc một replica hay cache bị cũ, thì các verifier khác model vẫn **đồng ý trên cùng trạng thái sai**.

### Thiết kế

- **Benchmark:** 48 task template thuộc 4 lĩnh vực (scheduler, pipeline, storage, IAM). Mỗi template có 10 "thế giới" và 6 regime lỗi, tổng **2.880 scenario**.
- **Ba view bằng chứng:**
  - A: bản actor đã đọc;
  - A′: interface khác nhưng **cùng lineage** với A;
  - B: snapshot **độc lập**, tự trễ với xác suất 10%.
- **Model:** actor là Qwen3.5-9B và Gemma4-8B; verifier là các model nhỏ chạy local, Qwen3-4B (V1) và Phi-4-mini (V2).
- **Thí nghiệm 2×2 (RQ1):** mỗi ô đúng 2 lời gọi verifier. Hai yếu tố được tách riêng: cùng hay khác **model**, và cùng hay khác **nguồn**.

### Kết quả chính

**RQ1: đa dạng nguồn quan trọng hơn đa dạng model.** Tỷ lệ phê duyệt sai trên các đề xuất không an toàn:

| Regime | same model / same source | cross model / same source | same model / indep. source | cross model / indep. source |
|---|---:|---:|---:|---:|
| common stale | 91,5% | 81,7% | 9,8% | 7,3% |
| all degraded | 87,4% | 75,3% | 80,5% | 41,4% |
| gộp | 74,2% | 62,9% | 33,3% | 22,9% |

- **Hiệu ứng nguồn:** −0,409 [−0,479, −0,331], so với **hiệu ứng model:** −0,113.
- **Nguồn độc lập chỉ có ích khi nó thật sự có đường lỗi độc lập.** Khi mọi nguồn cùng hỏng (regime all degraded), lợi ích gần như mất.
- **Một nhánh dùng verifier dạng luật** (không phải LLM) cho kết quả cùng hướng. Vậy hiệu ứng đến từ cấu trúc bằng chứng, không phải do một cặp LLM cụ thể.

**RQ2: portfolio controller.** Bộ điều khiển chọn kế hoạch kiểm tra dựa trên metadata quan sát được (định danh nguồn và lineage, tuổi dữ liệu, cờ health…). Với mục tiêu rủi ro 5%, test set cho **1,9% unsafe** và **38,2% safe coverage**. Ở cùng ngân sách, portfolio tốt hơn các chính sách cố định.

**RQ3: giới hạn.**
- Gặp loại lỗi chưa thấy khi huấn luyện, rủi ro lên **16–26%** dù đặt mục tiêu 5%.
- Trên FinQA, **hiệu ứng nguồn đảo chiều**, vì verifier nhỏ không đủ năng lực đọc bằng chứng: *nguồn độc lập chỉ giúp khi verifier đủ giỏi*.
- Đưa bằng chứng tốt hơn cho actor tự sửa không thay được gate: sau một lần replan vẫn còn **69,8%** đề xuất không an toàn.

**RQ4: chạy thật (HTTP/SQLite, có preregistration).**
- Khi có một thay đổi xảy ra **sau** lúc kiểm tra và trước lúc ghi, mọi gate chỉ dựa vào verifier đều thua.
- Chỉ **full atomic guard** (kiểm tra ngay trong transaction ghi) đạt **0 unsafe trong 216 episode**.
- Request ID idempotent chặn được hiệu ứng ghi trùng khi mất phản hồi.

### Giới hạn mà chính tác giả nêu

- *"Lineage is supplied"*: lineage được cung cấp sẵn. Nguồn độc lập vẫn có thể trễ, hoặc chung một lỗi chưa được mô hình hóa.
- Phát hiện lineage và chống lineage giả nằm ngoài phạm vi.
- Model nhỏ, chạy local trên một laptop. Live study chỉ có một service và một writer.
- Hiệu chỉnh rủi ro chỉ là xấp xỉ, không phải đảm bảo.

**Khuyến nghị của họ:** nền tảng nên gắn **evidence identifier, upstream lineage, thời điểm quan sát, health** vào mọi tool result. Các kiểm tra chung lineage phải được tính là **một** failure domain, kể cả khi dùng model khác nhau.

## 2. EFD (He, Yu, 2026; arXiv:2609.02925)

*The Illusion of Independent Quorums: Epistemic Fault Domains and Correlated Cognitive Failures in Agentic Quorums.*

### Bài toán

Hệ multi-agent hay dùng **quorum**, ví dụ 3 trên 5 reviewer đồng ý thì mới cho phép hành động. Nhưng các reviewer thường đọc chung một telemetry, một tài liệu hay một tool backend. Khi nguồn đó sai, ba phiếu thật ra chỉ là **một nhân chứng**. Câu khẩu hiệu của bài: *"count fault-separated epistemic paths, not agent instances"*, tức là đếm số đường bằng chứng tách biệt, không đếm số agent.

### Khái niệm

- **Epistemic Fault Basis:** tập các lỗi gốc mà ta chọn mô hình hóa, ví dụ telemetry, retrieval, tool. Mọi kết luận đều **tương đối với tập này**.
- **Epistemic Fault Domain (EFD):** với mỗi lỗi gốc, tập các reviewer mà lỗi đó lan tới được.
- **Structural Epistemic Cut κE:** số **lỗi gốc ít nhất** cần để "phủ" một nhóm reviewer đủ quyền cho phép hành động.
  - Ví dụ: quorum 3 trên 5, nhưng một nguồn telemetry cũ đi tới cả 3 reviewer, nên **κE = 1** dù có 5 phiếu.
- **Semantic Compromise Cut κS:** số lỗi ít nhất thật sự gây ra một commit không an toàn.

### Kết quả lý thuyết

1. Dưới ba giả định (phê duyệt hành động không an toàn là sai; mọi phê duyệt sai đều truy được về một lỗi gốc; ước lượng mức lan của lỗi là bảo thủ), **κE ≤ κS**. Nghĩa là cut cấu trúc là chặn dưới cho số lỗi cần để gây hại.
2. **Quorum lớn tùy ý vẫn có thể có κE = 1.** Nhiều phiếu không bảo đảm an toàn.
3. **Phát hiện thêm phụ thuộc chung chỉ có thể làm giảm hoặc giữ nguyên** mức an toàn được ghi nhận, không bao giờ tăng.
4. **Thêm reviewer mà giữ ngưỡng cũ không tăng được cut.** Muốn sửa phải thay nguồn bằng chứng hoặc đổi luật bỏ phiếu.
5. Tính κE là bài toán **NP-hard**, vì quy về được set cover.

### Bộ điều khiển DAQC

DAQC chọn reviewer theo lineage dự kiến. Sau khi có phiếu, nó dựng lại provenance thực tế và chỉ cho commit nếu κE ≥ ngưỡng. **Phụ thuộc chưa biết được coi là chung** (bảo thủ), để không thổi phồng mức an toàn.

### Đánh giá

- **Chỉ có mô phỏng Monte Carlo** với reviewer kiểu Bernoulli đã được lập trình sẵn.
  - Quorum 2 trên 3 dùng chung bằng chứng: **97,3%** commit sai.
  - Khi tách đường bằng chứng: **6,7%**.
  - Đổi model nhưng giữ chung bằng chứng gần như **không giúp** (96,8%).
- Có kèm một benchmark 120 task đóng băng, nhưng **chưa có kết quả chạy model thật** trong bài.

### Giới hạn mà chính tác giả nêu

- κE là tính chất **cấu trúc** của mô hình đã khai báo, **không phải xác suất an toàn**.
- **"False separation":** nếu lineage bị thiếu hoặc bị làm giả, κE bị thổi phồng và đảm bảo mất ý nghĩa. Phụ thuộc chưa biết nên coi là chung; môi trường có đối thủ cần attestation.

## 3. Bara (2026; arXiv:2609.01873), chỉ đọc abstract

*Epistemic Sybil Resistance.* Thêm một agent không phải là thêm một quan sát. Một bộ tổng hợp **chỉ đọc nội dung báo cáo** không thể phân biệt báo cáo độc lập với bản sao từ cùng nguồn. Trong thí nghiệm, giữ một nguồn bằng chứng và tăng số báo cáo từ 1 lên 32 làm độ phủ của posterior sụp từ 0,940 xuống 0,263. Kết luận của bài: phải theo dõi **nguồn gốc bằng chứng**, không đếm số agent hay độ giống nhau của báo cáo.

## 4. Quan hệ với paper của tác giả

| | VP-Control | EFD | Paper này |
|---|---|---|---|
| Có chứng minh nguồn độc lập tốt hơn không | Có, thực nghiệm mạnh (2×2, LLM, live) | Có, định lý và mô phỏng | Có, nhưng chỉ là **replication** (RQ1) |
| Lineage lấy từ đâu | **Cung cấp sẵn** | Giả định khai báo; nêu rủi ro false separation | **Câu hỏi chính**: nhãn sai thì sao (RQ2), nhãn thật ra sao (RQ3) |
| Đo metadata thật | Không | Không | Có, 120 MCP server |
| Chạy agent thật | Có (model nhỏ, local) | Không (chỉ mô phỏng) | Không có hiệu ứng trên live agent |

**INFERENCE: chỗ ba bài nối với nhau.**
- "False separation" của EFD chính là **recall thấp** (bỏ sót phụ thuộc chung) trong RQ2. Định lý J định lượng được khi nào nó làm selection tệ hơn random: khi `r < φ`.
- EFD khuyên **coi phụ thuộc chưa biết là chung**, trong khi selector của paper này coi nhãn thiếu là "không phải ứng viên" rồi fallback ngẫu nhiên. Đây là hai chính sách khác nhau khi gặp missing label; so sánh chúng là một hướng mở rộng.
- VP-Control khuyên nền tảng **gắn lineage vào mọi tool result**. RQ3 cho thấy MCP server hiện tại **không làm điều đó** ở khoảng 70% cặp. Đây là bằng chứng thực nghiệm cho khoảng cách giữa khuyến nghị và thực tế.
- Kết quả FinQA của VP-Control nhắc một giả định của paper này: corroborator độc lập được coi là báo đúng, chỉ có leakage. Nếu verifier yếu, nguồn độc lập cũng không cứu được. Điều này nên được nêu trong threats.

## 5. Câu tự kiểm tra (trả lời không cần nhìn ghi chú)

1. Trong VP-Control, vì sao regime "all degraded" làm mất lợi ích của nguồn độc lập?
2. κE = 1 với quorum 5 người nghĩa là gì? Thêm người thứ 6 với cùng ngưỡng có giúp không, và vì sao?
3. VP-Control và EFD cùng giả định điều gì về lineage? Paper của anh lấp khoảng trống đó ra sao?
4. Vì sao không thể nói "paper của chúng tôi là người đầu tiên chứng minh nguồn độc lập tốt hơn"?
5. Kết quả FinQA của VP-Control cảnh báo gì cho giả định "corroborator độc lập thì báo đúng"?
