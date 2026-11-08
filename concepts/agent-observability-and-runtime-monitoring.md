---
title: >-
  Agent Observability and Runtime Monitoring
category: concepts
tags: [ai-agents, observability, runtime-monitoring, diagnosis]
sources: [https://arxiv.org/abs/2607.18754, https://arxiv.org/abs/2607.06273, https://arxiv.org/abs/2604.13954]
summary: >-
  Phát hiện, định vị và chẩn đoán lỗi agent dựa trên bằng chứng trong trace, trong hoặc sau khi agent dùng tool thực thi.
provenance:
  extracted: 0.67
  inferred: 0.33
  ambiguous: 0.00
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: supporting
created: 2026-09-09T17:16:31Z
updated: 2026-09-12T00:00:00Z
---

# Khả năng quan sát và giám sát lúc chạy của AI Agent

`Agent Observability and Runtime Monitoring`

**FACT:** HINTBench báo cáo phát hiện rủi ro tốt ở cấp quỹ đạo nhưng strict F1 dưới 35 khi định vị bước rủi ro. AgentDebugX và AgentTether xử lý attribution kết hợp repair, với kết quả được báo cáo trong các setting riêng của chúng.

**RESOLVED 2026-09-12:** External monitor có thể cảnh báo trước terminal failure với false-alarm/lead-time được hiệu chỉnh và chi phí thấp; PrefixGuard, AgentForesight, weakly supervised alerting và AgentTrajectorySentinel cung cấp direct evidence. Broad claim không còn là research gap. Phần còn chưa chắc là semantic verification cho schema-valid silent tool output khi telemetry không chứa anomaly đủ quan sát được.

Xem [[synthesis/Research - Early Failure Detection in Tool-Using Agents]].
