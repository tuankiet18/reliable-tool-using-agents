# Chuyển repo research sang máy khác (Windows)

- **Không commit `.claude/`**: `settings.json` chứa đường dẫn hook tuyệt đối `/home/kiet/...`, vô dụng trên máy khác. Cài lại hook bằng obsidian-wiki trên máy mới.
- **File sinh ra bị gitignore, phải build lại hoặc chép tay:** `paper/latex/main.pdf` (chạy `pdflatex` và `bibtex` trong `paper/latex/`), `supervisor-overview.pdf` và `.docx`.
- **Trước khi chuyển, kiểm tra `git status --ignored`** để thấy file nào chỉ tồn tại cục bộ, và `git log origin/main..main` để chắc chắn không còn commit chưa push.
- **Gói chạy RQ4 tự đủ** trong `data/rq4_agent_choice/runner/` (Python stdlib và Ollama); script `src/` dùng `pathlib` nhưng chưa được thử trên Windows.
