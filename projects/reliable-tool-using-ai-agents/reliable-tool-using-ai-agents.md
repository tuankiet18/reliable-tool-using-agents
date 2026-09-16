---
title: >-
  Reliable Tool-Using AI Agents — Undergraduate Research Project
category: project
tags: [ai-agents, reliability, tool-use, software-engineering, research]
sources: []
summary: >-
  Dự án 12 tuần, dựa trên bằng chứng, nghiên cứu phát hiện, chẩn đoán, phục hồi, xác minh và kiểm soát đặc quyền tối thiểu cho AI agent dùng tool.
provenance:
  extracted: 0.00
  inferred: 0.90
  ambiguous: 0.10
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-09-09
tier: core
created: 2026-09-09T17:16:31Z
updated: 2026-09-15T17:15:00+07:00
---

# AI Agent dùng tool đáng tin cậy

`Reliable Tool-Using AI Agents — Undergraduate Research Project`

Mục tiêu của dự án là tìm và kiểm chứng một can thiệp về độ tin cậy được xác định rõ cho AI agent dùng tool (tool-using AI agent). Đầu ra mong muốn là một đóng góp thực nghiệm có thể tái lập, không phải một ứng dụng agent chung chung. Bản đồ lĩnh vực ban đầu nằm tại [[synthesis/Research: Reliable Tool-Using AI Agents]].

## Phạm vi và ràng buộc

- 12 tuần; không huấn luyện foundation model; chỉ dùng API/local model và Docker với chi phí vừa phải.
- Ưu tiên benchmark có thể chạy được, quỹ đạo thực thi (execution trajectory) có thể quan sát, và metric rõ ràng về hiệu quả, chi phí, an toàn.
- Ưu tiên agent gọi API tool; chỉ dùng coding agent khi benchmark tái lập được và mô hình quyền truy cập đủ rõ.

## Câu hỏi đã loại bỏ

- `Selective Recovery Routing`: `REJECTED` vì direct prior art đã chọn động retry/switch/abstain/replan.
- Broad `Early Failure Detection from Execution Trajectories`: `REJECTED` vì nhiều work 2026 đã làm prefix prediction, controlled failures, calibration, transfer và intervention.
- Không tiếp tục xây ToolBench-X hoặc local 20–30-task harness như thesis contribution.

## Candidate RQ hiện tại

**PRELIMINARY:**

> Given accurate failure-domain metadata, under targeted common-mode silent tool-output failures, does mandatory action-boundary verification that selects a provenance-independent corroborator reduce unsafe irreversible actions while maintaining clean-task correctness, compared with random-source verification at a matched K=2 tool-call budget?

Giải thích và thiết kế thực nghiệm nằm tại [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]. Đây là RQ tốt nhất hiện tại sau novelty gate, chưa phải thesis topic được xác nhận.

Exploratory pilot gồm `600` paired episodes đã hoàn tất. Kết quả cho thấy safety gain đi kèm abstention cost, vì vậy main study phải đo trade-off thay vì chỉ detection recall.

Gate tiếp theo gồm `3,600` deterministic episodes trên 30 disjoint tasks và hai partial local-model subsets đã hoàn tất. Accurate provenance giảm unsafe acceptance so với random-K, nhưng expected-loss gain chỉ rõ khi abstention rất rẻ; wrong metadata làm gain suy giảm nhanh. Full live-agent validation chưa pass. Xem [[journal/2026-09-14-correlated-tool-verification-next-gate]].

Full live-agent gate tiếp theo đã chạy đủ `36` episodes trên sáu tasks bằng local `Qwen2.5-1.5B-Instruct`. Gate **fail experimental validity**: self-verification compliance bằng zero, enforced verification coverage chỉ `50–67%`, và reply completion thấp. Candidate RQ chưa bị bác bỏ hoàn toàn vì có cả positive lẫn negative cases, nhưng phải chuyển điểm kiểm tra sang action boundary trước `issue_refund`. Xem [[journal/2026-09-14-full-live-agent-verification-gate]].

Action-boundary gate sau đó chạy `108` episodes và pass mechanism gate: `69/69` refund attempts được verified; dưới targeted common-mode fault, provenance đạt unsafe refund `0/18` so với random-K `2/18`, và accuracy `11/18` so với `6/18`. RQ hẹp hiện được giữ làm candidate RQ chính, vẫn `PRELIMINARY` do fault topology synthetic và chưa external validation.

Main deterministic study hiện đã có fresh frozen split gồm `30` tasks (`INS-00060`–`INS-00089`), tách hoàn toàn khỏi mọi pilot trước đó và có SHA-256 ghi trước main harness. Xem [[synthesis/Protocol: Action-Boundary Provenance Verification Main Study]] và [[journal/2026-09-15-main-study-manifest]].

Main deterministic gate sau đó đã chạy đủ `1,350` episodes và `PASS` toàn bộ preregistered criteria. Targeted common-mode unsafe refund giảm từ `0.200` (`random_k`) xuống `0.000` (`provenance_k`), paired 95% CI `[-0.273, -0.127]`; clean correctness của cả hai là `1.000`. RQ được hỗ trợ trong controlled benchmark nhưng gap vẫn `PRELIMINARY`, vì effect phụ thuộc accurate synthetic failure-domain metadata. Xem [[journal/2026-09-15-action-boundary-main-study]].

Post-main robustness gate chạy thêm `3,750` episodes trên task IDs `INS-00090`–`INS-00119`. Gate `FAIL ROBUSTNESS`: accurate và missing-label conditions giữ advantage, nhưng `wrong_25 + leakage 0.10` có CI chạm zero. Vì vậy RQ đã được thu hẹp rõ thành **given accurate failure-domain metadata**; không claim robustness với metadata sai. Xem [[journal/2026-09-15-imperfect-provenance-robustness-gate]].

Adversarial prior-art gate cho metadata/source selection đã hoàn tất. TEA-CXA, hai work tên ProvenanceGuard, GRADE và AgentFlow bác bỏ novelty claims rộng về learned tool trust, provenance-based action gating và dependency derivation/validation. Exact RQ chỉ sống ở tổ hợp hẹp về failure-domain-independent corroboration dưới correlated silent failures; status vẫn `SURVIVES WITH REFINEMENT — PRELIMINARY`. Không mở thêm metadata-learning subproject. Xem [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]].

External-validity artifact gate tiếp theo cho kết quả âm quan trọng. EnvTrustBench không public executable cases/oracles/runners nên không thể dùng để chạy external experiment hiện tại. ProvenanceGuard artifact setup và offline notebooks pass, cung cấp 182 Agent-SafetyBench cùng 388 WorkBench traces, nhưng không có failure domains hoặc redundant evidence. Nó chỉ phù hợp làm nguồn task semantics cho benchmark-derived secondary pilot. Xem [[journal/2026-09-15-external-validity-artifact-gate]].

Living paper version `0.1` đã được mở tại [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]. Draft hiện có Introduction, Related Work, Problem Formulation, Methodology, Results, Discussion, Threats to Validity và working references. [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]] giữ ranh giới giữa supported, preliminary, inferred và rejected claims; mọi result mới phải cập nhật ledger trước manuscript.

## Khái niệm chính

- [[concepts/reliable-tool-using-agent-lifecycle]]
- [[concepts/agent-reliability-research-lanes]]
- [[concepts/agent-recovery-policy]]
- [[concepts/agent-verification-and-premature-completion]]
- [[concepts/least-privilege-tool-use]]
- [[concepts/reliable-tool-using-ai-agents-glossary]]

## Bằng chứng và ứng viên hiện tại

- [[synthesis/Research: Reliable Tool-Using AI Agents]] — bản đồ lĩnh vực đầu tiên và đánh giá tính khả thi.
- [[synthesis/Preliminary Gap: Selective Recovery Routing]] — `REJECTED`.
- [[synthesis/Preliminary Gap: External Runtime Monitoring]] — `REJECTED`.
- [[synthesis/Preliminary Gap: Failure-Aware Least Privilege]]
- [[synthesis/Preliminary Gap: Completion Verification Under Degraded Tools]]
- [[synthesis/Research: Early Failure Detection in Tool-Using Agents]] — novelty gate `REJECTED` và câu hỏi hẹp còn mở.
- [[synthesis/Research: Correlated Silent Tool Failures and Verification]] — adversarial search cho semantic verification và common-mode fault.
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]] — gap hẹp `SURVIVES WITH REFINEMENT — PRELIMINARY`.
- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]] — novelty boundary sau adversarial search.

## Nhật ký nghiên cứu

- [[journal/2026-09-09-reliable-agents-field-map]]
- [[journal/2026-09-11-toolbench-x-reproducibility-pilot]]
- [[journal/2026-09-12-early-failure-detection-novelty-gate]]
- [[journal/2026-09-13-correlated-tool-verification-rq]]
- [[journal/2026-09-13-correlated-tool-verification-pilot]]
- [[journal/2026-09-14-correlated-tool-verification-next-gate]]
- [[journal/2026-09-14-full-live-agent-verification-gate]]
- [[journal/2026-09-15-main-study-manifest]]
- [[journal/2026-09-15-action-boundary-main-study]]
- [[journal/2026-09-15-imperfect-provenance-robustness-gate]]
- [[journal/2026-09-15-adversarial-prior-art-provenance-metadata]]
- [[journal/2026-09-15-external-validity-artifact-gate]]

## Living paper

- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]] — manuscript version 0.1, Vietnamese reasoning draft.
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]] — claim, evidence, scope và prohibited wording.
