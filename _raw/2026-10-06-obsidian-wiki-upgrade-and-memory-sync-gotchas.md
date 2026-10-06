---
title: "obsidian-wiki upgrade và gotcha của memory sync"
category: skills
tags:
  - topic/obsidian-wiki
  - research-methods
  - reproducibility
summary: "Nâng cấp obsidian-wiki dưới PEP 668 bằng uv tool; `memory sync` ghi đè hot.md và viết lại index.md; lint có false positive với URL .md."
tier: supporting
related: []
extends: null
contradicts: null
superseded_by: null
capture_source: claude-session
project: "reliable-tool-using-ai-agents"
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: 2026-10-06
provenance:
  extracted: 0.9
  inferred: 0.1
sources:
  - "reliable-tool-using-ai-agents session (2026-10-06)"
---

# obsidian-wiki: upgrade và các gotcha khi bảo trì vault

Các phát hiện khi nâng cấp obsidian-wiki 2026.9 lên 2026.10.1 và bảo trì vault nghiên cứu.

## pip bị chặn bởi PEP 668

**Problem:** `pip install -U obsidian-wiki` thất bại với `externally-managed-environment`.

**Fix:** dùng `uv tool install --force obsidian-wiki` (ghi đè script cũ trong `~/.local/bin`), rồi chạy lại `obsidian-wiki setup` để symlink 40 skill sang đường dẫn mới.

**Confirmed by:** `obsidian-wiki -V` báo 2026.10.1, `doctor` pass `setup-version`.

## `obsidian-wiki memory sync` ghi đè hot.md và index.md

**Behavior:** lệnh này tái sinh `hot.md` (623 từ xuống 52 từ) và viết lại cả `index.md` (~250 dòng diff), kể cả nội dung viết tay.

**Workaround:** commit checkpoint trước khi chạy; nếu mất nội dung thì `git checkout HEAD -- hot.md index.md`. Chỉ giữ nội dung bền trong `## Key Takeaways` của `hot.md`. Hệ quả: `doctor` vẫn cảnh báo `memory-surface` drift.

**Confirmed by:** `git diff --stat` và đọc `hot.md` sau khi chạy.

## Lint false positive và giới hạn

**Behavior:** `obsidian-wiki lint` báo broken link cho Markdown link tới URL GitHub kết thúc bằng `.md` (ví dụ `B4_ASSUMPTIONS.md`); wikilink tới file `.json`/`.py` cũng bị tính là hỏng; không có cơ chế ignore, nên file kết quả sinh tự động (`results/summary.md`) luôn bị báo thiếu frontmatter.

**Workaround:** đổi wikilink tới file không phải `.md` thành inline code; chấp nhận false positive; không thêm frontmatter vào frozen results.

**Notes:** `trust-record` cần duyệt thủ công của chủ vault, không tự điền `base_confidence`/`lifecycle`.
