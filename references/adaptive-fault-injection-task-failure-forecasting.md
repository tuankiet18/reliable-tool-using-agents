---
title: >-
  Efficient Forecasting of Task Failures in LLM Agents through Adaptive Fault Injection
category: references
tags: [paper, ai-agents, failure-detection, forecasting, fault-injection]
sources:
  - "https://openreview.net/pdf/f81b4d72b4ac58cbc7ec781bdc3f8e3c705d4650.pdf"
  - "https://openreview.net/forum?id=d3Qq4weuwz"
source_url: https://openreview.net/forum?id=d3Qq4weuwz
summary: >-
  Paper ICML 2026 workshop về dự báo failure từ partial execution trace bằng adaptive fault injection; phát hiện sớm, không phải policy chọn nhiều recovery action.
provenance:
  extracted: 0.83
  inferred: 0.12
  ambiguous: 0.05
base_confidence: 0.90
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: supporting
created: 2026-09-10T00:00:00Z
updated: 2026-09-12T00:00:00Z
---

# Efficient Forecasting of Task Failures in LLM Agents through Adaptive Fault Injection

> [!tldr] Paper dự báo online liệu policy hiện tại có đi tới task failure từ partial trace; đây là failure prediction, không chứng minh việc chọn `retry` hay `fallback` nào là tối ưu.

## Vấn đề và lý do quan trọng

Agent dài hạn có thể có lỗi cục bộ còn cứu được hoặc lỗi khiến policy hiện tại khó thành công. Paper định nghĩa **Task Failure Forecasting** là ước lượng từ prefix trace liệu tiếp tục theo policy hiện tại có dẫn đến failure không, trước khi task kết thúc.

## Agent setting và failure model

Setting là LLM agent dài hạn có tool call và reasoning step. Failure được tạo bằng cách perturb successful trace ở intermediate step; nhãn xác định bằng rollout continuation. Paper phân biệt prefix có rủi ro cao với lỗi vẫn recoverable theo policy hiện tại, không tập trung riêng vào service/API fault.

## Observable signals và thời điểm can thiệp

Đầu vào là partial execution trajectory. Forecaster chạy khi trajectory chưa kết thúc nên về nguyên tắc có thể kích hoạt reflection, resampling hoặc human handoff. Tuy nhiên, phần đã xác minh không nêu một action router chọn giữa các action này theo state.

## Phương pháp và kết quả chính

Từ successful trace, adaptive fault injection dùng multi-armed bandit ưu tiên error category có nhiều high-risk prefix; rollout xác minh nhãn downstream. Paper báo cáo Qwen-3-8B forecaster đạt 78.01% weighted F1, vượt Claude-4.5 Sonnet 18 điểm ở chi phí thấp hơn 100×, và cải thiện agent success 2–16 điểm trên benchmark đa dạng. Đây là số do paper báo cáo, chưa tái lập độc lập.

## Recovery policy: kết luận nghiêm ngặt

**✗ Không có bằng chứng đã xác minh về policy dạng `signals → chọn recovery action`.** Paper dự báo rủi ro của việc *tiếp tục policy hiện tại*. Nó là prior art mạnh cho failure prediction, nhưng không phải prior art trực tiếp cho recovery-action selection.

## Artifact và tính tái lập

- **Trạng thái:** ICML 2026 Forecasting workshop theo trang tác giả; PDF đã xem vẫn mang nhãn anonymous/under review. ^[ambiguous]
- **Code/dataset/license:** chưa tìm thấy repository hoặc license chính thức trong lần kiểm tra cập nhật ngày 2026-09-12.
- **Compute:** huấn luyện Qwen-3-8B forecaster và rollout labeling có thể vượt phạm vi 12 tuần nếu phải tái tạo từ đầu.

## Hạn chế và hàm ý

- Nhãn phụ thuộc rollout của policy; cùng prefix có thể recoverable với policy mạnh hơn. Đây là ý nghĩa đúng của paper, đồng thời khiến nó không trực tiếp trả lời “action nào nên chọn”.
- Synthetic perturbation có thể tạo artifact. Paper cố giảm rủi ro này, nhưng cần kiểm tra code/appendix trước khi dùng làm benchmark. ^[inferred]
- Paper còn kiểm tra khả năng tổng quát qua agent policies theo mô tả đã xác minh; vì vậy “cross-policy failure forecasting” cũng không nên được coi là gap mới chỉ từ intuition.

## Cập nhật novelty gate 2026-09-12

Khi đặt cạnh PrefixGuard, AgentForesight, weakly supervised early alerting, AgentTrajectorySentinel và Automata from Agent Traces, paper này là một phần của cụm prior art trực tiếp. **Kết luận:** broad early failure forecasting từ partial trace đã `REJECTED` về novelty cho project hiện tại.

## Liên hệ

- [[concepts/agent-observability-and-runtime-monitoring]]
- [[synthesis/Deep Comparison - Recovery Routing Anchor Works]]
- [[synthesis/Prior-Art Threat - Recovery-Action Selection]]
- [[synthesis/Research - Early Failure Detection in Tool-Using Agents]]
