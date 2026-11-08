---
title: "Điểm yếu của paper failure-domain metadata và các hướng nâng cấp (đánh giá kiểu reviewer, 2026-10-18)"
captured: 2026-10-18
source: claude-code session (reliable-tool-using-ai-agents)
tags: [research-methods, paper-draft, evidence]
---

# Điểm yếu và hướng nâng cấp, theo góc nhìn reviewer workshop

Sắp xếp từ nặng đến nhẹ. Bài nộp môn đã đủ; các mục dưới đây là để bài đủ mạnh khi nộp workshop.

1. **Chưa có hành vi của agent thật.** RQ1 và RQ2 là mô phỏng gần như by-construction; RQ3 chỉ chiếu kết quả lên selector model.
   - Hướng sửa: thí nghiệm LLM thật chọn corroborator. Cho agent xem mô tả tool lấy từ survey, có hoặc không có tên provider, rồi đo tỷ lệ chọn đúng nguồn độc lập.
   - Chi phí: 0 USD nếu dùng model local (Qwen 7B / RTX 4060), khoảng 5–10 USD nếu dùng API. Thời gian khoảng 3–4 ngày, gồm viết protocol trước.
2. **Không có human validation cho nhãn survey.** Cả coder 2 và tác giả phân xử đều không độc lập.
   - Hướng sửa: tác giả gán nhãn mù khoảng 15 server chọn ngẫu nhiên, chưa xem nhãn AI, rồi tính agreement giữa người và AI. Mất khoảng 4–5 giờ.
3. **Định lý J có thể bị cho là hiển nhiên.**
   - Hướng sửa: so sánh hai chính sách xử lý missing label:
     - "missing thì bỏ qua rồi fallback ngẫu nhiên" (selector hiện tại);
     - "missing thì coi là chung" (khuyến nghị của EFD);
   - Chạy so sánh với k ≈ 0,5 quan sát được. Đây là phân tích giải tích, khoảng 1–2 ngày, phải ghi là exploratory.
4. **Ba RQ rời rạc.** Ở bản workshop, đưa RQ1 xuống thành motivation, trọng tâm là RQ2 và RQ3.
5. **Mục nhỏ:**
   - Robustness của RQ1 với 60 task: ưu tiên thấp.
   - Mẫu lấy từ MCP registry chính thức: ưu tiên thấp.
   - Nhờ một người độc lập kiểm tra chứng minh: rẻ, nên làm.

**Nguyên tắc:** mọi thí nghiệm thêm vào đều cần protocol được xác nhận trước. Nếu không, các bước phân tích tùy ý (forking paths) sẽ làm bài yếu đi thay vì mạnh lên.
