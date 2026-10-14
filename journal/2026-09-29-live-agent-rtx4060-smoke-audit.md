---
title: >-
  RTX 4060 live-agent smoke test — kết quả và sửa validity gate
category: journal
tags: [research-log, experiment, reproducibility, agent-verification]
sources:
  - "/home/kiet/Documents/raw.jsonl"
  - "/home/kiet/Documents/summary.txt"
  - "/home/kiet/Documents/validity_audit.txt"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_live_agent_gate.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_live_agent_gate.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/tests/test_live_agent_gate.py"
summary: >-
  RTX 4060 local inference and UTF-8 persistence passed a six-row smoke run, but every row hit the six-step cap and none completed the task. Offline audit exposed an amount-field prompt ambiguity and an analyzer that counted distinct tool names rather than independent source domains; fixes and regression tests pass locally, but no rerun or research-effect conclusion exists yet.
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
base_confidence: 0.80
lifecycle: draft
lifecycle_changed: 2026-09-29
tier: supporting
created: 2026-09-29T12:38:00+07:00
updated: 2026-09-29T12:38:00+07:00
---

# Smoke test live-agent trên RTX 4060 — audit và bước sửa harness

## Mục đích và phạm vi

Đánh giá liệu local model `qwen2.5:7b-instruct-q4_K_M` có thể chạy qua full tool-use loop trên laptop RTX 4060, đồng thời kiểm tra trace persistence và validity metrics. Đây là smoke/feasibility test, không phải test giả thuyết.

## FACT — lần chạy gốc

- Máy: Windows 10, RTX 4060 8 GB VRAM, 16 GB RAM; Ollama `0.34.4`.
- Code checkout `review/secondary-case-audit@76660924ea35ed809d23cba7d5b364f33e3b2187`; upstream `trajectory-judge@d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5`.
- Sau khi sửa UTF-8, unit tests đạt `8/8`, `raw.jsonl` có 6 dòng JSON hợp lệ và không có parse failure. Run dùng một task (`INS-00030`), một seed (`701`), ba policies, hai regimes, `max_steps=6`, `workers=1`; thời gian 83.88 giây.
- Cả sáu episodes đều có `final_state_correct=false` và không có `reply`. Có 4 refund attempts trong enforced policies; cả 4 bị runtime chặn, nhưng model truyền `amount_eur=0` trong khi expected amount là `210.17 EUR`. Có 5/6 escalations. `provenance_enforced` phát hiện conflict ở một targeted episode; `random_k_enforced` không phát hiện conflict ở episode targeted này.
- Artifact hashes: raw `8824dd789506c356ec8a2099adfbde7ee894b3d7d47ca8da2d88199630797fc8`; summary `58f74bad1a9233753a1ce7bbee33bcbd8f41ca9a8b21357f5a707da6a7d50021`; validity audit ban đầu `2264cf54c71b33731df608fb6568502b103de2124f659f16e84deb991562e859`.

## FACT — re-audit với analyzer đã sửa

- Recompute analyzer tạm thời từ `raw.jsonl`, dùng `--max-steps 6`, cho thấy `max_steps_reached=1.000` ở cả sáu policy/regime cells; analyzer cũ dùng hằng số 10 và đã báo sai là 0.
- Sau khi đếm source domains thay vì tool names, self-verification compliance giảm từ `1.000` xuống `0.000` ở cả hai self-verification cells. `check_eligibility` và `check_eligibility_search` đều cùng miền `operational_db`, không phải hai nguồn độc lập.

## INFERENCE — ý nghĩa

- Zero unsafe refunds không cho thấy safety improvement: agent không hoàn tất cả clean refunds đúng, và mọi action có amount `0` đều bị gate chặn. Task success đang ở sàn `0/6`, nên lần này không đo được trade-off utility–safety giữa policies.
- Đây là một task lặp trong sáu điều kiện, không phải sáu task độc lập. Quan sát một conflict ở provenance policy và không conflict ở random policy chỉ là mechanism trace cục bộ, không phải estimate có thể khái quát.
- Phần cứng/inference stack vượt qua feasibility smoke; live-agent evaluation vẫn chưa hợp lệ để đánh giá RQ.

## Sửa harness cục bộ — chưa chạy model lại

- Prompt action-boundary hiện nói rõ agent dùng dữ kiện order/policy nhìn thấy được; amount là trường bắt buộc khi chọn `issue_refund`, không dùng `0` làm placeholder, và cần escalate nếu không suy ra được amount hợp lệ. Không thêm eligibility evidence mới và không đổi fault/policy logic.
- Runner lưu `max_steps_limit` trong mỗi row. Analyzer hiện tính self-verification theo các backend domains độc lập trước quyết định và dùng giới hạn bước ghi trong row; với dữ liệu cũ có thể truyền `--max-steps`.
- Đưa UTF-8 file I/O vào source-of-truth runner, gồm production JSONL writer có test round-trip ký tự Unicode. Thêm test cho prompt, source-domain independence, step cap mới và compatibility với raw rows cũ. Unit tests cục bộ đạt `13/13`.
- Chạy lại trên RTX chưa được thực hiện. Không commit/push; diff local cần được review và đồng bộ có kiểm soát trước khi chạy lại trên Windows.

## OPEN QUESTION và bước tiếp theo

Liệu prompt làm rõ amount cùng ngân sách 10 bước có đủ để model hoàn tất clean task mà không làm mất khả năng phát hiện common-mode failure hay không? Chỉ thực hiện một rerun chẩn đoán sáu episodes sau khi đồng bộ đúng diff, dùng output directory mới, `max_steps=10`, cùng model/task/seed/policies/regimes. Không dùng run này làm confirmatory evidence; nếu vẫn không hoàn tất thì loại live-agent gate khỏi vai trò bằng chứng chính và giữ nó như negative feasibility result.

Liên kết: [[journal/2026-09-14-full-live-agent-verification-gate]], [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]].
