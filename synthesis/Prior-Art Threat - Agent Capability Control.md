---
title: "Prior-Art Threat: Agent Capability Control"
category: synthesis
tags: [prior-art, novelty, authorization, ai-agents, security]
sources:
  - https://arxiv.org/abs/2504.11703
  - https://arxiv.org/abs/2605.14859
  - https://arxiv.org/abs/2606.20023
  - https://arxiv.org/abs/2607.27267
  - https://arxiv.org/abs/2606.25189
summary: "Adversarial matrix: broad task-aware/dynamic capability-control claims đã bị prior art phủ; còn software-evidence scoping nhưng evidence chưa đủ."
provenance: {extracted: 0.87, inferred: 0.10, ambiguous: 0.03}
base_confidence: 0.90
lifecycle: draft
lifecycle_changed: 2026-09-10
tier: core
created: 2026-09-10T00:00:00Z
updated: 2026-09-10T00:00:00Z
---

# Prior-art threat analysis — Agent Capability Control

| Paper | Year | Setting | Permission / recovery choices | Dynamic selection? | Inputs / signals | Cost-aware? | Same problem? |
|---|---:|---|---|---|---|---|---|
| [[references/authbench]] | 2026 | terminal/coding | file R/W/X whitelist before run | no | task + terminal environment | security/utility trade-off, not runtime cost | **YES** for GAP-A |
| [[references/progent]] | 2025/26 | generic tool, MCP integrations | allow/forbid tool+arguments; narrowing; expansion + approver fallback | yes | task, tool returns, current policy | approval frequency; no minimality oracle | **YES** for broad C/D; PARTIAL B |
| [[references/toolprivbench]] | 2026 | simulated tool agent | retry/switch low privilege/escalate high privilege/stop | agent dynamic tool choice | transient error, tool history, tool descriptions | OPUR/PED; no real side effects | **YES** for failure-aware escalation; PARTIAL C |
| [[references/fava]] | 2026 | generic / coding scenarios | authorize/intercept capabilities before effect | yes | task IR, dataflow, dependencies, runtime labels | latency; soft capability minimization | **PARTIAL** B/C |
| [[references/actplane]] | 2026 | coding-agent harness | OS policy allow/block/notify | runtime adaptation of policy | task/repository context, OS events/dataflow | runtime overhead | **PARTIAL** B |
| [[references/toolguardian]] | 2026 | MCP-style tool agent | admit / deny tool and task-aware authorization | yes, authorization per scenario | description, syscall trace, mock effect, source analysis, task context | no authority-minimality metric | **PARTIAL** B |
| [[references/miniscope]] | 2025 | tool-call agent | mobile-style grant / confirmation over tool hierarchy | partial | inferred tool-call hierarchy | latency/operational cost | **PARTIAL** A/C/D |

## Kill test

1. **Dynamic selection:** Progent and FAVA are direct counterexamples.
2. **Multiple permissions/actions:** Progent covers tool and argument rules; ToolPrivBench covers low/high tool choice.
3. **Runtime evidence:** Progent consumes tool returns; FAVA tracks dataflow/context; ToolPrivBench injects transient failures.
4. **Realistic tool failure:** ToolPrivBench directly tests transient failure but is simulated; this weakens external validity, not novelty claim.
5. **Cost / side effect:** Progent reports approval frequency and security/utility; ToolPrivBench measures OPUR/PED. Comprehensive real side-effect cost remains limited, but adding it alone is an evaluation extension, not a defensible standalone gap.

## Overall finding

The broad direction “adaptive task-aware least-privilege capability control” is **too broad and already covered**. Only a narrow, testable statement about independently computed software evidence improving a known static permission-inference benchmark remains *possible*, pending a source/code search and pilot ground-truth audit.
