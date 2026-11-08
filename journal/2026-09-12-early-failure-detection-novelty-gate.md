---
title: Nhật ký nghiên cứu — Early failure detection novelty gate
category: journal
tags: [research-log, prior-art, failure-detection, runtime-monitoring, reproducibility]
sources:
  - "https://arxiv.org/abs/2605.06455"
  - "https://arxiv.org/abs/2605.08715"
  - "https://arxiv.org/abs/2606.05414"
  - "https://arxiv.org/abs/2608.02464"
  - "https://arxiv.org/abs/2608.23670"
summary: >-
  Ba search round và một local smoke reproduction bác bỏ broad early-failure-detection gap; plan dừng tại novelty gate và chuyển sang semantic verification prior-art search.
provenance:
  extracted: 0.80
  inferred: 0.17
  ambiguous: 0.03
base_confidence: 0.92
lifecycle: draft
lifecycle_changed: 2026-09-12
tier: core
created: 2026-09-12T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# Nhật ký nghiên cứu — Early failure detection novelty gate

## Mục tiêu

Trả lời các open question trước khi xây pilot harness, và cố bác bỏ hướng “early failure detection trong tool-using agents bằng controlled failures”.

## Đã tìm gì

Ba vòng search tập trung vào:

1. `partial trajectory`, `prefix failure prediction`, `online auditing`;
2. controlled/adaptive fault injection, silent failure và cross-policy/cross-model transfer;
3. lightweight runtime monitor, false-alarm/lead-time trade-off và public artifacts.

Các work trực tiếp nhất: Adaptive Fault Injection, PrefixGuard, AgentForesight/AFTraj-2K, When Evidence is Sparse, AgentTrajectorySentinel, Automata from Agent Traces và anonymous web-agent prefix-risk submission.

## Đã kiểm tra artifact gì

Clone public repository `agent-trajectory-sentinel` tại commit `1b3e07fee53ae13407173c3ea932adb4a43e8230`, tạo Python 3.13 environment trong thư mục tạm và chỉ dùng local CPU.

- Targeted tests: `89 passed`, `6 skipped`, `3 failed`; ba failure do optional/live dependencies không cài (`langchain_core`, `sqlalchemy`, Ollama), không phải lỗi core monitor.
- Quick study seed `99173`: hoàn tất trong `16.6s`.
- 121 claims khớp committed artifacts.
- Behavior snapshot khác 12 mục vì môi trường không dùng pinned lockfile và bỏ optional GRU/LSTM/TCN; không gọi đây là exact reproduction.

## Học được gì

**FACT:** online prefix monitoring, controlled failure generation, cross-corpus evaluation, false-alarm/lead-time metrics và repair closure đều đã có prior art.

**FACT:** failure evidence thường thưa và xuất hiện muộn; warning ranking cao có thể vẫn vô dụng ở low false-alarm operating point.

**FACT:** fault exposure, onset và final task failure là ba nhãn khác nhau.

**INFERENCE:** một local 20–30-task harness sẽ yếu hơn artifact công khai hiện có và khó tạo novelty. Giá trị tốt nhất của nó chỉ là học/reproduction, không phải thesis contribution.

## Uncertainties

- Code chính thức của PrefixGuard, Automata và weakly supervised alerting chưa được xác minh public.
- Adaptive Fault Injection artifact/license vẫn chưa được xác minh.
- Trường hợp schema-valid, plausible-but-wrong tool output có thể cần external semantic oracle; chưa search đủ prior art ở runtime verification/data validation.

## Quyết định

Broad direction `early failure detection from execution trajectories under controlled tool failures`: **REJECTED**.

Plan kết thúc hợp lệ tại novelty gate; không tạo harness, không gọi thêm paid/free API và không đề xuất RQ yếu.

## Bước tiếp theo duy nhất

Adversarial prior-art search cho `task-grounded runtime verification of schema-valid silent tool outputs`, bao gồm reference execution, invariants, state-transition checks và cross-tool consistency.

## Related

- [[synthesis/Research - Early Failure Detection in Tool-Using Agents]]
- [[synthesis/Preliminary Gap - External Runtime Monitoring]]
- [[references/real-time-detection-and-repair-agent-failures]]

