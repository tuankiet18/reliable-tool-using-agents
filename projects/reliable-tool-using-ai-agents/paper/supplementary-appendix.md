---
title: >-
  Phụ lục — Chronology, debugging và evidence scope
category: project
tags: [paper-draft, reproducibility, evidence, research-methods, verification]
sources:
  - "journal/2026-10-05-main-study-influence-audit.md"
  - "journal/2026-10-04-clean-environment-core-reproduction.md"
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "journal/2026-09-13-correlated-tool-verification-pilot.md"
  - "journal/2026-09-14-full-live-agent-verification-gate.md"
  - "journal/2026-09-15-action-boundary-main-study.md"
  - "journal/2026-09-15-imperfect-provenance-robustness-gate.md"
  - "journal/2026-09-15-external-validity-artifact-gate.md"
  - "journal/2026-09-20-ai-review-provenance-correction.md"
  - "journal/2026-09-28-secondary-exploratory-matrix.md"
  - "journal/2026-09-28-secondary-varied-schedule-replication.md"
  - "journal/2026-09-30-rtx4060-live-agent-diagnostic.md"
  - "journal/2026-10-02-ins32-rtx4060-validity-audit.md"
  - "journal/2026-10-03-live-agent-opportunity-diagnostic.md"
  - "projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03.md"
created: 2026-10-03T22:26:57+07:00
updated: 2026-10-05T08:15:00+07:00
summary: >-
  Giữ pilots, schema/Windows debugging, protocol deviations và negative live diagnostics ngoài main narrative; không gộp chúng thành independent evidence.
provenance:
  extracted: 0.85
  inferred: 0.13
  ambiguous: 0.02
base_confidence: 0.59
lifecycle: draft
lifecycle_changed: 2026-10-03
tier: supporting
---

# Phụ lục của living paper

**FACT — EDITORIAL REORGANIZATION:** Giữ discovery/debugging history được rút gọn khỏi main manuscript. Không thêm samples, không sửa frozen artifacts, không biến retrospective analysis thành pre-specified hypothesis. Journals/protocols gốc là nguồn chronology đầy đủ.

## A. Chronology và mức evidence

| Stage | Quy mô lịch sử | Vai trò / giới hạn |
|---|---:|---|
| Exploratory pilot | 600 rows | Mechanics/baseline selection, không primary sample. |
| 30-task next gate | 3,600 rows | Metadata/fault exploration, không independent preregistration. |
| Qwen2.5-1.5B full live-agent gate | 36 episodes | Validity fail về compliance/completion. |
| Action-boundary mechanism gate | 108 rows | Exploratory enforcement-point check. |
| Main deterministic study | 1,350 decision rows | Internal pre-specified comparison với task/protocol chronology trước run. |
| Imperfect-provenance robustness | 3,750 decision rows | Post-main amendment trước stress-test run. |
| Secondary adapter smoke | 32 rows | Executor/schema mechanics, không effect estimate. |
| Secondary matrix ban đầu | 704 rows | Exploratory/internal, historical superseded schedule. |
| Secondary varied schedule | 1,056 rows | Current exploratory adaptation, không native reproduction. |
| RTX 4060 INS-00030 / INS-00032 | 6 / 8 episodes | Không hợp lệ để estimate selector safety advantage. |
| RTX prospective opportunity gate | 16 episodes | 0/4 matched unsafe-capable pairs, stop scaling. |
| Reviewer/analytic/editorial revisions | 0 new episodes | Construct correction, reconstruction và manuscript revisions. |

**Giới hạn timestamp:** Internal notes/hashes không independent registry. Initial Git snapshot chứa cả study và results; không dùng Git history riêng để chứng nhận external preregistration. Wording preregistered còn trong historical raw/scripts không mở rộng current claim.

## B. Pilots và quyết định baseline

600-row pilot: provenance_aware có common-mode unsafe acceptance 0.00 so với fixed-K 0.34, nhưng abstention tăng 0.00 → 0.64. So với random-K, difference chỉ −0.06, CI [-0.12,0.00]. Vì vậy chọn random-K là primary baseline và phải báo safety cùng utility. Pilot policies/actor/endpoints không tự tương đương main; không pool rows/CIs. [[journal/2026-09-13-correlated-tool-verification-pilot]].

Qwen2.5-1.5B gate: prompt-only compliance zero, enforced coverage 50–67%, reply completion thấp. Negative result dẫn tới mandatory boundary trong controlled actor study, không chứng minh đã sửa mọi live-agent failure. [[journal/2026-09-14-full-live-agent-verification-gate]].

## C. Secondary schema/case-review history

Artifact gate load được 182 selected Agent-SafetyBench và 388 WorkBench traces từ ProvenanceGuard, chạy ba analysis notebooks offline; không native redundant sources/failure domains. Audit chọn 12 IDs (6+6) trên 10 atomic domains. P/S/I và fault topology do project thêm. Technical availability không direct external validity.

AI-assisted review phát hiện omission-only cases, thiếu distractors, no-op mutation và incomplete search scope. WB-110 cần latest-email completeness; WB-433 cần full-scope snapshot/shared context; WB-295 cần historical CRM fixture với wrong target thật; ASB-977 đổi proposed 300000 no-op sang 200000. Exact-schema review từng trả 2 APPROVE / 5 REVISE; subsequent v1.2 recheck/smoke kiểm typed observations/actions/oracles và fairness hashes. Không có human sign-off. [[journal/2026-09-20-ai-review-provenance-correction]], [[projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/secondary-schema-gate]].

Current denominators: 8 safety cases/6 domains, 2 utility-only; WB-295 restoration diagnostic ngoài denominator, ASB-267 INVALID_NOT_RUN. Contract còn candidate; amendment công khai thiếu human review, không gọi AI là teammate/peer reviewer.

704-row schedule cũ: unsafe 40/64 vs 16/64, cùng difference −0.375 ở cả 8 cases, CI [-0.375,-0.375] suy biến vì schedule đồng nhất. Utility-only false blocks 6/16 vs 12/16. Varied schedule giữ cohort; whole unsafe-count variation suy được từ overlap quotas. Không independent topology replications. [[journal/2026-09-28-secondary-exploratory-matrix]], [[journal/2026-09-28-secondary-varied-schedule-replication]].

## D. RTX 4060 và debugging portability

- Windows checkout gặp filenames chứa dấu hai chấm; dùng WSL2/Linux hoặc Windows-safe experimental branch để materialize. Đây không research result.
- Runner từng fail cp1252 khi ghi Unicode; UTF-8 regression/output logging là technical checks. Python/uv permission/cache fixes không model/policy failures.
- INS-00030 output ở Downloads bị generic filenames tái sử dụng; recovered ZIP khớp năm historical hashes. Re-audit dùng run-specific directory. [[journal/2026-09-30-rtx4060-live-agent-diagnostic]].
- INS-00032 seed 809 được chọn hậu nghiệm; 12 refund requests đều 0 EUR sau escalation. 8/8 final-state đúng không selector-effect evidence. [[journal/2026-10-02-ins32-rtx4060-validity-audit]].

Prospective 16-cell run: INS-00032..35, seed topology 1111, strict opportunity criterion khóa trước run. 0/8 targeted unsafe-capable cells, 0/4 matched pairs; mọi refund attempts 0 EUR sau escalation. 16/16 final-state correct, 0/16 unsafe, 6/6 checked attempts, 8/16 replies và 99 escalation calls là diagnostic outcomes. Random đôi khi không conflict nhưng vẫn block do amount mismatch; provenance conflict cũng block. Không outcome contrast, nên dừng scaling. [[journal/2026-10-03-live-agent-opportunity-diagnostic]].

## E. Editorial amendments

| Version | Sửa gì? | Điều không thay đổi |
|---|---|---|
| 0.2 | Decision-level endpoints; tách no-proposal và gate rejection. | Raw keys, actor/policy, measured outcomes. |
| 0.3 | Main πq=2/9, secondary 9−r reconstruction, abstention counterfactuals. | Không baseline episodes/CI mới; hậu nghiệm. |
| 0.4 | Contributions, prior-art matrix, 14 citation IDs/reading scope. | PRELIMINARY novelty, không head-to-head. |
| 0.5 | Whole-manuscript scope/chronology và reproduction package. | RQ/H1, frozen data và stop rule. |
| 0.6 | Hai frozen-data figures, denominator/counterfactual guide. | Không study rows, bootstrap hoặc effect estimate mới. |
| 0.7 | Bounded AgentOS/LBYL26 contrasts và 15 citation IDs. | Không head-to-head hoặc novelty upgrade. |
| 0.8 | Claim–evidence audit và course/public-release checklist; sửa version/chronology wording. | Numerical results, RQ/H1, raw/figure hashes; scientific limitations giữ nguyên. |
| 0.9 | Same-host clean-venv core installation/generation/analysis: 10 files byte-identical, 15 tests đạt. | Cùng tasks/seeds, không thêm independent samples, live effect hoặc human review. |

AI-assisted verdict **MAJOR REVISION** không tự đóng bởi editorial pass. Human review tập trung RQ/methodology/contribution, không giả định giảng viên đã audit case/oracle.

## F. Ảnh hưởng của task, seed và stratum — bổ sung hậu nghiệm 2026-10-05

**FACT — POST_HOC DESCRIPTIVE SENSITIVITY:** Trên frozen main raw, lần lượt loại một task (30 lần), một seed (5 lần) hoặc một difficulty stratum (6 lần), giữ nguyên pairing giữa policies, rồi tính lại unsafe-rate difference `provenance_k − random_k`. Đây là phép tổng hợp subsets, không thêm experiment; main manuscript v0.9 và primary inference giữ nguyên.

| Regime | Full-sample Δ | Task-deletion range | Seed-deletion range | Stratum-deletion range |
|---|---:|---:|---:|---:|
| clean | 0.00 pp | 0.00–0.00 pp | 0.00–0.00 pp | 0.00–0.00 pp |
| independent | +0.67 pp | 0.00 đến +1.38 pp | 0.00 đến +0.83 pp | −0.80 đến +1.60 pp |
| targeted_common_mode | −20.00 pp | −20.69 đến −17.93 pp | −22.50 đến −17.50 pp | −24.00 đến −16.00 pp |

Targeted giữ Δ âm ở cả 41 subsets; errors của random không tập trung hoàn toàn vào một task/seed/stratum. Nhưng treatment zero unsafe được fault model bảo đảm, nên mọi subset vốn có Δ ≤ 0. Bỏ stratum còn đổi task composition; các ranges là **min–max mô tả, không confidence intervals**. Không suy ra population generalization, robustness với metadata sai hoặc live-agent effect. Independent sign thay đổi theo stratum deletion, phù hợp việc chưa có evidence rõ về advantage.

Script `src/analyze_main_influence.py` khóa raw hash, kiểm paired grid và từ chối overwrite. Report `results_main_influence_20261005/analysis.json` có từng deletion/numerator/denominator và exact difference; 7 tests đạt, 123 retained differences được đối chiếu qua SQL, replay cùng-host byte-identical. Chi tiết, hashes và recipe ở [[journal/2026-10-05-main-study-influence-audit]]; claim được phép dùng ở ledger C32. Đây là bổ sung cho statistical interpretation, không đóng reviewer R7.

## Related

- [[projects/reliable-tool-using-ai-agents/paper/submission-readiness]]
- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]
- [[projects/reliable-tool-using-ai-agents/paper/reproducibility-package]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
- [[projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03]]
