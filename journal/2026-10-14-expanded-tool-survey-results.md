---
title: "2026-10-14 — Kết quả survey 2: 78 MCP server, 12 nhóm, dự đoán P1–P6"
category: journal
tags: [research-log, provenance, external-validity, tool-use, evidence]
sources:
  - "synthesis/Protocol: Expanded Real-Tool Metadata Survey.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tool_survey_2/coding.csv"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_tool_survey2_20261014/summary.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_tool_survey2.py"
created: 2026-10-14T11:00:00+07:00
updated: 2026-10-14T11:00:00+07:00
summary: >-
  Survey 2 (74 server trong ước lượng, 245 cặp): ρ 0.27 [0.18, 0.37]; L1 thiếu nhãn 71%; khi có nhãn J_L2 = 0.89. Đạt P1, P2, P4, P6; không đạt P3 (φ_L1 = 3/45) và P5 (web_search ρ_origin 0.71). Phát hiện "thiếu nhãn" của survey 1 lặp lại gần như y hệt.
provenance:
  extracted: 0.70
  inferred: 0.30
base_confidence: 0.6
lifecycle: draft
lifecycle_changed: 2026-10-14
---

# Kết quả survey 2 — 2026-10-14

**Phạm vi:** khảo sát mô tả (descriptive survey) theo [[synthesis/Protocol: Expanded Real-Tool Metadata Survey]] v1.0 + Amendment A1, A2. 78 MCP server, 12 nhóm thông tin; **ước lượng gộp dùng 74 server, 10 nhóm, 245 cặp**, vì geocoding (3) và ip_geolocation (1) chỉ được báo cáo riêng. Coder A là **AI-assisted**. **Chưa có nhãn của người gán nhãn**, nên kết quả **chưa được con người kiểm chứng (not human-validated)**. Không gọi API, không chạy server, không đo hành vi agent.

`coding.csv` SHA-256 `1e1f386d…`. Kết quả nằm ở `results_tool_survey2_20261014/`. Amendment A2 (luật diễn giải và cách cài đặt phân tích) được commit ở `fb41192`, **trước khi** tính bất kỳ chỉ số nào.

## FACT — mức bên vận hành (operator level)

| Nhóm | Cặp | Chung | ρ | m L1 | m L2 |
|---|---:|---:|---:|---:|---:|
| currency_exchange | 28 | 18 | 0.64 | 0.64 | 0.25 |
| web_search | 28 | 11 | 0.39 | 0.46 | 0.00 |
| weather | 28 | 10 | 0.36 | 1.00 | 0.25 |
| movies | 28 | 9 | 0.32 | 0.64 | 0.46 |
| stock_quotes | 28 | 7 | 0.25 | 1.00 | 0.64 |
| crypto_prices | 28 | 6 | 0.21 | 0.64 | 0.00 |
| books | 6 | 1 | 0.17 | 0.50 | 0.50 |
| news | 28 | 3 | 0.11 | 0.46 | 0.25 |
| air_quality | 15 | 1 | 0.07 | 0.60 | 0.00 |
| translation | 28 | 1 | 0.04 | 0.89 | 0.00 |
| **Gộp** | **245** | **67** | **0.27** | **0.71** | **0.22** |

- **ρ gộp** = 67/245 = 0.27. Khoảng tin cậy 95% bootstrap theo server trong từng nhóm là [0.179, 0.374]. Khoảng này rộng 0.19, chỉ hẹp hơn survey 1 (0.21) một chút, chứ không hẹp tới mức 0.14 như kế hoạch. Lý do là ρ chênh lệch nhiều giữa các nhóm.
- **L1, trên các cặp có nhãn:** r = 23/27 = 0.85; φ = 3/45 = 0.067; J = 0.79.
- **L2 (L1 cộng README):** m = 0.22; r = 52/55 = 0.95; φ = 7/135 = 0.05; J = 0.89.
- **Hai nhóm hoàn toàn không có nhãn ở L1:** weather và stock_quotes đều có m_L1 = 1.00. Tức là không server nào trong hai nhóm này nêu tên provider ở metadata mà agent thấy.
- **Độ nhạy:**
  - Bỏ 16 server đổi được provider (còn 58 server): ρ 0.29; L1 m 0.75, r 0.79, φ 0.11.
  - Coi cặp AMBIGUOUS là không chung: kết quả không đổi.
- **Phép chiếu lên mô hình selector:** đây là phép chiếu, không phải phép đo. Lấy trung bình trên 45 primary có ít nhất một peer chung:
  - L1 với tỷ lệ thiếu nhãn quan sát được (k = 0.53): xác suất chọn nhầm peer chung là 0.289 với provenance, so với 0.436 khi chọn ngẫu nhiên.
  - L2 (k = 0.88): 0.109 so với 0.436.

## FACT — mức nguồn gốc dữ liệu (origin level, đăng ký trước, bằng chứng (a))

| Biến thể | ρ | r L2 | φ L2 | J L2 |
|---|---:|---:|---:|---:|
| Mức bên vận hành | 0.27 | 0.95 (52/55) | 0.05 | 0.89 |
| Nguồn gốc, đọc tên theo chữ | 0.31 | 0.83 (55/66) | 0.03 | 0.80 |
| Nguồn gốc, biết ánh xạ | 0.31 | 0.97 (64/66) | 0.02 | 0.95 |

- web_search tăng từ ρ 0.39 lên ρ_origin 0.71. Biến thể đọc tên theo chữ có r_L2 = 0.55 (11/20). Nguyên nhân là các engine đứng sau ddgs, SearXNG và GroundRoute trùng nhau, nhưng tên khai báo chỉ là tên của lớp bọc ngoài.
- crypto_prices tăng từ 0.21 lên 0.32. Lý do: dữ liệu giá của `bca-mcp` lấy từ CoinGecko.
- movies **giảm** từ 0.32 xuống 0.25. Xem mục "Lỗi cài đặt" bên dưới.

## Đối chiếu dự đoán ghi trước (protocol §2)

| Dự đoán | Quy tắc | Giá trị | Kết quả |
|---|---|---|---|
| P1 Có dùng chung, nhưng không phổ biến | 0.05 ≤ ρ ≤ 0.30 | 0.27 | **Đạt**. Cận trên khoảng tin cậy là 0.37, vượt 0.30. |
| P2 L1 thường thiếu nhãn | m_L1 > 0.50 | 0.71 | **Đạt** |
| P3 Có nhãn thì hiếm khi sai | φ_L1 ≤ 0.05 | 0.067 (3/45) | **Không đạt** |
| P4 Tên bên vận hành bỏ sót phụ thuộc ở mức nguồn gốc | r_origin,L2 < r_operator,L2 | 0.83 < 0.95 | **Đạt** |
| P5 Có nhóm không có nguồn độc lập | ρ_origin ≥ 0.80 ở ít nhất một nhóm | cao nhất là web_search 0.71 | **Không đạt** |
| P6 Metadata thật có J > 0 | J_operator,L2 > 0 | 0.89 | **Đạt** |

**INFERENCE — vì sao P3 không đạt.** Ba cặp "báo chung nhầm" ở L1 đều không phải metadata nêu sai tên. Đó là trường hợp metadata nêu tên một tầng khác với bên vận hành:
- 2 cặp `bca-mcp` với các server CoinGecko: tool description nêu CoinGecko là nguồn dữ liệu, còn bên vận hành là Blockchain Academics. Ở mức nguồn gốc, hai cặp này thực sự là chung, nên nhãn khai báo đúng.
- 1 cặp `hpuhsp` với `groundroute`: cả hai đều nêu tên Brave Search. Với `hpuhsp`, Brave không bật mặc định. Với GroundRoute, Brave là một trong các engine mà nó định tuyến tới.

Vì vậy φ_L1 ở mức nguồn gốc chỉ còn 1/37 = 0.03. Đây là **diễn giải post-hoc**. Kết quả chính thức vẫn là **không đạt**.

**INFERENCE — vì sao P5 không đạt.** Survey 1 có web_search ρ_origin = 1.00 trên 6 server. Survey 2 có 8 server, trong đó 20 trên 28 cặp dùng chung ít nhất một engine; mọi server đều chung với ít nhất một server khác. 8 cặp độc lập đều có `menesekinci` (chỉ gọi Google) hoặc `groundroute` (Serper, Brave, Exa, Tavily, Firecrawl, Perplexity). Phát hiện "có nhóm không có nguồn độc lập" của survey 1 **không lặp lại được** ở ngưỡng đã chọn. Kết luận đúng hơn là: web_search có mức chung **cao** (0.71), nhưng vẫn có nguồn độc lập.

## Lỗi cài đặt phát hiện sau khi chạy (POST-HOC)

Theo luật đã ghi trong A2, mức nguồn gốc lấy cột `origin_a` **thay cho** provider vận hành. Với `movies/Grinv/tmdb-mcp`, `origin_a` liệt kê IMDb, Rotten Tomatoes và Metacritic (các nguồn điểm đánh giá mà OMDb trả về), nên server này mất liên kết OMDb với hai server OMDb còn lại. Hai server kia không có bằng chứng trong repo về nguồn gốc của OMDb, nên vẫn giữ tên OMDb. Hệ quả là mức nguồn gốc làm **mất** 2 cặp chung, trái với ý định "mức nguồn gốc là cận dưới, chỉ có thể tăng".

Độ nhạy post-hoc: lấy nguồn gốc là `origin_a` **hợp** provider vận hành đã ánh xạ (`posthoc_origin_union.txt`). Kết quả: ρ 0.32, r_L2 đọc tên theo chữ 0.84 (56/67), web_search vẫn 0.71. **Kết luận về P4 và P5 không đổi.**

## So sánh với survey 1 (7 nhóm chung, mô tả, không kiểm định)

| | Survey 1 | Survey 2 |
|---|---|---|
| ρ gộp | 0.16 [0.075, 0.281] | 0.27 [0.179, 0.374] |
| m L1 gộp | 0.70 | 0.71 |
| r / φ L2 | 17/17, 0/83 | 52/55, 7/135 |

Theo từng nhóm, ρ của survey 1 → survey 2:

| Nhóm | Survey 1 | Survey 2 |
|---|---:|---:|
| currency | 0.00 | 0.64 |
| weather | 0.07 | 0.36 |
| stock | 0.07 | 0.25 |
| crypto | 0.13 | 0.21 |
| news | 0.20 | 0.11 |
| web_search | 0.47 | 0.39 |

geocoding không so sánh được, vì survey 2 chỉ có 3 server.

**INFERENCE.**
- **Tỷ lệ thiếu nhãn ở L1 ổn định (0.70 → 0.71).** Đây là phát hiện lặp lại vững nhất.
- **ρ theo nhóm biến động mạnh giữa hai mẫu.** Ví dụ, currency đổi từ 0 sang 6 server dùng Frankfurter. Nghĩa là mức dùng chung phụ thuộc nhiều vào việc mẫu rơi vào những repo nào, nên **không nên báo cáo ρ của một nhóm như một hằng số**.

## Inter-coder agreement — cập nhật 2026-10-14

Coder thứ hai nộp đủ 20/20 server (`data/tool_survey_2/coder_2_labels.csv`), nhưng cột `coder` ghi **Codex (AI)**; tác giả xác nhận người này dùng Claude hoặc Codex cho cả survey 1 và survey 2. Đây là agreement giữa hai AI (Claude và Codex), **không phải human validation**.

| Trường | Khớp nguyên chữ | Bảng chuẩn hóa survey 1 (cố định trước) |
|---|---|---|
| Upstream | 0.40 (κ 0.38) | 0.45 (κ 0.43) |
| L1 | 0.65 | 0.65 (κ 0.57) |
| L2 | 0.40 | 0.40 (κ 0.38) |
| Có/thiếu nhãn L1 | | **1.00 (κ 1.00)** |

**INFERENCE.**
- Phần lớn bất đồng về upstream là cùng một tổ chức nhưng khác mức đặt tên: `Google Maps Platform` và `Google`; `Amazon Location Service` và `Amazon Web Services`; `Eastmoney` và `East Money`; `360 Search` và `Qihoo 360`.
- Có/thiếu nhãn L1 khớp tuyệt đối, nên ước lượng m (P2) tái lập được giữa hai AI coder.
- Bất đồng thật ở L1/L2 tập trung vào một luật chưa rõ: tên nguồn dữ liệu phía sau API trung gian có tính là provider khai báo không. Ví dụ `bca-mcp` nêu CoinGecko, `Grinv` nêu IMDb/Rotten Tomatoes/Metacritic, `wudalu` nêu các platform.
  - Coder A tính, theo câu "ghi đúng tên được nêu" của codebook.
  - Codex không tính.
- Trường hợp `bca-mcp` tạo ra 2/3 cặp gán nhầm của P3, nên **P3 phụ thuộc vào cách hiểu codebook**. Không dùng điều này để đổi kết quả P3 (vẫn là không đạt).

## Author adjudication — cập nhật 2026-10-16 (Amendment A3)

Tác giả (con người duy nhất) phân xử bất đồng giữa Claude và Codex: 4 luật codebook, 4 trường hợp che tên X/Y, và kiểm tra 10 bằng chứng `file:dòng` chọn ngẫu nhiên.

- **Luật của tác giả:**
  - R1: tính tên nguồn dữ liệu cuối cùng ("nguồn là nguồn cuối cùng").
  - R2: không tính provider không bật mặc định.
  - R3: WSJ và MarketWatch là hai provider.
  - R4: tên thương hiệu được tính.
- **So với hai coder:** tác giả giống Claude 7/8 lần, giống Codex 1/8 lần (R2).
- **Kiểm tra bằng chứng:** 10/10 đúng.
- **Sensitivity với nhãn đã phân xử:**
  - Luật R2 đổi 7 nhãn ở 5 server.
  - P1, P2, P4, P6 và P5 không đổi.
  - P3 từ 3/45 thành **2/45 = 0.044**, tức là đạt ngưỡng 0.05, nhưng chỉ chênh **một cặp**.
- **Agreement giữa Claude và Codex sau gộp tên ở mức tổ chức** (bảng do AI lập, post-hoc): upstream 0.85, L1 0.80, L2 0.70.

**INFERENCE.**
- P3 nằm sát ngưỡng và phụ thuộc vào định nghĩa codebook, nên không nên kết luận mạnh theo chiều nào. Hai cặp còn lại đều do metadata nêu nguồn dữ liệu cuối (CoinGecko). Theo chính luật R1 của tác giả, nhãn đó "đúng" ở data-origin level.
- Việc tác giả gần như luôn chọn giống Claude có thể do Claude đúng hơn. Nhưng cũng có thể vì Claude là người giải thích câu hỏi và vì tác giả đã biết lập trường của từng coder ở R1. Đây là giới hạn cần nêu.

## Giới hạn

- Không có human validation độc lập: coder thứ hai của cả hai survey dùng AI. Phần con người duy nhất là tác giả phân xử bất đồng và kiểm tra 10 bằng chứng, với dòng code do Claude trích.
- Không thực hiện phân tích phụ (a)+(b), vì không thu thập bằng chứng từ tài liệu provider. Đây là sai lệch so với §5 và đã ghi ở A2.
- Bốn lỗi sàng lọc được sửa theo thứ tự hạng. Một server nằm trong tập của người gán nhãn được giữ lại chỉ để tính agreement.
- Các cặp không độc lập với nhau. Bootstrap theo server đã xử lý một phần vấn đề này.
- Năm luật diễn giải là do coder A tự đặt khi gán nhãn. Chúng được ghi trước khi tính chỉ số, nhưng sau khi đã đọc code.

## Tiếp theo

1. Cập nhật ledger: C36–C38 về survey 1 và các claim mới về survey 2.
2. Cập nhật paper: abstract, §4.8, §5.10, §6.4, §7.7. Tiêu đề nên đổi, vì "42 MCP servers" không còn đúng phạm vi.
3. ~~Tính agreement khi có nhãn của người gán nhãn.~~ Đã tính (AI và AI). Còn mở: tác giả tự phân xử các bất đồng thật (author adjudication) nếu muốn có yếu tố con người.

## Liên quan

- [[synthesis/Protocol: Expanded Real-Tool Metadata Survey]]
- [[journal/2026-10-09-real-tool-metadata-survey-results]]
- [[projects/reliable-tool-using-ai-agents/paper/proof-j-condition]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
