---
title: Wiki Index
---

# Wiki Index

*This index is automatically maintained. Last updated: 2026-09-15T17:15:00+07:00*

## Concepts

- [[concepts/reliable-tool-using-agent-lifecycle]] — Failure points and interventions from goal through verified stop ( #ai-agents #reliability #tool-use)
- [[concepts/agent-recovery-policy]] — Runtime choice of retry, replan, rollback, escalation, or stop ( #ai-agents #recovery)
- [[concepts/agent-verification-and-premature-completion]] — Independent goal-state verification rather than self-declared success ( #ai-agents #verification)
- [[concepts/least-privilege-tool-use]] — Authorization boundaries and failure-triggered privilege escalation ( #ai-agents #security)
- [[concepts/agent-observability-and-runtime-monitoring]] — Trace-based detection and diagnosis ( #ai-agents #observability)
- [[concepts/agent-reliability-research-lanes]] — Comparative taxonomy of reliability research directions ( #ai-agents #research)
- [[concepts/reliable-tool-using-ai-agents-glossary]] — Thuật ngữ tiếng Việt cho research về AI agent dùng tool đáng tin cậy ( #ai-agents #glossary)

## Entities

## Skills

## References

- [[references/tau-bench]] — Stateful tool-agent-user benchmark with goal-state scoring and pass^k ( #benchmark #tool-use)
- [[references/toolsandbox]] — Stateful conversational tool-use evaluation with milestones ( #benchmark #tool-use)
- [[references/failing-tools]] — Under-review controlled runtime tool-failure recovery benchmark ( #benchmark #recovery)
- [[references/agenttether]] — Graph-guided diagnosis and rerun repair ( #diagnosis #recovery)
- [[references/hintbench]] — Long-horizon intrinsic-risk detection and localization benchmark ( #benchmark #monitoring)
- [[references/benchtrace]] — Reflection and failure-avoidance benchmark ( #benchmark #reflection)
- [[references/miniscope]] — Least-privilege authorization framework for tool agents ( #security #authorization)
- [[references/agentdojo]] — Dynamic prompt-injection evaluation environment ( #benchmark #security)
- [[references/osworld]] — Executable real-computer task benchmark ( #benchmark #long-horizon)
- [[references/seed-papers-and-benchmarks-reliable-agents]] — 21-item prioritized reading registry ( #research #reading-list)
- [[references/adaptive-fault-injection-task-failure-forecasting]] — Failure forecasting từ partial trajectory ( #failure-detection #research)
- [[references/retry-switch-or-abstain]] — Prior art trực tiếp về retry/switch/abstain dưới tool failure ( #recovery #tool-failure)
- [[references/toolbench-x]] — Controlled fault modules chạy được, nhưng pilot loại ToolBench-X khỏi vai trò benchmark chính do data validity, leakage, trace và throughput ( #benchmark #reproducibility)
- [[references/progent]] — Runtime privilege control với task policy, SMT và approval ( #security #authorization)
- [[references/authbench]] — Benchmark task-to-file least-privilege authorization cho coding agent ( #benchmark #authorization)
- [[references/toolprivbench]] — Benchmark over-privileged tool selection và escalation sau transient failure ( #benchmark #security)
- [[references/fava]] — Formal runtime authorization với evidence-backed permission graph ( #security #formal-methods)
- [[references/actplane]] — OS-level policy enforcement cho agent harness ( #coding-agents #security)
- [[references/toolguardian]] — Tool vetting và task-aware authorization bằng structured evidence ( #mcp #security)
- [[references/real-time-detection-and-repair-agent-failures]] — Online telemetry monitor, deterministic verification và rollback/rerun với public reproducible artifact ( #failure-detection #runtime-monitoring)
- [[references/prefixguard]] — Lightweight prefix warning monitor và low-FAR actionability analysis ( #failure-detection #runtime-monitoring)
- [[references/agentforesight]] — Online auditor và public AFTraj-2K dataset có decisive-error labels ( #failure-detection #benchmark)
- [[references/weakly-supervised-early-failure-alerting]] — Early alert từ sparse trajectory-level supervision ( #failure-detection #early-stopping)
- [[references/automata-from-agent-traces]] — FSM từ trace corpus cho failure/next-step prediction ( #failure-detection #automata)
- [[references/from-confident-closing-to-silent-failure]] — False-success evidence trên tau2-bench và AppWorld ( #false-success #verification)
- [[references/trajectory-judge]] — Deterministic silent/loud fault benchmark và judge comparison ( #failure-detection #verification)
- [[references/riva]] — Cross-tool verification dưới erroneous tool outputs và independence assumption ( #verification #tool-failure)
- [[references/robustness-inconsistent-incomplete-tool-responses]] — Return-boundary signals cho schema-valid inconsistent tool outputs ( #tool-failure #failure-detection)
- [[references/verified-tool-calls-non-atomic-failures]] — Postcondition verification và verify-before-retry cho non-atomic tool calls ( #verification #software-engineering)
- [[references/reason-less-verify-more]] — Deterministic pre-write gates cho silent policy violations ( #verification #tool-use)
- [[references/correlated-errors-in-large-language-models]] — ICML evidence rằng diversity không bảo đảm independent errors ( #reliability #failure-correlation)
- [[references/tea-cxa]] — Learned tool-expertise selection khi medical tools mâu thuẫn ( #tool-use #prior-art)
- [[references/provenanceguard-source-aware-factuality]] — Source-aware factuality verification cho MCP traces ( #verification #provenance)
- [[references/provenanceguard-misalignment-provenance-analysis]] — Provenance-based pre-execution guardrail cho tool calls ( #runtime-monitoring #safety)
- [[references/envtrustbench]] — Benchmark environmental evidence bị stale, wrong hoặc malicious ( #benchmark #verification)
- [[references/grade-agent-dependency-execution]] — Graded execution/dependency graph cho agent traces ( #observability #dependency)
- [[references/agentflow-agent-dependency-graphs]] — Static Agent Dependency Graph từ agent source code ( #static-analysis #security)

## Synthesis

- [[synthesis/Research: Reliable Tool-Using AI Agents]] — First-pass field map, research lanes, feasibility, and next evidence ( #ai-agents #research)
- [[synthesis/Preliminary Gap: Selective Recovery Routing]] — PRELIMINARY recovery-policy candidate ( #research-gap #recovery)
- [[synthesis/Preliminary Gap: External Runtime Monitoring]] — REJECTED bởi direct online-monitoring prior art ( #research-gap #monitoring)
- [[synthesis/Preliminary Gap: Failure-Aware Least Privilege]] — PRELIMINARY authorization/recovery candidate ( #research-gap #security)
- [[synthesis/Preliminary Gap: Completion Verification Under Degraded Tools]] — PRELIMINARY verification candidate ( #research-gap #verification)
- [[synthesis/Deep Comparison: Recovery Routing Anchor Works]] — So sánh sâu Failing Tools, Adaptive Fault Injection và AgentTether ( #recovery #comparison)
- [[synthesis/Prior-Art Threat: Recovery-Action Selection]] — Prior-art search bác bỏ broad recovery-routing gap ( #prior-art #novelty)
- [[synthesis/Agent Capability and Permission Control]] — Taxonomy và evidence map cho least-privilege capability control ( #authorization #security)
- [[synthesis/Prior-Art Threat: Agent Capability Control]] — Ma trận adversarial prior art cho capability-control claims ( #prior-art #authorization)
- [[synthesis/Preliminary Gap: Task-Aware Permission Inference]] — REJECTED bởi AuthBench và Progent ( #research-gap #authorization)
- [[synthesis/Preliminary Gap: Software-Evidence-Grounded Capability Scoping]] — PRELIMINARY scope hẹp cho coding agent ( #research-gap #program-analysis)
- [[synthesis/Preliminary Gap: Progressive Capability Expansion]] — REJECTED bởi Progent/FAVA/ToolPrivBench ( #research-gap #authorization)
- [[synthesis/Preliminary Gap: Risk-Aware Human Escalation for Permissions]] — WEAK, chưa có benchmark/ground truth đủ mạnh ( #research-gap #human-in-the-loop)
- [[synthesis/Research: Early Failure Detection in Tool-Using Agents]] — Novelty gate bác bỏ broad early-failure topic và trả lời experimental open questions ( #failure-detection #prior-art)
- [[synthesis/Research: Correlated Silent Tool Failures and Verification]] — Prior-art map và reproducibility gate cho common-mode tool verification ( #verification #prior-art)
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]] — PRELIMINARY dependency-aware verification gap ( #research-gap #tool-failure)
- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]] — Candidate RQ chính và experimental design ( #research-question #experiment)
- [[synthesis/Protocol: Action-Boundary Provenance Verification Main Study]] — Internal preregistration cho main deterministic study ( #research-protocol #experiment)
- [[synthesis/Protocol Amendment: Imperfect Provenance and Partial Correlation]] — Post-main robustness gate với noisy metadata và cross-domain fault leakage ( #research-protocol #experiment)
- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]] — Adversarial novelty boundary cho metadata validation và source selection ( #prior-art #novelty)

## Journal

- [[journal/2026-09-09-reliable-agents-field-map]] — First-pass search record, uncertainties, and next action ( #research-log #ai-agents)
- [[journal/2026-09-10-adversarial-prior-art-recovery-routing]] — Adversarial search bác bỏ broad recovery-routing gap ( #research-log #prior-art)
- [[journal/2026-09-10-adversarial-prior-art-capability-control]] — Adversarial search cho capability control ( #research-log #authorization)
- [[journal/2026-09-11-toolbench-x-reproducibility-pilot]] — Pilot ToolBench-X hoàn tất clean/exception pair, audit 5 task và quyết định chỉ giữ làm secondary stress test ( #research-log #benchmark)
- [[journal/2026-09-12-early-failure-detection-novelty-gate]] — Prior-art search và local smoke reproduction bác bỏ broad early-failure-detection gap ( #research-log #prior-art)
- [[journal/2026-09-13-correlated-tool-verification-rq]] — Search, artifact gate và quyết định candidate RQ về common-mode tool failures ( #research-log #research-question)
- [[journal/2026-09-13-correlated-tool-verification-pilot]] — 600-episode exploratory pilot và safety–abstention trade-off ( #research-log #experiment)
- [[journal/2026-09-14-correlated-tool-verification-next-gate]] — 30-task metadata-robustness gate và hai partial local-model subsets ( #research-log #experiment)
- [[journal/2026-09-14-full-live-agent-verification-gate]] — 36-episode full tool-loop gate; kỹ thuật pass nhưng experimental validity fail vì verification coverage và procedure compliance ( #research-log #experiment)
- [[journal/2026-09-15-main-study-manifest]] — Fresh 30-task main-study split đã đóng băng, có SHA-256 và không trùng pilot ( #research-log #reproducibility)
- [[journal/2026-09-15-action-boundary-main-study]] — 1.350-episode deterministic main gate, preregistered PASS với adversarial interpretation ( #research-log #experiment)
- [[journal/2026-09-15-imperfect-provenance-robustness-gate]] — 3.750-episode stress test fail khi provenance labels sai 25% ( #research-log #robustness)
- [[journal/2026-09-15-adversarial-prior-art-provenance-metadata]] — Search bác bỏ broad novelty claims và giữ exact RQ ở phạm vi hẹp ( #research-log #prior-art)
- [[journal/2026-09-15-external-validity-artifact-gate]] — EnvTrustBench fail executable gate; ProvenanceGuard pass technical nhưng partial RQ fit ( #research-log #reproducibility)

## Projects

- [[projects/reliable-tool-using-ai-agents/reliable-tool-using-ai-agents]] — 12-week research effort on reliable tool-using agents ( #ai-agents #research)
- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]] — Living paper v0.1 về failure-domain-aware action-boundary verification ( #paper-draft #verification)
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]] — Ledger kiểm soát claim, evidence và phạm vi diễn giải ( #paper-draft #evidence)
