---
title: >-
  Research: Reliable Tool-Using AI Agents
category: synthesis
tags: [ai-agents, reliability, tool-use, research, field-map]
sources: [https://arxiv.org/abs/2406.12045, https://arxiv.org/abs/2408.04682, https://arxiv.org/abs/2406.13352, https://arxiv.org/abs/2404.07972, https://arxiv.org/abs/2607.06273, https://arxiv.org/abs/2604.13954, https://arxiv.org/abs/2512.11147, https://openreview.net/pdf/2be5795add6ec19f401efc71c99e69f5dea50e1c.pdf]
summary: >-
  Bản đồ nghiên cứu về AI agent dùng tool đáng tin cậy; recovery routing và broad early failure detection đã bị prior art bác bỏ, các lane khác vẫn cần novelty gate.
provenance:
  extracted: 0.63
  inferred: 0.32
  ambiguous: 0.05
base_confidence: 0.90
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: core
created: 2026-09-09T17:16:31Z
updated: 2026-09-12T00:00:00Z
---

# Nghiên cứu: AI Agent dùng tool đáng tin cậy

`Research: Reliable Tool-Using AI Agents`

## Bức tranh lớn

**FACT:** Benchmark gần đây cho thấy tương tác tool thực tế có state vẫn chưa đáng tin cậy: τ-bench báo cáo GPT-4o thành công dưới 50% task và độ ổn định thấp qua nhiều lần chạy; OSWorld báo cáo baseline rất thấp trong môi trường máy tính thật. Công trình mới đã trực tiếp nghiên cứu định vị quỹ đạo, lỗi tool được kiểm soát, sửa có hướng dẫn từ chẩn đoán, và least-privilege authorization.

**INFERENCE:** Lĩnh vực này mạnh ở việc xây agent, benchmark và can thiệp riêng lẻ. Điểm nối phù hợp nhất với quy mô đồ án đại học có thể là đánh giá có kiểm soát về cách bằng chứng runtime nên chọn một can thiệp—thay vì đề xuất thêm một agent chung chung. ^[inferred]

## Bản đồ vòng đời thực thi

See [[concepts/reliable-tool-using-agent-lifecycle]].

```text
Goal → plan → choose action/tool → execute → observe/update state → verify → control decision
                  │                 │                  │                 │
        wrong capability/privilege   outage/stale/silent  hidden drift     premature DONE
                  │                 │                  │                 │
          authorization/policy   retry/fallback/rollback  monitors       validators/escalation
```

## Các hướng nghiên cứu

| Hướng                                   | Vấn đề cốt lõi và bằng chứng seed mạnh                                            | Hạn chế chưa giải quyết                                              | Đánh giá 12 tuần                                        |
| --------------------------------------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------- |
| A. Phát hiện & phục hồi lỗi             | Dự báo từ partial trace; [[references/failing-tools]]; [[references/agenttether]] | Detection, diagnosis và chọn action thường được đánh giá tách rời    | **Phù hợp cao**; có thể dùng API benchmark và wrapper   |
| B. Least privilege / capability control | [[references/miniscope]], ToolPrivBench, AuthBench                                | Recovery/fallback có thể đổi quyền; cần kiểm tra artifact và so sánh | Trung bình; policy/nhãn security dễ nở phạm vi          |
| C. Độ tin cậy dài hạn                   | [[references/osworld]], SWE-Bench Pro, HINTBench                                  | Lẫn perception, planning, memory và environment drift                | Trung bình-thấp; tốn kém/nhiễu cho dự án đầu tiên       |
| D. Planning khi tool lỗi                | [[references/failing-tools]], ToolSandbox, PlanBench                              | Cần policy retry so với replan/fallback có tính đến tác dụng phụ     | **Phù hợp cao** nếu benchmark sẵn có                    |
| E. Verification / premature completion  | [[references/tau-bench]], [[references/osworld]]                                  | Chi phí và độ bao phủ của verification online chưa rõ                | Trung bình-cao khi là thành phần, yếu nếu đứng một mình |
| F. Observability / runtime monitoring   | [[references/hintbench]], AgentDebugX, AgentTether                                | Localization/generalization và giá trị quyết định online             | Trung bình; tránh train detector mới                    |
| G. Coding-agent reliability             | SWE-bench, SWE-Bench Pro, SWE-Sharp-Bench                                         | Tái lập agent/task đầy đủ tốn kém; benchmark thay đổi nhanh          | Trung bình; chỉ dùng harness hẹp có sẵn                 |

### Khu vực đã đông người nghiên cứu

**FACT:** RAG/chatbot cơ bản, demo multi-agent chung chung, điểm function-calling tĩnh, các biến thể self-reflection và leaderboard benchmark tổng quát đều đã đông người làm. BenchTrace cũng đưa bằng chứng rằng chỉ thêm reflection chưa đủ tạo đóng góp nghiên cứu.

**INFERENCE:** “Luôn reflect/retry/replan” là cách đóng khung can thiệp yếu. Một đóng góp tốt hơn phải xác định rõ điều kiện, policy quyết định có thể quan sát, baseline chặt chẽ và end state được xác minh. ^[inferred]

## Các vấn đề lớn về độ tin cậy

1. Kế hoạch/hành động sai khi quan sát không đầy đủ và có phụ thuộc state ẩn.
2. Tool không hoàn hảo: error, outage, quan sát cũ, schema mismatch và silent write.
3. Định vị lỗi yếu: phát hiện rủi ro ở cấp trajectory dễ hơn tìm ra critical step.
4. Recovery chưa được hiệu chỉnh: retry có thể tốn ngân sách/lặp tác động có hại; replan/fallback có thể không cần thiết hoặc đòi quyền quá cao.
5. Dừng không được xác minh: `DONE` của agent không phải bằng chứng mục tiêu người dùng đã đạt.
6. Biên an toàn: output tool có thể mang tính đối kháng, còn recovery hợp lệ có thể dẫn đến leo thang quyền.

## Trạng thái các research gap đã điều tra

1. [[synthesis/Preliminary Gap - Selective Recovery Routing]] — `REJECTED`: direct recovery-action-selection prior art.
2. [[synthesis/Preliminary Gap - External Runtime Monitoring]] — `REJECTED`: direct online prefix monitoring/forecasting prior art.
3. Capability control — Task-Aware Permission Inference và Progressive Expansion bị `REJECTED`; Software-Evidence-Grounded Scoping chỉ `SURVIVES WITH REFINEMENT`; Risk-Aware Escalation là `WEAK`.
4. [[synthesis/Preliminary Gap - Completion Verification Under Degraded Tools]] — chưa qua adversarial search mới; không được coi là accepted gap.

## Hướng có vẻ khả thi nhất (đã lỗi thời sau prior-art search)

Hướng dẫn đầu trước đây là **selective recovery routing khi tool failure được kiểm soát**:

- Xây wrapper nhỏ bên ngoài, không xây kiến trúc agent mới.
- Dùng API benchmark có kiểm tra goal state thực thi được.
- Thao tác fault persistence và loại tool fault.
- So sánh retry cố định, replan/fallback cố định, self-reflection và selective router minh bạch.
- Đo verified success, chi phí, action trùng/không an toàn và abstention—không chỉ success.

**CẬP NHẬT 2026-09-10:** Broad idea này bị [[references/retry-switch-or-abstain]] phủ trực tiếp. Xem [[synthesis/Prior-Art Threat - Recovery-Action Selection]]. Không tạo candidate RQ cho hướng này.

## Bằng chứng cần có tiếp theo — cập nhật 2026-09-12

1. Không chọn broad recovery routing hoặc broad early failure detection.
2. Giữ [[references/toolbench-x]] làm secondary stress test, không làm benchmark chính.
3. Kiểm tra adversarial nhánh task-grounded runtime semantic verification cho schema-valid silent tool output; xem [[synthesis/Research - Early Failure Detection in Tool-Using Agents]].

## Sources Consulted

- [[references/tau-bench]]
- [[references/toolsandbox]]
- [[references/failing-tools]]
- [[references/agenttether]]
- [[references/hintbench]]
- [[references/benchtrace]]
- [[references/miniscope]]
- [[references/agentdojo]]
- [[references/osworld]]
- [[references/seed-papers-and-benchmarks-reliable-agents]]
