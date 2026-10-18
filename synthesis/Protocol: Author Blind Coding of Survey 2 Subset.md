---
title: >-
  Protocol: Author Blind Coding of Survey 2 Subset
category: synthesis
tags: [research-protocol, evidence, reproducibility, external-validity]
sources:
  - "synthesis/Protocol: Expanded Real-Tool Metadata Survey.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tool_survey_2/HUMAN_CODER_GUIDE.md"
created: 2026-10-18T10:00:00+07:00
updated: 2026-10-18T10:00:00+07:00
summary: >-
  Protocol cho lần kiểm tra của con người đầu tiên của survey: tác giả gán nhãn mù 15 server chọn bằng hash trong số server chưa từng xem, rồi so với nhãn coder A (AI).
lifecycle: draft
lifecycle_changed: 2026-10-18
protocol_version: "1.0"
protocol_status: awaiting-author-confirmation
---

# Protocol: Tác giả gán nhãn mù 15 server của survey 2

> [!important] **PROSPECTIVE.** Viết ngày 2026-10-18, trước khi tác giả xem bất kỳ server nào trong mẫu. Mọi thay đổi sau khi khóa phải ghi thành amendment ở §8.

## 1. Mục tiêu

Coder thứ hai của cả hai survey đã dùng AI, nên survey **chưa có lần kiểm tra nào của con người**. Ở đây tác giả gán nhãn độc lập một mẫu nhỏ, không xem nhãn AI, để đo mức đồng thuận giữa người và AI.

**Câu hỏi.** *How well do the AI coder's survey-2 labels agree with an independent human coding by the author on a hash-selected subset?* Giải thích: nhãn do AI gán có khớp với nhãn do chính tác giả, là con người, tự gán không?

## 2. Mẫu

- **Tập gốc:** 74 server trong tập ước lượng của survey 2.
- **Loại các server tác giả đã từng thấy nhãn hoặc code:**
  - 20 server của tập coder 2;
  - 7 server trong phân xử;
  - 10 server trong phần kiểm tra bằng chứng.
- Còn lại **48 server**. Chọn **15 server** có `sha256(server_id + "|author-blind-2026-10-18")` nhỏ nhất. Kiểm tra ngày 2026-10-18: 4 news, 3 stock, 2 web search, 2 crypto, 2 movies, 1 weather, 1 books.
- Danh sách được ghi vào template trước khi giao cho tác giả.

## 3. Cách gán nhãn

- Dùng **codebook của survey 2**: §5 của protocol survey 2, Amendment A1, năm luật diễn giải của A2, và bốn luật R1–R4 do chính tác giả quyết định ngày 2026-10-16.
- Với mỗi server, ghi:
  - provider mặc định (`upstream_providers`) và bằng chứng `file:dòng`;
  - provider được nêu ở L1 (hoặc `unknown`) và đoạn trích làm bằng chứng;
  - provider được nêu ở L2 (hoặc `unknown`).
- **Quy tắc độc lập:**
  - tác giả **không dùng AI** để đọc code, dịch hay tóm tắt;
  - tác giả không mở `coding.csv` hay bất kỳ file nhãn nào khác;
  - Claude chỉ cung cấp link repo tại commit đã ghim và hướng dẫn chung, không bàn về server cụ thể cho tới khi tác giả nộp.
- Tác giả được dùng công cụ tìm kiếm có sẵn trên GitHub và trình duyệt.
- Ước tính 15–20 phút mỗi server, tổng 4–5 giờ, chia nhiều buổi.

## 4. Đo lường (cố định trước khi so sánh)

- **Chỉ số chính:** đồng thuận về việc **L1 có hay không có tên provider**, vì đây là đại lượng của finding chính (m ≈ 70%). Báo cáo percent agreement và Cohen's κ.
- **Chỉ số phụ:** đồng thuận về upstream provider, tên ở L1 và tên ở L2, theo hai cách:
  - khớp nguyên chữ;
  - sau chuẩn hóa tên bằng bảng **cố định từ bây giờ**: bảng của survey 1 cộng 10 cặp gộp ở mức tổ chức đã lập ngày 2026-10-16.
- **Quy tắc diễn giải ghi trước:**
  - nếu đồng thuận về L1 có/không có tên ≥ 0,80, kết luận "kiểm tra của con người ủng hộ nhãn AI ở đại lượng chính";
  - nếu thấp hơn, báo cáo là điểm yếu và phân tích nguyên nhân.
- Bất đồng được liệt kê đầy đủ. **Không sửa nhãn chính** của survey theo kết quả này.

## 5. Ghi nhận trong paper

Ghi là *"independent blind coding of a 15-server subset by the author"*, kèm giới hạn: tác giả không phải người ngoài dự án, và đã biết codebook cùng các luật tự đặt.

## 6. Giới hạn biết trước

- Mẫu nhỏ (15 server), nên κ có khoảng tin cậy rộng.
- Tác giả đã quen dự án và codebook, nên đây chưa phải coder hoàn toàn độc lập.
- Tác giả là người mới đọc code; bất đồng có thể do kinh nghiệm chứ không chỉ do codebook.

## 7. Tài liệu giao cho tác giả

- File Excel `data/tool_survey_2/author_blind/author_blind_template.xlsx`, gồm 15 dòng, link repo tại commit, các cột cần điền và một dòng ví dụ.
- Hướng dẫn ngắn bằng tiếng Việt: các bước đọc code, luật codebook và các tình huống khó.

## 8. Nhật ký khóa và amendment

| Ngày | Sự kiện | Ghi chú |
|---|---|---|
| 2026-10-18 | Protocol v1.0 được viết | Chờ tác giả xác nhận; chưa tạo template |

## Liên quan

- [[synthesis/Protocol: Expanded Real-Tool Metadata Survey]]
- [[synthesis/Protocol: Agent Corroborator Choice with Real Tool Metadata]]
