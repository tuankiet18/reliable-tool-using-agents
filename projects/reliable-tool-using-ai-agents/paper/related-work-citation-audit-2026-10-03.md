---
title: "Rà Contributions, Related Work và citations — 2026-10-03"
category: project
tags: [paper-draft, prior-art, evidence, reproducibility, research-methods]
sources:
  - "journal/2026-10-04-pre-action-prior-art-audit.md"
  - "references/look-before-you-leap-pre-action-verification.md"
  - "projects/reliable-tool-using-ai-agents/paper/paper-draft.md"
  - "projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03.md"
  - "projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger.md"
  - "https://www.epfl.ch/labs/sacs/publications/"
  - "https://conf.researchr.org/track/ase-2026/ase-2026-research-track"
  - "https://github.com/EnvTrustBench/EnvTrustBench"
  - "references/agentos-typed-tool-mediation.md"
created: 2026-10-03T21:46:13+07:00
updated: 2026-10-04T10:31:00+07:00
summary: >-
  Paper v0.7 có 15 citation IDs; AgentOS contrast giới hạn ở artifact và LBYL26 ở realizability. Giữ reading scopes/ambiguities, không nâng novelty hoặc thêm experiments.
provenance:
  extracted: 0.65
  inferred: 0.30
  ambiguous: 0.05
base_confidence: 0.61
lifecycle: draft
tier: supporting
---

# Rà Contributions, Related Work và citations

## Phạm vi lượt ban đầu — v0.4, 2026-10-03

**FACT — EDITORIAL / SOURCE AUDIT:** Lượt này sửa paper `0.3 → 0.4`, không chạy runner, model API hoặc GPU, không sửa raw/protocol, không thêm CI. Đây là AI-assisted audit, không independent human review. Đối chiếu lại metadata và những sections cần cho contrast; **không** nói đã deep-read toàn bộ 14 papers.

## Contributions có thể trình bày

1. Controlled decision-level comparison với actor, topology, oracle và matched two-observation budget tại mỗi refund proposal.
2. Characterization có analytical expectation, conditional utility, negative controls và metadata-sensitivity failure. Counterfactuals là hậu nghiệm, secondary variation được tái dựng từ schedule.
3. Reproducible artifact để kiểm tra lại assumptions/counts; secondary executor và negative live-agent diagnostics chỉ là supplementary evidence.

**INFERENCE:** Đây là framing phù hợp hơn một “new agent algorithm”. Tổ hợp features chưa tìm thấy exact match không tự trở thành contribution. Giảng viên vẫn cần đánh giá độ sâu này có đủ cho môn học hay không.

## Citation ledger lịch sử — phạm vi đã đọc ở v0.4

Tên đầy đủ, authors, URLs và DOI nằm ở References của [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]; bảng này ghi mức evidence, không tạo bibliography song song.

| ID | Metadata/status đã đối chiếu | Mức đọc dùng cho contrast | Giới hạn |
|---|---|---|---|
| RIVA26 | arXiv v1; EuroMLSys ’26, pp. 499–509; DOI trên EPFL publications | Full text, §3–5 và published PDF | Có alternative verification paths; không được mô tả chỉ là đổi tên tool. Không chạy implementation. |
| RLVM26 | arXiv 2607.07405v2, preprint | Full HTML, read-only pre-write gate và evaluation | No head-to-head; không suy hệ thống chắc chắn fail ở topology của mình. |
| VTC26 | arXiv 2608.02645v1, preprint | Full HTML, verify-before-retry và verifier assumptions | Non-atomic execution/retry khác failure-domain selection. |
| ROB26 | arXiv 2608.22676v2, preprint | Full HTML, return-boundary signals và evaluation | Detection endpoint khác authorization endpoint. |
| TEA26 | arXiv 2602.21517v1, preprint | Full HTML, trust selection/training/evaluation | Learned expertise theo query, không mặc nhiên là fault independence. |
| PC24 | ACL Anthology; Findings EMNLP 2024, pp. 16781–16805, DOI | Metadata/abstract; PDF mở nhưng không rà mọi section | Chỉ dùng calibration claim hẹp; không suy capability chưa đọc. |
| PGF26 | arXiv 2606.18037v3, preprint | Full HTML, attribution/support và limitations; official repo page | Phân biệt với PGA26; code không rerun trong lượt này. |
| PGA26 | arXiv 2607.01236v2; ASE ’26 official program | Full HTML, §4/5/8; official program và repo | DOI có trong paper; publisher page không đọc được. Chưa xác minh pagination. |
| GRADE26 | arXiv 2606.22741v2, preprint | Full HTML, dependency evidence grades/controls | Dependency edge không phải validated failure-domain ground truth. |
| AF26 | arXiv 2607.01640v1, preprint | Full HTML, static ADG và evaluation | Bổ sung entry AgentFlow từng bị thiếu; không chạy static analyzer. |
| ENV26 | arXiv 2605.08828v2, preprint | Full HTML và current public README/release scope | Public aggregate không thay thế executable cases/oracles/runners. |
| AGOS26 | Authors/title/DOI/track từ official ASE ’26 page | Metadata và official README; full paper chưa được đọc | Chỉ adjacent-work evidence; không suy absence của correlated-failure evaluation. |
| CE25 | Official ICML 2025/PMLR 267, pp. 30038–30066 | Metadata/abstract/BibTeX | Analogous model-error correlation, không direct tool-output prevalence. |
| KL86 | IEEE TSE 12(1), pp. 96–109, DOI; DBLP corroboration | Metadata; publisher full text không đọc lại được | Không thêm quantitative claims từ full text chưa kiểm tra. |

## Các contrast đã sửa

- **FACT:** RIVA thực sự tìm alternative verification techniques. Contrast phải dựa trên evaluated fault/dependency model, không strawman “họ chỉ đếm tên tools”. [Full text §3–5](https://arxiv.org/html/2603.02345v1).
- **INFERENCE:** Contextual provenance support không đồng nghĩa external truth hoặc failure independence. Nhưng không có head-to-head thì không được nói hai ProvenanceGuard methods chắc chắn thất bại trong setting này. [PGA26 §4/5/8](https://arxiv.org/html/2607.01236v2), [PGF26 limitations](https://arxiv.org/html/2606.18037v3).
- **FACT:** AgentOS là additional adjacent threat với framing rộng về pre-execution mediation và world-effect evaluation; coverage còn hạn chế, xem [[references/agentos-typed-tool-mediation]].
- **FACT — RELEASE CHECK:** EnvTrustBench public page vẫn chưa đủ để tái lập nguyên benchmark; không dùng aggregate attack rates để suy production prevalence. [Official repository](https://github.com/EnvTrustBench/EnvTrustBench).

## Điều chưa được giải quyết

**OPEN QUESTION:** Contribution có đủ sức nặng ngoài môn học? Hiện chưa có independent topology, human case/oracle audit, direct system comparison hoặc live policy-effect evidence. Analytical result gần by-construction làm novelty yếu hơn, không được che bằng tổng số episodes.

`SURVIVES WITH REFINEMENT — PRELIMINARY` chỉ còn là trạng thái tìm kiếm của setting hẹp, không confirmed novelty. Không mở lại recovery routing hoặc học metadata để cứu novelty.

## Bước tiếp theo

**Historical — 2026-10-03:** Rà toàn văn và structure/reproduction pass đã được thực hiện ở v0.5–v0.6. [[projects/reliable-tool-using-ai-agents/paper/supervisor-methodology-rq-briefing]] dùng cho giảng viên review methodology/RQ/contribution, không xin case-level sign-off.

**Delta search — 2026-10-04, trước v0.7:** [[journal/2026-10-04-pre-action-prior-art-audit]] nâng AgentOS coverage lên targeted pinned-code/72-task-archive inspection, **full paper vẫn chưa đọc được**; thêm [[references/look-before-you-leap-pre-action-verification]] từ full HTML. Bảng trên là hồ sơ lượt v0.4, không sửa ngược lịch sử phạm vi đọc.

## Current citation delta — paper v0.7

**FACT — INTEGRATION:** §3.2/§3.7 và bibliography đã tích hợp hai contrasts dưới đây. Có 15 unique IDs trong manuscript; 13 IDs còn lại giữ nguyên reading scope của bảng lịch sử, không tuyên bố re-read chúng trong lượt này. Không numerical comparison, head-to-head, study episodes hoặc novelty upgrade.

| ID | Phạm vi được phép dùng hiện tại | Evidence locator | Giới hạn giữ nguyên |
|---|---|---|---|
| AGOS26 | Artifact-level typed authorization và world-integrity/task predicates | `authorization_policy.py`, `run_vtrm_eval.py` ở commit `4147c7f780ccb59b83f3dba8da5f19e73a1d1a8c`; [[references/agentos-typed-tool-mediation]] | Full paper chưa đọc, published experiment mapping và baseline fairness chưa xác minh; không suy absence của correlated-fault evaluation hoặc formal end-to-end correctness. |
| LBYL26 | Realizability khác semantic correctness; deterministic pre-action verification đã có prior art | HTML §2/§5; [[references/look-before-you-leap-pre-action-verification]] | Preprint, supplementary/code/data chưa kiểm tra; date/release/wording ambiguity giữ trong note. Không trích quantitative result hoặc guarantee zero silent failure. |

**INFERENCE — QUYẾT ĐỊNH CITATION:** Nguồn có uncertainty vẫn có thể dùng cho claim hẹp được kiểm tra trực tiếp; không dùng phần uncertainty làm supporting evidence. Không biến số citations tăng từ 14 lên 15 thành evidence research mạnh hơn hoặc confirmed novelty.

**Bước tiếp theo hiện hành:** final claim–evidence consistency check giữa manuscript, appendix và reproduction package, kèm danh sách submission-readiness blockers. Không cần chạy RTX 4060; human review/course format/license vẫn là việc riêng.

## Related

- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
- [[projects/reliable-tool-using-ai-agents/paper/reviewer-audit-2026-10-03]]
- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]]
- [[synthesis/Preliminary Gap: Provenance-Aware Verification under Correlated Tool Failures]]
- [[projects/reliable-tool-using-ai-agents/reliable-tool-using-ai-agents]]
