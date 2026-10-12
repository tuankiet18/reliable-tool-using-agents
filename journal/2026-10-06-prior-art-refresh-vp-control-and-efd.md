---
title: "2026-10-06 — Prior-art refresh: VP-Control và Epistemic Fault Domains"
category: journal
tags: [research-log, prior-art, novelty, verification, tool-failure]
sources:
  - "https://arxiv.org/abs/2609.10969"
  - "https://arxiv.org/abs/2609.02925"
  - "https://arxiv.org/abs/2509.25292"
  - "https://arxiv.org/abs/2507.16044"
created: 2026-10-06T12:00:00+07:00
updated: 2026-10-06T12:00:00+07:00
summary: >-
  Hai paper mới (VP-Control 2609.10969, EFD 2609.02925) preempt phần lớn claim chính; khác biệt còn lại là độ chính xác của failure-domain metadata và prevalence thực tế.
provenance:
  extracted: 0.75
  inferred: 0.25
base_confidence: 0.6
lifecycle: draft
lifecycle_changed: 2026-10-06
---

# Prior-art refresh — 2026-10-06

**Phạm vi:** AI-assisted, một lượt tìm kiếm web + đọc văn bản PDF của hai paper. Chưa có human review. Không thay đổi paper, ledger hay số liệu. Các nhận định dưới đây cần tác giả tự đọc lại hai paper trước khi dùng trong bài.

## Phát hiện chính

**FACT — VP-Control (arXiv:2609.10969, nộp 2026-09-10).** Zheng, Li, Yao, Long. *Engineering Reliable Commit Gates for Agentic AI: Cost-Aware Verification Portfolios under Common-Mode Data Failures.* Đã đọc văn bản PDF.
- Thiết kế 2×2 tách model diversity khỏi evidence-source diversity, mỗi ô dùng đúng hai call (matched budget).
- Regime `common_stale`: A và A′ (hai interface cùng upstream) cùng stale. Same-source so với independent-source dưới common-mode data failure.
- Bảng locked-test (unsafe approve, %): `common stale` same-model/same-source 91.5, cross-model/same-source 81.7, same-model/indep-source 9.8, cross-model/indep-source 7.3; pooled 74.2 / 62.9 / 33.3 / 22.9.
- Có live study 216 episode với SQLite/HTTP và preregistration; artifact công khai trên Figshare (DOI `10.6084/m9.figshare.33511441.v1`).
- **Lineage metadata được cung cấp sẵn** ("Lineage is supplied; independent sources can still lag or share an unmodeled fault"). Tác giả nêu "lineage discovery and protection against forged provenance remain outside the implementation".
- Trong văn bản PDF tôi **không tìm thấy** thí nghiệm gán sai hoặc làm nhiễu lineage label (grep `mislabel|wrong label|label noise|misspecif` không ra kết quả; chỉ có "noisy health flags"). Đây là kết quả tìm chuỗi, không phải đọc toàn bộ từng trang.

**FACT — Epistemic Fault Domains (arXiv:2609.02925, nộp 2026-08-24).** He, Yu. Lý thuyết và mô phỏng về quorum reviewer chia sẻ upstream; định nghĩa EFD và structural cut κ_E; controller DAQC; benchmark 120 task. Đã trích văn bản PDF cho phần giới hạn: unknown dependencies được xử lý bảo thủ là shared; tác giả nêu rõ rủi ro "incomplete provenance, or fabricated lineage metadata. False separation can therefore inflate κ_E". Chưa đọc kỹ phần benchmark/kết quả.

## INFERENCE — Tác động lên novelty

1. Claim "nguồn đối chứng độc lập về failure domain giảm quyết định sai dưới common-mode failure so với cùng nguồn/ngẫu nhiên" đã được VP-Control đo trước, với thiết kế mạnh hơn (preregistered, live study, artifact công khai). Nhãn "SURVIVES WITH REFINEMENT" trong [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]] cần được xem lại, vì audit [[journal/2026-10-04-pre-action-prior-art-audit]] không có hai paper này (cả hai xuất bản trước ngày audit).
2. Hiện tượng "thêm voter không sửa common-mode" (EFD) và "evidence lineage quan trọng hơn model diversity" (VP-Control) không còn là phát hiện mới. Bài của vault nên trình bày chúng như **replication độc lập trong miền refund**, không phải discovery.
3. Khoảng trống còn lại (cả hai paper tự nêu là giới hạn): **độ chính xác của lineage metadata** và **lineage discovery**. Robustness gate hiện có của vault (wrong_25 + leakage 0.10 FAIL) chính là phần liên quan trực tiếp nhất tới khoảng trống này; cần làm nó mạnh và hệ thống hơn (nhiều mức noise, sweep có đường cong), thay vì chỉ một điều kiện.
4. Prevalence thực tế của shared backend giữa các tool vẫn chưa được hai paper đo. Search snippet (chưa đọc sâu) cho thấy các measurement study MCP có số liệu liên quan: 88,6% official MCP server dựa trên REST API (arXiv:2507.16044), dependency monoculture trong marketplace (arXiv:2509.25292). Cần đọc trực tiếp trước khi trích.

## Hành động đề xuất (chưa thực hiện)

- Đọc trực tiếp toàn văn VP-Control và EFD; cập nhật Related Work, ledger và nhãn novelty **sau khi** tác giả xác nhận.
- Chuyển trọng tâm contribution sang: metadata-validity characterization (sweep noise) + khảo sát prevalence trên tool thật.
- Giữ cảnh báo: kết quả của vault vẫn là mô phỏng quyết định; VP-Control có thiết kế mạnh hơn nên không dùng so sánh superiority.

## Phân tích sweep nhiễu nhãn (post-hoc, exploratory) — cùng ngày

**Việc làm:** `src/analyze_metadata_sweep.py` (file mới) dẫn công thức chính xác xác suất `provenance_k` chọn từng corroborator theo tỷ lệ nhãn thiếu `m` và nhãn sai `w`, bằng cách liệt kê toàn bộ `4^4` trạng thái nhãn quan sát. Output ở `results_metadata_sweep_20261006/` (summary.json, sweep.csv). Không có episode mới, không gọi model, không ghi đè kết quả đóng băng.

**FACT — kiểm chứng với code thật:** công thức khớp selector trong `run_robustness_gate.py` với sai lệch tối đa `0.0036` trên 7 cặp (m, w), 40.000 draws mỗi cặp.

**FACT — kết quả trong mô hình nhiễu độc lập:**
- Provenance **không bao giờ tệ hơn random** trên toàn lưới (`m ≤ 0.5`, `w` đến `1−m`, leakage `0–0.5`). Chênh lệch luôn âm.
- Xác suất chọn nhầm tool cùng domain **không đơn điệu theo `w`**: ở leakage 0.10, m=0 là `0 → 0.187 (w=.25) → 0.307 (w=.5) → 0.208 (w=1)`.

**INFERENCE — diễn giải robustness gate FAIL:** với tỷ lệ escalation `π=2/3` (giả định cho tập robustness, chưa kiểm), điều kiện `wrong .25, leakage .10` có dự đoán chênh lệch `≈ −0.088` (provenance 0.179, random 0.267). Quan sát đã lưu: `−0.067`, CI `[−0.133, 0.000]`; provenance 0.187, random 0.253. Dự đoán nằm trong CI quan sát. Do đó "FAIL" phù hợp với **một lợi ích thật nhưng nhỏ mà 30 task chưa đủ power để tách khỏi 0 theo tiêu chí "upper CI < 0"**, không phải bằng chứng lợi ích biến mất. Đây là suy luận: chưa tính power chính thức, chưa kiểm `π` của tập robustness.

**Giới hạn quan trọng:** mô hình nhiễu giả định các nhãn sai **độc lập** theo từng tool. Lỗi nhãn có hệ thống (ví dụ phụ thuộc ẩn: hai tool độc lập bị gán nhầm cùng domain với primary) có thể khiến provenance tệ hơn random. Điều này chưa được phân tích; là hướng tiếp theo.

**Cập nhật:** đã kiểm `π` cho tập robustness: `20/30` task escalation, đúng `2/3`. Các mean chênh lệch theo task tái tính từ raw khớp số đã lưu (`−0.133`, `−0.153`, `−0.067`).

## Lỗi nhãn có hệ thống (hidden dependency) — post-hoc, exploratory

**Việc làm:** `src/analyze_hidden_dependency.py`, output `results_hidden_dependency_20261006/`. Metadata được mô hình như một bộ phân loại "tool có dùng chung failure domain với primary không": recall `r` (1−r = phụ thuộc ẩn) và tỷ lệ gán nhầm là chung `φ`. Liệt kê chính xác theo phân phối nhị thức, kiểm bằng Monte Carlo độc lập (sai lệch tối đa `0.0018`).

**FACT — quy tắc dấu (kiểm số trên lưới, chưa có chứng minh hình thức):** trên `2.205` điểm lưới thuộc 5 topology (`n,s` = 3,1 / 4,2 / 6,2 / 10,3 / 10,7), provenance chọn nhầm tool cùng domain **ít hơn random khi và chỉ khi `r > φ`** (Youden `J = r − φ > 0`), bằng random khi `J = 0`, và **tệ hơn random khi `J < 0`**. Không có vi phạm nào trên lưới.

**Ví dụ topology main (n=3, s=1), leakage 0.10 — unsafe | task escalation:**

| r | φ | J | provenance | random |
|---|---|---|---:|---:|
| 1.00 | 0.00 | 1.00 | 0.100 | 0.400 |
| 0.50 | 0.00 | 0.50 | 0.250 | 0.400 |
| 0.00 | 0.00 | 0.00 | 0.400 | 0.400 |
| 0.25 | 0.50 | −0.25 | 0.512 | 0.400 |
| 0.00 | 0.50 | −0.50 | 0.625 | 0.400 |

**INFERENCE:** mô hình nhiễu độc lập của robustness gate tương ứng `J > 0` với mọi `w < 1`, nên provenance không thể tệ hơn random ở đó. Rủi ro thật nằm ở lỗi nhãn có hệ thống khiến `J ≤ 0`: phụ thuộc ẩn kết hợp gán nhầm "chung" cho nguồn độc lập. Câu hỏi thực nghiệm then chốt chuyển thành: **metadata thực tế có J bao nhiêu?** Đây là cầu nối sang khảo sát prevalence (hướng B).

> [!warning] **Đính chính 2026-10-12.** Câu "mô hình nhiễu độc lập tương ứng `J > 0`" ở trên là suy luận chưa được chứng minh và không được định lý trong [[projects/reliable-tool-using-ai-agents/paper/proof-j-condition]] bao phủ, vì trong mô hình đó nhãn của primary cũng có thể sai. Kết quả "không tệ hơn random" của mô hình đó chỉ đúng trên lưới đã liệt kê.

## Power của tiêu chí robustness — post-hoc, exploratory

**Việc làm:** `src/analyze_robustness_power.py`, output `results_robustness_power_20261006/`. Mô phỏng 300 study tổng hợp cho mỗi cỡ mẫu bằng chính `run_episode` thật (π=2/3, 5 seeds, `wrong_25`, leakage 0.10), áp tiêu chí gate gốc (task-cluster percentile bootstrap, upper 95% CI < 0).

**FACT — kết quả mô phỏng:**

| Số task | Power (upper CI < 0) | Mean effect |
|---:|---:|---:|
| 30 | 0.56 | −0.089 |
| 45 | 0.73 | −0.088 |
| 60 | 0.83 | −0.087 |
| 90 | 0.95 | −0.090 |
| 120 | 0.98 | −0.087 |

Mean effect mô phỏng (`≈ −0.088`) khớp dự đoán giải tích độc lập. Xấp xỉ chuẩn với SD quan sát `0.199` cho power `0.68` ở 30 task (lạc quan hơn vì SD mô phỏng `≈0.23`); nếu hiệu ứng thật bằng mức quan sát `−0.067`, power ở 30 task chỉ `≈0.45` và cần `≈70` task.

**INFERENCE:** nếu mô hình đúng, tiêu chí đã khóa chỉ có khoảng **56% cơ hội** pass ngay cả khi lợi ích tồn tại. Kết quả `FAIL ROBUSTNESS` vì vậy là bằng chứng yếu về việc lợi ích biến mất; nó chủ yếu phản ánh thiếu power. Không được đổi kết quả đã khóa thành PASS. Nếu muốn kết luận, phải chạy **một robustness study mới với ~60 task mới, protocol khóa trước** (chỉ CPU, $0).

**Ảnh hưởng lên claim:** không đổi claim hiện có của paper (RQ, kết quả `FAIL ROBUSTNESS` giữ nguyên là kết quả theo tiêu chí đã khóa). Phân tích này chỉ giúp giải thích và nên được trình bày là post-hoc.

## Liên quan

- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
- [[projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03]]
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]]
