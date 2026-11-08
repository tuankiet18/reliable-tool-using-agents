---
title: "Prior-Art Threat: Provenance Metadata and Source Selection"
category: synthesis
tags: [prior-art, novelty, ai-agents, provenance, verification]
sources:
  - "projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03.md"
  - "references/agentos-typed-tool-mediation.md"
  - "references/look-before-you-leap-pre-action-verification.md"
  - "journal/2026-10-04-pre-action-prior-art-audit.md"
  - "https://arxiv.org/html/2603.02345v1"
  - "https://arxiv.org/html/2607.07405v2"
  - "https://arxiv.org/html/2608.02645v1"
  - "https://arxiv.org/abs/2602.21517"
  - "https://arxiv.org/abs/2606.18037"
  - "https://arxiv.org/abs/2607.01236"
  - "https://arxiv.org/abs/2605.08828"
  - "https://arxiv.org/abs/2606.22741"
  - "https://arxiv.org/abs/2607.01640"
  - "https://aclanthology.org/2024.findings-emnlp.978/"
  - "https://arxiv.org/abs/2609.01360"
created: 2026-09-15T15:34:48+07:00
updated: 2026-10-04T10:31:00+07:00
summary: >-
  Audit AgentOS code và Look Before You Leap tiếp tục bác bỏ broad gate novelty; giữ controlled characterization PRELIMINARY, không đổi RQ hoặc tăng experiments.
---

# Prior-art threat — Provenance metadata và source selection

## Câu hỏi bị tấn công

Prior art đã nghiên cứu việc validate/calibrate provenance/dependency metadata và dùng uncertainty để chọn source/tool đủ gần với RQ hiện tại hay chưa?

## Kết luận ngắn

`SURVIVES WITH REFINEMENT — PRELIMINARY` cho **exact RQ**, nhưng ba novelty claim rộng đã bị bác bỏ. Không được nói rằng project là hệ thống đầu tiên chọn tool theo trust, đầu tiên dùng provenance để gate action, hoặc đầu tiên kiểm tra dependency metadata.

**Cập nhật 2026-10-03:** Matrix dưới đây giữ hồ sơ search ban đầu. Comparison có full-text/source coverage cập nhật nằm ở paper v0.4 §3.7 và [[projects/reliable-tool-using-ai-agents/paper/related-work-citation-audit-2026-10-03]]. RIVA đã dùng alternative verification techniques và independence intuition; RLVM/VTC đã có deterministic verification trước actions/retries. [[references/agentos-typed-tool-mediation]] là adjacent threat mới, chỉ đọc metadata/README nên direct overlap còn `?`. Không chạy head-to-head systems. Analytical reconstruction của project làm yếu claim discovery: main advantage có điều kiện được suy từ topology; secondary variation được suy từ schedule.

## Cập nhật hiện hành — 2026-10-04

**INFERENCE — QUYẾT ĐỊNH:** Không mở thêm lane, không đổi RQ, không tìm một tổ hợp features để tuyên bố novelty. AgentOS đã được targeted code/artifact inspection; thêm [[references/look-before-you-leap-pre-action-verification]] từ full HTML. **Paper v0.7 đã tích hợp bounded contrasts ở §3.2/§3.7 và 15 citation IDs**; không numerical comparison hoặc head-to-head. Verdict **MAJOR REVISION**, gap **SURVIVES WITH REFINEMENT — PRELIMINARY** không đổi.

### Ba lớp kiểm tra không được đồng nhất

| Lớp | Câu hỏi dễ hiểu | Evidence/setting đã inspect | Liên hệ với study của mình |
|---|---|---|---|
| Authorization / policy enforcement | Agent có quyền làm operation này không? | AgentOS VTRM code; xem source-level audit trong [[references/agentos-typed-tool-mediation]] | Không tự chứng minh dữ kiện eligibility/amount là đúng. |
| Action realizability | Operation có áp dụng đúng cách, đúng vị trí không? | [[references/look-before-you-leap-pre-action-verification]] §2–5 | Arguments hợp lệ vẫn có thể biểu diễn quyết định refund sai. |
| Decision evidence under correlated faults | Nguồn kiểm tra có thể sai cùng primary không? | Main/robustness của project; frozen data và analytical topology | Chỉ characterize authorization decisions với nguồn/metadata tự định nghĩa, không chứng minh end-to-end agent safety. |

**INFERENCE:** Các lớp có thể bổ sung nhau. Đây là taxonomy để tránh đo/claim sai construct, không chứng minh system nào yếu hơn system nào. Chưa chạy head-to-head; không suy absence từ việc full paper không truy cập được.

### Threat matrix bổ sung

| Work | Broad claim bị đe dọa | Exact-RQ overlap theo evidence đã đọc | Điều chưa thể kết luận |
|---|---|---|---|
| [[references/agentos-typed-tool-mediation]] | Pre-execution mediation, approval, world-effect scoring không mới | `PARTIAL`: quyền/policy và post-execution world changes; chưa thấy failure-domain selector comparison trong inspected code/tasks | Full paper chưa đọc; không biết toàn bộ published evaluation hoặc code-to-paper alignment. |
| [[references/look-before-you-leap-pre-action-verification]] | Deterministic pre-action gate, controlled silent-error measurement và utility trade-off không đủ làm novelty | `PARTIAL`: realizability khác business-truth/decision endpoint | Artifact chưa xác minh public; một số wording/table/metadata ambiguity; không measured comparison với project. |

### Phân tích khắt khe hơn với chính project

1. **INFERENCE — ANALYTICAL, KHÔNG DISCOVERY:** Khi independent corroborator được định nghĩa luôn đúng ở targeted condition, zero unsafe có thể suy ra trước run. Row count không làm cơ chế đó trở thành phát minh.
2. **INFERENCE — METADATA ASSUMPTION:** Project nhận failure-domain labels từ bên ngoài; chưa derive/validate chúng. Wrong-label robustness FAIL phải tiếp tục xuất hiện cạnh main positive result.
3. **INFERENCE — UTILITY:** Chặn sai khác bảo vệ đúng. Main targeted condition không phục hồi correct refunds; clean utility và false denial cần trình bày riêng, không gọi chung là “agent reliability tăng”.
4. **OPEN QUESTION — CONTRIBUTION:** Mức controlled comparison/characterization/artifact này có đủ cho course paper do giảng viên đánh giá. Prior-art search không thể trả lời thay người chấm hoặc dự đoán acceptance.

### Evidence còn thiếu, theo ưu tiên

- Paper-level AgentOS contrast cần full text và version mapping; có thể ghi “artifact-level comparison only” nếu không lấy được. Không chặn hoàn thiện bản môn học chỉ vì publisher access.
- Nguồn mới cần citation verification/wording nhất quán trước khi vào manuscript; không dùng results còn ambiguity làm supporting quantitative evidence.
- Public snapshot/license, course template và tác giả tự hiểu lập luận còn mở. Không cần thêm policy episodes để giải quyết các việc này.

## Prior-art threat matrix

| Work | Setting | Nó estimate/validate gì? | Dynamic selection/intervention? | Correlated tool faults? | Metadata uncertainty? | Irreversible action boundary? | Same problem? |
|---|---|---|---|---|---|---|---|
| [[references/tea-cxa]] | Medical multimodal tools | Learned per-tool expertise theo query type | ✓ chọn response nên tin | ✗ | △ learned trust | ✗ | PARTIAL |
| [[references/provenanceguard-source-aware-factuality]] | MCP medical traces | Claim–source attribution/support | ✓ allow/block answer | ✗ | △ thiếu source ID có fallback | ✗ | PARTIAL |
| [[references/provenanceguard-misalignment-provenance-analysis]] | Generic tool agents | Action justification từ query/docs/history/plan | ✓ pre-execution block | ✗ | △ plan reconstructed | ✓ | PARTIAL |
| [[references/grade-agent-dependency-execution]] | Tool, coding, web agents | Dependency edges: observed/declared/inferred | ✗ selection; ✓ diagnosis | ✗ | ✓ evidence grade và controls | ✗ | PARTIAL |
| [[references/agentflow-agent-dependency-graphs]] | Agent source code | Static component/control/data dependencies | ✗ | ✗ | △ static overapproximation | ✗ | NO |
| [[references/envtrustbench]] | Files/logs/APIs/commands | Oracle cho true state và false path | ✗ method; benchmark only | ✗ explicit shared domains | △ stale/wrong/malicious evidence | △ consequential false path | PARTIAL |
| `ProbeCal` | Tool-using language agents | Calibrated expected effectiveness của prompt/trace | ✓ execution-path selection | ✗ | ✓ model uncertainty | ✗ | NO |
| `EDGE` | Multi-agent failures | Counterfactual validation của error-dependency edges | △ guides attribution/repair | ✗ tool-source faults | ✓ observational vs intervention-validated | ✗ | NO |

Legend: `✓` rõ ràng có; `△` một phần; `✗` không có trong setting được báo cáo, **không** khẳng định cả system không thể hỗ trợ feature. Matrix là historical search classification, không measured head-to-head performance.

## Falsification theo từng claim

### 1. “Uncertainty-aware source/tool selection chưa tồn tại”

**REJECTED.** TEA-CXA học tool expertise và chọn response nên tin khi tools xung đột. `ProbeCal` cũng dùng calibrated uncertainty để chọn prompts/execution traces. Đây không phải exact failure-domain policy, nhưng đủ bác bỏ novelty wording rộng.

### 2. “Provenance-aware runtime action gating chưa tồn tại”

**REJECTED.** `Safeguarding LLM Agents from Misalignment through Provenance Analysis` chặn tool calls trước execution dựa trên provenance của tool, parameters và interpretation.

### 3. “Dependency/provenance metadata chưa được validate”

**REJECTED ở mức rộng.** GRADE phân loại dependency edges theo cách chúng được biết và kiểm tra inferred structure bằng controls; EDGE dùng counterfactual rollout để giữ causal subset; AgentFlow derive dependency graph từ source code. Các work này chưa validate `failure_domain_id`, nhưng câu tuyên bố rộng không còn đúng.

### 4. “Realistic incorrect environmental evidence chưa có benchmark”

**REJECTED.** EnvTrustBench tạo stale/wrong/malicious environmental evidence, lưu trajectory và dùng machine oracle. Tuy nhiên public artifact hiện chưa đủ cho full reproduction.

### 5. Tổ hợp exact RQ

**Chưa tìm thấy direct match** đồng thời có đủ:

1. schema-valid silent tool-output corruption;
2. shared/common failure domains giữa các tool interfaces;
3. mandatory verification ngay trước irreversible action;
4. selector chọn corroborator độc lập theo failure domain;
5. comparison với random source ở matched `K=2`;
6. unsafe-action và clean-task utility metrics.

Đây là negative search result, không phải bằng chứng về confirmed novelty. Tổ hợp sáu features không tự là contribution độc lập. Main/robustness hiện đo authorization decisions/action-oracle correctness, không executed irreversible actions; xem current working RQ trong [[projects/reliable-tool-using-ai-agents/paper/paper-draft]].

## Contradictions và implications

- TEA-CXA cho thấy learned trust có thể resolve conflict, nhưng cần heavy RL và domain-specific reward; RQ hiện tại dùng deterministic metadata và không training.
- GRADE cho thấy inferred dependency structure có thể transfer kém. Robustness gate của project cũng cho thấy wrong labels nhanh chóng phá safety gain. Hai nguồn cùng chống giả định “graph/metadata có là dùng được”.
- ProvenanceGuard (ASE) kiểm tra căn cứ của action trong context. **INFERENCE:** justification không chứng nhận external truth; evaluation đã đọc chưa test comparison failure-domain này. Không đủ để nói system chắc chắn không bảo vệ khi context sai.
- EnvTrustBench cho evidence về misgrounding trong constructed benchmark, **không** production prevalence. Public artifact rechecked chưa cung cấp executable cases/runners cho reproduction của project.

## Novelty boundary phải dùng

Không claim một method hoàn toàn mới. Claim có thể bảo vệ là:

> **PRELIMINARY:** controlled characterization of failure-domain-independent corroboration for refund authorization decisions, with matched modeled boundary observations, metadata sensitivity and conditional utility.

## Có nên đổi RQ sang metadata validation không?

**Không.** Đây sẽ là scope creep. Derive/validate failure-domain metadata là một bài toán riêng, có threat trực tiếp từ GRADE, EDGE và AgentFlow, đồng thời cần ground truth về backend dependencies khó xây trong 12 tuần. RQ hiện tại nên giữ assumption `given accurate failure-domain metadata` và nêu đây là external-validity limitation.

## Gap survival status

`SURVIVES WITH REFINEMENT — PRELIMINARY`.

- Internal causal mechanism: đã có evidence mạnh trong controlled benchmark.
- Novelty: chưa chứng minh; exact-setting difference không thay thế contribution. Giá trị hiện tại là controlled characterization/artifact, chờ đánh giá của giảng viên.
- External validity: yếu.
- Reproducibility trong 12 tuần: tốt cho core controlled study; chưa đạt cho external benchmark.

## Bước tiếp theo duy nhất

**Hiện hành:** Delta prior art đã tích hợp ở v0.7; rà claim–evidence toàn manuscript cùng appendix/reproduction package và lập submission-readiness checklist. Giữ full-text AgentOS blocker và source ambiguities rõ ràng. Journal giải thích thứ tự đọc và công việc tiếp theo tại [[journal/2026-10-04-pre-action-prior-art-audit]].

**Historical:** Structure/appendix/inventory/figures đã hoàn thành ở v0.5–v0.6; live opportunity gate fail và scaling đã dừng. Không xóa negative evidence hoặc đổi lịch sử AI review thành human sign-off.

## Related

- [[synthesis/Candidate RQ - Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Preliminary Gap - Provenance-Aware Verification under Correlated Tool Failures]]
- [[journal/2026-09-15-adversarial-prior-art-provenance-metadata]]
