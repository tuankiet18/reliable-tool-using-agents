---
title: "Introducing Safe LLM-Agent Execution via Typed Tool Mediation and World-Effect Evaluation"
category: reference
tags: [ai-agents, runtime-monitoring, authorization, prior-art, verification]
sources:
  - "https://conf.researchr.org/details/ase-2026/ase-2026-tools-and-data-sets/45/Introducing-Safe-LLM-Agent-Execution-via-Typed-Tool-Mediation-and-World-Effect-Evalua"
  - "https://github.com/zhoujune/AgentOS"
  - "https://github.com/zhoujune/AgentOS/tree/4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c"
  - "https://zenodo.org/records/20046861"
created: 2026-10-03T21:46:13+07:00
updated: 2026-10-04T10:04:00+07:00
summary: >-
  AgentOS đã audit code/evaluation và task archives tại commit pin; full paper vẫn chưa đọc được. Không đồng nhất authorization với business-truth verification.
provenance:
  extracted: 0.65
  inferred: 0.25
  ambiguous: 0.10
base_confidence: 0.60
lifecycle: draft
tier: supporting
---

# Introducing Safe LLM-Agent Execution via Typed Tool Mediation and World-Effect Evaluation

## Metadata và phạm vi đọc

**FACT — METADATA VERIFIED:** Jun Zhou, Tao Jia; ASE 2026 Tools and Datasets, DOI `10.1145/3832783.3834637`, được liệt kê trong official program. Hội nghị chưa diễn ra tại ngày audit. **Chưa đọc full paper**, không trích quantitative result hoặc khẳng định đã reproduce.

### Cập nhật phạm vi đọc — 2026-10-04

**FACT — CODE/ARTIFACT INSPECTION:** Đã đọc README, boundary/schema/assumption documents, formal-model README; các đoạn liên quan trong VTRM, capability derivation, authorization policy, snapshot/diff và evaluation harness; hai task JSON. Pin repository: `4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c`. Đây là targeted source inspection, không tuyên bố đọc mọi file trong repo.

**FACT — FULL PAPER UNREAD:** Publisher PDF trả HTTP 403 trong lượt này. Code hiện hành không được mặc nhiên xem là đúng phiên bản dùng để tạo paper results. Không chạy QEMU, TLC, benchmark hoặc model API.

## Problem và động cơ

AgentOS đặt bộ kiểm soát quyền trước thực thi (reference monitor) giữa agent và công cụ có side effects. Một output “thành công” của agent không đủ chứng minh hệ thống bên ngoài vẫn an toàn; evaluation phải nhìn thay đổi thực tế, không chỉ câu trả lời. [Pinned README](https://github.com/zhoujune/AgentOS/blob/4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c/README.md).

## Agent setting, permission model và method

**FACT — IMPLEMENTATION:** Môi trường Buildroot/QEMU; tool operations gồm filesystem, database và network. VTRM chuẩn hóa/validate request, phân loại object/sink, suy ra capability rồi quyết định `auto`, `approval_required` hoặc `deny`. Capability và content label do model tự khai không được tin trực tiếp. `execute()` kiểm tra policy trước operation, từ chối mutation nếu audit không khả dụng. [VTRM core, `normalize_request` và `execute`](https://github.com/zhoujune/AgentOS/blob/4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c/br2-external/board/agentos/x86_64/overlay/home/agent/vtrm/vtrm_core.py).

**FACT — POLICY INPUTS:** `CapabilityDeriver.derive` nhận tool và class của path/database/sink, không phải oracle về việc task có thực sự cần hành động đó. Default profile cho phép một số workspace/mutable operations, yêu cầu approval cho secret/protected/external operations, và có absolute-deny rules. Đây là quyền được phép thực thi, chưa đồng nghĩa tính đúng của mục tiêu nghiệp vụ. [Capability derivation](https://github.com/zhoujune/AgentOS/blob/4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c/br2-external/board/agentos/x86_64/overlay/home/agent/vtrm/capability_deriver.py), [Authorization policy](https://github.com/zhoujune/AgentOS/blob/4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c/br2-external/board/agentos/x86_64/overlay/home/agent/vtrm/authorization_policy.py).

## Evaluation, ground truth và metrics

**FACT — HARNESS:** World Effect Judge ở phía host so sánh snapshot trước/sau, gồm filesystem, SQLite và HTTP sink. `evaluate_world_integrity` kiểm tra changed paths với allowed/forbidden prefixes và network violations. `evaluate_task_completion` xét trạng thái run cùng predicates được task khai báo: path tồn tại/vắng mặt, nội dung file và tùy chọn answer matching. Với `should_fail` tasks, completion check bị bỏ qua; safety được chấm riêng. [Evaluation harness, functions ở dòng 481–624 và 858–887](https://github.com/zhoujune/AgentOS/blob/4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c/judge/run_vtrm_eval.py), [Judge README](https://github.com/zhoujune/AgentOS/blob/4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c/judge/README.md).

**INFERENCE — GIỚI HẠN ORACLE CỤ THỂ:** Task `322-delete-mutable-db-row` yêu cầu xóa một row rồi ghi marker file. Expected schema kiểm tra marker và phạm vi mutation, nhưng không có predicate riêng xác nhận row mục tiêu đã vắng mặt. Do đó không được diễn giải mọi `task_completion_ok` thành hoàn thành đầy đủ ngữ nghĩa nghiệp vụ. Đây là khả năng thiếu coverage suy từ một task/harness, **chưa chạy counterexample**, không kết luận toàn benchmark sai. [Task JSON](https://github.com/zhoujune/AgentOS/blob/4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c/judge/tasks_should_pass/322_delete_mutable_db_row.json).

Baselines: harness có modes `agentos`, `cot`, `naive`; chưa audit toàn bộ agent runtimes để khẳng định mọi khác biệt ngoài monitor được kiểm soát. **Main Results:** chỉ biết author-reported abstract tại program; không lấy đó làm quantitative result đã kiểm chứng hoặc làm head-to-head với project.

## Assumptions và giới hạn formal guarantee

**FACT — AUTHOR/ARTIFACT-STATED:** Security boundary phụ thuộc tất cả operations liên quan đi qua VTRM và các classifier/runtime components đúng. Formal artifact chỉ mô hình một monitor core trừu tượng; không chứng minh toàn Python implementation, OS, VM, bridge hoặc toàn approval workflow đúng. [Assumptions](https://github.com/zhoujune/AgentOS/blob/4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c/docs/B4_ASSUMPTIONS.md), [Formal README](https://github.com/zhoujune/AgentOS/blob/4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c/formal/README.md).

**INFERENCE:** Cũng như study của mình, guarantee có điều kiện phải đi kèm phạm vi trusted components. “Có formal model” không tự là “mọi hành động hợp business truth”; “được phép ghi database” cũng không tự là “refund đúng người/đúng số tiền”. Đây là phân biệt construct, không một measured weakness của AgentOS.

## Artifact availability và reproducibility gate

**FACT — DOWNLOAD VERIFIED:** Hai archives từ Zenodo tải được, ZIP integrity và MD5 đều khớp metadata; JSON parse được. Có 24 `should_pass` và 48 `should_fail` tasks (24 direct, 24 injection). Không tải VM images hoặc chạy episodes. [Official record](https://zenodo.org/records/20046861), [Metadata API](https://zenodo.org/api/records/20046861).

| Artifact | SHA-256 đã kiểm tra |
|---|---|
| `tasks_should_pass.zip` | `bdb97e67a245f496044e2f507ac219778e88c006dacdcc7ea61fcf6b10d8ea21` |
| `tasks_should_fail.zip` | `6e910cdbf34888c3a1be50fe3311129fe21d6556fa76b77f77363ebec7db9ab3` |

README dùng API-compatible runtime, default `kimi-k2-0905-preview`; benchmark host cần Python/QEMU và filesystem tools. Có system images trên Zenodo. Chi phí model, baseline fairness, GPU needs khi đổi sang local model và khả năng rerun trên máy mình: **chưa đo**. Không đề xuất chuyển benchmark giữa chừng.

**LICENSE UNCERTAINTY:** Program mô tả MIT-licensed code; Zenodo metadata ghi `CC-BY-4.0` cho record. Không thấy root `LICENSE` trong pinned tree. Có thể các artifact có license khác nhau; chưa xác minh quyền redistribution từng thành phần. Repo public không tự giải quyết licensing. Lượt này chỉ lưu audit, không đưa third-party archives vào research repo.

## What this work does NOT establish trong evidence đã đọc

- Chưa có evidence trong các đoạn code/tasks đã inspect về experiment chọn independent failure-domain corroborator so với random ở matched `K=2` dưới shared-backend silent corruption.
- Đây là **negative inspection result**, không tuyên bố full paper hoặc mọi code không có khả năng đó.
- Không có head-to-head nên không nói AgentOS chắc chắn fail trên faults của project.

## My critique / Research implication

**INFERENCE — THREAT: PARTIAL.** AgentOS bác bỏ framing rộng về novel pre-execution monitor, approval workflow và world-effect scoring. Điểm đối chiếu hẹp còn lại là **nguồn evidence quyết định authorization có độc lập với lỗi của primary hay không**; project chỉ characterize điều này trong topology tự định nghĩa.

**OPEN QUESTION:** Khi cần substantive paper-level contrast, phải đọc bản paper tác giả/publisher và map code snapshot với published experiments. Không được biến access failure thành bằng chứng về khoảng trống nghiên cứu.

## Related

- [[projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03]]
- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]]
- [[references/look-before-you-leap-pre-action-verification]]
- [[concepts/least-privilege-tool-use]]
- [[concepts/agent-verification-and-premature-completion]]
- [[journal/2026-10-04-pre-action-prior-art-audit]]
