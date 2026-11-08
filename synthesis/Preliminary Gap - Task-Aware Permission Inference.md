---
title: "Preliminary Gap: Task-Aware Permission Inference"
category: synthesis
tags: [research-gap, preliminary, authorization, coding-agents]
sources: [https://arxiv.org/abs/2605.14859, https://arxiv.org/abs/2504.11703]
summary: "REJECTED: AuthBench trực tiếp benchmark task-to-file permission inference; Progent cũng sinh policy từ task."
provenance: {extracted: 0.94, inferred: 0.05, ambiguous: 0.01}
base_confidence: 0.94
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# REJECTED — Task-Aware Permission Inference

## Gap statement đã bị kiểm tra

“Tự suy ra minimal capability set từ task” đã được AuthBench formalize và benchmark trực tiếp ở file-level R/W/X. Progent còn sinh initial tool/argument policy từ task.

## Evidence bác bỏ

- [[references/authbench]] có 120 terminal tasks, permission specification do người rà soát, executable validator, baseline Full-Access/Golden-Perm và STD.
- [[references/progent]] tạo task-specific policy và enforce nó ở runtime.

## Kết luận

**REJECTED.** Một thay đổi prompt, framework hoặc stack không tạo khác biệt nghiên cứu đủ lớn. Bất kỳ proposal nào chỉ “dùng task + LLM để sinh quyền” sẽ overlap trực tiếp.

## Điều không biến nó thành gap mới

AuthBench chưa có dynamic execution, nhưng chuyển sang dynamic permission nói chung cũng overlap Progent/FAVA; xem [[synthesis/Preliminary Gap - Progressive Capability Expansion]].
