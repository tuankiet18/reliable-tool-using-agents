---
title: "Gán nhãn độc lập và xuất tài liệu: các bẫy gặp ngày 2026-10-14"
captured: 2026-10-14
source: claude-code session (reliable-tool-using-ai-agents, survey 2)
tags: [research-methods, evidence, reproducibility]
---

# Bẫy khi kiểm chứng nhãn và xuất tài liệu

## Kiểm chứng nhãn
- **"Coder con người" có thể giao việc cho AI.** File coder 2 của survey 2 ghi `coder = Codex (AI)` ở cả 20 dòng. Từ đây, khi gửi việc cho người gán nhãn, hãy làm hai điều:
  - dặn rõ là phải tự làm, hoặc nếu có dùng công cụ thì phải khai báo;
  - kiểm tra cột `coder` trước khi gọi kết quả là human validation.
- **Bất đồng giữa hai coder phần lớn là do cách đặt tên provider**, không phải bất đồng thật: tên sản phẩm và tên công ty, ví dụ `Google Maps Platform` và `Google`, `Amazon Location Service` và `AWS`. Nên cố định trước một bảng chuẩn hóa ở **mức tổ chức**.
- **Đại lượng quan trọng nhất có thể khớp tuyệt đối dù khớp tên thấp.** Ở đây, việc L1 có nhãn hay thiếu nhãn khớp 1.00. Hãy báo cáo agreement theo đúng đại lượng mà phân tích dùng.
- **Codebook còn mơ hồ ở một điểm:** metadata nêu nguồn dữ liệu phía sau một API trung gian thì có tính là provider khai báo không. Chính điểm này quyết định việc P3 không đạt.

## Git
- Merge PR bằng **merge commit**, không dùng squash, để giữ mốc thời gian chứng minh protocol hoặc amendment được commit trước khi chạy phân tích.

## Xuất tài liệu
- **CSV lưu từ Excel có BOM.** Đọc bằng `encoding="utf-8-sig"`.
- **Mermaid** bỏ qua `direction` trong subgraph khi có cạnh nối giữa các subgraph. Muốn sơ đồ rộng thì tách thành nhiều sơ đồ riêng.
- **LibreOffice** khi chuyển HTML sang docx sẽ làm mất SVG inline và lệch font. Nên dựng docx bằng `python-docx` (`uv run --with python-docx`), và xuất hình SVG thành PNG bằng screenshot của Chrome headless.
- **Tài liệu gửi giảng viên phải đọc độc lập được:** không link nội bộ, không mã claim, không checkbox.

## Bổ sung 2026-10-15: phân xử khi không có coder con người
- Nếu không có người gán nhãn độc lập, tác giả có thể **phân xử** các bất đồng giữa hai AI coder (author adjudication) và tự **kiểm tra ngẫu nhiên** các bằng chứng `file:dòng`. Ghi quy trình vào protocol (amendment) trước khi tác giả xem các trường hợp.
- **Che tên câu trả lời** thành X/Y, xếp ngẫu nhiên theo seed, và giữ khóa ở một file riêng, để tác giả không thiên vị coder nào.
- **Tách câu hỏi luật khỏi câu hỏi sự thật.** Câu hỏi luật (tên nguồn đứng sau API trung gian có tính không) quyết định một lần, rồi áp cho mọi server. Câu hỏi sự thật thì xét từng trường hợp.
- Kết quả phân xử chỉ dùng cho **sensitivity analysis**; không thay phân tích chính đã khóa.
- **Mẹo kỹ thuật:**
  - thư mục tạm bị xóa giữa các phiên, nên lấy lại file tại commit đã ghim bằng `https://raw.githubusercontent.com/<repo>/<sha>/<path>`;
  - link GitHub dạng `blob/<sha>/<path>#L<a>-L<b>` sẽ tô sáng đúng các dòng cần đọc;
  - `openpyxl` chưa cài trong Python hệ thống, nên chạy bằng `uv run --no-project --with openpyxl`.
- **Link trong file xlsx có thể không bấm được** (LibreOffice cần giữ Ctrl rồi bấm, một số trình xem bỏ qua hyperlink). Ô nên hiện nguyên URL thay vì chữ "Mở link", và gửi kèm danh sách link trong chat.

## Bổ sung 2026-10-16: kiểm chứng prior art
- **Lấy metadata arXiv (tác giả, abstract):** gọi `https://export.arxiv.org/api/query?id_list=<id1>,<id2>` (phải dùng https; http trả về rỗng), hoặc đọc thẻ `citation_author` trong trang `arxiv.org/abs/<id>`.
- **Số trong abstract và số trong bảng có thể khác nhau mà vẫn đều đúng.** Ví dụ VP-Control: abstract dùng số gộp mọi regime (62,9% so với 22,9%); Table IV có số theo từng regime (common stale: 91,5% so với 9,8%). Khi trích, phải ghi rõ regime.
- **Đọc toàn văn bài gần nhất thường tìm thêm được prior art ở phần related work.** Ví dụ VP-Control dẫn tới Bara, Epistemic Sybil Resistance (arXiv:2609.01873).

## Bổ sung 2026-10-17: dựng paper LaTeX trên máy này
- **lualatex hỏng font ngoài:** luaotfload báo "Error in luaotfload: reverting to OT1" và thiếu `luaotfload-tool`, nên fontspec không nạp được font OTF.
- **`~/.local/bin/xelatex` không đáng tin:** đó là script gọi `xetex` với một file format nằm trong thư mục của dự án khác (`~/.gemini/...`), nên không tái lập được.
- **Cách chắc chắn:** dùng `pdflatex` chuẩn với T1, lmodern và utf8; tên tiếng Việt ghi không dấu. Máy có sẵn `latexmk` và `bibtex`; không có IEEEtran, acmart, llncs hay siunitx.
- **SVG sang PDF vector** khi không có rsvg/inkscape: bọc SVG trong HTML có `@page{size:Wpx Hpx;margin:0}`, rồi chạy `google-chrome --headless=new --print-to-pdf`. Kết quả là đúng một trang, kích thước bằng px × 0,75 pt.

## Bổ sung 2026-10-21: lần thử human check bằng tác giả gán nhãn mù thất bại
- **Gán nhãn mù vẫn hỏng nếu người gán dùng AI để tra repo.** Mẫu 15 server đã chọn bằng hash và đã bỏ nhãn AI, nhưng tác giả dùng AI tra cứu và để trống 6/15 server. Dấu hiệu nhận ra là cách diễn đạt trong ô ghi chú giống văn AI. Cách xử lý: hỏi thẳng trước khi tính agreement.
- **Quyết định (option B):** dừng hẳn, không tính κ. Đổi trạng thái protocol thành `terminated-not-completed`, và commit file đã nộp như một bản ghi deviation. Ghi một câu công khai trong paper (cả bản đầy đủ, bản rút gọn, LaTeX phần Threats) và ledger O5: lần thử này "not reported as validation".
- **Bài học cho lần sau:** yêu cầu "không dùng AI" phải ghi trong protocol và nhắc lại ngay trên template; nên có một câu tự khai báo việc dùng AI trong sheet nộp.
- **File PDF tiếng Anh** nằm ở `paper/latex/main.pdf`. File này bị gitignore, build lại bằng `pdflatex main.tex`. Người dùng hay hỏi "bản PDF là bản nào", nên gửi file kèm đường dẫn.
