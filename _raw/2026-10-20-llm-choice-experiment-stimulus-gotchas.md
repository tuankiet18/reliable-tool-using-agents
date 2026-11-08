---
title: "Dựng stimuli cho thí nghiệm LLM chọn tool: các bẫy (RQ4, 2026-10-20)"
captured: 2026-10-20
source: claude-code session (reliable-tool-using-ai-agents)
tags: [research-methods, ai-agents, reproducibility]
---

# Bẫy khi dựng stimuli từ mô tả tool thật

- **Tên server trùng nhau tạo confound.** Hai repo khác chủ có thể cùng tên (`crypto_mcp_server`). Nếu chỉ hiện tên repo, model có thể né tool "trùng tên với primary" mà không cần đọc metadata. Hãy dùng `owner/repo`, và kiểm tra tự động không có tên trùng.
- **Bộ trích regex có thể ghép nhầm description.** Ví dụ decorator FastMCP không có docstring khiến regex lấy nhầm docstring của hàm kế tiếp.
  - Kiểm tra (a): description phải xuất hiện nguyên văn trong file nguồn.
  - Kiểm tra (b): tên tool phải nằm trong khoảng ±40 dòng quanh đó.
  - Sau hai bước này vẫn nên đọc lướt từng cặp tên tool và mô tả, vì lỗi khớp nghĩa phải nhìn mới thấy.
- **Description trong TS/JS hay được nối bằng `"a" + "b"`,** nên regex chỉ lấy được đoạn đầu. Cần dò dấu hiệu `" +` ngay sau đoạn đã trích và ghép lại.
- **Mỗi server có thể có nhiều tool.** Hãy chọn đúng tool gọi upstream mà coder đã ghi bằng chứng; tool đầu tiên hay tool có tên hấp dẫn nhất không phải lúc nào cũng là tool đó (ví dụ tool phân tích AI, tool so sánh HTML).
- **Gói chạy trên máy khác:**
  - chỉ dùng thư viện chuẩn của Python, gọi Ollama `/api/chat` với `format: json` và temperature 0;
  - runner kiểm tra SHA-256 của file items, chạy tiếp được khi bị ngắt, có `--dry-run`;
  - runner ghi digest của model và thông tin GPU vào file kết quả.
- **Kiểm thử script phân tích trên hai bộ dữ liệu giả** (model ngẫu nhiên và model lý tưởng) trước khi có dữ liệu thật.
- **Lộ nhãn qua chat:** tên server lỡ nhắc trong chat cũng tính là đã lộ khi chọn mẫu cho gán nhãn mù. Ghi lại trong nhật ký, giữ nguyên mẫu, và báo cáo kết quả có và không có server đó.

## Bổ sung: gán nhãn "thủ công" bị AI hỗ trợ
- **Dấu hiệu nhận ra:**
  - các câu kiểu "chưa truy xuất được mã nguồn tại commit ghim", "không suy đoán provider từ tên repo";
  - số dòng dạng `30–36` với dấu gạch dài;
  - upstream lấy từ README thay vì từ code;
  - cột thời gian để trống.
- **Cách xử lý:**
  - hỏi thẳng, không buộc tội, **trước khi** so với nhãn AI;
  - ghi sai lệch vào nhật ký protocol;
  - lưu file làm hồ sơ nhưng không dùng làm human validation.
- **Phòng ngừa:**
  - nói rõ những gì được dùng: trình duyệt, ô tìm kiếm của GitHub, Ctrl+F, Google Translate cho văn bản;
  - nói rõ những gì không được dùng: AI chat, agent, code assistant;
  - bắt buộc ghi thời gian thật cho từng server;
  - làm mẫu một server ngoài mẫu trước khi người đó tự làm.
