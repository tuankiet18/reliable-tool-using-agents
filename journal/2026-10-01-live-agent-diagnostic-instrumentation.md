---
title: >-
  2026-10-01 — Instrumentation cho live-agent safety diagnostic
category: journal
tags: [research-log, experiment, reproducibility, verification]
sources:
  - "synthesis/Protocol Amendment: Exploratory RTX 4060 Safety Diagnostic.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_live_agent_gate.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_live_agent_gate.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/tests/test_live_agent_gate.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/tests/test_analyze_live_agent_gate.py"
  - "/home/kiet/Downloads/raw.jsonl"
summary: >-
  Runner/analyzer đã hỗ trợ ma trận tám cell và process metrics; 58 unit tests cùng dry-run trên upstream pinned pass, nhưng chưa chạy INS-00032 trên 7B/RTX.
provenance:
  extracted: 0.78
  inferred: 0.20
  ambiguous: 0.02
base_confidence: 0.59
lifecycle: draft
lifecycle_changed: 2026-10-01
tier: supporting
created: 2026-10-01T20:39:33+07:00
updated: 2026-10-02T01:19:30+07:00
---

# Instrumentation cho diagnostic `INS-00032`

## Mục tiêu

Thực thi bước chuẩn bị đã khóa ở [[synthesis/Protocol Amendment: Exploratory RTX 4060 Safety Diagnostic]]: chọn chính xác một task/hai enforced policies và đo hành vi trong trajectory thay vì chỉ nhìn final outcome. Không thay đổi fault model, selector, intervention hoặc main deterministic results.

## FACT — đã thực hiện

- `run_live_agent_gate.py` nhận `--task-ids`, `--policies` và `--dry-run`; lệnh dry-run liệt kê exact cell keys cùng expected action và planned corroborator mà không gọi model hoặc ghi output. Mặc định cũ `--task-count`/ba policies được giữ. `summary.json` dùng `null` cho boundary-attempt coverage khi không có refund attempt, thay vì báo `1.0` giả tạo.
- `analyze_live_agent_gate.py` đọc `steps[].call` và `steps[].observation.ok` để đếm accepted unsafe refunds, actual escalation calls, refund attempts sau refund thành công, escalation sau refund, successful reply và diagnostic cells có/không có refund attempt. Analyzer báo riêng số boundary checks/attempts, phản ánh `N/A` nếu denominator bằng zero và đánh dấu counter mismatch. Các metric outcome-based cũ vẫn được giữ riêng.
- Unit tests mới kiểm tra CLI dry-run bằng upstream giả trong bộ nhớ: đúng `INS-00032` × hai regimes × seeds `701,809` × hai enforced policies = **8 cells**, expected action `escalate`, không tạo output/model call. Diff review phát hiện và sửa `planned_corroborator` bị đặt nhầm trong model API payload; test bổ sung xác nhận payload không chứa metadata nội bộ và raw episode row có metadata này. Nếu targeted row thiếu oracle, analyzer gắn `UNKNOWN_ORACLE`, không đếm là decisive. Toàn bộ suite hiện tại **58/58 pass**; `py_compile`, `git diff --check` và `ruff check` trên bốn source/test files đều pass (`ruff` chạy từ tool environment tạm).
- Re-audit **đọc-only** sáu raw rows RTX cũ bằng analyzer mới cho: `0` accepted unsafe refunds, `5` episodes có successful `escalate`, `12` escalation calls, `2` post-success escalation episodes và `2` refund attempts sau successful refund. Số này nhất quán với đọc trace ở [[journal/2026-09-30-rtx4060-live-agent-diagnostic]], không phải result mới về hiệu quả policy.
- Dry-run thật đã pass trên checkout tạm của `trajectory-judge@d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5` dùng `uv`/Python 3.13: in đúng **8 cells**, tất cả expected action `escalate`; seed `701` hai independent corroborators, seed `809` random=`check_eligibility_search` và provenance=`check_eligibility_audit`. Runner không tạo output directory và không gọi model. Checkout tạm nằm ngoài vault tại `/tmp/trajectory-judge-dryrun-S9ZiB400`; đây không phải môi trường RTX Windows.

## Điều chưa hoàn tất tại thời điểm 2026-10-01

- Chưa commit/push thay đổi code; Windows clone chưa nhận instrumentation. Chưa chạy Qwen2.5 7B trên `INS-00032`; không có outcome mới cho RQ.
- Dry-run trên Linux/upstream pinned đã pass, nhưng sau khi sync vẫn cần kiểm tra lại trên **Windows clone thực tế** trước model run.

## Đánh giá

**INFERENCE:** Measurement readiness đã tốt hơn: việc agent không attempt refund sẽ hiện thành `NON_DECISIVE_NO_ATTEMPT`, không bị tính như gate bảo vệ thành công; outcome escalation không che actual tool calls. Điều này xử lý lỗi diễn giải ở pilot trước nhưng **chưa** tăng evidence về safety effect. ^[inferred]

## Bước tiếp theo duy nhất

Đồng bộ đúng bốn file runner/analyzer/tests cùng hướng dẫn README sang Windows clone an toàn, chạy lại `--dry-run` tại máy đó rồi mới chạy một diagnostic tám episode vào output directory mới. Không scale lên 72 episodes và không cập nhật claim paper trước khi audit raw trace.

## Cập nhật trạng thái — 2026-10-02

Những mục “chưa hoàn tất” phía trên là ảnh chụp trạng thái ngày 2026-10-01. Code và README đã được đồng bộ sang nhánh Windows-safe `codex/rtx4060-ins32-diagnostic@e265c358df3fd20a274f0ce3f6b53bc774694ed1`; máy RTX 4060 đã chạy dry-run và tám episodes. Audit raw trace cho thấy **technical pass nhưng policy-effect validity fail** vì mọi refund request là `0 EUR` sau escalation. Xem [[journal/2026-10-02-ins32-rtx4060-validity-audit]].

Path `/home/kiet/Downloads/raw.jsonl` ở frontmatter từng chứa raw sáu rows cũ khi re-audit ngày 2026-10-01, nhưng hiện đã bị lượt `INS-00032` thay nội dung. Hash lịch sử của lượt cũ vẫn ghi tại [[journal/2026-09-30-rtx4060-live-agent-diagnostic]]; không dùng path hiện tại để tái kiểm chứng lượt trước.
