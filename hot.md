---
title: Hot Cache
updated: 2026-09-15T17:15:00+07:00
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-09-15] LIVING PAPER v0.1 — [[projects/reliable-tool-using-ai-agents/paper/paper-draft]] đã có full argument skeleton và current results. [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]] ngăn strength/novelty drift; Abstract và Conclusion vẫn provisional.
- [2026-09-15] EXTERNAL-VALIDITY ARTIFACT GATE — EnvTrustBench public release chỉ có aggregate data: tái tính được `3,206/3,850`, nhưng không có cases/oracles/runners nên gate fail. ProvenanceGuard artifact setup pass, load 182 ASB + 388 WorkBench traces và execute ba notebooks offline; exact-RQ fit chỉ partial.
- [2026-09-15] ADVERSARIAL PRIOR-ART GATE — TEA-CXA, two ProvenanceGuard papers, GRADE, AgentFlow, EnvTrustBench, ProbeCal và EDGE đã được đối chiếu. Broad novelty claims về tool trust selection, provenance-aware action gating và dependency validation bị bác bỏ.
- [2026-09-15] ROBUSTNESS GATE FAIL — 3.750 episodes; accurate and missing-label conditions pass, nhưng `wrong_25 + leakage .10` CI chạm zero. RQ narrowed to accurate failure-domain metadata.
- [2026-09-15] ROBUSTNESS PROTOCOL FROZEN — 30 new tasks, 3.750 planned episodes, four provenance-noise conditions và cross-domain leakage `0–0.50`; thresholds ghi trước code/result.
- [2026-09-15] MAIN DETERMINISTIC GATE — 1.350 episodes, all preregistered conditions pass; targeted unsafe refund provenance `0.000` vs random `0.200`, CI `[-0.273,-0.127]`; clean success both `1.000`.
- [2026-09-15] MAIN STUDY MANIFEST — Fresh split `INS-00060`–`INS-00089` đã được tạo trước main harness, SHA-256 `a122dda63a40ab8db43d1af2a6a7019ca561c4c9e533db0e798fe9470e88cfa6`; rerun identical, không giao với pilot.
- [2026-09-15] MAIN STUDY PROTOCOL — RQ1 và H1 được đóng băng trước code main harness: 30 fresh tasks, 1,350 deterministic episodes, matched K=2, task-cluster bootstrap.
- [2026-09-14] ACTION-BOUNDARY GATE — 108 episodes, `69/69` refund attempts verified; common-mode unsafe refund provenance `0/18` vs random `2/18`.
- [2026-09-14] FULL LIVE-AGENT GATE — 36 episodes trên sáu tasks, 331 model calls, 19 tests pass. Technical execution pass nhưng experimental validity fail.

## Active Thread

Research hiện tập trung vào [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]. RQ1 pass controlled main gate nhưng fail broad imperfect-provenance robustness; canonical scope hiện là **given accurate failure-domain metadata**. Exact combination chưa có direct match, nhưng external executable benchmark cũng chưa có. Gap vẫn `SURVIVES WITH REFINEMENT — PRELIMINARY`, novelty confidence trung bình và external validity yếu.

## Guardrails

- Gap vẫn `SURVIVES WITH REFINEMENT — PRELIMINARY`, không confirmed novel.
- Không quay lại Selective Recovery Routing, broad Early Failure Detection hoặc generic Completion Verification.
- Không dùng ToolBench-X làm primary benchmark.
- Core experiment phải offline/deterministic; Groq/Gemini free tier chỉ optional validation.
- Không giao safety enforcement cuối cùng cho LLM self-assessment nếu deterministic runtime monitor có thể kiểm tra disagreement.
- Không claim “first tool trust selector”, “first provenance-aware action gate” hoặc “first dependency validation”.
- Không mở rộng RQ sang học/validate failure-domain metadata; đó là một research problem riêng vượt scope 12 tuần.
- Mọi experiment/literature result mới phải cập nhật claim–evidence ledger trước khi sửa Abstract, contributions hoặc Conclusion.
- Vault lint vẫn báo các vấn đề cũ ở `AGENTS.md`, root daily note, generated experiment READMEs và missing trust ledger; không có broken link hay frontmatter issue mới từ main-study journal.

## Next Action

Manual-audit và freeze 12 read-before-write cases từ Agent-SafetyBench/WorkBench trên ít nhất sáu domains. Mỗi case cần decisive claim, irreversible action, canonical truth, primary evidence, same-domain replica, independent corroborator và programmatic oracle; nếu không đủ 12 cases mà không bóp méo semantics, bỏ secondary adaptation.
