---
title: >-
  Thuật ngữ nghiên cứu về AI Agent dùng tool đáng tin cậy
category: concepts
tags: [ai-agents, reliability, glossary, tool-use]
sources: [https://arxiv.org/abs/2406.12045, https://arxiv.org/abs/2408.04682, https://arxiv.org/abs/2607.06273, https://arxiv.org/abs/2512.11147, https://arxiv.org/abs/2603.02345, https://doi.org/10.1109/TSE.1986.6312924]
summary: >-
  Glossary tiếng Việt cho các thuật ngữ cốt lõi về độ tin cậy, phục hồi, xác minh, giám sát và phân quyền của AI agent dùng tool.
provenance:
  extracted: 0.50
  inferred: 0.50
  ambiguous: 0.00
base_confidence: 0.84
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-13T00:00:00Z
---

# Thuật ngữ nghiên cứu về AI Agent dùng tool đáng tin cậy

## Agent Recovery

**Tiếng Việt:** Khả năng/phương pháp phục hồi của agent.

**Ý nghĩa:** Các bước đưa agent trở lại quá trình hoàn thành mục tiêu sau khi có lỗi hoặc dấu hiệu lệch hướng.

**Trong research này:** Đây là outcome chính của hướng selective recovery routing.

**Related:** [[concepts/agent-recovery-policy]], [[concepts/reliable-tool-using-agent-lifecycle]]

## Failure Detection

**Tiếng Việt:** Phát hiện lỗi.

**Ý nghĩa:** Nhận ra agent hoặc tool có thể đã/sắp thực thi sai.

**Trong research này:** Detection là tín hiệu đầu vào, chưa phải quyết định recovery.

**Related:** [[concepts/agent-observability-and-runtime-monitoring]]

## Failure Diagnosis

**Tiếng Việt:** Chẩn đoán lỗi.

**Ý nghĩa:** Xác định lỗi nằm ở đâu, loại gì và vì sao nó dẫn đến thất bại.

**Trong research này:** Cần phân biệt chẩn đoán với việc chỉ phát hiện task đã thất bại.

**Related:** [[references/agenttether]], [[references/hintbench]]

## Execution Trajectory

**Tiếng Việt:** Quỹ đạo thực thi.

**Ý nghĩa:** Chuỗi reasoning, action, tool call, observation và state update của một lần chạy agent.

**Trong research này:** Router/monitor có thể sử dụng trace của quỹ đạo thay vì chỉ nhìn kết quả cuối.

**Related:** [[concepts/reliable-tool-using-agent-lifecycle]]

## Runtime Monitoring

**Tiếng Việt:** Giám sát lúc chạy.

**Ý nghĩa:** Theo dõi agent trong khi thực thi để phát hiện tín hiệu cần can thiệp.

**Trong research này:** Được so sánh với self-assessment của agent.

**Related:** [[concepts/agent-observability-and-runtime-monitoring]]

## Tool Failure

**Tiếng Việt:** Lỗi công cụ.

**Ý nghĩa:** Tool trả error, không khả dụng, trả dữ liệu cũ, sai schema hoặc silent failure.

**Trong research này:** Đây là điều kiện thực nghiệm chính, đặc biệt là khác biệt giữa lỗi tạm thời và kéo dài.

**Related:** [[references/failing-tools]], [[references/toolsandbox]]

## Retry

**Tiếng Việt:** Thử lại.

**Ý nghĩa:** Thực hiện lại action/tool call trước đó.

**Trong research này:** Là baseline đơn giản; chỉ hợp lý nếu lỗi có thể là tạm thời và action an toàn để lặp lại.

**Related:** [[concepts/agent-recovery-policy]]

## Replanning

**Tiếng Việt:** Lập kế hoạch lại.

**Ý nghĩa:** Tạo kế hoạch mới từ trạng thái hiện tại khi giả định hoặc capability đã thay đổi.

**Trong research này:** Baseline recovery mạnh hơn retry nhưng có thể tốn token/tool call.

**Related:** [[concepts/agent-recovery-policy]]

## Fallback

**Tiếng Việt:** Phương án thay thế.

**Ý nghĩa:** Dùng tool, provider hoặc chuỗi hành động khác để đạt cùng mục tiêu.

**Trong research này:** Fallback có thể tăng thành công nhưng cũng có thể đòi hỏi quyền cao hơn.

**Related:** [[concepts/least-privilege-tool-use]]

## Rollback

**Tiếng Việt:** Hoàn tác.

**Ý nghĩa:** Đưa state bên ngoài về trước action gây lỗi hoặc có nguy cơ gây tác dụng phụ.

**Trong research này:** Quan trọng với action không idempotent, nhưng chỉ nghiên cứu nếu benchmark hỗ trợ.

**Related:** [[concepts/agent-recovery-policy]]

## Human Escalation

**Tiếng Việt:** Leo thang cho con người xử lý.

**Ý nghĩa:** Agent dừng tự động và yêu cầu người dùng/người vận hành quyết định.

**Trong research này:** Một hình thức abstention có thể an toàn hơn retry mù quáng.

**Related:** [[concepts/agent-recovery-policy]]

## Goal-State Verification

**Tiếng Việt:** Xác minh trạng thái mục tiêu.

**Ý nghĩa:** Kiểm tra độc lập xem state cuối có thỏa mục tiêu/ràng buộc hay không.

**Trong research này:** Metric thành công chính phải dựa trên goal state, không dựa trên lời agent tự báo.

**Related:** [[concepts/agent-verification-and-premature-completion]], [[references/tau-bench]]

## Premature Task Completion

**Tiếng Việt:** Kết thúc nhiệm vụ quá sớm.

**Ý nghĩa:** Agent báo/dừng hoàn thành khi mục tiêu thực sự chưa được xác minh là đạt.

**Trong research này:** Một loại lỗi cần đo nếu tool có silent failure hoặc output cũ.

**Related:** [[concepts/agent-verification-and-premature-completion]]

## Idempotency

**Tiếng Việt:** Tính lặp lại an toàn.

**Ý nghĩa:** Lặp cùng action một hay nhiều lần vẫn cho hiệu ứng tương đương một lần.

**Trong research này:** Đây là điều kiện quan trọng trước khi retry action có tác dụng lên state.

**Related:** [[concepts/agent-recovery-policy]]

## Least-Privilege Control

**Tiếng Việt:** Kiểm soát đặc quyền tối thiểu.

**Ý nghĩa:** Chỉ cho agent quyền tối thiểu cần để hoàn thành tác vụ.

**Trong research này:** Đo đánh đổi an toàn–utility khi recovery muốn dùng tool có quyền cao hơn.

**Related:** [[concepts/least-privilege-tool-use]], [[references/miniscope]]

## Over-Privileged Tool Selection

**Tiếng Việt:** Chọn tool có quyền quá mức cần thiết.

**Ý nghĩa:** Agent dùng hoặc leo thang lên tool nhiều quyền hơn dù tool ít quyền đã đủ.

**Trong research này:** Có thể tăng khi tool cấp thấp gặp transient failure.

**Related:** [[concepts/least-privilege-tool-use]]

## External Runtime Monitor

**Tiếng Việt:** Bộ giám sát lúc chạy bên ngoài.

**Ý nghĩa:** Thành phần tách khỏi acting agent, đọc event/trace để đưa cảnh báo hoặc can thiệp.

**Trong research này:** Ứng viên để giảm thiên lệch tự đánh giá của agent.

**Related:** [[synthesis/Preliminary Gap: External Runtime Monitoring]]

## Selective Recovery Routing

**Tiếng Việt:** Định tuyến phục hồi có chọn lọc.

**Ý nghĩa:** Policy chọn recovery action theo tín hiệu và bối cảnh thay vì luôn áp một chiến lược cố định.

**Trong research này:** Hướng rộng này đã bị `REJECTED` vì direct prior art; giữ thuật ngữ để đọc các note lịch sử.

**Related:** [[synthesis/Preliminary Gap: Selective Recovery Routing]]

## Fault Persistence

**Tiếng Việt:** Tính kéo dài của lỗi.

**Ý nghĩa:** Lỗi tạm thời có thể tự hết; lỗi kéo dài cần thay đổi cách làm hoặc dừng.

**Trong research này:** Biến độc lập cốt lõi để kiểm tra retry và replanning.

**Related:** [[references/failing-tools]], [[concepts/agent-recovery-policy]]

## Recovery Router

**Tiếng Việt:** Bộ định tuyến phục hồi.

**Ý nghĩa:** Cơ chế nhận tín hiệu runtime rồi chọn continue, retry, replan/fallback, rollback, escalate hoặc stop.

**Trong research này:** Can thiệp tối thiểu có thể triển khai như wrapper độc lập với agent framework.

**Related:** [[concepts/agent-recovery-policy]], [[synthesis/Preliminary Gap: Selective Recovery Routing]]

## Common-Mode Failure

**Tiếng Việt:** Lỗi chung nguyên nhân.

**Ý nghĩa:** Nhiều component cùng fail vì phụ thuộc một nguyên nhân chung, ví dụ hai tool khác API nhưng cùng đọc một stale database replica.

**Trong research này:** Đây là fault regime chính để kiểm tra liệu cross-tool agreement có tạo false confidence hay không.

**Related:** [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]], [[references/riva]]

## Failure Domain

**Tiếng Việt:** Miền lỗi / nhóm phụ thuộc có thể cùng hỏng.

**Ý nghĩa:** Tập component chia sẻ resource hoặc failure mechanism, nên một lỗi có thể ảnh hưởng cả tập.

**Trong research này:** Selector phải ưu tiên evidence từ các failure domain khác nhau, không chỉ tool name khác nhau.

**Related:** [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]

## Provenance-Aware Verification

**Tiếng Việt:** Xác minh có xét nguồn gốc và dependency của evidence.

**Ý nghĩa:** Khi kiểm tra một claim/tool output, hệ thống biết evidence đến từ source/backend nào và có chia sẻ failure domain với evidence ban đầu hay không.

**Trong research này:** Đây là biến can thiệp của candidate RQ, không đồng nghĩa với generic citation tracking.

**Related:** [[synthesis/Research: Correlated Silent Tool Failures and Verification]]

## Fixed-K Cross-Validation

**Tiếng Việt:** Kiểm tra chéo bằng số lượng `K` đường kiểm chứng cố định.

**Ý nghĩa:** Hệ thống chỉ kết luận sau khi thu đủ `K` tool calls hoặc diagnostic paths.

**Trong research này:** Đây là baseline gần với RIVA; hạn chế là `K` distinct calls không bảo đảm evidence độc lập.

**Related:** [[references/riva]], [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]
