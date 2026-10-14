---
title: >-
  Reliable Tool-Using AI Agents — Undergraduate Research Project
category: project
tags: [ai-agents, reliability, tool-use, software-engineering, research]
sources:
  - "journal/2026-10-05-main-study-influence-audit.md"
  - "journal/2026-10-04-clean-environment-core-reproduction.md"
  - "journal/2026-10-04-pre-action-prior-art-audit.md"
  - "projects/reliable-tool-using-ai-agents/paper/figure-guide.md"
  - "projects/reliable-tool-using-ai-agents/paper/review/paper-review-v0.9-2026-10-05.pdf"
  - "projects/reliable-tool-using-ai-agents/paper/reproducibility-package.md"
  - "projects/reliable-tool-using-ai-agents/paper/supplementary-appendix.md"
  - "projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03.md"
  - "projects/reliable-tool-using-ai-agents/paper/supervisor-methodology-rq-briefing.md"
  - "journal/2026-09-20-ai-review-provenance-correction.md"
  - "journal/2026-09-24-secondary-schema-v12-recheck.md"
  - "journal/2026-09-26-secondary-adapter-smoke-tests.md"
  - "synthesis/Protocol Amendment: Exploratory Secondary Runtime Matrix.md"
  - "journal/2026-09-28-secondary-exploratory-matrix.md"
  - "synthesis/Protocol: Secondary Varied-Schedule Replication.md"
  - "journal/2026-09-28-secondary-varied-schedule-replication.md"
  - "journal/2026-09-30-rtx4060-live-agent-diagnostic.md"
  - "journal/2026-09-30-live-agent-safety-preflight.md"
  - "synthesis/Protocol Amendment: Exploratory RTX 4060 Safety Diagnostic.md"
  - "journal/2026-10-01-live-agent-diagnostic-instrumentation.md"
  - "journal/2026-10-02-ins32-rtx4060-validity-audit.md"
  - "synthesis/protocol-prospective-live-agent-opportunity-gate.md"
  - "journal/2026-10-02-live-agent-opportunity-preflight.md"
  - "journal/2026-10-03-live-agent-opportunity-diagnostic.md"
  - "projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03.md"
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_topology_diagnostics_20261003/analysis.json"
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
updated: 2026-10-05T09:14:46+07:00
---

# AI Agent dùng tool đáng tin cậy

`Reliable Tool-Using AI Agents — Undergraduate Research Project`

Mục tiêu của dự án là tìm và kiểm chứng một can thiệp về độ tin cậy được xác định rõ cho AI agent dùng tool (tool-using AI agent). Đầu ra mong muốn là một đóng góp thực nghiệm có thể tái lập, không phải một ứng dụng agent chung chung. Bản đồ lĩnh vực ban đầu nằm tại [[synthesis/Research: Reliable Tool-Using AI Agents]].

## Phạm vi và ràng buộc

**Cập nhật 2026-10-04:** Paper v0.9 bổ sung clean-venv core reproduction trên cùng host: mới clone/cài pinned upstream, replay main/robustness và analyses, 10 selected files byte-identical, 15 focused tests đạt. Không thêm independent samples, đổi RQ/results, nâng novelty hoặc live scaling. Đọc [[journal/2026-10-04-clean-environment-core-reproduction]] để hiểu evidence mới, rồi [[projects/reliable-tool-using-ai-agents/paper/submission-readiness]] để hoàn thiện course paper. Related Work vẫn 15 IDs; PRELIMINARY/MAJOR REVISION và human feedback gate giữ nguyên.

- Quyết định hiện hành 2026-10-03: hoàn thiện **controlled empirical paper cho môn học**. Môn học không bắt buộc kết quả trên agent thật; dừng live-agent scaling theo stop rule, không biến external validation thành điều kiện phải đạt để nộp bản course paper.
- 12 tuần; không huấn luyện foundation model; chỉ dùng API/local model và Docker với chi phí vừa phải.
- Ưu tiên benchmark có thể chạy được, quỹ đạo thực thi (execution trajectory) có thể quan sát, và metric rõ ràng về hiệu quả, chi phí, an toàn.
- Ưu tiên agent gọi API tool; chỉ dùng coding agent khi benchmark tái lập được và mô hình quyền truy cập đủ rõ.

## Câu hỏi đã loại bỏ

- `Selective Recovery Routing`: `REJECTED` vì direct prior art đã chọn động retry/switch/abstain/replan.
- Broad `Early Failure Detection from Execution Trajectories`: `REJECTED` vì nhiều work 2026 đã làm prefix prediction, controlled failures, calibration, transfer và intervention.
- Không tiếp tục xây ToolBench-X hoặc local 20–30-task harness như thesis contribution.

## Candidate RQ hiện tại

Reviewer-style audit ngày 2026-10-03 cho verdict **MAJOR REVISION**: main/robustness đo **action-oracle correctness**, không thực thi refund rồi đo final state; main `false_block` gộp actor abstention với gate blocking. Targeted main condition có `0/50` correct expected-refund outcomes ở cả hai policies. Paper v0.2–v0.4 sửa construct, thêm analytical/counterfactual diagnostics và thu hẹp Contributions/Related Work; v0.5 thêm structure/appendix/reproduction package, v0.6 thêm frozen-data figures. Raw, estimates và RQ/H1 không đổi; không study episodes mới hoặc human sign-off. Course formatting/author proofreading và human methodology feedback còn mở. Xem [[projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03]] và ledger.

**INFERENCE — GIỚI HẠN CONTRIBUTION:** Main random unsafe expectation là `2/9`; observed fixed seeds cho `30/150=0.20`. Provenance zero unsafe phụ thuộc independent sources còn đúng. Dưới main targeted faults, luôn escalation có cùng safety/correctness với provenance; provenance hơn ở clean refund utility (`50/50` vs `0/50`). Secondary unsafe counts `59/96` vs `24/96` được tái dựng hoàn toàn từ schedule overlap. Do đó contribution nên là controlled characterization, metadata/utility trade-offs và artifact tái lập, không phát minh nguyên lý independence hoặc generalization trên agent thật.

**PRELIMINARY:**

> Given accurate failure-domain metadata, under targeted common-mode silent tool-output failures, does independent-domain corroboration reduce unsafe refund authorization decisions relative to random corroboration at a matched two-observation boundary budget, while preserving clean action-oracle correctness in a deterministic controlled workflow?

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

Case-audit gate sau đó đã `CONDITIONAL PASS`: đóng băng `12` cases từ Agent-SafetyBench/WorkBench trên `10` atomic domains, với decisive claim, action boundary, canonical truth và programmatic oracle. Vì independent corroborators và failure topology vẫn do project bổ sung, đây chỉ là benchmark-derived adaptation nhằm kiểm tra semantic breadth, chưa phải external validation. Xem [[journal/2026-09-18-benchmark-derived-case-audit]].

Secondary protocol gốc được freeze trước adapter, nhưng quy trình review dự kiến đã không diễn ra như kế hoạch: project chỉ có một researcher và các verdict là AI-assisted, không có human sign-off. Case audit hạ `ASB-267` khỏi ma trận safety, giữ `WB-295` ngoài denominator, sửa mutation `ASB-977`, và khóa tám safety cases/sáu domains. Static v1.2 checks cùng smoke test 32 episodes pass; chi tiết chronology nằm tại [[synthesis/Protocol Amendment: Secondary Case Review and Safety Eligibility]], [[journal/2026-09-24-secondary-schema-v12-recheck]] và [[journal/2026-09-26-secondary-adapter-smoke-tests]].

Ngày 2026-09-28, varied-schedule replication tiếp tục trong cùng nhãn **exploratory internal adaptation**. 1.056 episodes/528 pairs chạy hai lần byte-identical, với schedule theo case được hash trước runtime. Tại `targeted_common_mode_25`, unsafe accepted actions là `59/96` (`random_k`) so với `24/96` (`provenance_k`); mean case difference `−0.3646`, advantage mô tả ở `8/8` safety cases và bootstrap CI theo case `[-0.396,-0.323]`. Các differences không còn đồng nhất như ở ma trận đầu, cho thấy overlap giữa lịch selector/leakage ảnh hưởng mức effect trong thiết kế này. Utility false blocks là `9/24` so với `18/24`; safety task success dưới targeted faults vẫn là 0 vì gate không tự sửa action. Đây không phải confirmatory evidence, native benchmark reproduction hay external validation: cohort purposive, source topology/fault model project-defined, schema còn candidate và chưa có human review. Xem [[journal/2026-09-28-secondary-varied-schedule-replication]] và [[synthesis/Protocol: Secondary Varied-Schedule Replication]].

RTX 4060/Qwen2.5 7B đã chạy được sáu episode diagnostic, nhưng case `INS-00030` chỉ thử false denial và trace lộ refund attempt lặp cùng escalation sau refund thành công; **chưa có live-agent safety validation**. Preflight offline tiếp theo xác nhận `INS-00032` là false-positive safety case: canonical phải escalation, còn targeted fault báo đủ điều kiện refund. Seed `809` tạo khác biệt về failure domain giữa selectors nhưng được chọn hậu nghiệm, nên diagnostic dự kiến vẫn `EXPLORATORY`; tại thời điểm preflight đó chưa có episode Qwen2.5 7B mới. Xem [[journal/2026-09-30-rtx4060-live-agent-diagnostic]], [[journal/2026-09-30-live-agent-safety-preflight]] và [[synthesis/Protocol Amendment: Exploratory RTX 4060 Safety Diagnostic]].

Ngày 2026-10-01, runner/analyzer cho diagnostic tám cell đã được instrument: chọn exact task/policies, CLI dry-run không gọi model, và các process metrics đọc trực tiếp raw trajectory. Unit tests `58/58` pass; re-audit sáu RTX rows cũ khớp kiểm tra thủ công. Dry-run trên upstream `trajectory-judge` commit pinned tại Linux in đúng tám cells và expected action `escalate`; **tại thời điểm đó** code chưa sync sang Windows. Xem [[journal/2026-10-01-live-agent-diagnostic-instrumentation]].

Ngày 2026-10-02, branch Windows-safe `codex/rtx4060-ins32-diagnostic@e265c358df3fd20a274f0ce3f6b53bc774694ed1` đã được chạy trên RTX 4060 với Qwen2.5 7B: tám cells/65 model calls, `12/12` refund attempts đi qua boundary, `8/8` final states đúng và `0/8` unsafe accepted refunds. Nhưng **cả 12 requests đều là `0 EUR` và tất cả tám trajectories đã escalation trước refund attempt**. Seed `809` random không phát hiện conflict nhưng vẫn bị chặn do amount mismatch. Vì vậy technical gate pass, **live-agent policy-effect validity fail**; không scale lên 72 episodes hoặc nâng claim paper. Artifact được lưu riêng theo hash tại [[journal/2026-10-02-ins32-rtx4060-validity-audit]].

Sau audit, đã khóa [[synthesis/protocol-prospective-live-agent-opportunity-gate]]: refund request phải có amount dương khớp primary sai **trước** successful escalation, và hai policies phải có matched proposal mới được so sánh. Static preflight chọn bốn safety tasks `INS-00032`–`INS-00035` cùng seed topology `1111`. Diagnostic **16 cells đã chạy** trên RTX 4060; raw/analyzer được kiểm tra lại local, `62/62` tests pass. Không có targeted unsafe-capable cell (`0/8`) hoặc matched pair (`0/4`), nên **dừng live-agent scaling theo protocol**. `0/16` unsafe accepted refunds không phải policy-effect evidence. Xem [[journal/2026-10-02-live-agent-opportunity-preflight]] và [[journal/2026-10-03-live-agent-opportunity-diagnostic]].

Living paper version `0.9` nằm tại [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]. Giữ RQ/H1, outcomes, appendix, 21-file inventory và hai SVG; thêm §8 clean-venv core replay, không fresh-machine reproduction. Historical figure tests/reanalysis giữ chronology riêng. Package còn CANDIDATE; course/public-release gates được tách trong [[projects/reliable-tool-using-ai-agents/paper/submission-readiness]]. Paper vẫn MAJOR REVISION, novelty PRELIMINARY. Bước tiếp theo: tác giả viết explanation một trang về assumptions/endpoints/trade-offs trước final template/citations và giảng viên feedback; không tăng independent experiment rows.

Đã bổ sung ba worked examples vào [[projects/reliable-tool-using-ai-agents/paper/figure-guide]] §6, không tạo note trùng: cùng backend sai → đồng thuận sai; false denial → không có proposal nên gate không được gọi; always-escalate → zero unsafe nhưng mất clean refund utility. Bảy frozen rows có line IDs/khóa task-regime-seed-policy và raw hash để đối chiếu. Đây là hỗ trợ học cách đọc evidence, không thêm independent samples hoặc thay author readback/human review. Đọc phần này trước khi tự viết explanation.

**Cập nhật paper 2026-10-05:** [[journal/2026-10-05-main-study-influence-audit]] kiểm tra mức tập trung của main effect bằng cách lần lượt bỏ task, seed hoặc stratum. Targeted Δ vẫn âm (stratum-deletion từ −24 đến −16 pp), nhưng sign một phần do constructed zero-unsafe treatment; independent-fault difference đổi dấu theo thành phần task. Appendix §F và ledger C32 giữ nhãn hậu nghiệm; paper v0.9/primary estimates/CIs không đổi. Đã xuất [[projects/reliable-tool-using-ai-agents/paper/review/paper-review-v0.9-2026-10-05.pdf]] để tác giả/giảng viên đọc; PDF gắn với paper source hash và chưa theo template môn học. Tiếp theo, tác giả proofread rồi gửi giảng viên xin góp ý RQ/methodology/contribution; author readback, course format và supervisor feedback vẫn mở. Không scale RTX hoặc mở thêm sensitivity variants để tăng evidence count.

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
- [[synthesis/Protocol: Secondary Multi-Domain Benchmark-Derived Adaptation]] — protocol gốc, giữ nguyên lịch sử.
- [[synthesis/Protocol Amendment: Secondary Case Review and Safety Eligibility]] — eligibility và giới hạn safety denominator.
- [[synthesis/Protocol Amendment: Exploratory Secondary Runtime Matrix]] — deviation và scope đã khóa trước full run.
- [[synthesis/Protocol: Secondary Varied-Schedule Replication]] — varied schedule prospective; kết quả exploratory đã chạy.
- [[journal/2026-09-19-workbench-full-state-gate]] — original WorkBench fixture/code xác lập WB-110/433 truth và WB-295 distractor; adapter/schema còn mở.
- [[journal/2026-09-20-secondary-resign-freeze-readiness]] — re-sign semantic pass; schema/matrix gate pending và WB-295 chưa vào cohort.
- [[projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate]] — contract v1.2 và kết quả full exploratory matrix.
- [[journal/2026-09-20-secondary-schema-preflight]] — hashes, claims, mutations, exclusions và giới hạn của preflight.
- [[journal/2026-09-28-secondary-exploratory-matrix]] — ma trận 704 episodes ban đầu, degenerate CI và limitations.
- [[journal/2026-09-28-secondary-varied-schedule-replication]] — 1.056 episodes, phân tích theo case và schedule sensitivity.

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
- [[journal/2026-09-18-benchmark-derived-case-audit]]
- [[journal/2026-09-19-secondary-semantic-review]]
- [[journal/2026-09-19-workbench-full-state-gate]]
- [[journal/2026-09-20-secondary-resign-freeze-readiness]]
- [[journal/2026-09-20-secondary-schema-preflight]]
- [[journal/2026-10-02-ins32-rtx4060-validity-audit]] — diagnostic RTX 4060 đủ tám cell nhưng chưa có unsafe-capable live attempt.
- [[synthesis/protocol-prospective-live-agent-opportunity-gate]] — tiêu chí và 16-cell exploratory matrix cho diagnostic tương lai.
- [[journal/2026-10-02-live-agent-opportunity-preflight]] — kiểm tra offline, code/test status và giới hạn claim trước RTX run.
- [[journal/2026-10-03-live-agent-opportunity-diagnostic]] — kiểm tra artifact 16 cells, opportunity gate `0/4`, stop scaling và giới hạn claim live-agent.

## Living paper

- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]] — manuscript version 0.9, controlled results và clean-venv core replay; chưa submission approval.
- [[projects/reliable-tool-using-ai-agents/paper/figure-guide]] — hướng dẫn đọc safety, utility và metadata sensitivity trước buổi review.
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]] — claim, evidence, scope và prohibited wording.
- [[projects/reliable-tool-using-ai-agents/paper/supervisor-methodology-rq-briefing]] — briefing ngắn để giảng viên review RQ, methodology, contribution và validation plan; không yêu cầu review case/oracle chi tiết.
