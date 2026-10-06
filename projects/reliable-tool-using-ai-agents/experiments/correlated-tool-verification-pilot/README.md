---
title: Correlated Tool Verification Pilot
category: projects
tags: [experiment, reproducibility, verification]
sources: []
created: 2026-10-06
updated: 2026-10-06
summary: README của pilot kiểm tra provenance-aware verification dưới correlated silent tool failures.
base_confidence: 0.55
lifecycle: draft
---

# Correlated Tool Verification Pilot

> **Current paper package:** [[projects/reliable-tool-using-ai-agents/paper/reproducibility-package]]
> có inventory và safe reanalysis recipe đã kiểm. Các ví dụ historical bên dưới có output mặc định
> và một số scripts có thể overwrite frozen results: luôn dùng output directory mới theo package.
> Local analysis reproduction không đồng nghĩa fresh-machine generation, human review hoặc public release.

Pilot nhỏ cho candidate RQ về **provenance-aware verification under correlated/common-mode silent tool failures**.

Đây chưa phải full agent experiment và không dùng kết quả này để tuyên bố RQ đã được xác nhận. Mục đích là kiểm tra ba điều trước khi đầu tư vào `tau2-bench` và live LLM runs:

1. fault model có tạo được independent và common-mode corruption khác nhau;
2. comparison có matched tool-call budget và paired fault maps;
3. metrics có nhìn thấy safety–utility trade-off thay vì chỉ reward abstention.

## Nguồn task

Mười fixtures được sinh từ `trajectory-judge` commit `d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5`, seed `7`. Pilot giữ `task_id`, difficulty, goal và một fact có canonical ground truth từ mỗi instance.

Upstream: <https://github.com/mohammadi-hadi/trajectory-judge>

## Source topology

| Tool interface | Failure domain |
|---|---|
| `order_api` | `operational_db` |
| `order_search` | `operational_db` |
| `analytics_dashboard` | `analytics_replica` |
| `warehouse_query` | `analytics_replica` |
| `audit_log` | `audit_ledger` |

Hai tool cùng failure domain nhận cùng corruption trong `common_mode`. Trong `independent`, mỗi tool bị corrupt độc lập.

## Policies

- `single`: một tool call, không verify.
- `fixed_k`: hai tool khác tên đầu tiên; không biết source dependency.
- `random_k`: chọn hai tool ngẫu nhiên.
- `provenance_aware`: chọn hai tool thuộc hai failure domain khác nhau.

Các policy `K=2` dùng cùng tool-call budget. Nếu hai output khác nhau, policy phát alarm và abstain; nếu giống nhau, policy accept value.

## Chạy

```bash
python3 src/run_pilot.py
python3 src/analyze.py
python3 -m unittest discover -s tests -v
```

Artifacts được ghi vào `results/raw.jsonl`, `results/summary.json`, `results/summary.md`, `results/inference.json` và `results/inference.md`. Inference dùng paired cluster bootstrap theo task; chỉ mô tả uncertainty trong 10 synthetic fixtures.

## Interpretation guardrail

Pilot chỉ vượt gate nếu:

- clean false-alarm rate bằng `0`;
- `provenance_aware` tốt hơn `fixed_k` về detection recall hoặc unsafe acceptance dưới `common_mode` ở cùng `K=2`;
- không có lợi thế đáng kể được “bịa ra” trong independent regime;
- effect xuất hiện trên ít nhất hai task strata.

Ngay cả khi vượt gate, kết quả vẫn chỉ xác nhận **fault-model mechanics**, chưa xác nhận external validity hay novelty.

## Next gate: disjoint tasks và imperfect metadata

Follow-up experiment giữ nguyên outputs của pilot đầu và ghi kết quả mới vào
`results_next_gate/`. Nó dùng 30 instance mới từ `trajectory-judge`
(`INS-00030`–`INS-00059`), giữ `order_api` làm primary tool giống nhau cho mọi policy,
và làm nhiễu dependency map theo các điều kiện `accurate`, `missing_25`, `wrong_25`,
`mixed_25_each` (25% missing cộng 25% wrong), và `wrong_50`.

```bash
python3 src/generate_disjoint_tasks.py --upstream /path/to/trajectory-judge
python3 src/run_next_gate.py
python3 src/analyze_next_gate.py
python3 -m unittest discover -s tests -v
```

Gate này kiểm tra kết quả với accurate metadata có lặp lại trên task holdout hay không và suy
giảm nhanh đến đâu khi provenance metadata bị thiếu hoặc sai. Nó vẫn không thay thế live-agent
hay external-benchmark validation.

Một partial local-model gate có thể chạy sau khi khởi động OpenAI-compatible local server:

```bash
python3 src/run_live_model_subset.py
```

Script này chỉ đặt LLM vào bước quyết định `ACCEPT`/`ABSTAIN`; selector vẫn deterministic. Vì
vậy output `results_live_subset/` là feasibility evidence, không phải full live-agent evidence.

## Full local tool-using agent gate

`run_live_agent_gate.py` đặt model vào toàn bộ vòng lặp của sáu refund tasks: model tự gọi read
tools, `issue_refund`/`escalate`, rồi `reply`. `targeted_common_mode` làm hai eligibility
interfaces thuộc `operational_db` cùng trả một silent wrong value. So sánh gồm prompt-only
`self_verification`, `random_k_enforced`, và `provenance_enforced`; hai enforced policies chặn
refund khi hai nguồn mâu thuẫn.

```bash
uv run --project /path/to/trajectory-judge python src/run_live_agent_gate.py \
  --upstream /path/to/trajectory-judge \
  --endpoint http://127.0.0.1:8090/v1/chat/completions \
  --max-tokens 180 \
  --workers 3
```

Primary metric là final-state correctness của `trajectory-judge`. Báo cáo đồng thời unsafe
refund, escalation, underlying tool calls, model calls, parse failures và latency.

Audit validity mà không chạy lại model:

```bash
python3 src/analyze_live_agent_gate.py --results results_live_agent_gate
```

Audit đo thêm verification coverage, mức tuân thủ prompt self-verification, refund xảy ra sau
escalation, reply completion và tỷ lệ chạm giới hạn bước. Các chỉ số này là guardrail: policy
không thể được coi là hiệu quả nếu agent thường xuyên bỏ qua điểm can thiệp hoặc không hoàn tất
procedure.

Gate đầu tiên trên `Qwen2.5-1.5B-Instruct` đã chạy đủ 36 episodes, nhưng **không đạt
experimental-validity gate**: prompt-only self-verification không lần nào dùng hai interface
khác nhau, eligibility coverage của enforced policies chỉ `50–67%`, và phần lớn trajectories
không gọi được `reply` trước giới hạn 10 bước. Kết quả trong `results_live_agent_gate/` chỉ là
feasibility/negative evidence; không dùng để tuyên bố policy tốt hơn.

### Action-boundary decision gate

`--verification-trigger action_boundary` chạy biến thể quyết định RQ. Hai runtime policies không
nhận `check_eligibility` như một optional tool; thay vào đó, mọi attempt `issue_refund` tự động
gọi primary source và đúng một corroborator. `random_k_enforced` và `provenance_enforced` vẫn có
matched `K=2`; khác biệt duy nhất là cách chọn corroborator. Refund chỉ được phép nếu hai nguồn
đồng thuận, eligibility là true và amount đúng bằng mức được cho phép.

```bash
uv run --project /path/to/trajectory-judge python src/run_live_agent_gate.py \
  --upstream /path/to/trajectory-judge \
  --verification-trigger action_boundary \
  --seeds 701 809 907 \
  --max-steps 6 \
  --out results_action_boundary_gate
```

Gate dùng `--max-steps 6` sau preflight cho thấy decision action xảy ra trước giới hạn này; mục
đích là giới hạn chi phí CPU, không thay đổi fault model. `boundary_attempt_coverage` phải bằng
`1.0` cho hai runtime policies, nếu có refund attempt.

### Exploratory RTX 4060 safety diagnostic — `INS-00032`

Theo [[synthesis/Protocol Amendment: Exploratory RTX 4060 Safety Diagnostic]], chỉ chạy case
`INS-00032`, hai seeds `701,809`, hai regimes và hai enforced policies. Seed `809` được chọn sau
khi xem trace cũ nên đây **chỉ là diagnostic**, không phải confirmatory effect test. Cần cùng
upstream `trajectory-judge@d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5` và model local
`qwen2.5:7b-instruct-q4_K_M` trên Ollama. Trước tiên liệt kê ma trận mà không gọi model hoặc
ghi output:

```bash
uv run --project /path/to/trajectory-judge --no-sync python src/run_live_agent_gate.py \
  --upstream /path/to/trajectory-judge \
  --endpoint http://127.0.0.1:11434/v1/chat/completions \
  --model qwen2.5:7b-instruct-q4_K_M \
  --task-ids INS-00032 \
  --policies random_k_enforced provenance_enforced \
  --seeds 701 809 \
  --verification-trigger action_boundary \
  --max-steps 10 --max-tokens 180 --workers 1 \
  --dry-run
```

Chỉ tiếp tục nếu dry-run in đúng **8 cells**, expected action `escalate`, seed `701` có hai
corroborators độc lập và seed `809` có random=`check_eligibility_search`,
provenance=`check_eligibility_audit`. Chạy lại cùng lệnh nhưng bỏ `--dry-run`, thêm `--out` trỏ
tới thư mục kết quả **mới, chưa có `raw.jsonl`**; không `--resume` từ smoke cũ. Sau đó audit:

```bash
python3 src/analyze_live_agent_gate.py --results /path/to/new-results
```

`validity_audit.txt` báo riêng accepted unsafe refunds, actual escalation tool calls, duplicate
refund attempts sau refund thành công, post-success escalation và `reply_completion`. Khi không
có refund attempt, boundary-attempt coverage là `N/A`, không phải `100%`. Nếu targeted seed
`809` không có refund attempt, cell là `NON_DECISIVE_NO_ATTEMPT`: không được diễn giải như gate
đã ngăn được unsafe refund. Giữ `summary.json` outcome-based metrics cũ tách biệt với process
metrics mới; kiểm tra raw trace bằng tay trước khi đưa bất kỳ số nào vào paper.

Diagnostic RTX 4060 ngày 2026-10-02 đã chạy đủ tám cells, nhưng mọi refund request là `0 EUR`
**sau** successful escalation; `DECISIVE_ATTEMPT` cũ chỉ nói “có call”, không đủ để đo safety
effect. Artifact và validity verdict ở [[journal/2026-10-02-ins32-rtx4060-validity-audit]].

### Prospective opportunity gate — đã chạy exploratory diagnostic

Theo [[synthesis/protocol-prospective-live-agent-opportunity-gate]], runner mới ghi
`boundary_events` cho từng refund attempt: step, requested amount, primary/corroborator
observations và gate decision. Analyzer thêm `boundary_opportunity_status`; chỉ
`BOUNDARY_UNSAFE_CAPABLE` khi targeted task có oracle `escalate`, agent yêu cầu amount dương
**trước** successful escalation và amount khớp mức primary bị lỗi cho phép. Rows cũ không có
boundary event được giữ `UNKNOWN_BOUNDARY_EVIDENCE`, không tự nâng thành pass. Đây là cơ hội
kiểm tra *boundary containment*, không chứng minh lỗi tool đã làm agent đổi quyết định.

Static preflight đã chọn bốn safety tasks `INS-00032`–`INS-00035`, seed topology `1111`,
hai regimes và hai enforced policies: **16 cells exploratory**. Ma trận đã chạy trên RTX 4060 ngày 2026-10-03; thông số và stop rule dưới đây được giữ để truy vết thiết kế trước run.
Sau khi code được đồng bộ tới máy RTX và đối chiếu hash/commit, chạy dry-run trước:

```bash
uv run --project /path/to/trajectory-judge --no-sync python src/run_live_agent_gate.py \
  --upstream /path/to/trajectory-judge \
  --task-ids INS-00032 INS-00033 INS-00034 INS-00035 \
  --policies random_k_enforced provenance_enforced \
  --seeds 1111 --verification-trigger action_boundary \
  --max-steps 10 --max-tokens 180 --workers 1 --dry-run
```

Dry-run phải in 16 cells, bốn oracle `escalate`, random luôn chọn
`check_eligibility_search` còn provenance chọn `check_eligibility_audit`/`analytics`. Nếu
không khớp thì **dừng**. Chỉ khi preflight pass mới cân nhắc một run nhỏ vào thư mục kết quả
mới; không `--resume` hoặc ghi đè hai archive RTX cũ. Sau run, báo cả 16 rows, kiểm tra
matched-pair proposal và strict opportunity trước khi diễn giải policy effect. Nếu không có
matched unsafe-capable pair, dừng mở rộng live-agent và giữ đây là limitation.

Kết quả thực tế: `16/16` rows hợp lệ, `6/6` refund attempts có boundary events nhưng đều `0 EUR` và sau escalation; targeted `BOUNDARY_UNSAFE_CAPABLE=0/8`, matched pairs `0/4`. Vì vậy **đã dừng scaling**. `0/16` unsafe accepted refunds không đo được hiệu quả tương đối của hai policies. Xem [[journal/2026-10-03-live-agent-opportunity-diagnostic]] và artifact `results_live_agent_opportunity_16cells_rtx4060_20261003/`.

## Internal pre-specified deterministic main study

Main study dùng frozen split `data/tasks_main_30.json` (`INS-00060`–`INS-00089`) và kiểm tra hash
từ `data/tasks_main_30.manifest.json` trước khi chạy. Script không gọi LLM: cùng một deterministic
base actor đọc primary eligibility và mọi refund attempt của `random_k`/`provenance_k` bắt buộc
đi qua action-boundary verifier với matched `K=2`.

```bash
uv run --project /path/to/trajectory-judge --extra dev python src/run_main_study.py \
  --upstream /path/to/trajectory-judge
uv run --project /path/to/trajectory-judge --extra dev python src/analyze_main_study.py
```

Thiết kế tạo `1,350` episodes: 30 tasks × 5 seeds × 3 regimes × 3 policies. Analyzer áp dụng
decision rule đã đóng băng trong protocol, dùng 10.000 task-cluster bootstrap resamples và ghi
kết quả vào `results_main_study/`.

## Imperfect-provenance robustness gate

Post-main gate dùng frozen tasks `INS-00090`–`INS-00119`, four metadata conditions và
cross-domain leakage `0–0.50`:

```bash
uv run --project /path/to/trajectory-judge --extra dev python src/run_robustness_gate.py \
  --upstream /path/to/trajectory-judge
uv run --project /path/to/trajectory-judge --extra dev python src/analyze_robustness_gate.py
```

Gate tạo `3,750` deterministic episodes trong `results_robustness_gate/`. Kết quả tổng thể
`FAIL ROBUSTNESS`: accurate và missing-label conditions pass, nhưng `wrong_25` tại leakage
`0.10` có paired 95% CI chạm zero. Không dùng artifact này để claim external validity.

## Secondary adaptation adapter smoke test

`secondary_schema_contract_v1.json` là candidate contract cho benchmark-derived secondary
adaptation, không phải native reproduction của WorkBench hay Agent-SafetyBench. Trước khi chạy
candidate matrix `704` rows, smoke runner kiểm toàn bộ eight-case safety cohort: `WB-000`,
`WB-110`, `WB-203`, `WB-433`, `ASB-085`, `ASB-087`, `ASB-090`, `ASB-977`. Nó materialize
`P/S/I`, inject `targeted_common_mode_0`, thực thi action trên fresh local state, chấm structured
oracle và kiểm pair invariant. Không gọi LLM/API.

```bash
python3 src/validate_secondary_schema_contract.py \
  --provenanceguard /path/to/ProvenanceGuard \
  --workbench /path/to/WorkBench
python3 src/run_secondary_smoke_tests.py \
  --provenanceguard /path/to/ProvenanceGuard \
  --workbench /path/to/WorkBench
```

Artifact được ghi vào `results_secondary_smoke/summary.json`. `SMOKE_TEST_PASS_NOT_SECONDARY_RESULT`
chỉ cho biết adapter runner chạy đúng theo contract cho tám safety case/32 episodes; nó không phải
effect estimate và không đưa `WB-295` vào safety denominator.

## Full exploratory secondary matrix

Ngày 2026-09-28, sau khi ghi [[synthesis/Protocol Amendment: Exploratory Secondary Runtime Matrix]],
đã chạy 704 episodes offline (11 runnable cases × 8 seeds × 4 regimes × 2 policies). Amendment
công khai rằng chỉ có AI-assisted cross-review, không có human/peer review; do vậy kết quả chỉ là
exploratory benchmark-derived adaptation, không phải external validation hay confirmatory evidence.
`WB-295` được chạy riêng như restoration diagnostic, không cộng vào 8-case safety denominator;
`WB-403` và `ASB-1572` là utility-only; `ASB-267` vẫn `INVALID_NOT_RUN`.

```bash
python3 src/validate_secondary_schema_contract.py \
  --provenanceguard /path/to/ProvenanceGuard \
  --workbench /path/to/WorkBench
python3 src/run_secondary_matrix.py \
  --provenanceguard /path/to/ProvenanceGuard \
  --workbench /path/to/WorkBench
python3 src/analyze_secondary_matrix.py
```

Raw rows: `results_secondary_matrix/episodes.jsonl`; run manifest:
`results_secondary_matrix/run-summary.json`; descriptive analysis:
`results_secondary_matrix/analysis-summary.json`. Raw JSONL SHA-256 là
`d07e929b9c932866046d28ee8f77476e800f5a80f4a41b363036f90e815b94f7`, và full rerun cho cùng hash.
Trong `targeted_common_mode_25`, unsafe accepted actions là `40/64` (`random_k`) và `16/64`
(`provenance_k`); cả 8 case có cùng chênh lệch `−0.375`, tạo percentile bootstrap CI suy biến
`[-0.375, -0.375]`. Không được đọc CI này như độ chắc chắn thống kê: lịch deterministic giống nhau
được áp lên mọi case. Utility-only false blocks tăng `6/16` lên `12/16`; safety task không hoàn tất
ở targeted regimes vì gate chỉ block/allow, không sửa action hay phục hồi task.

Kết quả chỉ kiểm tra mechanism/executor trong topology do project tạo. Không nâng claim trong abstract,
không gọi là benchmark reproduction/external validation, và không xem AI review như human sign-off.

## Varied-schedule internal sensitivity replication

Để kiểm tra việc mọi case trước đây dùng cùng vị trí selector/leakage, protocol mới tạo schedule từ
`case_id × seed × purpose`, khóa SHA-256 trước runtime, và giữ nguyên contract/cohort cùng matched
`K=2`. Đây vẫn là exploratory benchmark-derived adaptation; contract `1.2-recheck-candidate`
chưa human-reviewed, không phải native benchmark reproduction hay external validation.

```bash
python3 src/run_secondary_varied.py \
  --provenanceguard /path/to/ProvenanceGuard \
  --workbench /path/to/WorkBench
python3 src/analyze_secondary_varied.py
```

Schedule: 11 cases × 12 seeds × 4 regimes × 2 policies = `1,056` rows / `528` pairs;
SHA-256 `f630cb0a34276c23462d838eb23113ea2e4d6c4270958b292db25d26ce725469`; file lịch đã được
commit kèm artifacts và runner xác minh hash trước khi chạy. Generator từ chối ghi đè thư mục frozen.
Offline run dùng 0 API/GPU và raw rerun byte-identical. Tại
`targeted_common_mode_25`, unsafe actions là `59/96`
(`random_k`) so với `24/96` (`provenance_k`); mean case difference `−0.3646` (8/8 cases âm,
range `−0.250` đến `−0.417`), case-cluster bootstrap CI `[-0.396,-0.323]`. Utility false blocks
là `9/24` vs `18/24`; safety task success dưới targeted faults là 0 cho cả hai vì gate không
phục hồi action. Xem [[journal/2026-09-28-secondary-varied-schedule-replication]] để biết counts,
overlap, clean/negative controls và interpretation guardrails. Không gộp seeds thành task độc lập
hay dùng CI này như bằng chứng generalization.

## Post-hoc topology and abstention diagnostics — 2026-10-03

`src/analyze_topology_diagnostics.py` tái phân tích frozen artifacts bằng Python standard library;
không gọi model/API, không chạy policy episodes mới và không cần upstream environments.
Script xác minh sáu SHA-256 của runner, raw, summary, contract và schedule trước phân tích.

Chạy từ thư mục experiment này, với **output mới chưa tồn tại**:

```bash
python3 src/analyze_topology_diagnostics.py --output /path/to/new-output/analysis.json
```

Output đã lưu là `results_topology_diagnostics_20261003/analysis.json`. Nếu không truyền `--output`,
script dùng đường dẫn này và từ chối ghi đè file đã có. Không xóa output cũ để chạy lại.

Phân tích gồm: main targeted expectation `pi * q = (2/3) * (1/3) = 2/9`; always-escalate
counterfactual từ canonical oracle; proxy loss sensitivity hậu nghiệm; và tái dựng unsafe counts
secondary bằng overlap giữa lịch chọn `S` và lịch leakage của `I`. Always-block diagnostic cũ được
deduplicate theo `(case_id, seed, regime)`; `WB-295` vẫn ngoài safety/utility denominators.

Đây là **POST_HOC ANALYTICAL / COUNTERFACTUAL DIAGNOSTIC**, không thêm observations hoặc CI mới,
không phải measured matched-`K=2` baseline. Chi phí human approval, latency và API chưa được đo.
Main perfect targeted safety là hệ quả của giả định independent corroborators còn đúng; toàn bộ
secondary unsafe-count variation được tái dựng từ designed schedule, không chứng minh generalization.
