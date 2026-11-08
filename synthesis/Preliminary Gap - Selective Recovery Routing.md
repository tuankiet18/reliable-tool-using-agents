---
title: >-
  Preliminary Gap: Selective Recovery Routing Under Runtime Tool Failures
category: synthesis
tags: [research-gap, preliminary, ai-agents, recovery, tool-failure]
sources:
  - "https://openreview.net/pdf?id=j7YsSnA64D"
  - "https://arxiv.org/abs/2607.06273"
  - "https://arxiv.org/abs/2605.29225"
  - "https://arxiv.org/abs/2608.11977"
  - "https://arxiv.org/abs/2606.01416"
summary: >-
  REJECTED (broad form): Retry, Switch, or Abstain? đã nghiên cứu policy chọn retry, switch/fallback và abstain/escalate dưới tool failure có kiểm soát.
provenance:
  extracted: 0.42
  inferred: 0.48
  ambiguous: 0.10
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: core
created: 2026-09-09T17:16:31Z
updated: 2026-09-10T00:00:00Z
---

# PRELIMINARY Gap: định tuyến phục hồi có chọn lọc khi tool lỗi lúc chạy

`Selective Recovery Routing Under Runtime Tool Failures`

## Trạng thái sau adversarial prior-art search

### REJECTED

Phiên bản rộng của gap bị bác bỏ. [[references/retry-switch-or-abstain]] đã xây `BENCH2ROBUST` với scenario `retry_works`, `switch_needed`, `impossible`; dùng Bayesian Tool Memory (BTM) và DAPO RL để hỗ trợ/huấn luyện behavior `retry`, `switch/fallback`, `abstain/escalate`; đo S1 retry success, S2 switch success và premature escalation. [[synthesis/Prior-Art Threat - Recovery-Action Selection]] lưu bằng chứng và các phản ví dụ.

Điều này không phủ định giá trị thực tiễn của recovery routing. Nó phủ định phát biểu novelty rộng “chưa ai nghiên cứu chọn recovery action động dưới tool failure”.

## Phát biểu gap ban đầu (đã bị bác bỏ)

**PRELIMINARY RESEARCH GAP CANDIDATE:** Bằng chứng hiện có hỗ trợ riêng lẻ cho đánh giá tool failure có kiểm soát, chẩn đoán/sửa quỹ đạo và đánh giá reflection; chưa xác lập rằng policy nhẹ, được external monitor hỗ trợ, đã được so sánh chặt chẽ với retry cố định và replan/fallback cố định khi đồng thời kiểm soát fault persistence, tác dụng phụ và ngân sách tool.

**CẬP NHẬT:** Câu trên không còn đúng ở phần `retry/switch/abstain`; chỉ phần kết hợp chặt chẽ với tác dụng phụ không đảo ngược, verified escalation và benchmark public mới còn chưa rõ.

## Bằng chứng

- **FACT:** [[references/failing-tools]] phân biệt runtime fault tạm thời/kéo dài và đặt recovery trajectory làm trung tâm.
- **FACT:** [[references/agenttether]] chẩn đoán quỹ đạo thất bại và hướng dẫn rerun trên τ-bench.
- **FACT:** [[references/benchtrace]] báo cáo diagnosis là nút thắt của reflection và reflection từ episode nhiễu khó tổng quát hóa.
- **INFERENCE:** Các kết quả này khiến việc định tuyến recovery action trở thành điểm nối có lý, nhưng không chứng minh nó chưa có trong literature. ^[inferred]
- **FACT (negative evidence):** [[references/retry-switch-or-abstain]] là counterexample trực tiếp.
- **FACT (negative evidence):** Self-Healing Agentic Orchestrators ánh xạ observable failure signal sang targeted recovery action dưới budget và so sánh retry-only/full replanning trong controlled setting.

## Candidate hypothesis (đã không còn là hypothesis đề xuất)

### H1 — English

Given partial trace signals (error class, retry history, state-change evidence, alternative availability, and action idempotency), a selective router improves verified task success per tool call over always-retry and always-replan policies.

### Diễn giải tiếng Việt

Nếu biết tín hiệu từ trace một phần—loại lỗi, lịch sử retry, bằng chứng state đã đổi, lựa chọn thay thế và idempotency—router có chọn lọc có thể tăng verified task success trên mỗi tool call so với policy luôn retry hoặc luôn replan.

## Biến số và thực nghiệm (lưu lịch sử, không triển khai)

| Vai trò | Ứng viên |
|---|---|
| Biến độc lập | recovery policy; fault type; tính tạm thời/kéo dài; idempotency/tác dụng phụ; model |
| Biến phụ thuộc | verified success; precision/recall của recovery; tool call; token; action trùng không an toàn; escalation rate |
| Baseline | chỉ continue; retry một lần/N; luôn replan/fallback; agent self-reflection; oracle biết fault persistence |
| Benchmark | Failing Tools nếu code/license cho phép tái lập; nếu không, fault wrapper tối thiểu quanh τ-bench/ToolSandbox |

## Thực nghiệm tối thiểu khả thi (không khuyến nghị)

Trước hết, triển khai event schema độc lập framework và router rule/score xác định. Chạy một subset phân tầng, có seed, với một API model chính và lặp 3–5 lần. Chỉ thêm ablation LLM-judge/router khi pipeline xác định đã ổn định.

## Đe dọa tính hợp lệ

- A direct equivalent may already exist in the final Failing Tools paper or related recovery literature.
- Fault injection may favor rules designed against its taxonomy.
- API nondeterminism and evaluator errors can overwhelm a small study.

## Điều gì đã bác bỏ gap này?

[[references/retry-switch-or-abstain]] là method accessible thực hiện gần đúng điều đó ở core action space. Vì vậy broad gap bị bác bỏ.

## Điều kiện hẹp có thể nghiên cứu về sau

Một condition hẹp có thể còn mở là: `không RL`, `auditable controller`, penalty cho non-idempotent side effect và ground-truth evaluator cho correct human escalation. Nhưng chưa có bằng chứng benchmark công khai phù hợp; không nên xem đây là đề tài 12 tuần hiện tại.

## Liên hệ

- [[synthesis/Deep Comparison - Recovery Routing Anchor Works]]
- [[synthesis/Prior-Art Threat - Recovery-Action Selection]]
