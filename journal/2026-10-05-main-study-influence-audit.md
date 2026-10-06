---
title: "2026-10-05 — Kết quả main study có phụ thuộc một task, seed hoặc stratum?"
category: journal
tags: [research-log, evidence, research-methods, verification, reproducibility]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_main_study/raw.jsonl"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_main_study/inference.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_main_study.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_main_influence.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/tests/test_main_influence.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_main_influence_20261005/analysis.json"
  - "projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03.md"
  - "projects/reliable-tool-using-ai-agents/paper/artifact-inventory.json"
created: 2026-10-05T08:15:00+07:00
updated: 2026-10-05T08:15:00+07:00
summary: >-
  Loại lần lượt task/seed/stratum giữ targeted Δ âm; independent đổi dấu theo composition. Phân tích hậu nghiệm từ frozen raw, không CI hoặc samples mới.
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
base_confidence: 0.59
lifecycle: draft
lifecycle_changed: 2026-10-05
tier: supporting
---

# Mức giảm unsafe có bị một nhóm dữ liệu chi phối?

**FACT — POST_HOC DESCRIPTIVE SENSITIVITY:** Khi lần lượt loại một task, một seed hoặc một difficulty stratum khỏi frozen main data, chênh lệch targeted unsafe decision rate vẫn âm. Tất cả 41 subsets của targeted condition giữ chiều provenance ít unsafe hơn random. Independent-fault difference nhỏ và có thể đổi dấu khi loại một stratum. Đây là phân tích độ nhạy bằng loại từng nhóm (leave-one-group-out sensitivity), không chạy thêm agent hoặc policy episode.

**INFERENCE:** Kết quả targeted không dồn hoàn toàn vào một task, seed hoặc stratum đơn lẻ trong mẫu đã đo. Nhưng main fault model vốn bảo đảm provenance zero unsafe; giữ dấu âm chưa giải quyết hạn chế by construction, metadata reliability hoặc generalization. Đây là một kiểm tra mô tả liên quan reviewer finding R7, không đóng R7 hay thay human review.

## 1. Vì sao kiểm tra này cần thiết?

Main study có 1,350 rows, nhưng chỉ 30 task instances, năm seeds, ba regimes và ba policies. Riêng random-versus-provenance ở một regime có 150 matched task-seed pairs. Cùng task xuất hiện nhiều lần không tạo thành 150 tasks độc lập.

Nếu toàn bộ chênh lệch đến từ một nhóm nhỏ, headline trung bình có thể gây ấn tượng quá mạnh. Câu hỏi cụ thể trong lượt này là: **giữ các kết quả đã quan sát, nếu bỏ một đơn vị/nhóm khỏi phép tổng hợp thì mức chênh lệch còn bao nhiêu?** Đây là câu hỏi về ảnh hưởng của thành phần mẫu, không giả thuyết mới về hành vi agent. Nguồn định hướng: [[projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03]] R7; source code `paired_bootstrap` trong main analyzer.

## 2. Phép tính và phạm vi

Với mỗi task `t`, seed `s`, regime `r`:

`d(t,s,r) = unsafe(provenance_k) − unsafe(random_k)`.

Sau khi bỏ nhóm `g`, lấy tổng các `d` còn lại chia số matched pairs còn lại. Vì grid balanced, trung bình trên rows còn lại bằng trung bình các task means còn lại trong từng phép loại này. Phải giữ cặp policies, cùng primary và cùng task/seed; không loại riêng policy thua.

| Phép kiểm tra | Số lần mỗi regime | Task instances còn lại | Seeds còn lại | Matched pairs mỗi lần |
|---|---:|---:|---:|---:|
| Bỏ một task | 30 | 29 | 5 | 145 |
| Bỏ một seed | 5 | 30 | 4 | 120 |
| Bỏ một stratum | 6 | 25 | 5 | 125 |

Chạy cùng ba phép này cho clean, independent và targeted_common_mode: **123 phép tổng hợp subsets**, không phải 123 thí nghiệm độc lập. Đây là lựa chọn phân tích sau khi biết main result; các khoảng dưới đây là min–max quan sát được qua phép loại, **không phải confidence interval**. Không bootstrap, không p-value, không sửa main pass/fail criterion.

## 3. Kết quả

Đơn vị bảng là **điểm phần trăm (percentage points, pp)**; số âm nghĩa provenance ít unsafe hơn random. Headline targeted giữ `−20.00 pp` trên toàn mẫu.

| Regime | Toàn mẫu | Bỏ một task: min–max | Bỏ một seed: min–max | Bỏ một stratum: min–max |
|---|---:|---:|---:|---:|
| clean | 0.00 | 0.00 đến 0.00 | 0.00 đến 0.00 | 0.00 đến 0.00 |
| independent | +0.67 | 0.00 đến +1.38 | 0.00 đến +0.83 | −0.80 đến +1.60 |
| targeted_common_mode | −20.00 | −20.69 đến −17.93 | −22.50 đến −17.50 | −24.00 đến −16.00 |

**FACT:** Targeted giữ Δ < 0 trong 30/30 task deletions, 5/5 seed deletions, 6/6 stratum deletions. Năm seed groups đứng riêng có Δ lần lượt `−13.33`, `−20.00`, `−10.00`, `−30.00`, `−26.67 pp` với seeds `101,211,307,401,503`; đây là các nhóm của cùng frozen data, không năm independent task replications.

### Thành phần task giải thích một phần độ lớn

| Stratum bị bỏ | Δ riêng của stratum /25 pairs | Δ của 125 pairs còn lại |
|---|---:|---:|
| already_refunded | −20.00 pp | −20.00 pp |
| expired | −36.00 pp | −16.80 pp |
| happy | 0.00 pp | −24.00 pp |
| non_refundable | −24.00 pp | −19.20 pp |
| restocking | 0.00 pp | −24.00 pp |
| wrong_customer | −40.00 pp | −16.00 pp |

**FACT:** Hai strata `happy` và `restocking` là các expected-refund tasks. Targeted fault làm primary báo ineligible, actor không tạo proposal, nên cả hai policies không có unsafe refund decision ở các rows này. Loại một nhóm zero-effect làm unsafe-rate difference lớn hơn về trị tuyệt đối do mẫu số và thành phần task thay đổi. Nó không làm policy tự nhiên hoạt động tốt hơn. Xem cơ chế từng row trong [[projects/reliable-tool-using-ai-agents/paper/figure-guide]] §6.

**FACT — EVIDENCE BẤT LỢI ĐƯỢC GIỮ:** Trong independent regime, bỏ `non_refundable` làm Δ từ `+1/150` thành `−1/125`; bỏ `already_refunded` hoặc `wrong_customer` cho `+2/125`. Các thay đổi nhỏ này không thiết lập advantage mới. CI main đã lưu vẫn `[-0.020,0.033]`; wording tiếp tục là “no evidence of advantage in this study”.

## 4. Điều phép kiểm tra này không giải quyết

- Targeted provenance có zero unsafe ở từng row theo constructed topology. Vì vậy mọi subset đều có Δ ≤ 0; dấu âm không phải một phát hiện bất ngờ. Phép loại chỉ kiểm tra rằng random errors vẫn còn sau khi bỏ từng nhóm.
- Bỏ một stratum thay đổi tỷ trọng các loại task và đại lượng đang tổng hợp. Không diễn giải min–max thành uncertainty cho một production population chưa xác định.
- Cả 30 tasks cùng task generator và topology; deletion không cung cấp task, backend, fault distribution hoặc environment độc lập.
- Đây không phải stress test metadata. Wrong-label robustness vẫn **FAIL ROBUSTNESS** theo kết quả đã lưu.
- Clean zero differences không chứng minh population equality hoặc formal non-inferiority. Safety phải đọc cùng targeted correct refunds `0/50` ở cả hai policies.
- Không thay thế matched unsafe-capable opportunities còn thiếu ở live-agent diagnostic, không tạo lý do scale RTX trở lại.

**Wording được phép:** “Trong phân tích hậu nghiệm trên frozen main sample, targeted difference giữ âm khi lần lượt bỏ một task, seed hoặc difficulty stratum; độ lớn phụ thuộc task composition.”

**Wording không được phép:** “Đã chứng minh robust/generalizable”, “41 replications xác nhận hiệu quả”, “CI mới là −24 đến −16 pp”, hoặc “đã loại bỏ bias do task generator”.

## 5. Artifact, kiểm tra và tái lập

Artifact mới: `results_main_influence_20261005/analysis.json`. Nó lưu cả exact rational difference, numerator/denominator, từng nhóm bị bỏ, raw hash, source-script hash và giới hạn diễn giải. Thư mục này tách khỏi frozen study outputs.

- Raw SHA-256: `a51aebcb207f996e7a4d065b2e424fe794346d685d5f37a615d0de6bcb872234`.
- Script SHA-256: `b0f864406725214080d562705f9fb0670db9a4b516a457d991f6355a80a093e5`.
- Report SHA-256: `7e49c1bdbfa518c9a30a520494cb9612b05e850b31e818f201d3efeb8f433803`.
- 7/7 focused tests đạt: arithmetic với toy fixture, duplicate/missing cells, primary mismatch, metadata drift và row-order invariance.
- Đối chiếu riêng bằng SQLite: **123/123** retained differences/denominators khớp; ba full-sample estimates khớp stored inference.
- CLI từ chối existing output và sai input hash; tạo lại report trong thư mục tạm khớp byte-for-byte. Đây là cùng-host analysis replay, không independent reproduction.
- 21 frozen inventory hashes và main manuscript v0.9 giữ nguyên tại kiểm tra artifact; không sửa original CI hoặc decision.json. Không gọi model/API, không dùng GPU; phân tích chỉ cần Python standard library.

Từ experiment directory, mỗi lượt dùng output mới:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_main_influence.py' -v
task_influence_parent=$(mktemp -d)
python3 src/analyze_main_influence.py --out "$task_influence_parent/report"
```

## 6. Research log và quyết định tiếp theo

**Đã tra cứu:** hot cache, reviewer R7, main actor/analyzer, frozen raw/inference, task composition và current paper. Đây là phân tích artifact có sẵn; không mở literature search hoặc thêm source-paper claims.

**Đã học:** Targeted advantage có ở nhiều phần của sample, nhưng độ lớn thay đổi theo composition. Independent negative control vẫn yếu; evidence không cho phép nâng claim robustness hoặc applicability.

**Quyết định:** Giữ controlled course-paper scope và **SURVIVES WITH REFINEMENT — PRELIMINARY**. Đưa kết quả này vào supplementary material, giữ headline main study. Không tiếp tục tạo thêm sensitivity variants chỉ để có nhiều kết quả thuận lợi.

**Bước tiếp theo:** chuẩn bị một bản paper dễ đọc theo format học thuật thống nhất để tác giả/giảng viên đánh giá toàn bài; dùng [claim ledger](../projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger.md) giới hạn wording. Author readback và course-format confirmation vẫn mở; chưa có human sign-off.

Related: [[projects/reliable-tool-using-ai-agents/paper/supplementary-appendix]], [[projects/reliable-tool-using-ai-agents/paper/submission-readiness]], [[projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03]].
