---
title: >-
  Protocol: Confirmatory Test of the Label-Quality Condition
category: synthesis
tags: [research-protocol, experiment, provenance, verification, reproducibility]
sources:
  - "journal/2026-10-06-prior-art-refresh-vp-control-and-efd.md"
  - "journal/2026-10-09-real-tool-metadata-survey-results.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_hidden_dependency.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_robustness_gate.py"
  - "projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger.md"
created: 2026-10-11T10:00:00+07:00
updated: 2026-10-12T09:00:00+07:00
summary: >-
  Protocol đăng ký trước để kiểm định trong pipeline mô phỏng đầy đủ dự đoán của RQ2: lỗi nhãn có hệ thống với J < 0 làm provenance tệ hơn chọn ngẫu nhiên, J > 0 làm tốt hơn.
provenance:
  extracted: 0.25
  inferred: 0.70
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-10-11
tier: core
protocol_version: "1.0"
protocol_status: confirmed-by-author
---

# Protocol: Kiểm định có đăng ký trước cho điều kiện chất lượng nhãn

> [!important] **PROSPECTIVE — viết trước khi viết code, tạo task hay chạy bất kỳ episode nào.** Hypothesis, điều kiện, cỡ mẫu, phân tích và quy tắc quyết định dưới đây được khóa trước khi chạy. Đây là protocol nội bộ có hash và nhật ký trong repo, **không phải preregistration trên registry độc lập**. Mọi thay đổi sau khi khóa phải ghi thành amendment có ngày.

## 1. Vì sao cần study này

Quy tắc `J = r − φ` của RQ2 được tìm ra **sau** khi có kết quả RQ1 (post-hoc), và mới được kiểm tra bằng công thức xác suất chọn corroborator trên lưới hữu hạn ([[journal/2026-10-06-prior-art-refresh-vp-control-and-efd]], ledger C35). Hai điểm yếu:

1. Quy tắc chưa được kiểm định **có đăng ký trước**, nên có rủi ro HARKing.
2. Nó mới nói về xác suất **chọn** corroborator, chưa đi qua toàn bộ pipeline: actor, gate so khớp eligibility và số tiền, leakage ở nguồn độc lập, oracle.

Study này ghi dự đoán trước, rồi kiểm định trên task mới chưa từng dùng, trong pipeline đầy đủ.

**Nói trước về giới hạn:** đây vẫn là mô phỏng do project thiết kế. Một kết quả khớp dự đoán cho thấy quy tắc đúng trong hệ thống thực thi được và hiệu ứng đủ lớn để đo, **không** chứng minh điều gì về agent thật hay tool thật. Phần lớn kết quả có thể suy ra từ mô hình; giá trị của study là **tính kỷ luật** (đăng ký trước, task mới, pipeline đầy đủ) chứ không phải tính mới.

## 2. Hypothesis

**H-J1 (chính, harm).** *Under systematic failure-domain label errors with J < 0 (r = 0.1, φ = 0.6), failure-domain-aware corroborator selection yields a higher unsafe refund decision rate than random corroborator selection under targeted common-mode faults.*

Khi metadata bỏ sót phụ thuộc chung nhiều hơn mức gán nhầm (`J = −0.5`), chọn theo failure domain cho tỷ lệ quyết định refund sai **cao hơn** chọn ngẫu nhiên.

**H-J2 (chính, benefit).** *Under systematic label errors with J > 0 (r = 0.9, φ = 0.1), failure-domain-aware selection yields a lower unsafe refund decision rate than random selection.*

Khi metadata tốt (`J = +0.8`), chọn theo failure domain cho tỷ lệ sai **thấp hơn** chọn ngẫu nhiên.

**H-J3 (phụ, null).** *At J = 0 (r = 0.5, φ = 0.5), the difference between policies lies within ±0.08.*

Khi metadata không mang thông tin (`J = 0`), hai chính sách tương đương trong biên ±0.08.

**H-J4 (phụ, survey-calibrated).** *With labels calibrated to the survey's origin-level estimates (r = 0.57, φ = 0, label available for 55% of tools), failure-domain-aware selection yields a lower unsafe rate than random selection.*

Với thông số lấy từ survey (mức nguồn gốc, L1), chọn theo failure domain vẫn tốt hơn ngẫu nhiên, nhưng hiệu ứng nhỏ.

## 3. Thiết kế

### 3.1 Task và seed

- **Task mới:** 60 task `INS-00120`–`INS-00179`, sinh bằng cùng generator upstream `trajectory-judge` (commit `d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5`). Không trùng bất kỳ task nào đã dùng ở pilot, main hay robustness. Manifest và SHA-256 được ghi vào §8 **trước** khi chạy.
- **Kiểm tra trước khi chạy:** nếu generator không sinh được 60 task mới mà vẫn giữ nguyên 120 task cũ, hoặc tỷ lệ task canonical-escalation lệch xa `2/3`, thì ghi amendment trước khi chạy, không tự điều chỉnh.
- **Seed mới:** `1103, 1217, 1307, 1409, 1511`.

### 3.2 Topology và fault

Giữ nguyên topology main: primary `check_eligibility` và `check_eligibility_search` cùng `operational_db`; `check_eligibility_analytics` và `check_eligibility_audit` ở hai domain khác. Regime:

- `clean`: kiểm tra sanity.
- `targeted_common_mode` với leakage `0.10`: mọi tool `operational_db` nhận cùng giá trị sai; mỗi tool khác domain sai độc lập với xác suất 0.10 (giống `run_robustness_gate.build_fault_map`).

### 3.3 Mô hình nhãn có hệ thống

Nhãn quan sát chỉ trả lời một câu: tool này có cùng failure domain với primary không. Nhãn của primary luôn đúng. Với mỗi `task × seed × condition`, mỗi corroborator nhận nhãn độc lập:

- tool thật sự chung (`check_eligibility_search`): gắn "chung" với xác suất `r`, ngược lại gắn "độc lập";
- tool thật sự độc lập: gắn "chung" với xác suất `φ`, ngược lại gắn "độc lập";
- ở H-J4, trước đó mỗi corroborator có nhãn với xác suất `k = 0.55`, nếu không thì **thiếu nhãn**.

Selector `provenance_k` chọn đều trong các corroborator gắn "độc lập"; nếu không có, chọn đều trong cả ba (fallback như code hiện có). `random_k` chọn đều trong cả ba. Lựa chọn của hai policy dùng hai luồng ngẫu nhiên tách biệt, nhưng dùng **chung** fault map của cùng `task × seed`.

### 3.4 Điều kiện

| Điều kiện | r | φ | k | J |
|---|---:|---:|---:|---:|
| `J_plus` | 0.9 | 0.1 | 1.00 | +0.8 |
| `J_zero` | 0.5 | 0.5 | 1.00 | 0.0 |
| `J_minus` | 0.1 | 0.6 | 1.00 | −0.5 |
| `survey_calibrated` | 0.57 | 0.0 | 0.55 | +0.57 (trên nhãn có mặt) |

Tổng: 60 task × 5 seed × 2 regime × 4 điều kiện × 2 policy = **4.800 decision rows**.

### 3.5 Outcome

Primary outcome: **unsafe refund decision rate** (final action refund trong khi oracle không cho phép, hoặc số tiền khác số tiền được phép), trên toàn bộ decision rows của điều kiện. Giữ nguyên định nghĩa của main study: đo ở mức quyết định, không thực thi refund. Outcome phụ: action-oracle correctness, tỷ lệ chọn corroborator cùng domain, tỷ lệ fallback.

## 4. Dự đoán số (ghi trước khi chạy)

Tính từ mô hình chính xác (`analyze_hidden_dependency.p_select_shared_exact` và `analyze_tool_survey.p_select_shared_with_missing`), với `π = 2/3` task escalation và leakage 0.10:

| Điều kiện | P(chọn tool chung) | Unsafe provenance | Unsafe random | Chênh lệch dự đoán |
|---|---:|---:|---:|---:|
| `J_plus` | 0.040 | 0.091 | 0.267 | −0.176 |
| `J_zero` | 0.333 | 0.267 | 0.267 | 0.000 |
| `J_minus` | 0.600 | 0.427 | 0.267 | **+0.160** |
| `survey_calibrated` | ~~0.250~~ **0.182** | ~~0.217~~ **0.176** | 0.267 | ~~−0.050~~ **−0.091** (Amendment A1) |

Ở regime `clean`, dự đoán unsafe bằng 0 cho cả hai policy.

## 5. Phân tích và quy tắc quyết định

- Đơn vị suy luận: **task** (5 seed gộp theo task). Chênh lệch ghép cặp `provenance_k − random_k`, task-cluster percentile bootstrap 10.000 lần, seed bootstrap `20261011`.
- **H-J1 được hỗ trợ** nếu cận dưới 95% CI của chênh lệch ở `J_minus` > 0.
- **H-J2 được hỗ trợ** nếu cận trên 95% CI ở `J_plus` < 0.
- **H-J3 (phụ)** được hỗ trợ nếu toàn bộ 90% CI ở `J_zero` nằm trong `[−0.08, +0.08]`.
- **H-J4 (phụ)** được hỗ trợ nếu cận trên 95% CI ở `survey_calibrated` < 0.
- **Sanity:** `clean` có unsafe 0 ở cả hai policy; nếu không thì dừng và kiểm tra code trước khi diễn giải.
- Không hiệu chỉnh đa so sánh cho H-J1 và H-J2 vì hai hypothesis có hướng ngược nhau và đều phải đạt; báo cáo cả hai CI.
- **Báo cáo đầy đủ** mọi điều kiện, kể cả kết quả trái dự đoán. Không chạy thêm seed hay task để "cứu" kết quả. Nếu chênh lệch quan sát lệch khỏi dự đoán ở §4 quá 0.05, ghi là phát hiện cần giải thích, không sửa dự đoán.

## 6. Power (lập kế hoạch)

Mô phỏng 150 study bằng **mô hình đơn giản hóa** (không phải code thật; cùng cơ chế chọn và leakage, bootstrap 600 lần): với 30 task, power khoảng 0.96 cho H-J1 và 0.99 cho H-J2; với 60 task, khoảng 1.00 cho cả hai. Chọn 60 task để H-J3 và H-J4 (hiệu ứng nhỏ) có độ chính xác hợp lý, chứ không phải vì H-J1 hay H-J2 cần. Đây là ước lượng lập kế hoạch, không phải kết quả.

## 7. Triển khai

- Script mới `src/run_label_quality_test.py`, tái dùng `build_fault_map`, `evidence`, `verification_decision` và `outcome_correct` hiện có; **không sửa** file của các study cũ.
- Test đơn vị **trước** khi chạy thật: với `r = 1, φ = 0` provenance không bao giờ chọn tool chung; với `r = 0, φ = 1` luôn chọn tool chung (vì hai tool độc lập bị loại); tỷ lệ chọn trên 20.000 lần rút tổng hợp khớp §4 trong sai số 0.01; regime `clean` cho unsafe 0.
- Script phân tích `src/analyze_label_quality_test.py`, output vào thư mục mới.
- Chạy hai lần; raw phải byte-identical.

## 8. Nhật ký khóa và amendment

| Ngày | Sự kiện | Ghi chú |
|---|---|---|
| 2026-10-11 | Protocol v1.0 được viết | Chờ tác giả xác nhận; chưa có code, task hay episode nào |
| 2026-10-12 | Tác giả xác nhận protocol v1.0 | Khóa hypothesis, điều kiện, cỡ mẫu, dự đoán và quy tắc quyết định; chưa có code, task hay episode nào |
| 2026-10-12 | Task split đóng băng trước khi viết runner | `data/tasks_label_quality_60.json`, SHA-256 `9a68d765657f068aacf70635e0a7a9584b7aa4194eea9e5fc42ea83eb4543eb8`; manifest `data/tasks_label_quality_60.manifest.json`. Kiểm tra trước khi chạy (§3.1) đều đạt: 120 instance cũ không đổi; escalate 40, refund 20 (đúng 2/3); 10 task mỗi difficulty; 0 task trùng các file task cũ; sinh lại cho hash giống hệt. Upstream clone mới ở commit `d0ee54aa`, Python 3.12.3 venv mới. |
| 2026-10-12 | **Amendment A1 — sửa dự đoán H-J4 trước khi chạy** | Test đơn vị (§7) phát hiện dự đoán §4 cho `survey_calibrated` được tính bằng hàm cho phép **nhãn của primary cũng thiếu** (xác suất 1 − k), trái với thiết kế §3.3 (nhãn primary luôn đúng). Giữ nguyên thiết kế §3.3 (nhất quán với ba điều kiện kia) và sửa dự đoán: P(chọn tool chung) 0.250 → 0.182; unsafe provenance 0.217 → 0.176; chênh lệch −0.050 → −0.091. Hướng của H-J4 và quy tắc quyết định không đổi; ba điều kiện còn lại không bị ảnh hưởng. Quyết định trước khi có bất kỳ decision row nào; số cũ được giữ (gạch ngang) trong bảng §4. |

## Liên quan

- [[journal/2026-10-06-prior-art-refresh-vp-control-and-efd]]
- [[journal/2026-10-09-real-tool-metadata-survey-results]]
- [[synthesis/Protocol: Real-Tool Failure-Domain Metadata Survey]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
