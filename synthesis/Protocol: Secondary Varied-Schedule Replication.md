---
title: >-
  Protocol: Secondary Varied-Schedule Replication
category: synthesis
tags: [research-protocol, experiment, verification, reproducibility, external-validity]
sources:
  - "synthesis/Protocol Amendment: Exploratory Secondary Runtime Matrix.md"
  - "journal/2026-09-28-secondary-exploratory-matrix.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/secondary_schema_contract_v1.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/validate_secondary_schema_contract.py"
  - "projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger.md"
summary: >-
  Protocol prospective cho replication nội bộ: lịch chọn nguồn và fault placement thay đổi theo case, giữ matched K=2 và phân tích safety riêng với utility.
provenance:
  extracted: 0.34
  inferred: 0.62
  ambiguous: 0.04
base_confidence: 0.59
lifecycle: draft
lifecycle_changed: 2026-09-28
tier: supporting
created: 2026-09-28T14:13:02+07:00
updated: 2026-09-28T14:13:02+07:00
---

# Protocol — Replication với lịch lỗi thay đổi theo case

> [!important] **ĐÃ CHẠY — EXPLORATORY INTERNAL REPLICATION.** Protocol được ghi sau khi đã xem secondary exploratory matrix 704 rows; varied schedule được hash/freeze trước runtime mới. Đây là kiểm tra độ nhạy nội bộ đối với lịch gây lỗi/chọn nguồn, không phải confirmatory study độc lập hoặc external validation. Giữ nguyên raw results và protocol trước đó.

## 1. Lý do và câu hỏi kiểm tra

Secondary matrix cũ cho cùng chênh lệch unsafe rate `−0.375` ở cả tám safety cases, do lịch fault và random-source selection dùng chung vị trí seed. Bootstrap CI `[-0.375,-0.375]` vì vậy suy biến. [[journal/2026-09-28-secondary-exploratory-matrix]]

**Câu hỏi của replication:** Khi mỗi case có lịch chọn corroborator và fault leakage riêng được tạo trước kết quả, lợi thế của `provenance_k` so với `random_k` còn xuất hiện hay không, và safety–utility trade-off thay đổi thế nào?

Đây là stress test cho **schedule dependence**. Nó không giải quyết việc case được chọn có chủ đích, P/S/I và failure-domain topology do project bổ sung, hoặc thiếu human case-level audit.

## 2. Cohort cố định

- Safety denominator giữ đúng tám cases: `WB-000`, `WB-110`, `WB-203`, `WB-433`, `ASB-085`, `ASB-087`, `ASB-090`, `ASB-977`.
- Utility-only diagnostic giữ `WB-403` và `ASB-1572`; không đưa vào unsafe denominator.
- `WB-295` chỉ chạy restoration diagnostic riêng, ngoài mọi aggregate safety/utility chính.
- `ASB-267` giữ `INVALID_NOT_RUN`.
- Giữ nguyên contract `1.2-recheck-candidate`, typed actions, canonical state, source payloads và post-state oracles. Không thêm case hoặc đổi eligibility sau khi xem result.

## 3. Ma trận và ngân sách

- 12 seeds mới, theo thứ tự: `1901, 1993, 2017, 2081, 2143, 2213, 2281, 2347, 2411, 2477, 2551, 2617`.
- Bốn regimes: `clean`, `independent_single_source`, `targeted_common_mode_0`, `targeted_common_mode_25`.
- Hai matched policies: `random_k`, `provenance_k`.
- 11 runnable cases × 12 seeds × 4 regimes × 2 policies = **1,056 rows / 528 matched pairs**; primary safety analysis chỉ dùng tám safety cases. `WB-295` có 96 diagnostic rows riêng trong tổng 1,056.
- Mỗi matched policy có đúng một primary decisive call và một corroborator (`K=2`). `WB-433` có thêm một shared non-decisive context call giống nhau ở hai policies và phải báo total calls riêng.

## 4. Lịch xác định trước, thay đổi theo case

Tạo SHA-256 trên UTF-8 string `secondary-varied-v1|<case_id>|<seed>|<purpose>`, với ba `purpose` tách biệt: `selector`, `leakage`, `single_fault`. Với mỗi cặp `(case_id, purpose)`, xếp 12 seeds theo `(digest_hex, seed)` tăng dần. Thuật toán không đọc action outcome, oracle result hoặc comparative metric.

- **`selector`:** sáu seeds đầu chọn `S` cho `random_k`, sáu seeds còn lại chọn `I`. `provenance_k` luôn chọn `I` theo accurate failure-domain metadata. Như vậy `random_k` cân bằng 6/12 cùng domain ở mỗi case, nhưng vị trí seed thay đổi theo case.
- **`leakage`:** ba seeds đầu trong thứ tự riêng được gán `I` leakage ở `targeted_common_mode_25`; chín seeds còn lại chỉ fault `P/S`. Tỷ lệ leakage là đúng 3/12 ở mỗi case và overlap giữa leakage với selector không bị chỉnh tay.
- **`single_fault`:** bốn seeds đầu fault `P`, bốn tiếp theo fault `S`, bốn cuối fault `I` trong `independent_single_source`.
- **`clean`:** không fault nguồn nào; **`targeted_common_mode_0`:** fault `P/S` ở mọi seed.

Trong cùng `(case_id, seed, regime)` pair, hai policies phải nhận cùng fault map, P observation, proposed action, canonical initial state và shared context. Chỉ cách chọn corroborator được khác. Proposal rule giữ nguyên secondary contract: safety case dùng `fault_action_typed` khi P bị fault; utility-only case giữ `clean_action_typed`.

Trước khi chạy action executor, xuất toàn bộ row keys, selector/fault schedules và SHA-256 manifest sang artifact riêng; kiểm tra hash rồi mới chạy episodes. Nếu schedule không thay đổi giữa ít nhất hai safety cases, dừng và sửa thuật toán trước khi xem outcomes. Không điều chỉnh seeds hoặc schedule sau khi xem comparative result.

## 5. Baselines và kết quả cần đo

**Primary comparison:** `provenance_k − random_k` trên unsafe accepted-action rate ở tám safety cases dưới `targeted_common_mode_25`, cùng `K=2`.

**Negative/control checks:** clean exact correctness, clean false blocks, independent-single-source regime, matched evidence calls, action-boundary coverage, paired fault-map equality và post-state oracle validity.

**Utility:** task success và false-block rate báo riêng cho safety cases và hai utility-only cases. Hành động sai bị chặn không được tính là task hoàn thành.

**`always-block` diagnostic:** tính riêng trên cùng proposed actions để cho thấy unsafe rate bằng zero đổi lấy bao nhiêu clean-task/utility loss. Baseline này không thuộc primary matched-`K=2` comparison và không được dùng để claim hiệu quả về tool-call cost.

## 6. Phân tích đã định trước

1. Tính numerator/denominator theo từng case, policy và regime; tính chênh lệch paired theo case.
2. Báo mean unweighted trên tám safety cases, median, số cases có cải thiện và leave-one-case-out range. Episodes/seeds là repeated schedules, không phải tám lần số mẫu độc lập.
3. Nếu báo 95% case-cluster bootstrap CI, dùng 10.000 resamples với analysis seed `20260928` và ghi rõ cohort nhỏ/purposive. CI không đại diện population-level generalization.
4. Báo bảng overlap giữa `selector=S` và `I leakage` của từng case để giải thích effect; không ẩn mechanism do lịch tạo ra.
5. Báo clean correctness, utility-only false blocks, task success, unsafe actions, total/decisive calls và execution errors riêng. Không gộp safety và utility thành một điểm số tự chọn sau kết quả.

**Diễn giải:** Nếu case-level effects vẫn giống hệt nhau, hạn chế schedule chưa được giải quyết. Nếu effect giảm mạnh hoặc đổi dấu trên nhiều cases, paper phải thu hẹp secondary claim. Nếu effect vẫn âm nhưng utility loss lớn, kết luận phải nêu trade-off. Mọi kết quả vẫn mang nhãn `EXPLORATORY INTERNAL REPLICATION`.

## 7. Reproducibility và stop rules

- Xác minh upstream `ProvenanceGuard@3ad7141db44096e1440718618bdb24fa46c003ff` và historical `WorkBench@00670510c8a476acd247925cefb17fee88500737`, cùng source hashes trong contract. Không dùng bản upstream mới thay thế âm thầm.
- Giữ nguyên `results_secondary_matrix/`; lưu outputs mới trong `results_secondary_varied/` với manifest, schedule hash, raw rows, analysis và runner version.
- Dừng nếu source hashes lệch, thiếu một matched pair, payload rò rỉ oracle/failure-domain fields, wrong action không được executor chấp nhận như contract mô tả, `K=2` sai, hoặc `WB-433` context không khớp.
- Một lỗi runtime cần được lưu nguyên trạng; mọi sửa chữa phải có amendment trước rerun và không được xóa kết quả trước đó.
- Offline CPU; không yêu cầu API, GPU hoặc model training. RTX 4060 live-agent feasibility là gate riêng sau replication.

## 8. Trạng thái và liên kết

**Kết quả đã ghi:** 1.056 rows / 528 matched pairs chạy hai lần byte-identical. `targeted_common_mode_25`: unsafe accepted actions `59/96` với `random_k` và `24/96` với `provenance_k`; mean paired case difference `−0.3646` trên tám case, khác biệt theo case `−0.250` đến `−0.417`, case-cluster bootstrap percentile 95% CI `[-0.396,-0.323]`. Đây là kết quả mô tả nội bộ trên tám case purposive, không phải CI quần thể hay external validation. Utility-only false blocks ở targeted 25% là `9/24` và `18/24`; safety task success là `0/96` cho cả hai vì gate không phục hồi action.

Artifacts, schedule hash, per-case counts, negative controls và limitations nằm tại [[journal/2026-09-28-secondary-varied-schedule-replication]]. Contract còn trạng thái `1.2-recheck-candidate`; chưa có human review. Ma trận cũ vẫn giữ nguyên ở `results_secondary_matrix/`. Supervisor feedback về RQ/methodology có thể tiếp tục làm rõ framing; không được nâng exploratory result thành confirmatory evidence.

- [[synthesis/Protocol Amendment: Exploratory Secondary Runtime Matrix]] — protocol và kết quả tiền nhiệm.
- [[journal/2026-09-28-secondary-exploratory-matrix]] — lý do phải thay schedule.
- [[journal/2026-09-28-secondary-varied-schedule-replication]] — varied-schedule result, pair-level outputs và giới hạn diễn giải.
- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]] — living manuscript.
