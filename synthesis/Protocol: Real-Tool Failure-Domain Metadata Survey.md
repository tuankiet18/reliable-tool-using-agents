---
title: >-
  Protocol: Real-Tool Failure-Domain Metadata Survey
category: synthesis
tags: [research-protocol, provenance, external-validity, tool-use, evidence]
sources:
  - "journal/2026-10-06-prior-art-refresh-vp-control-and-efd.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_hidden_dependency.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_hidden_dependency_20261006/summary.json"
  - "https://arxiv.org/abs/2609.10969"
  - "https://arxiv.org/abs/2507.16044"
  - "https://arxiv.org/abs/2509.25292"
created: 2026-10-06T15:00:00+07:00
updated: 2026-10-09T11:00:00+07:00
summary: >-
  Protocol khảo sát ~42 MCP server mã nguồn mở để ước lượng tỷ lệ cặp tool dùng chung upstream (ρ) và chất lượng metadata agent nhìn thấy (r, φ, m, J = r − φ).
provenance:
  extracted: 0.30
  inferred: 0.65
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-10-06
tier: core
protocol_version: "1.0"
protocol_status: confirmed-by-author
---

# Protocol: Khảo sát failure-domain metadata trên tool thật

> [!important] **PROSPECTIVE EXPLORATORY — viết trước khi thu thập dữ liệu.** Tiêu chí dưới đây được ghi trước khi tạo sampling frame hoặc gán nhãn bất kỳ server nào. Đây là protocol nội bộ, **không phải preregistration độc lập**: tác giả đã biết kết quả giải tích về `J` trước khi viết. Mọi thay đổi sau khi bắt đầu thu thập phải ghi thành amendment có ngày, không sửa ngược nội dung này.

## 1. Mục tiêu

Phân tích [[journal/2026-10-06-prior-art-refresh-vp-control-and-efd]] cho thấy: chọn nguồn theo provenance tốt hơn chọn ngẫu nhiên **khi và chỉ khi** metadata phát hiện phụ thuộc chung tốt hơn mức gán nhầm (chỉ số Youden `J = r − φ > 0`). VP-Control ([2609.10969](https://arxiv.org/abs/2609.10969)) và EFD ([2609.02925](https://arxiv.org/abs/2609.02925)) đều giả định nhãn lineage có sẵn và đúng. Survey này đo **trên tool thật** hai đại lượng mà các nghiên cứu đó chưa đo:

1. **Prevalence (ρ):** trong các tool cung cấp cùng một loại thông tin, tỷ lệ cặp thật sự dùng chung nguồn dữ liệu upstream.
2. **Chất lượng metadata:** thông tin agent nhìn thấy (tên, description) phát hiện việc dùng chung đó tốt đến đâu: recall `r`, false-sharing `φ`, tỷ lệ thiếu nhãn `m`, và `J`.

### Câu hỏi nghiên cứu

**RQ-S (English canonical).** *Among open-source MCP servers that provide the same information type, how often do two servers share an upstream data provider, and how well does agent-visible metadata reveal that sharing?*

**Giải thích:** Trong các MCP server cùng cung cấp một loại thông tin (ví dụ thời tiết), bao nhiêu cặp thật sự lấy dữ liệu từ cùng một nhà cung cấp? Và nếu agent chỉ đọc tên tool và description, nó có nhận ra điều đó không?

### Kỳ vọng ghi trước (EXPLORATORY, không phải hypothesis xác nhận)

- **E1.** *In at least two information types, more than 20% of within-type server pairs share an upstream provider.* Ít nhất hai nhóm có trên 20% cặp server dùng chung upstream, do nhiều server bọc cùng một API miễn phí.
- **E2.** *For runtime-visible metadata, more than half of within-type pairs have a missing (undeterminable) sharing label.* Với metadata agent thấy lúc chạy, hơn một nửa số cặp không xác định được có dùng chung hay không.
- **E3.** *Among pairs with a determinable label, J = r − φ is positive.* Trong các cặp xác định được nhãn, `J` dương.

Không có ngưỡng pass/fail. Kết quả trái kỳ vọng phải được báo cáo đầy đủ.

## 2. Định nghĩa

| Thuật ngữ | Định nghĩa vận hành |
|---|---|
| Server | Một MCP server mã nguồn mở, ghim theo commit SHA tại thời điểm gán nhãn. |
| Information type | Một trong 7 nhóm ở §3. Chỉ ghép cặp các server **cùng nhóm**. |
| Upstream provider (ground truth) | Tổ chức sở hữu hostname API mà code của tool thuộc nhóm đó gọi theo **cấu hình mặc định**, ví dụ `api.open-meteo.com` → Open-Meteo. Nhiều hostname của một tổ chức gộp làm một. |
| Truly shared pair | Hai server có tập upstream provider mặc định giao nhau. |
| L1 metadata (chính) | Thông tin agent thấy lúc chạy: server name, tool name, tool description, input schema. |
| L2 metadata (phụ) | L1 cộng README của repo. Agent thường không thấy README; dùng để phân tích độ nhạy. |
| Declared provider | Provider được nêu đích danh trong metadata ở mức L1 hoặc L2. Không nêu thì là `unknown`. |
| Declared pair label | Cả hai server có declared provider: trùng thì `shared`, khác thì `independent`. Một bên `unknown` thì `missing`. |

**Mapping sang mô hình selector:** nhãn `missing` tương ứng với tỷ lệ thiếu `m` (selector fallback ngẫu nhiên); `r = P(declared shared | truly shared)`, `φ = P(declared shared | truly independent)`, cả hai chỉ tính trên các cặp không `missing`.

## 3. Sampling frame — khóa trước khi gán nhãn

**Nhóm thông tin (7):** thời tiết (weather), tỷ giá (currency exchange), giá cổ phiếu (stock quotes), giá crypto (cryptocurrency prices), geocoding, web search, tin tức (news).

**Nguồn và thứ tự chọn:** với mỗi nhóm, chạy truy vấn GitHub search cố định `"<từ khóa nhóm> mcp server"` (repositories, sắp theo số sao giảm dần). Lưu nguyên danh sách 30 kết quả đầu, ngày truy vấn và truy vấn chính xác vào sampling frame **trước** khi đọc code bất kỳ repo nào. Duyệt theo đúng thứ tự đó và lấy **6 server đầu tiên đạt tiêu chí**. Mục tiêu khoảng 42 server.

**Tiêu chí chọn:**
- repo công khai, mã nguồn đọc được;
- có ít nhất một tool trả về loại thông tin của nhóm;
- tool gọi một API bên ngoài (không chỉ trả dữ liệu giả hoặc dữ liệu tĩnh).

**Tiêu chí loại (ghi lý do cho từng repo bị loại):** fork hoặc bản sao gần như y hệt của repo đã chọn; placeholder không có implementation; không xác định được upstream từ code; repo không phải MCP server.

**Nhóm thiếu mẫu:** nhóm có dưới 4 server đạt tiêu chí trong 30 kết quả đầu vẫn được báo cáo nhưng loại khỏi ước lượng gộp.

**Lưu trữ:** `data/tool_survey/sampling_frame.json` kèm SHA-256 ghi vào note này (§8) trước khi bắt đầu gán nhãn.

## 4. Quy trình gán nhãn

Mỗi server được ghi một dòng trong `data/tool_survey/coding.csv`:

| Cột | Nội dung |
|---|---|
| `server_id`, `category`, `repo_url`, `commit_sha` | Định danh, ghim commit |
| `upstream_providers` | Tập provider mặc định, tách bằng `;` |
| `upstream_evidence` | Đường dẫn file và số dòng chứa hostname |
| `configurable_upstream` | `true` nếu người dùng có thể đổi provider |
| `l1_declared_provider`, `l1_evidence` | Provider nêu trong L1 hoặc `unknown`, kèm trích dẫn ngắn |
| `l2_declared_provider`, `l2_evidence` | Tương tự cho L2 |
| `coder`, `notes` | Người gán nhãn và ghi chú |

**Luật gán nhãn:**
1. Ground truth chỉ dựa trên code, không dựa trên README.
2. Declared provider phải là **tên provider xuất hiện đích danh** trong văn bản metadata. Không suy luận từ ngữ cảnh (ví dụ không suy "weather" là OpenWeather).
3. Server có nhiều provider mặc định thì tính là shared với server khác nếu giao nhau ít nhất một provider.
4. Trường hợp mơ hồ ghi `ambiguous` trong `notes` và được báo cáo riêng; không tự giải quyết.

**Người gán nhãn:**
- **Coder A (AI-assisted, Claude):** gán nhãn toàn bộ mẫu. Mọi kết quả phải ghi rõ là AI-assisted.
- **Coder B (con người, thành viên nhóm, tùy chọn nhưng được khuyến nghị):** gán nhãn **độc lập** một tập con 10 server được chọn bằng hash cố định (`sha256(server_id)` nhỏ nhất), không xem nhãn của coder A. Báo cáo percent agreement và Cohen's kappa cho `upstream_providers` (khớp tập) và `l1_declared_provider`.
- Nếu không có coder B trước khi phân tích, ghi rõ là **giới hạn**; không gọi kết quả là human-validated.

## 5. Phân tích

- Ghép mọi cặp server trong cùng nhóm.
- Với mỗi nhóm và gộp: `ρ` (tỷ lệ cặp truly shared), `m` (tỷ lệ cặp `missing`), `r`, `φ`, `J`, kèm **số đếm thô** (tử số và mẫu số).
- Báo L1 là kết quả chính, L2 là độ nhạy.
- **Độ nhạy:** (a) định nghĩa shared theo "bất kỳ provider nào code có thể gọi" thay vì chỉ mặc định; (b) loại các server `configurable_upstream = true`.
- **Uncertainty:** các cặp không độc lập vì một server xuất hiện trong nhiều cặp. Dùng bootstrap theo server trong từng nhóm (resample server, ghép lại cặp) cho khoảng tin cậy của `ρ`. Với `r`, `φ`, `J` có thể chỉ báo số đếm nếu mẫu số quá nhỏ (dưới 10 cặp).
- **Nối với kết quả giải tích:** đặt các điểm `(r, φ)` quan sát được lên phase diagram của `analyze_hidden_dependency.py` và ghi rõ đây là phép chiếu, không phải đo hiệu quả của agent.

Script phân tích dự kiến: `src/analyze_tool_survey.py`, output vào thư mục mới `results_tool_survey_<ngày>/`.

## 6. Giới hạn biết trước

- **Upstream là xấp xỉ thô của failure domain.** Hai provider khác nhau có thể cùng mua dữ liệu từ một nguồn gốc (ví dụ cùng dữ liệu khí tượng quốc gia); dạng phụ thuộc ẩn này không thấy được trong code, nên `ρ` là **cận dưới**.
- **Mẫu thiên về repo phổ biến** trên GitHub, không đại diện cho mọi MCP server hoặc tool nội bộ doanh nghiệp.
- **MCP chỉ là một hệ sinh thái tool.** Không tổng quát hóa sang function calling nói chung khi chưa có bằng chứng.
- **Metadata thay đổi theo thời gian.** Ghim commit SHA để tái lập được.
- **Mẫu nhỏ** (khoảng 42 server). Kết quả là mô tả, không phải ước lượng quần thể.
- Nghiên cứu này **không đo hành vi agent**; nó chỉ đo cấu trúc phụ thuộc và metadata.

## 7. Đạo đức và bản quyền

Chỉ đọc repo công khai. Lưu URL, commit SHA, đường dẫn file và trích dẫn ngắn làm bằng chứng; không sao chép mã nguồn vào vault. Không gọi API của các server và không cần API key.

## 8. Nhật ký khóa và amendment

| Ngày | Sự kiện | Ghi chú |
|---|---|---|
| 2026-10-06 | Protocol v1.0 được viết | Chờ tác giả xác nhận trước khi tạo sampling frame |
| 2026-10-09 | Tác giả xác nhận protocol v1.0; có coder B | Hướng dẫn coder B: `data/tool_survey/CODER_B_GUIDE.md`. Sampling frame chưa tạo; SHA-256 sẽ ghi tại đây trước khi gán nhãn. |
| 2026-10-09 | Sampling frame tạo bằng `src/build_tool_survey_frame.py`, trước khi đọc code | `data/tool_survey/sampling_frame.json`, SHA-256 `287d5f468f31a49c5a054184f82f31a95ff1bd75ea58c6799b758502e46c5177`. Số kết quả: weather 30, currency_exchange **3**, stock_quotes 30, crypto_prices 30, geocoding **5**, web_search 30, news 30. Theo §3, nhóm dưới 4 server đạt tiêu chí bị loại khỏi ước lượng gộp. Chưa đọc code repo nào. |

## Liên quan

- [[journal/2026-10-06-prior-art-refresh-vp-control-and-efd]]
- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]]
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
