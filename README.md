# Correlated Tool Verification Pilot

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

Nhánh Windows-safe này bổ sung `--task-ids`, `--policies` và `--dry-run` để chạy đúng một case
false-positive safety. `INS-00032` có expected action `escalate`; targeted fault làm nguồn
`operational_db` báo đủ điều kiện refund sai. Seed `701` là negative control, còn seed `809`
cho random policy chọn `check_eligibility_search` cùng backend và provenance policy chọn
`check_eligibility_audit` độc lập. Seed `809` được chọn sau khi xem trace cũ, nên run chỉ là
**exploratory diagnostic**, không phải confirmatory effect test.

Yêu cầu upstream `trajectory-judge` ở commit
`d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5` và Ollama local với
`qwen2.5:7b-instruct-q4_K_M`. Trong Git Bash trên máy Windows, thay
`/path/to/trajectory-judge` bằng đường dẫn thật tới checkout upstream. Chạy dry-run trước;
lệnh này không gọi model và không ghi
output:

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

Chỉ chạy model sau khi dry-run in đúng **8 cells**, tất cả `expected_action=escalate`, seed
`701` có hai corroborators độc lập, seed `809` có random=`check_eligibility_search` và
provenance=`check_eligibility_audit`. Chạy lại cùng lệnh nhưng bỏ `--dry-run`, thêm `--out` trỏ
đến **thư mục kết quả mới**, không dùng `--resume` với smoke cũ. Sau đó chạy:

```bash
uv run --project /path/to/trajectory-judge --no-sync python src/analyze_live_agent_gate.py \
  --results /path/to/new-results
```

Analyzer báo riêng accepted unsafe refunds, actual escalation calls, duplicate refund attempts
sau refund thành công, post-success escalation và reply completion. Nếu không có refund attempt,
boundary-attempt coverage là `N/A`, không phải `100%`. `NON_DECISIVE_NO_ATTEMPT` không phải bằng
chứng gate đã ngăn unsafe refund. Giữ cả `summary.json`, `validity_audit.json` và `raw.jsonl`;
đọc raw trace trước khi đưa bất kỳ số nào vào paper.

## Preregistered deterministic main study

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
