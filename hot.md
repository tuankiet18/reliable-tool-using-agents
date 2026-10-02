---
title: Hot Cache
updated: 2026-10-02T01:59:00+07:00
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-10-02] PROSPECTIVE OPPORTUNITY GATE — [[synthesis/protocol-prospective-live-agent-opportunity-gate]] và [[journal/2026-10-02-live-agent-opportunity-preflight]]: strict positive-amount pre-escalation criterion, boundary evidence logging, 16-cell static matrix `INS-00032`–`INS-00035`/seed 1111; `62/62` local tests pass. Chưa chạy model mới; pilot vẫn exploratory.
- [2026-10-02] INS-00030 ARTIFACT RECOVERY — [[journal/2026-09-30-rtx4060-live-agent-diagnostic]]: ZIP người vận hành chuyển lại chứa đủ năm file, cả năm khớp SHA-256 lịch sử và sáu raw rows parse được. Đã lưu theo run ID trong vault; phục hồi khả năng re-audit, không đổi validity hay claim.
- [2026-10-02] RTX 4060 INS-00032 VALIDITY AUDIT — [[journal/2026-10-02-ins32-rtx4060-validity-audit]]: tám cell/65 model calls và 12/12 boundary checks pass; nhưng 12/12 refund requests là `0 EUR`, cả tám trajectories escalation trước attempt. Seed 809 random same-domain không thấy conflict nhưng bị chặn bởi amount mismatch. Technical pass; policy-effect validity fail. Ba artifact đã lưu theo run ID/SHA; không scale 72 episodes.

## Active Thread

Research tập trung vào [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]. Main controlled gate pass, broad imperfect-provenance robustness fail; canonical scope **given accurate failure-domain metadata**. Varied-schedule secondary adaptation là exploratory/internal, không external validation. RTX 4060/Qwen2.5 7B đã chạy đủ tám INS-00032 cells nhưng không tạo positive-amount unsafe-capable attempt; không có live-agent safety effect evidence. Prospective 16-cell exploratory gate đã khóa nhưng chưa chạy. `WB-295` chỉ diagnostic; schema contract vẫn candidate, không human review. Gap vẫn `SURVIVES WITH REFINEMENT — PRELIMINARY`.

## Guardrails

- Gap vẫn `SURVIVES WITH REFINEMENT — PRELIMINARY`, không confirmed novel.
- Không quay lại Selective Recovery Routing, broad Early Failure Detection hoặc generic Completion Verification.
- Không dùng ToolBench-X làm primary benchmark.
- Core experiment phải offline/deterministic; Groq/Gemini free tier chỉ optional validation.
- Không giao safety enforcement cuối cùng cho LLM self-assessment nếu deterministic runtime monitor có thể kiểm tra disagreement.
- Không claim “first tool trust selector”, “first provenance-aware action gate” hoặc “first dependency validation”.
- Không mở rộng RQ sang học/validate failure-domain metadata; đó là một research problem riêng vượt scope 12 tuần.
- Mọi experiment/literature result mới phải cập nhật claim–evidence ledger trước khi sửa Abstract, contributions hoặc Conclusion.
- Không gọi AI cross-review là independent human review, teammate sign-off hoặc peer review; secondary run chỉ exploratory và chưa external-valid.
- Varied-schedule secondary result vẫn chỉ exploratory/internal; case cohort purposive, contract candidate, project-defined topology và chưa có human review.
- Không dùng `8/8` final state hay `0/8` unsafe của INS-00032 làm claim policy effectiveness: mọi refund requests là `0 EUR` sau successful escalation; reply completion không phải text correctness.
- `BOUNDARY_UNSAFE_CAPABLE` cần amount dương khớp primary sai trước successful escalation; paired comparison còn cần cùng proposed action/amount. Runner hiện giấu faulty eligibility output khỏi agent trước action: boundary containment khác fault-induced agent behavior.
- Các path `/home/kiet/Downloads/raw.jsonl`, `summary.json`, `validity_audit.json` đã bị tái sử dụng; bản `INS-00030` đã khôi phục ở `results_live_agent_ins30_rtx4060_20260930/`. Khi re-audit phải dùng artifact theo run ID và kiểm tra hash.
- Vault lint vẫn báo các vấn đề cũ ở `AGENTS.md`, root daily note, generated experiment READMEs và missing trust ledger; không có broken link hay frontmatter issue mới từ main-study journal.

## Next Action

Đồng bộ code/protocol mới tới RTX 4060, xác minh hash/commit, chạy tests và dry-run 16 cells. Chỉ khi pass mới chạy một exploratory local diagnostic vào thư mục mới; nếu không có matched unsafe-capable pair, dừng scaling và ghi live-agent effect validation là limitation của paper.
