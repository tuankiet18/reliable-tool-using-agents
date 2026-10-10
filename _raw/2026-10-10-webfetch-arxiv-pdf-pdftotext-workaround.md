---
title: "Đọc PDF arXiv khi WebFetch trả nhị phân: dùng pdftotext trên file đã lưu"
category: skills
tags:
  - topic/literature-review
  - research-methods
  - reproducibility
summary: "WebFetch trên arxiv.org/pdf trả nội dung nhị phân nhưng vẫn lưu file; chạy pdftotext lên file đó để grep và trích chính xác câu chữ khi kiểm chứng prior art."
tier: supporting
related: []
extends: null
contradicts: null
superseded_by: null
capture_source: claude-session
project: "reliable-tool-using-ai-agents"
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: 2026-10-10
provenance:
  extracted: 0.9
  inferred: 0.1
sources:
  - "reliable-tool-using-ai-agents session (2026-10-06)"
---

# Đọc PDF arXiv để kiểm chứng prior art

## WebFetch không đọc được PDF arXiv

**Behavior:** `WebFetch` trên `https://arxiv.org/pdf/<id>` trả lời rằng nội dung là luồng PDF nén, không trích được câu. Bản tóm tắt từ trang `abs`/`html` lại do một model nhỏ viết, có thể sai chi tiết (ví dụ khẳng định "không có thí nghiệm nhiễu nhãn" mà không dẫn chứng).

**Workaround:** kết quả WebFetch vẫn ghi đường dẫn file nhị phân đã lưu (`.../tool-results/webfetch-*.pdf`). Chạy `pdftotext` (không `-layout` để văn bản liền mạch; có `-layout` để đọc bảng) ra file trong scratchpad, rồi `grep -n` các cụm từ cần kiểm (ví dụ `mislabel|label noise|lineage`) và đọc đoạn quanh đó. Cách này cho phép trích nguyên văn và ghi "không tìm thấy" một cách có căn cứ.

**Confirmed by:** dùng để xác minh VP-Control (2609.10969) ghi "Lineage is supplied" và không có thí nghiệm nhiễu nhãn; xem `journal/2026-10-06-prior-art-refresh-vp-control-and-efd.md`.

**Notes:** tìm chuỗi không thay cho đọc toàn văn; ghi rõ phạm vi đã đọc trong ledger/paper.
