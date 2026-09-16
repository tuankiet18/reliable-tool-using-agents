---
title: >-
  2026-09-15 — Main-Study Task Manifest Frozen
category: journal
tags: [research-log, experiment, reproducibility, verification, benchmark]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tasks_main_30.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tasks_main_30.manifest.json"
  - "https://github.com/mohammadi-hadi/trajectory-judge"
summary: >-
  Đóng băng 30 task mới cho main deterministic study trước khi viết harness: split tái lập, không trùng pilot và có SHA-256 đã ghi nhận.
provenance:
  extracted: 0.96
  inferred: 0.04
  ambiguous: 0.00
base_confidence: 0.96
lifecycle: draft
lifecycle_changed: 2026-09-15
tier: core
created: 2026-09-15T00:12:18+07:00
updated: 2026-09-15T00:12:18+07:00
---

# Main-study task manifest đã được đóng băng

## Mục tiêu

Thực hiện bước đầu tiên sau internal preregistration trong [[synthesis/Protocol: Action-Boundary Provenance Verification Main Study]]: tạo bộ task chính độc lập với toàn bộ exploratory và pilot. Việc này diễn ra trước khi có main harness hoặc main result, để tránh chọn task sau khi đã thấy outcome.

## FACT — Split được tạo

- Upstream: `trajectory-judge` tại commit `d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5`.
- Generator: seed `20260914`, offset `60`, count `30`.
- Task IDs: `INS-00060`–`INS-00089`.
- Artifact: [`tasks_main_30.json`](../projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tasks_main_30.json).
- SHA-256: `a122dda63a40ab8db43d1af2a6a7019ca561c4c9e533db0e798fe9470e88cfa6`.

## FACT — Kiểm tra hợp lệ

| Kiểm tra | Kết quả |
|---|---|
| Số task | `30` |
| ID trùng với `INS-00000`–`INS-00059` | Không có |
| ID duy nhất/range | `30` IDs duy nhất, từ `INS-00060` đến `INS-00089` |
| Difficulty balance | 6 strata × 5 task |
| `fact_key` balance | 10 keys × 3 task |
| Generator rerun | Cùng SHA-256 |

Metadata có thể máy đọc tại [`tasks_main_30.manifest.json`](../projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tasks_main_30.manifest.json).

**FACT:** Test suite của exact upstream checkout (`22 passed`) và `ruff check` của generator đều pass sau khi sinh split. Đây là kiểm tra generator/environment, không phải một kết quả của main study.

## Ý nghĩa đối với research

Đây **không phải kết quả ủng hộ RQ**. Nó chỉ tạo một điều kiện thực nghiệm công bằng: khi so sánh `random-K` với `provenance-K`, cả hai sẽ được đánh giá trên task chưa từng xuất hiện trong các lần chọn design/pilot trước.

## Điều chưa chắc chắn

Split độc lập không giải quyết external validity: tất cả task vẫn có chung generator và domain refund của `trajectory-judge`. Main study vì vậy chỉ có thể kết luận trong phạm vi controlled benchmark này.

## Bước tiếp theo duy nhất

Implement deterministic action-boundary harness tách biệt với exploratory artifacts, kèm tests bắt buộc cho fresh-ID exclusion, coverage `1.000`, matched `K=2`, fault-domain correlation và amount authorization. Chưa chạy main experiment trong bước này.

## Related

- [[synthesis/Protocol: Action-Boundary Provenance Verification Main Study]]
- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]
- [[journal/2026-09-14-full-live-agent-verification-gate]]
