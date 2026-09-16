---
title: Nhật ký nghiên cứu — ToolBench-X reproducibility pilot
category: journal
tags: [research-log, benchmark, reproducibility, ai-agents, tool-failure]
sources: [https://github.com/Foreverskyou/ToolBench-X, https://huggingface.co/datasets/Foreverskyou/ToolBench-X, https://arxiv.org/abs/2606.25819, https://console.groq.com/docs/openai, https://console.groq.com/docs/tool-use/overview, https://console.groq.com/docs/rate-limits, https://ai.google.dev/gemini-api/docs/openai, https://ai.google.dev/gemini-api/docs/rate-limits]
summary: >-
  Pilot hoàn tất clean/exception pair và audit 5 task. Data path, signal semantics, event export, hard-coded branches và free-tier throughput không đạt yêu cầu benchmark chính.
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
base_confidence: 0.96
lifecycle: draft
lifecycle_changed: 2026-09-11
tier: supporting
created: 2026-09-11T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# Nhật ký nghiên cứu — ToolBench-X reproducibility pilot

## Mục tiêu

Kiểm tra xem [[references/toolbench-x]] có thực sự là một benchmark khả thi cho pilot 3 tháng về phát hiện sớm failure trong tool-using agent hay không, trước khi chọn nó làm nền thực nghiệm.

## Đã làm

1. Clone repository vào thư mục tạm cô lập; đọc README, `requirements.txt`, runner và local runtime adapter.
2. Cài dependency cục bộ; workaround vì Python thiếu `ensurepip` nên không tạo được virtual environment bình thường.
3. Tải/extract public dataset, sau đó kiểm tra số artifact và task-to-tool mapping.
4. Gọi trực tiếp một exception tool với seed cố định để xác minh controlled tool failure.
5. Chạy runner baseline trên 5 task: một lần không API key, một lần dùng endpoint loopback cố ý không có model để kiểm tra hành vi lỗi/output.

## Kết quả đã xác minh

| Câu hỏi                   | Kết quả                                                                        | Ý nghĩa                                                       |
| ------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| Dependency cài được?      | Có, với `pip --target .deps`.                                                  | Pilot không cần GPU hay system install.                       |
| Dataset dùng được?        | Có: 522 task-config JSON và 1,106 exception tool module sau extract.           | Artifact có thể tải và chạy local.                            |
| Tool failure có thật?     | Có: cùng seed tạo ba `TimeoutError` retryable rồi tool thành công ở attempt 4. | Failure được kiểm soát, quan sát được và tái lập được.        |
| 5 task map được tool lỗi? | Có, coverage `5/5`.                                                            | Cấu trúc path/runner hoạt động.                               |
| Trajectory có lưu?        | Có `openai_trajectory`; rich trace bị strip ở evaluator output mặc định.       | Cần gate trace trước khi làm monitor experiment.              |
| Success/failure có rõ?    | Có các field `success`, `error`, exact-match, aggregate summary.               | Có thể chấm outcome; phải tách lỗi hạ tầng khỏi task failure. |
| Baseline thật đã chạy?    | Có, một clean task đạt exact-match sau context adapter.                        | Chỉ là feasibility smoke test, chưa phải performance result. |
| Chi phí API?              | Dùng Groq/Gemini Free tier; không bật paid billing.                            | Không phát sinh chi phí trả tiền đã biết; quota/throughput là giới hạn chính. |

## Pilot model thật — Groq, 2026-09-12

Không ghi API key vào vault. Đã dùng key do owner cung cấp chỉ trong process chạy.

| Kiểm tra | Kết quả | Kết luận |
|---|---|---|
| `openai/gpt-oss-20b`, plain chat | Thành công. | Key/endpoint hoạt động. |
| `openai/gpt-oss-20b`, forced function call | HTTP 400 `tool_use_failed`. | Không tương thích với pattern tool-call bắt buộc của ToolBench-X trong pilot này. |
| `qwen/qwen3.6-27b`, forced function call tối giản | Thành công. | Model vượt preflight đơn giản. |
| Qwen, 5 task baseline | `0/5`; HTTP 429 output-token limit. | Không phải task score; free-tier quota chặn request. |
| Qwen, 1 task sau vá `max_tokens=512` | Có 2 tool calls nhưng args đầu là `{}`, sau đó `tool_use_failed`/`Connection error`; `0/1`. | Chưa tới controlled tool failure; chưa hợp lệ cho đo reliability. |
| Gemini `gemini-3.8-flash`, forced function call | Thành công, arguments `{"x":1}`. | OpenAI-compatible endpoint hoạt động. |
| Gemini, 1 task ToolBench-X | Một tool call/fallback JSON rồi HTTP 429; `0/1`. | Free-tier request quota 5 RPM chặn multi-step task trước injected failure. |
| Gemini, 1 task với pacing 15 giây | 382.44 giây; 4 tool calls, 10 trajectory messages; vẫn `0/1`. | Hết daily quota 20 request; các tool result trước đó `ok=false` do args/input path, chưa có controlled fault. |
| Groq Qwen 3.8, forced function call | Thành công với arguments `{"x":1}`; cờ `--disable-thinking` bị endpoint từ chối. | Basic function calling hoạt động nếu bỏ cờ không tương thích. |
| Groq Qwen 3.8, 1 task pacing 40 giây | 601.065 giây; 10 rounds, 5 tool calls; không 429; đáp án `4` thay vì `18412733`. | API quota gate qua, task-validity gate fail do mọi nested tool result `ok=false`. |
| Spreadsheet clean, context adapter | 525.93 giây; exact-match `118-7-4-63`; `1/1`. | Xác nhận một task end-to-end có thể chạy nếu backfill request gốc vào optional `user_prompt`. |
| Spreadsheet exception/no-hint | 440.99 giây; 5 explicit `TimeoutError`; final unresolved; `0/1`. | Có paired controlled-fault trajectory, nhưng chỉ là một sample và structured injection events bị strip. |

### Lỗi runner đã xác minh

`run_evalscope_local_runtime.py` có cờ `--max-tokens` nhưng `evalscope_adapter/local_runtime.py` không truyền giá trị đó vào `LLMClient`. Do đó runner báo cấu hình 512 nhưng request thực không dùng giới hạn này. Bản clone tạm đã được vá tối thiểu để truyền `llm_max_tokens`, và `py_compile` thành công. Đây là thay đổi **local instrumentation**, không được xem là thay đổi benchmark chính thức hay contribution research.

Adapter thứ hai backfill request gốc vào tham số `user_prompt` khi model sinh null/rỗng. Nó không đưa expected answer vào model/tool, nhưng cần được khai báo trong methodology vì không thuộc code upstream.

## Audit clean-task validity

Gọi trực tiếp tools của năm task pilot, không dùng LLM:

| Trạng thái | Task |
|---|---|
| Component/final đúng | Spreadsheet cleanup, Personal budget |
| Final đúng nhưng component calls ban đầu không khớp | Report generation |
| Không có input data | Survey response |
| Thiếu private telemetry/external fallback lỗi và final sai | Credit-card monitoring |

**FACT:** Repository không chứa CSV fixture được Survey task yêu cầu. **FACT:** Credit-card tools có thể trả `ok=true` đồng thời chứa `error` và unsupported private telemetry. Vì vậy `ok`, wrapper success và final success phải được tách riêng.

**FACT:** Static audit 1,106 clean modules: 87.3% có known-task branch, 60.7% có `urllib.request`; chỉ 705 exception modules có `get_injection_events`. `tasks/` chứa 2,610 records, khác con số 1,106 trong README. Các tỷ lệ này mô tả source code, không phải runtime pass/fail rate.

## Lỗi/giới hạn phát hiện

- README nhắc `config/.env.example` nhưng repository không chứa file đó.
- Không có API key khiến `LLMClient` raise `OpenAIError` trước task-level exception handling, làm batch dừng.
- API endpoint giả cho phép runner hoàn tất 5 task nhưng tất cả fail tại LLM request; không có tool call nào, nên kết quả `0/5` không phải benchmark score.
- Groq Free tier/Qwen không vượt qua ToolBench-X end-to-end gate: quota output-token thấp và tool calls phức tạp sinh arguments không hợp lệ. Không ngoại suy điều này thành chất lượng của ToolBench-X hay của tất cả model Groq.
- Gemini Free tier qua basic compatibility nhưng request quota 5 RPM thấp hơn nhu cầu nhiều bước của ToolBench-X. Throttle/retry patch có thể làm task chạy chậm, nhưng đó là thay đổi harness và chưa phải bước hợp lý trước khi xác minh model compatibility với tool schema thực.
- Pacing 15 giây tránh burst RPM nhưng một task đã tiêu phần lớn daily request budget và mất hơn 6 phút. Latency này là artifact của quota control, không phải agent latency.
- Wrapper-level `success=true` không đồng nghĩa tool result hợp lệ: ba call không raise Python exception nhưng payload trả `ok=false`. Khi đánh giá phải dùng nested `result.ok`/final state, không chỉ `tool_executions.success`.
- Groq pacing 40 giây loại bỏ 429 trong run một task, nhưng bốn tool call dùng file path không tồn tại và một call thiếu input. Không có controlled injected failure; không được dùng trajectory này như positive fault-injection sample.
- ToolBench-X nói về **recoverable** unreliability. Sample vừa kiểm tra có failure tạm thời/rút lui sau retry; chưa có bằng chứng rằng benchmark biểu diễn persistent tool failure theo nghĩa cần cho một RQ rộng.
- Hints/oracle labels chứa thông tin hazard/recovery. Một external monitor phải chỉ dùng agent-visible trace; dùng các file này trong `no_hint` sẽ gây leakage.
- Official A/B path đổi cả hint context lẫn injection profile (`strict_no_hint_profile` sang `guided_with_hint_profile`), bao gồm probability/max-times khác nhau. Không dùng trực tiếp so sánh đó để kết luận causal effect của hint hoặc detector dưới cùng fault distribution.
- Nhiều faults là explicit exception ngay lần gọi tool đầu. Nếu label “sẽ fail” được dự đoán sau khi exception đã xuất hiện, bài toán có thể trở thành detection hiển nhiên thay vì early prediction.
- Pacing 40 giây giúp tránh Groq 429 nhưng clean task mất 525.93 giây và exception task mất 440.99 giây. Throughput này chỉ phù hợp pilot nhỏ.

## Diễn giải cho hướng research

**FACT:** Benchmark vượt qua gate cơ bản về tải artifact, chạy local và inject tool failure.

**INFERENCE:** ToolBench-X không nên là benchmark chính cho đề tài early failure detection hiện tại. Nó vẫn hữu ích như secondary stress test và nguồn taxonomy/fault patterns, nếu chỉ chọn task đã qua clean gate và tuân thủ license. ^[inferred]

**RESOLVED 2026-09-12:** External monitor/early failure forecasting đã có direct prior art mạnh và artifact tái lập được; broad gap bị `REJECTED`. Benchmark khả thi không tạo novelty, nên không xây local 20–30-task harness theo plan cũ.

## Kết luận gate

**QUYẾT ĐỊNH:** Dừng mở rộng ToolBench-X với free APIs. Không chạy batch lớn vì một paired sample đã đủ chỉ ra các confounds về data, hard-coded branches, signal semantics, event export và throughput. Đây không phải kết luận rằng paper/benchmark vô giá trị; chỉ là kết luận về độ phù hợp với thesis 12 tuần và RQ early failure detection của project này.

## Bước tiếp theo cũ — đã superseded

Kế hoạch thiết kế pilot harness 20–30 task đã bị hủy tại novelty gate. Bước mới là adversarial prior-art search cho task-grounded runtime verification của schema-valid silent tool output. Xem [[journal/2026-09-12-early-failure-detection-novelty-gate]].

## Liên hệ

- [[references/toolbench-x]]
- [[references/adaptive-fault-injection-task-failure-forecasting]]
- [[synthesis/Preliminary Gap: External Runtime Monitoring]]
