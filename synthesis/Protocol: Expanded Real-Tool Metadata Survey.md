---
title: >-
  Protocol: Expanded Real-Tool Metadata Survey
category: synthesis
tags: [research-protocol, provenance, external-validity, tool-use, evidence]
sources:
  - "synthesis/Protocol: Real-Tool Failure-Domain Metadata Survey.md"
  - "journal/2026-10-09-real-tool-metadata-survey-results.md"
  - "projects/reliable-tool-using-ai-agents/paper/proof-j-condition.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_tool_survey.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_tool_survey_origin.py"
created: 2026-10-12T20:00:00+07:00
updated: 2026-10-13T09:00:00+07:00
summary: >-
  Protocol cho survey 2: khoảng 96 MCP server mới thuộc 12 nhóm, đăng ký trước dự đoán rút từ survey 1, phân tích mức nguồn gốc và kiểm tra của con người trên ít nhất 20 server.
provenance:
  extracted: 0.25
  inferred: 0.70
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-10-12
tier: core
protocol_version: "1.0"
protocol_status: confirmed-by-author
---

# Protocol: Survey mở rộng về metadata của tool thật (survey 2)

> [!important] **PROSPECTIVE — viết trước khi tạo sampling frame hay đọc code của bất kỳ repo mới nào.** Survey 2 là mẫu **mới, độc lập** với survey 1. Kết quả survey 1 ([[journal/2026-10-09-real-tool-metadata-survey-results]]) được dùng để viết **dự đoán** cho survey 2. Đây là protocol nội bộ, không phải preregistration trên registry độc lập. Mọi thay đổi sau khi khóa phải ghi thành amendment có ngày.

## 1. Mục tiêu

Survey 1 (42 server, 7 nhóm) có ba điểm yếu: mẫu nhỏ; phân tích mức nguồn gốc dữ liệu là post-hoc; nhãn do AI gán và chưa có kiểm tra của con người. Survey 2:

1. **Kiểm định** các phát hiện chính của survey 1 trên một mẫu mới lớn hơn, với dự đoán ghi trước.
2. **Đăng ký trước** phân tích mức nguồn gốc dữ liệu.
3. Đo độ đồng thuận giữa người và AI trên ít nhất 20 server.
4. Mở rộng sang 5 nhóm thông tin mới để kiểm tra phát hiện có giữ được ngoài 7 nhóm cũ không.

### Câu hỏi nghiên cứu

Giữ nguyên **RQ3** của paper:

**RQ3. Among open-source MCP servers that provide the same information type, how often do two servers share an upstream data provider, and how well does agent-visible metadata reveal that sharing?**

Survey 2 là bước kiểm định có dự đoán trước cho RQ3.

## 2. Dự đoán ghi trước (rút từ survey 1)

Mỗi dự đoán có câu tiếng Anh chuẩn và quy tắc đánh giá cụ thể.

- **P1 — Có dùng chung, nhưng không phổ biến.** *The pooled operator-level shared-pair rate ρ lies between 0.05 and 0.30.* Đạt nếu ước lượng điểm của ρ gộp nằm trong `[0.05, 0.30]`.
- **P2 — Metadata agent thấy thường thiếu.** *For agent-visible metadata (L1), more than half of within-type pairs have a missing sharing label.* Đạt nếu `m_L1 > 0.50`.
- **P3 — Khi có nhãn thì hiếm khi sai (mức bên vận hành).** *Among L1-labelled pairs, the operator-level false-sharing rate φ is at most 0.05.* Đạt nếu `φ_L1 ≤ 0.05`.
- **P4 — Tên bên vận hành bỏ sót phụ thuộc ở mức nguồn gốc.** *Origin-level recall of L2 names is lower than operator-level recall.* Đạt nếu `r_origin,L2 < r_operator,L2`.
- **P5 — Có nhóm không có nguồn độc lập.** *At least one information type has an origin-level shared-pair rate of at least 0.80.* Đạt nếu ít nhất một nhóm có `ρ_origin ≥ 0.80`.
- **P6 — Metadata thật có `J > 0` ở mức bên vận hành.** *Operator-level J (L2, labelled pairs) is positive.* Đạt nếu `J_operator,L2 > 0`.

Không gộp dữ liệu survey 1 vào phân tích chính. Báo cáo đầy đủ mọi dự đoán, kể cả dự đoán không đạt.

## 3. Sampling frame — khóa trước khi đọc code

**12 nhóm thông tin.**
- 7 nhóm cũ: weather, currency_exchange, stock_quotes, crypto_prices, geocoding, web_search, news.
- 5 nhóm mới: translation, ip_geolocation, movies, books, air_quality.

**Truy vấn chính và truy vấn dự phòng (định trước cho mọi nhóm).** Truy vấn chính là `"<từ khóa> mcp server"`, sắp theo số sao giảm dần, lấy 50 kết quả đầu. Nếu truy vấn chính trả **dưới 30** kết quả, chạy **đúng một** truy vấn dự phòng dưới đây và nối kết quả vào sau danh sách, bỏ trùng.

| Nhóm | Từ khóa chính | Truy vấn dự phòng |
|---|---|---|
| weather | `weather` | `weather mcp` |
| currency_exchange | `currency exchange` | `exchange rate mcp` |
| stock_quotes | `stock` | `stock price mcp` |
| crypto_prices | `crypto` | `crypto price mcp` |
| geocoding | `geocoding` | `geocode mcp` |
| web_search | `web search` | `search engine mcp` |
| news | `news` | `news api mcp` |
| translation | `translation` | `translate mcp` |
| ip_geolocation | `ip geolocation` | `ip lookup mcp` |
| movies | `movie` | `tmdb mcp` |
| books | `books` | `book search mcp` |
| air_quality | `air quality` | `aqi mcp` |

**Loại khỏi survey 2:** mọi repo đã xét trong survey 1 (54 repo trong `data/tool_survey/screening.csv`), để hai mẫu độc lập.

**Lưu trữ:** `data/tool_survey_2/sampling_frame.json` kèm SHA-256 ghi vào §9 trước khi đọc code.

## 4. Sàng lọc

Xét theo thứ tự hạng, lấy **8 server đầu tiên đạt tiêu chí** mỗi nhóm; mục tiêu 96 server. Tiêu chí giữ nguyên survey 1, và hai cách diễn giải đã dùng ở survey 1 nay được ghi thẳng vào tiêu chí:

1. Repo công khai, mã nguồn đọc được, ghim commit SHA.
2. **Triển khai Model Context Protocol thật** (MCP SDK hoặc JSON-RPC `tools/list`/`tools/call`). Service REST đặt tên "MCP" bị loại.
3. Có **ít nhất một tool** trả về loại thông tin của nhóm. Chỉ có resource hoặc prompt thì không tính.
4. Tool gọi API bên ngoài.
5. **Có upstream mặc định**, kể cả `localhost`. Provider phụ thuộc hoàn toàn vào biến môi trường không có giá trị mặc định thì bị loại.

Loại fork hoặc bản sao gần như y hệt; ghi lý do cho mọi repo bị loại. Nhóm có dưới 4 server đạt tiêu chí trong toàn bộ danh sách vẫn được báo cáo nhưng loại khỏi ước lượng gộp. Nếu một lỗi sàng lọc được phát hiện khi gán nhãn, sửa theo thứ tự hạng và ghi vào §9.

## 5. Codebook (định trước, gồm các làm rõ từ survey 1)

**Mức bên vận hành (operator level, phân tích chính).**
- Provider là tổ chức vận hành hostname API mà tool thuộc nhóm gọi theo cấu hình mặc định; gọi qua SDK thì tính theo dịch vụ mà SDK gọi.
- Chuỗi dự phòng (fallback) hoặc aggregator: mọi nguồn mặc định đều tính.
- Hai server "chung" nếu tập provider mặc định giao nhau.
- SearXNG hoặc metasearch tự host: gắn nhãn `SearXNG (self-hosted)` và đánh dấu `AMBIGUOUS`.

**Metadata khai báo.**
- L1: tên server; tên và description của **mọi** tool của server (docstring khi dùng FastMCP); input schema. Không gồm description của resource/prompt hay docstring của module/helper.
- L2: L1 cộng README.
- Chỉ tính provider được nêu **đích danh**. Nếu metadata nêu nguồn gốc dữ liệu thay vì bên vận hành, ghi đúng tên được nêu và chú thích.

**Mức nguồn gốc dữ liệu (origin level, đăng ký trước, trước đây là post-hoc).**
- Ánh xạ provider sang nguồn gốc dữ liệu **chỉ khi có bằng chứng** trong (a) code, cấu hình, README hoặc description của chính repo, hoặc (b) trang tài liệu chính thức của provider nói rõ nguồn dữ liệu (ghi URL).
- Phân tích chính ở mức nguồn gốc dùng **(a)**, để so sánh được với survey 1. Phân tích phụ dùng **(a) + (b)**.
- Hai biến thể như survey 1: "đọc tên theo chữ" (nhãn khai báo so sánh nguyên văn) và "biết ánh xạ" (nhãn khai báo cũng ánh xạ sang nguồn gốc).

## 6. Người gán nhãn

- **Coder A (AI, Claude):** gán toàn bộ mẫu; ghi là AI-assisted.
- **Coder con người:** gán độc lập **ít nhất 20 server**, chọn là các server có `sha256(server_id)` nhỏ nhất trong tập include, sau khi sàng lọc xong và trước khi coder A bắt đầu gán. Không xem nhãn của coder A.
- Báo cáo percent agreement và Cohen's kappa cho tập provider mặc định và cho L1 declared provider, sau khi chuẩn hóa tên theo một bảng ánh xạ viết trước khi so sánh.
- Nếu đến lúc phân tích chưa có nhãn của con người, ghi rõ là giới hạn và không gọi kết quả là human-validated.

## 7. Phân tích

Dùng lại `analyze_tool_survey.py` và `analyze_tool_survey_origin.py` (đổi đường dẫn đầu vào, không đổi logic), output vào thư mục mới:

- ρ, m, r, φ, J theo nhóm và gộp, cho L1 và L2, ở mức bên vận hành và mức nguồn gốc; luôn kèm số đếm thô.
- Bootstrap theo server trong từng nhóm (2.000 lần) cho ρ gộp.
- Độ nhạy: bỏ server có provider đổi được; coi cặp `AMBIGUOUS` là không chung.
- Phép chiếu lên mô hình selector theo [[projects/reliable-tool-using-ai-agents/paper/proof-j-condition]] (công thức đóng, có nhãn thiếu), ghi rõ là phép chiếu.
- Đánh giá P1–P6 theo đúng quy tắc ở §2.
- **Phân tích phụ, ghi trước:** so sánh 7 nhóm cũ giữa survey 1 và survey 2 (mô tả, không kiểm định).

**Độ chính xác dự kiến:** với khoảng 96 server, khoảng tin cậy bootstrap của ρ gộp dự kiến hẹp hơn survey 1 khoảng `sqrt(42/96) ≈ 0.66` lần, tức rộng khoảng 0.14 thay vì 0.21. Đây là ước lượng lập kế hoạch.

## 8. Giới hạn biết trước

- Upstream ở mức bên vận hành là cận dưới cho phụ thuộc thật; mức nguồn gốc chỉ dùng bằng chứng có thể kiểm tra.
- Quy tắc giao tập phóng đại phụ thuộc của aggregator nhiều nguồn.
- Mẫu thiên về repo phổ biến trên GitHub, chỉ trong hệ sinh thái MCP.
- Các cặp không độc lập vì mỗi server nằm trong nhiều cặp.
- Survey không đo hành vi agent.
- Survey 2 được thiết kế sau khi biết kết quả survey 1. Đó chính là mục đích (kiểm định dự đoán), nhưng nhóm mới và tiêu chí vẫn do cùng một nhóm tác giả chọn.

## 9. Nhật ký khóa và amendment

| Ngày | Sự kiện | Ghi chú |
|---|---|---|
| 2026-10-12 | Protocol v1.0 được viết | Chờ tác giả xác nhận; chưa tạo sampling frame, chưa đọc code repo mới nào |
| 2026-10-13 | Tác giả xác nhận protocol v1.0 | Khóa 12 nhóm, truy vấn chính và dự phòng, tiêu chí, codebook, dự đoán P1–P6; chưa tạo sampling frame |
| 2026-10-13 | Sampling frame tạo bằng `src/build_tool_survey2_frame.py`, trước khi đọc code repo mới | `data/tool_survey_2/sampling_frame.json`, SHA-256 `c1f87bbcded5391f79cb0bcd14051eb76168518d46ae3ed6fbafd2d5c0073146`. Số kết quả (trong ngoặc: số repo đã có ở survey 1, bị loại): weather 50 (6), currency_exchange 25 (6), stock_quotes 50 (7), crypto_prices 50 (14), geocoding 9 (6), web_search 50 (7), news 50 (8), translation 49 (0), ip_geolocation 1 (0), movies 43 (0), books 23 (0), air_quality 7 (0). Truy vấn dự phòng chạy cho currency_exchange, geocoding, translation, ip_geolocation, movies, books, air_quality theo §3. Theo §4: ip_geolocation (1 ứng viên) và geocoding (3 ứng viên mới) chắc chắn dưới 4 nên chỉ báo cáo riêng; air_quality tối đa 7. Không amendment. |

## Liên quan

- [[synthesis/Protocol: Real-Tool Failure-Domain Metadata Survey]]
- [[journal/2026-10-09-real-tool-metadata-survey-results]]
- [[projects/reliable-tool-using-ai-agents/paper/proof-j-condition]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
