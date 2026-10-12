# Hướng dẫn gán nhãn — Survey 2

Giống hệt hướng dẫn survey 1 bên dưới, với hai điểm khác:

- File cần điền: `human_coder_template.csv` (20 server, chọn bằng hash trước khi AI gán nhãn).
- Có 5 nhóm thông tin mới: `translation` (dịch máy), `ip_geolocation`, `movies`, `books` (thông tin sách), `air_quality`. Với server dịch dùng mô hình ngôn ngữ (LLM), ghi nhà cung cấp mô hình mặc định (ví dụ OpenAI, Ollama chạy cục bộ).
- **Hai luật bổ sung (sau survey 1):** (1) nếu dữ liệu là một bộ dữ liệu tĩnh phát qua CDN (jsDelivr, Cloudflare Pages, GitHub raw), ghi **chủ bộ dữ liệu** làm provider và ghi tên CDN vào `notes`; (2) nếu server gọi một SearXNG tự host, ghi `SearXNG (self-hosted)` và viết `AMBIGUOUS` vào `notes`.

---


**Thời gian dự kiến:** 10–15 phút mỗi server, 20 server, tổng khoảng 4–5 giờ. Có thể chia làm nhiều buổi.
**Cần biết:** đọc được code Python hoặc TypeScript ở mức cơ bản. **Không cần** biết gì về project nghiên cứu.

## Bạn đang giúp đo điều gì?

Nhiều MCP server khác tên nhau có thể cùng lấy dữ liệu từ **một nhà cung cấp API** (ví dụ hai server thời tiết cùng gọi OpenWeatherMap). Nếu nhà cung cấp đó trả dữ liệu sai, cả hai cùng sai. Chúng tôi muốn biết:
1. Mỗi server thật sự gọi nhà cung cấp nào (đọc từ code).
2. Một AI agent, chỉ nhìn tên và mô tả của tool, có biết được nhà cung cấp đó không.

## Quy tắc quan trọng

- **Làm độc lập.** Không mở file `coding.csv` của coder A, không hỏi coder A về server cụ thể cho tới khi bạn nộp xong.
- **Không đoán.** Không chắc thì ghi `ambiguous` và giải thích ngắn trong cột `notes`.
- **Không chạy server, không cần API key.** Chỉ đọc code trên GitHub.
- **Dùng đúng commit** được ghi trong cột `commit_sha` (mở link dạng `https://github.com/<repo>/tree/<commit_sha>`).

## Với mỗi server, trả lời 3 câu

Điền vào `human_coder_template.csv`, mỗi server một dòng.

### Câu 1 — Code thật sự gọi nhà cung cấp nào? (`upstream_providers`, `upstream_evidence`)

1. Trong repo, tìm (phím `t` trên GitHub hoặc ô Search) các chuỗi: `https://`, `api.`, `baseURL`, `BASE_URL`, `endpoint`.
2. Chỉ quan tâm tới URL mà **tool thuộc loại thông tin được giao** gọi (ví dụ tool lấy thời tiết), theo **cấu hình mặc định**.
3. Ghi tên **tổ chức** sở hữu hostname, không ghi URL đầy đủ: `api.openweathermap.org` → `OpenWeather`; `api.open-meteo.com` → `Open-Meteo`.
4. Nhiều nhà cung cấp mặc định thì ghi cách nhau bằng `;`.
5. `upstream_evidence`: đường dẫn file và số dòng, ví dụ `src/index.ts:42`.

### Câu 2 — Agent có thấy tên nhà cung cấp không? (`l1_declared_provider`, `l1_evidence`)

Chỉ đọc những gì agent thấy khi chạy: **tên server, tên tool, mô tả (description) của tool, và schema tham số**. Thường nằm trong đoạn code đăng ký tool, ví dụ `server.tool("get_weather", "Get weather from ...", ...)` hoặc `Tool(name=..., description=...)`.

- Nếu tên nhà cung cấp xuất hiện **đích danh** trong các chỗ đó → ghi tên đó.
- Nếu không → ghi `unknown`.
- **Không suy luận.** "Get current weather" không nêu nhà cung cấp → `unknown`.
- `l1_evidence`: trích tối đa khoảng 10 từ chứa tên nhà cung cấp, hoặc để trống nếu `unknown`.

### Câu 3 — README có nêu không? (`l2_declared_provider`, `l2_evidence`)

Giống câu 2 nhưng được đọc thêm README. Nếu cả tool description lẫn README đều không nêu → `unknown`.

## Ví dụ minh họa (giả định, không phải dữ liệu thật)

| Cột | Giá trị |
|---|---|
| `upstream_providers` | `Open-Meteo` |
| `upstream_evidence` | `src/weather.py:18` |
| `l1_declared_provider` | `unknown` (description chỉ ghi "Get forecast for a city") |
| `l2_declared_provider` | `Open-Meteo` (README: "Powered by Open-Meteo") |

## Khi gặp khó

| Tình huống | Cách ghi |
|---|---|
| Người dùng tự chọn provider qua biến môi trường | Ghi provider **mặc định**; thêm `configurable` vào `notes` |
| Không tìm thấy URL nào | `upstream_providers` = `ambiguous`, giải thích trong `notes` |
| Server gọi qua một thư viện (SDK) chứ không gọi URL trực tiếp | Ghi nhà cung cấp của SDK đó (ví dụ thư viện `yfinance` → `Yahoo Finance`), ghi tên thư viện vào `notes` |
| Một server có nhiều tool khác loại thông tin | Chỉ xét tool thuộc loại thông tin trong cột `category` |

Nộp file đã điền cho tác giả. Cảm ơn bạn!
