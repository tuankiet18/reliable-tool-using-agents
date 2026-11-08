---
title: "2026-10-12 — Kết quả kiểm định có đăng ký trước cho điều kiện J"
category: journal
tags: [research-log, experiment, provenance, verification, reproducibility]
sources:
  - "synthesis/Protocol - Confirmatory Test of the Label-Quality Condition.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_label_quality_20261012/analysis.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_label_quality_test.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_label_quality_test.py"
created: 2026-10-12T15:00:00+07:00
updated: 2026-10-12T15:00:00+07:00
summary: >-
  Kiểm định đăng ký trước trên 60 task mới: J < 0 làm provenance tệ hơn random (+0.133), J > 0 tốt hơn (−0.177), thông số survey tốt hơn (−0.093); tương đương ở J = 0 không được xác nhận.
provenance:
  extracted: 0.80
  inferred: 0.20
base_confidence: 0.6
lifecycle: draft
lifecycle_changed: 2026-10-12
---

# Kiểm định có đăng ký trước cho điều kiện J — 2026-10-12

**Phạm vi:** theo [[synthesis/Protocol - Confirmatory Test of the Label-Quality Condition]] v1.0, được tác giả xác nhận trước khi viết code. Mô phỏng quyết định do project thiết kế; không gọi model, không chạy agent thật, chi phí $0.

## Trình tự (có trong lịch sử git)

1. Protocol viết và xác nhận (commit `027caa6`, `af61287`).
2. Clone mới `trajectory-judge` ở commit `d0ee54aa`, venv Python 3.12.3 mới.
3. Kiểm tra trước khi chạy: 120 instance cũ không đổi; 40/60 task escalation; 0 task trùng; task split đóng băng, SHA-256 `9a68d765…` (commit `1d299d5`).
4. Test đơn vị phát hiện dự đoán H-J4 tính sai giả định → **Amendment A1** sửa dự đoán (0.250 → 0.182) trước khi có bất kỳ row nào; 84/84 test đạt (commit `3f37daa`).
5. Chạy 4.800 rows, hai lần, byte-identical (raw `fb69bcf2…`).
6. Phân tích đúng theo §5.

## FACT — Kết quả (regime targeted, 300 rows mỗi policy mỗi điều kiện)

| Điều kiện | Provenance | Random | Chênh lệch | Dự đoán | 95% CI | Kết luận |
|---|---:|---:|---:|---:|---|---|
| `J_plus` (J = +0.8) | 0.087 | 0.263 | −0.177 | −0.176 | [−0.233, −0.120] | H-J2 **hỗ trợ** |
| `J_zero` (J = 0) | 0.320 | 0.257 | +0.063 | 0.000 | [+0.003, +0.127] | H-J3 **không hỗ trợ** (90% CI [+0.013, +0.117]) |
| `J_minus` (J = −0.5) | 0.423 | 0.290 | **+0.133** | +0.160 | [+0.070, +0.200] | H-J1 **hỗ trợ** |
| `survey_calibrated` | 0.173 | 0.267 | −0.093 | −0.091 | [−0.157, −0.033] | H-J4 **hỗ trợ** |

Regime clean: 0 unsafe ở mọi điều kiện (sanity đạt).

## Về H-J3 không đạt

- Chênh lệch ở `J_zero` lệch dự đoán 0.063, vượt ngưỡng 0.05 nên được đánh dấu theo §5.
- **Thăm dò (không có trong protocol):** provenance chọn tool chung 79/200 lần, kỳ vọng 1/3 (z = +1.85, p = 0.064); random chọn 66/200 (đúng kỳ vọng). Test đơn vị với 20.000 lần rút cho 0.333, nên không có dấu hiệu lỗi code. Độ lệch phù hợp với biến thiên ngẫu nhiên của 200 lần chọn.
- **Thiếu sót của protocol:** power cho H-J3 không được tính khi lập kế hoạch; ước lượng sau là khoảng 59%. Không chạy thêm seed hay task để "cứu" H-J3.
- Cách viết đúng: *không có bằng chứng về tương đương ở J = 0*; **không** viết "J = 0 gây hại".

## INFERENCE — Ý nghĩa

1. Dự đoán chính của RQ2 (metadata sai có hệ thống **gây hại**) giờ có kiểm định đăng ký trước, trên task mới, qua toàn bộ pipeline (actor, gate, leakage, oracle). Độ lớn quan sát khớp dự đoán trong khoảng 0.03 ở ba điều kiện có hiệu ứng.
2. Điều này **tăng độ tin cậy về quy trình**, không tăng tính mới: kết quả gần như suy ra được từ mô hình, và đây vẫn là mô phỏng.
3. Bài học phương pháp: test đơn vị trước khi chạy đã bắt một lỗi trong dự đoán; còn việc không tính power cho mọi hypothesis đã làm một hypothesis phụ thiếu sức kiểm định.

## Liên quan

- [[synthesis/Protocol - Confirmatory Test of the Label-Quality Condition]]
- [[journal/2026-10-06-prior-art-refresh-vp-control-and-efd]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
