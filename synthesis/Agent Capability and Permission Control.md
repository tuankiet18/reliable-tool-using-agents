---
title: "Agent Capability and Permission Control"
category: synthesis
tags: [ai-agents, authorization, least-privilege, research, security]
sources:
  - https://arxiv.org/abs/2504.11703
  - https://arxiv.org/abs/2605.14859
  - https://arxiv.org/abs/2606.20023
  - https://arxiv.org/abs/2607.27267
  - https://arxiv.org/abs/2606.25189
summary: "Bản đồ adversarial về task-scoped least privilege: nhiều thành phần đã có prior art; software-evidence scoping còn cần kiểm chứng khắt khe về ground truth."
provenance: {extracted: 0.83, inferred: 0.14, ambiguous: 0.03}
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# Kiểm soát capability / permission cho AI Agent

## Taxonomy: đừng gộp các bài toán khác nhau

| Khái niệm | Cái được kiểm soát | Điều không suy ra được |
|---|---|---|
| Sandboxing | Container, VM, filesystem hoặc OS resource isolation | Không tự suy ra agent chỉ có đúng quyền cần thiết. |
| Static permissions | Allowlist/denylist định trước | Không thích nghi theo task hay execution state. |
| Task-scoped permissions | Authority suy từ user task và environment | Chưa chắc tối thiểu hoặc đúng khi task thay đổi. |
| Dynamic capability expansion | Policy/capability thay đổi khi runtime có observation mới | Không tự chứng minh expansion là cần thiết hay an toàn. |
| Failure-aware expansion | Failure/blocked action là một evidence cho request quyền | Failure không phải bằng chứng đủ để grant rộng hơn. |
| Least privilege | Tối thiểu authority nhưng vẫn hoàn thành task | Cần ground truth hoặc proxy chặt để đo. |

## Bức tranh evidence

[[references/authbench]] đã đánh giá task-to-file-policy inference trước execution. [[references/progent]] sinh policy theo task, cập nhật runtime, formal-check expansion/narrowing, và có human approval. [[references/toolprivbench]] đo over-privileged tool selection, kể cả escalation sau transient failure. [[references/fava]] formalize context/dataflow-aware authorization trước effectful call. [[references/actplane]] đưa task context xuống OS-level enforcement. Vì vậy, “xây permission system động” hay “thêm human approval” **không phải** contribution đủ mới.

| Dimension | AuthBench | Progent | ToolPrivBench | FAVA | ActPlane |
|---|---:|---:|---:|---:|---:|
| task-specific permission inference | ✓ | ✓ | △ | ✓ | △ |
| dynamic permission changes | ✗ | ✓ | △ | ✓ | ✓ |
| temporary grant / revocation | ✗ | △ | ✗ | △ | △ |
| runtime evidence | ✗ | ✓ | ✓ | ✓ | ✓ |
| failure-aware expansion | ✗ | △ | ✓ | ✗ | ✗ |
| human approval | ✗ | ✓ | ✗ | ✗ | ✗ |
| least-privilege objective | ✓ | ✓ | ✓ | △ | ✗ |
| over-privilege metric | ✓ | △ | ✓ | △ | ✗ |
| task-success metric | ✓ | ✓ | △ | △ | ✓ |
| fine-grained permission | path/RWX | tool/argument | tool level | capability/dataflow | syscall/action |
| coding-agent setting | ✓ | △ | △ | △ | ✓ |
| public benchmark/code | ? / ? | ✓ / ✓ | ✓ / ✓ | ? / ? | ? / ✓ |
| reproducible in 12 weeks | ? | △ | ✓ (evaluate only) | ? | △ |

**Legend:** ✓ rõ ràng; △ một phần/khác abstraction; ✗ vắng; ? chưa đủ evidence. “public” chỉ nói artifact được xác minh trong research pass, không khẳng định license tương thích.

## Contradictions có giá trị nghiên cứu

**FACT:** AuthBench thấy direct policy generation vừa thiếu quyền cần thiết vừa dư quyền nhạy cảm; ToolPrivBench thấy transient failure làm tăng over-privileged escalation; Progent cho expansion cần approval và báo cáo chi phí approval thấp trong AgentDojo.

**INFERENCE:** Mâu thuẫn đáng nghiên cứu không còn là “có dynamic permissions không?”, mà là liệu software evidence độc lập có thể làm policy *tighter* mà không hại completion, và đo điều đó bằng ground truth nào. Chưa có bằng chứng đủ để coi đây là gap mạnh.

## Ground truth: vấn đề quyết định

- AuthBench: human-reviewed $S_{gold}$ + safe oracle execution + validators; chính xác cho benchmark nhưng static proxy, không universal minimal policy.
- ToolPrivBench: annotator xác nhận từng tool independently sufficient; mạnh cho substitution/escalation, yếu cho multi-tool/repository workflow.
- Progent/FAVA/ActPlane: đánh giá compliance/security/utility với policy hoặc constraint đã cho; không thiết lập canonical minimal permission set.

**OPEN QUESTION:** Có thể tạo ground truth tái lập cho coding task bằng counterfactual permission removal trên một reference execution, sau đó human review các quyền thay thế hay không? Nếu không, claim “least privilege” sẽ đo proxy thay vì minimum authority.

## 12-week gate

ToolPrivBench là artifact khả thi nhất để reproduce evaluation, nhưng trực tiếp đã bao phủ failure-driven privilege escalation. AuthBench phù hợp nhất về coding/path permissions nếu artifact được xác minh, song chỉ 120 tasks và static phase. Một benchmark mới có repository + dependency graph + counterfactual oracle có nguy cơ thành dataset engineering; không nên bắt đầu khi chưa pilot được 10–20 tasks.

## Current status

- [[synthesis/Preliminary Gap: Task-Aware Permission Inference]] — **REJECTED**.
- [[synthesis/Preliminary Gap: Software-Evidence-Grounded Capability Scoping]] — **SURVIVES WITH REFINEMENT, PRELIMINARY**.
- [[synthesis/Preliminary Gap: Progressive Capability Expansion]] — **REJECTED**.
- [[synthesis/Preliminary Gap: Risk-Aware Human Escalation for Permissions]] — **WEAK, PRELIMINARY**.
