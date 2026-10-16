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
updated: 2026-10-14T13:00:00+07:00
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
- **(Amendment A1, 2026-10-13)** Bộ dữ liệu tĩnh phát qua CDN (jsDelivr, Cloudflare Pages, GitHub raw…): provider là **chủ bộ dữ liệu**; ghi tên CDN trong `notes`. Server metasearch tự host không ghim engine: ghi `SearXNG (self-hosted)` và đánh dấu `AMBIGUOUS`, không ghi `ambiguous` thay cho tên.

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
| 2026-10-13 | Sàng lọc xong (AI-assisted; clone nông, chỉ đọc tĩnh) | `data/tool_survey_2/screening.csv`, SHA-256 `9fbd13db441e2eb1d1a019d12b213777ab9fcbb1a7eb037e232bcbc94eb8d9c6`: 139 repo xét theo thứ tự hạng (script kiểm tra thứ tự), **78 include**, 61 exclude có lý do. Theo nhóm: weather 8, currency 8, stock 8, crypto 8, web_search 8, news 8, translation 8, movies 8, air_quality 6, books 4, geocoding 3, ip_geolocation 1. Theo §4, geocoding và ip_geolocation (dưới 4) chỉ báo cáo riêng; ước lượng gộp dùng 74 server. Tập người gán nhãn: 20 server có `sha256(server_id)` nhỏ nhất trong 78 include, ghi vào `human_coder_template.csv` **trước khi** coder A gán nhãn; hướng dẫn `HUMAN_CODER_GUIDE.md`. **Ghi chú tái lập:** công cụ quét tĩnh dùng ở survey 1 nằm trong thư mục tạm và đã mất; survey 2 dùng bản viết lại đã commit tại `src/survey_tools/` (cùng chức năng, mở rộng nhận diện MCP cho Kotlin/Spring/JSON-RPC). Đây là lỗ hổng tái lập của survey 1: quyết định sàng lọc và gán nhãn của survey 1 vẫn có bằng chứng file:dòng, nhưng công cụ hỗ trợ không còn nguyên bản. |
| 2026-10-13 | **Amendment A1 — làm rõ codebook trước khi gán nhãn survey 2** | Agreement của survey 1 cho thấy hai luật chưa rõ (bộ dữ liệu phát qua CDN; SearXNG tự host). Thêm hai luật vào §5 và vào hướng dẫn người gán nhãn **trước khi** coder A hay người gán nhãn bắt đầu survey 2. Bảng chuẩn hóa tên cho agreement của survey 2 sẽ dùng lại bảng trong `src/analyze_coder_agreement.py`, cố định trước khi so sánh. |
| 2026-10-13 | Coder A gán nhãn xong 78 server + 1 server chỉ dùng cho agreement (AI-assisted; clone tại commit ghim, chỉ đọc tĩnh) | Lưu theo nhóm tại `data/tool_survey_2/coding_partial/` (commit `609ba82`…`ad1f89d`). Coder A không mở nhãn của người gán nhãn. Chưa tính chỉ số nào. |
| 2026-10-14 | **Sửa lỗi sàng lọc phát hiện khi gán nhãn (theo §4), tác giả duyệt** | 4 server include không đạt tiêu chí khi đọc đường đi mặc định của code: `currency_exchange/raktim-shrestha/exchangeRate-mcp` (tiêu chí 5) → `vivart/exchange-rate-mcp` (hạng 17); `crypto_prices/Aditya-AP02/crypto-mcp-server` (tiêu chí 4) → hạng 30 `pras529` bị loại (không có mã nguồn) → `akshaygp18/crypto-mcp-server` (hạng 31); `translation/guvno/transdex-mcp` (tiêu chí 5) → `iamnotagentleman/localizable-xcstrings-mcp` (hạng 17); `translation/xdfzx711/translation-mcp-server` (tiêu chí 5) → `waxberry-dev/live-translate-mcp` (hạng 18). Lý do kèm file:dòng trong `coding_partial/screening_corrections.json`. Áp bằng `src/build_tool_survey2_coding.py`: `screening.csv` từ SHA-256 `9fbd13db…` thành `23b65f5ab73ff4503a43e1da5f965f03ffc9ed0446a358885084f9c3c8c59aa0` (144 dòng; vẫn 78 include, số theo nhóm không đổi). **Tập người gán nhãn giữ nguyên 20 server đã khóa**: `xdfzx711` nằm trong tập này, nên coder A vẫn gán nhãn để tính agreement trên đủ 20, nhưng server này bị loại khỏi mọi ước lượng (`coding_agreement_only.csv`). |
| 2026-10-14 | Ghép nhãn coder A | `data/tool_survey_2/coding.csv` (78 server), SHA-256 `1e1f386d89abe87eef36bf4e384ae4e67041115778c6d2a816cd607e48bb24fb`; `coding_agreement_only.csv` (1 server), SHA-256 `729575b062d00446598d1dca2e238cfa641bbca44d3c473a4afaf9f4f74b47cb`. |
| 2026-10-14 | **Amendment A2 — luật diễn giải khi gán nhãn và chi tiết cài đặt phân tích, tác giả duyệt; ghi trước khi tính bất kỳ chỉ số nào** | **(1) Năm luật diễn giải coder A dùng khi gán nhãn** (đã ghi trong cột `notes` từng server): (a) server tổng hợp tin: một nguồn là "mặc định" nếu tool gọi nó với tham số mặc định khi người dùng cung cấp đủ khóa API, không cần đổi thiết lập chọn nguồn; (b) server có nhiều tool cùng loại thông tin: lấy hợp các nguồn mặc định của mọi tool đó; (c) URL provider đổi được qua biến môi trường → `configurable_upstream = True`; (d) tên server chỉ nêu chủ đề hay địa danh (`aws-news`, `youtube-translate`, `yerevan-aqi`) không tính là nêu tên provider; (e) instance SearXNG công khai của bên thứ ba và Ollama chạy cục bộ được đánh dấu `AMBIGUOUS`, tương tự SearXNG tự host trong A1. **(2) Cài đặt phân tích** (`src/analyze_tool_survey2.py`, chỉ bọc các hàm của `analyze_tool_survey.py`, không đổi logic của chúng): tập ước lượng = `coding.csv` trừ nhóm dưới 4 server (geocoding, ip_geolocation báo cáo riêng); seed bootstrap 20261014. Mức nguồn gốc (bằng chứng (a)): nguồn gốc thật của server là cột `origin_a` nếu có, nếu không thì provider mức vận hành ánh xạ qua bảng chung chỉ gồm sự kiện ở mức provider có trong repo (Frankfurter → ECB; Algolia HN Search → Hacker News). Biến thể "đọc tên theo chữ" so sánh nhãn khai báo nguyên văn; biến thể "biết ánh xạ" ánh xạ nhãn khai báo theo cùng bảng, và tên khai báo trùng provider vận hành của chính server được thay bằng `origin_a` của server đó. **P4 dùng biến thể "đọc tên theo chữ"**, L2, gộp; nếu một trong hai r không xác định thì P4 "không đánh giá được". P5 xét các nhóm trong tập ước lượng. **(3) Sai lệch so với §5/§7:** phân tích phụ (a)+(b) **không thực hiện** vì coder A không thu thập bằng chứng từ tài liệu chính thức của provider; ghi là giới hạn. Script đã chạy thử trên dữ liệu giả (tính tay khớp) trước khi chạy trên `coding.csv`. |
| 2026-10-14 | Hướng dẫn người gán nhãn được bổ sung 5 luật của A2 **trước khi gửi** | Người gán nhãn chưa nhận file và chưa gán nhãn server nào. Họ nhận luật codebook (không nhận nhãn hay kết quả của coder A). Hệ quả: agreement đo độ nhất quán khi áp **cùng** codebook; luật A2 do coder A đặt sau khi đọc code nên agreement có thể cao hơn so với khi người gán nhãn tự diễn giải. Ghi là giới hạn. |
| 2026-10-14 | Tác giả gửi file cho người gán nhãn | Bản hướng dẫn có 5 luật A2 (commit `ec09a23`) và `human_coder_template.csv` 20 server. Coder A đã gán nhãn xong trước đó và không xem nhãn của người gán nhãn. |
| 2026-10-14 | **Nhận nhãn coder 2 — sai lệch so với §6** | `data/tool_survey_2/coder_2_labels.csv` (SHA-256 `5d98afb2…`, 20/20 server). Cột `coder` ghi **"Codex (AI)"** ở cả 20 dòng: người được giao đã dùng một hệ AI khác để gán nhãn, không phải coder con người như §6 quy định. Agreement tính theo đúng quy trình đã định (bảng chuẩn hóa của survey 1, cố định trước), lưu tại `results_tool_survey2_agreement_20261014/`, nhưng phải gọi là **agreement giữa hai AI độc lập (Claude và Codex)**, không phải human validation. `analyze_coder_agreement.py` chỉ đổi cách đọc file sang `utf-8-sig` (file nộp có BOM); logic không đổi. |
| 2026-10-14 | Tác giả xác nhận coder thứ hai của **cả survey 1 và survey 2** dùng AI (Claude hoặc Codex) | Không survey nào có human validation. Đính chính ở paper v1.6, ledger, journal và briefing. |
| 2026-10-15 | **Amendment A3 — tác giả phân xử bất đồng (author adjudication), ghi trước khi tác giả xem các trường hợp** | Vì không có coder con người, tác giả (con người duy nhất) phân xử bất đồng giữa coder A (Claude) và coder 2 (Codex) trong 20 server, **không dùng AI**. File `data/tool_survey_2/adjudication/author_adjudication.xlsx`: (1) 4 câu hỏi luật codebook (nguồn dữ liệu đứng sau API trung gian; provider không mặc định nêu trong README; hai thương hiệu cùng công ty mẹ ở upstream và ở L1); (2) 4 trường hợp sự thật, câu trả lời của hai coder được **che tên** thành X/Y, thứ tự ngẫu nhiên (seed 20261015, khóa ở `adjudication_key.json`); (3) duyệt gộp tên ở mức tổ chức, chỉ dùng cho agreement; (4) kiểm tra ngẫu nhiên 10 bằng chứng `file:dòng` của coder A (seed 20261015). **Cách dùng kết quả:** P1–P6 giữ nguyên (phân tích chính đã khóa). Quyết định của tác giả được áp vào nhãn coder A cho **toàn bộ 78 server** theo luật đã chọn, rồi chạy lại `analyze_tool_survey2.py` vào thư mục mới như **sensitivity analysis**; agreement tính lại với bảng gộp tên đã duyệt, ghi là post-hoc. Ghi trong paper là "author adjudication", không phải coder độc lập. |
| 2026-10-16 | Tác giả quyết định 4 luật ở sheet 1 (trong chat; Claude chép vào workbook, không đổi nội dung) | R1 = Tính (nguyên tắc của tác giả: "nguồn là nguồn dữ liệu cuối cùng"); R2 = Không tính (nguồn không bật thì không phải nguồn); R3 = Hai provider (WSJ, MarketWatch khác mục tiêu nội dung và mô hình dịch vụ); R4 = Tính, giữ tên thương hiệu (lựa chọn được thêm vào danh sách để nhất quán với R3). **Minh bạch:** trước khi quyết định R1, tác giả đã được cho biết lập trường của từng AI coder ở tình huống này; Claude giải thích câu hỏi và áp nguyên tắc tác giả nêu, không chọn thay. Các trường hợp ở sheet 2 vẫn được che tên X/Y. |

## Liên quan

- [[synthesis/Protocol: Real-Tool Failure-Domain Metadata Survey]]
- [[journal/2026-10-09-real-tool-metadata-survey-results]]
- [[projects/reliable-tool-using-ai-agents/paper/proof-j-condition]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
