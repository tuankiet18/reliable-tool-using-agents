---
title: >-
  ToolBench-X: Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability
category: references
tags: [paper, benchmark, ai-agents, tool-failure, reproducibility]
sources: [https://arxiv.org/abs/2606.25819, https://github.com/Foreverskyou/ToolBench-X, https://huggingface.co/datasets/Foreverskyou/ToolBench-X, https://console.groq.com/docs/openai, https://console.groq.com/docs/tool-use/overview, https://console.groq.com/docs/rate-limits, https://ai.google.dev/gemini-api/docs/openai, https://ai.google.dev/gemini-api/docs/rate-limits]
source_url: https://github.com/Foreverskyou/ToolBench-X
summary: >-
  Controlled fault modules chạy được, nhưng pilot phát hiện data không đồng đều, hard-coded branches, trace bị mất và throughput thấp. Chỉ nên dùng làm secondary stress test.
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
base_confidence: 0.95
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: supporting
created: 2026-09-10T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# ToolBench-X: Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability

> [!tldr] Đây là benchmark khả thi nhất trong các artifact đã kiểm tra: GitHub public, Hugging Face dataset và script local/API; nhưng không giải quyết novelty problem của broad recovery routing.

## Vấn đề và failure model

ToolBench-X tạo executable multi-step task với `Specification Drift`, `Invocation Error`, `Execution Failure`, `Output Drift` và `Cross-source Conflict`. Mỗi instance được thiết kế có ít nhất một recovery path như retry, fallback, verification hoặc cross-checking.

## Artifact và reproducibility

- GitHub public có agent, evaluation, generation/injection script và `requirements.txt`.
- Hugging Face dataset công khai khoảng 31.5 MB, gồm tool/tool-exception artifacts.
- README dùng `pip install -r requirements.txt`, API key và local runtime; có script chạy baseline/exception/hint với seed và giới hạn worker/round.
- Không cần GPU training cho baseline pilot; API model là yêu cầu thực tế chính.

## Pilot tái lập — 2026-09-11

**FACT:** Đã clone repository, cài đủ dependency vào thư mục cô lập và tải/extract `tasks.zip`, `tools.zip`, `tools_exception.zip` từ Hugging Face. `python -m venv` không chạy được vì Python hiện tại thiếu `ensurepip`; cài dependency với `pip --target .deps` là workaround cục bộ, không sửa hệ thống.

**FACT:** Dataset sau khi extract có 522 file cấu hình task (một file có thể chứa nhiều task) và 1,106 module Python cho exception tool. Một tập con 5 task có coverage `5/5` với `tools_exception`, tức runner map được từng task sang tool lỗi tương ứng.

**FACT:** Gọi trực tiếp `trim_blank_rows_sheet_a` trong `strict_no_hint_profile`, `FAIL_SEED=7` tạo `TimeoutError` ở ba lần gọi đầu tại failpoint `before_tool_logic`; lần thứ tư thành công. Event injection lưu `trace_id`, tên tool, failpoint, exception, `retryable`, attempt và profile. Điều này xác nhận lỗi tool được kiểm soát và tái lập được theo seed — không chỉ là mô tả trong README.

**FACT:** Đã chạy `run_evalscope_local_runtime.py` trên 5 task. Khi không có API key, runner dừng cả batch trước khi dispatch task do `OpenAIError`; đây là lỗi xử lý môi trường của runner. Với API key giả và endpoint loopback không có model, runner hoàn thành và sinh output/summary, nhưng `0/5` vì cả năm LLM request đều `Connection error.`; không có tool execution nào. **Không được xem `0/5` là chất lượng baseline.**

**FACT:** Internal agent có các trường `llm_trace`, `execution_rounds`, `complete_trajectory`, `tool_executions`, `policy_actions` và `openai_trajectory`. Tuy nhiên `evalscope_adapter/local_runtime.py` loại ba trường đầu khỏi raw result mặc định. Output clean trajectory vẫn được tạo, nhưng chưa đủ để kết luận rằng toàn bộ tín hiệu monitor cần cho nghiên cứu đã được lưu. ^[verified by local source inspection]

## Đánh giá sau pilot

- **Lỗi tool có xuất hiện?** Có, đã quan sát trực tiếp và có event có cấu trúc. Mẫu kiểm tra là failure retryable/kết thúc sau ba lần; không được suy diễn rằng mọi failure trong benchmark là persistent.
- **Trajectory có lưu được?** Có dạng `openai_trajectory`; rich trajectory được tạo nội bộ nhưng bị evaluator strip ở output mặc định. Cần kiểm tra lại với một lần chạy model thật, hoặc dùng wrapper chỉ-ghi để giữ field nội bộ.
- **Final success/failure có rõ?** Có: output có `success`, `error`, exact-match và aggregate summary. Trong chạy không-model, nhãn phản ánh lỗi kết nối LLM, không phản ánh năng lực giải task.
- **Chi phí API?** Pilot đã dùng endpoint loopback nên chi phí thực tế là US$0. Chưa thể ước lượng chi phí model thật từ artifact vì phụ thuộc model, prompt/token thực tế và retry; phải đo một pilot hợp lệ trước.
- **Lỗi môi trường?** Có hai điểm: README yêu cầu `config/.env.example` nhưng file đó không có trong repository; và thiếu API key làm runner crash batch thay vì ghi task-level failure.

## Pilot với Groq — 2026-09-12

**FACT:** Groq API nhận plain chat request. Với `openai/gpt-oss-20b`, forced function-call tối giản của ToolBench-X nhận HTTP 400 `tool_use_failed`; vì thế model này không vượt compatibility preflight mặc dù Groq documentation mô tả tool use.

**FACT:** `qwen/qwen3.6-27b` vượt forced function-call preflight. Tuy nhiên, 5-task baseline đầu tiên nhận HTTP 429 vì Groq Free tier giới hạn output tokens/phút là 1,000 trong khi runtime thực gửi request có output budget khoảng 1,426–2,428 tokens.

**FACT:** Inspection cho thấy `--max-tokens` của runner chỉ nằm trong `generation_config` và không được chuyển vào `LLMClient`. Đã vá **bản clone tạm cục bộ** (không sửa dataset/vault) để truyền `llm_max_tokens`; file vá: `evalscope_adapter/local_runtime.py`.

**FACT:** Sau vá với `max_tokens=512`, một task tạo được hai tool calls nhưng vẫn thất bại: model phát function arguments `{}`, sau đó có HTTP 400 `tool_use_failed` và `Connection error`. Không có injected `TimeoutError`; đây là model/provider failure, không phải controlled tool failure cần đo.

**INFERENCE:** Groq Free + `qwen/qwen3.6-27b` phù hợp để smoke-test API/function-call, nhưng **không vượt qua reproducibility gate** cho ToolBench-X baseline hiện tại. Không nên dùng các kết quả `0/5` hay 0/1 này làm metric agent reliability. ^[inferred]

### Groq Qwen 3.8 với pacing

**FACT:** `qwen/qwen3.8-27b` vượt forced function-call preflight và tạo arguments `{"x":1}`. Groq từ chối `chat_template_kwargs.enable_thinking=false`, nên cờ ToolBench-X `--disable-thinking` không dùng được qua endpoint này.

**FACT:** Với process-wide pacing 40 giây, `max_tokens=512`, `max_workers=1`, một task chạy 601.065 giây mà không gặp 429. Agent thực hiện 10 rounds, 5 tool calls, 10 policy actions và 12 clean trajectory messages.

**FACT:** Final answer là `4`, khác expected answer `18412733`. Cả 5 tool executions có wrapper-level `success=true`, nhưng nested result đều `ok=false`: bốn call dùng path không tồn tại (`survey_q2_feedback.csv` hoặc `/bench/inputs/feedback.csv`), một call có arguments rỗng/`null` và `no_input_data`. Không quan sát được controlled injected failure trong run này.

**INFERENCE:** Pacing 40 giây giải quyết Groq OTPM cho một task, nhưng Groq/Qwen 3.8 vẫn chưa vượt end-to-end task-validity gate. Chạy thêm 5 task sẽ tốn khoảng hàng chục phút mà chưa tạo dữ liệu controlled-failure hợp lệ. ^[inferred]

## Pilot với Gemini — 2026-09-12

**FACT:** Gemini OpenAI-compatible endpoint với `gemini-3.8-flash` vượt forced function-call preflight: trả một tool call có arguments hợp lệ `{"x":1}`. Điều này xác nhận key, endpoint và basic OpenAI compatibility hoạt động.

**FACT:** Với một task ToolBench-X thật, agent có một tool call và fallback sang plain JSON argument generation sau arguments rỗng `{}`. Sau đó Gemini trả HTTP 429 `RESOURCE_EXHAUSTED`: Free tier của project giới hạn `generate_content_free_tier_requests` là 5 request/phút cho model này. Task chưa đi tới injected `TimeoutError`.

**INFERENCE:** Gemini Free tier không phù hợp cho ToolBench-X multi-step pilot *theo runner hiện tại*: một task cần nhiều request để route tool, sinh arguments, retry và synthesize. Rate-limit event là provider/infrastructure failure, không phải controlled tool failure. ^[inferred]

### Thử pacing để tránh rate limit

**FACT:** Đã thêm process-wide request pacing 15 giây vào bản clone tạm và chạy lại một task. Run kéo dài 382.44 giây, tạo 4 tool calls và 10 message trong clean trajectory; không còn burst 5 RPM ban đầu.

**FACT:** Run vẫn không hoàn thành. Project chạm Free-tier daily quota 20 request/model/day. Ba tool call đầu không raise exception ở wrapper level nhưng kết quả bên trong đều `ok=false`: hai call có arguments `{}` và `no_input_data`; call thứ ba có arguments nhưng file CSV không tồn tại ở path được tạo, trả `file_read_failed`. Call thứ tư bị HTTP 429. Không có controlled injected failure hợp lệ.

**INFERENCE:** Pacing giải quyết RPM nhưng không giải quyết daily quota hoặc tool-argument quality. Vì vậy Gemini Free không đủ cho pilot 5–10 task và không nên dùng wall-clock latency từ paced run làm metric. ^[inferred]

## Gate cuối với clean/exception pair — 2026-09-12

**FACT:** Gọi trực tiếp cả bốn clean tools của `parallel/Data__Analytics/Spreadsheet_cleanup_and_formatting/task_1` với request gốc trả đúng các thành phần `118`, `7`, `4`, `63` và `final_value=118-7-4-63`. Với exception module, `strict_no_hint_profile` và seed 7, cả bốn lần gọi đầu đều phát sinh `TimeoutError` tại `before_tool_logic`; module-level event log ghi tool, failpoint, attempt, `retryable` và profile.

**FACT:** Trong runner nguyên bản, Groq `qwen/qwen3.8-27b` chọn đúng bốn tools nhưng sinh `user_prompt=null`, khiến clean tools bỏ qua deterministic benchmark branch và trả `0-0-0-0`. Bản clone tạm được thêm một adapter: nếu function có tham số `user_prompt` và model trả null/rỗng, runner backfill request gốc. Adapter không dùng expected answer hay hidden label.

**FACT:** Sau adapter, clean run đạt exact-match `118-7-4-63` (`1/1`) sau 525.93 giây. Exception/no-hint counterpart cùng model, task, seed và sáu rounds thất bại (`0/1`) sau 440.99 giây: năm tool executions đều gặp explicit `TimeoutError`; policy thử lại Sheet A một lần, chuyển sang các tools còn lại rồi dừng unresolved. Đây là một paired smoke test, không phải kết quả thống kê.

**FACT:** Raw runner output không giữ `exception_events` dù exception module có event log. Clean trajectory chỉ còn tool name, arguments/result hoặc error string, round và policy action. Muốn nghiên cứu trajectory signal có cấu trúc phải sửa instrumentation hoặc parse error strings.

### Audit 5 task không dùng LLM

| Task | Clean direct-call gate | Kết quả |
|---|---|---|
| Report generation | △ | Final aggregator trả expected `15`, nhưng ba component outputs là `0`; nhánh known-task tự điền các giá trị khác. |
| Spreadsheet cleanup | ✓ | Bốn component và final value đúng. |
| Survey response | ✗ | Cả bốn calls trả `ok=false`, `no_input_data`; artifact không chứa CSV được nhắc trong prompt. |
| Credit-card monitoring | ✗ | Thiếu private telemetry, external fallback timeout/reset; trả `0000` thay vì `2314` nhưng wrapper vẫn `ok=true`. |
| Personal budget | ✓ | Component totals/counts và final `1850` đúng. |

**FACT:** Static artifact audit tại commit `a0948f0eb34f6028ebc7af0a2d83fce94bbfc41a` cho thấy: 1,106 clean tool modules; 965/1,106 (87.3%) chứa chuỗi `known_task_exact_branch_applied=true`; 671/1,106 (60.7%) import `urllib.request`; và chỉ 705/1,106 exception modules định nghĩa `get_injection_events`. Thư mục `tasks/` có 522 JSON nhưng tổng cộng 2,610 task records, không khớp câu README “contains 1,106 tasks”. Đây là static code evidence; chưa phải tỷ lệ task runtime lỗi.

**INFERENCE:** Nhiều expected outputs được kích hoạt bằng prompt-signature/hard-coded branch thay vì dữ liệu môi trường thực. Điều này làm early-failure detection dễ học shortcut (prompt/tool identity) và giảm external validity. ^[inferred]

**INFERENCE:** `tool_executions.success`, nested `result.ok`, `error`, `confidence` và task success không có semantics nhất quán giữa modules; monitor không thể dùng các field này như label/signal chung nếu chưa chuẩn hóa. ^[inferred]

## Hệ quả cho research

**INFERENCE:** ToolBench-X đủ để chứng minh một controlled fault module có thể chạy và tạo paired trajectory, nhưng **không vượt qua gate để làm benchmark chính** cho early failure detection: clean-task validity không đồng đều, event metadata bị evaluator strip, fault thường là explicit exception ngay lần gọi đầu, và benchmark branches có nguy cơ leakage. ^[inferred]

**RESOLVED FOR CURRENT PROJECT:** chưa có đủ evidence về persistent/non-recoverable coverage hoặc fair monitor-visible trace, nhưng không cần mở rộng kiểm tra ngay vì broad external monitoring gap đã bị prior art bác bỏ. Giữ ToolBench-X làm secondary stress test, không dùng để tuyên bố persistent-failure forecasting.

**Khuyến nghị:** Không dùng ToolBench-X làm benchmark chính của đề tài 3 tháng. Có thể giữ 2–3 task đã qua clean gate làm secondary stress test hoặc tái sử dụng taxonomy/fault patterns sau khi làm rõ license. Benchmark chính nên là một harness nhỏ có task data thật, fault injector độc lập, trajectory schema nhất quán và paired clean/fault runs.

## Ràng buộc quan trọng

README/dataset README ghi dataset chỉ dùng academic research, cấm commercial use và cấm distribute/publish/copy/disseminate/modify toàn bộ hoặc một phần nếu không được approval. Root `LICENSE` lại là MIT. Hai văn bản không thống nhất về quyền modification/distribution; không nên phát hành derived artifact trước khi tác giả làm rõ. **OPEN QUESTION:** xin xác nhận bằng văn bản nếu muốn sửa/bổ sung fault harness hoặc công bố derived benchmark.

## Phù hợp với research này

**FACT:** ToolBench-X phù hợp để pilot/reproduce baseline recovery dưới tool unreliability.

**INFERENCE:** Nó không nên là benchmark chính cho một đề tài mới về broad routing: paper và [[references/retry-switch-or-abstain]] đã chiếm không gian vấn đề gần kề; license cũng có thể chặn modification cần thiết. ^[inferred]

## Liên hệ

- [[synthesis/Prior-Art Threat: Recovery-Action Selection]]
- [[references/retry-switch-or-abstain]]
