---
title: Hot Cache
updated: 2026-11-08T23:00:00+07:00
---

# Hot Cache

## Recent Activity

- [2026-11-13] PAPER LATEX VIẾT LẠI — bản tiếng Anh (paper/latex) được viết lại cho liền mạch: abstract ngắn gọn, intro có findings và roadmap, RQ3 gộp hai thí nghiệm (thêm provider; đảo nhãn), discussion/threats gom nhóm, thêm mục Reproducibility. 14 trang, build sạch. Số liệu và claim không đổi. Bản đầy đủ tiếng Việt (paper-draft) và short chưa viết lại theo cùng văn phong. Chưa commit.
- [2026-11-13] RQ4 MỞ RỘNG (đảo nhãn) — [[journal/2026-11-13-rq4-label-inversion-results]]: đảo nhãn provider (C4, 40/56 bộ), prompt "consistency", thêm gpt-4.1; Amendment B1 đổi đại lượng chính sang `d` trước lời gọi đầu tiên. **11/11 kiểm định ghi trước đạt** ở gpt-4o-mini, gpt-4.1-mini, gpt-4.1: model tránh candidate mang nhãn của primary khi được nhắc độc lập, chọn nó nhiều hơn ở prompt trung tính, và chọn tool cùng nguồn 0,86–0,92 khi hỏi "nhất quán". Giải thích "đọc nhãn → hiểu là nhất quán" được ủng hộ bằng can thiệp. Ledger C53–C55; paper v2.1, short, LaTeX. Chưa commit.
- [2026-11-08] DOCS REFRESH — paper đổi cấu trúc: **Baseline** (replication, cũ RQ1) + RQ1 điều kiện J + RQ2 survey + RQ3 LLM (cũ RQ4); số cũ vẫn dùng trong ledger/journal/protocol. Đã cập nhật briefing v3.0, supervisor-overview.html, HANDOFF-2026-11-08, trang project, reproducibility-package §6b, README thí nghiệm. Chưa dựng lại supervisor-overview .pdf/.docx.
- [2026-11-08] RQ4 + PAPER v2.0 — [[journal/2026-11-08-rq4-agent-choice-results]]: `gpt-4o-mini` và `gpt-4.1-mini` (Amendment A2, thay Qwen/Llama vì máy chỉ có GPU 4 GB), 1.008 lời gọi mỗi model, 0 invalid. Prompt chính: shared-choice C0 0.423/0.339 → C1 0.107/0.054; H-A1 và H-A2 đạt cả hai model (p Holm < 0.0001). **Prompt trung tính ngược chiều:** C1 tăng lên ~0.80 (mô tả, không kiểm định, cơ chế chưa đo). Ledger C48–C51, O7; paper-draft v2.0 (§1.1, §4.10, §5.13, §7.8), paper-short 1.1, LaTeX thêm `06b-rq4-llm-choice.tex`. Chưa commit.
- [2026-11-08] WINDOWS MIGRATION — 29 file `synthesis/` tên có dấu `:` đổi thành ` -` (git thấy rename), link trong 109 file md và `.manifest.json` đã sửa; `core.autocrlf=false` cục bộ (hash frozen); obsidian-wiki skills cài tại `.claude/skills/`; `.env` trỏ vault vào repo này. `.py`/`.json` dữ liệu vẫn chứa tên cũ có `:` để giữ hash. Xem [[projects/reliable-tool-using-ai-agents/HANDOFF-2026-11-08]].
- [2026-10-14] SURVEY 2 — [[journal/2026-10-14-expanded-tool-survey-results]]: 78 MCP server (74 trong ước lượng, 245 cặp). ρ 0.27 [0.18, 0.37]; m_L1 0.71; J_L2 0.89. Đạt P1, P2, P4, P6; không đạt P3 (φ_L1 3/45) và P5 (web_search ρ_origin 0.71). Amendment A2 commit trước khi tính chỉ số (`fb41192`). Ledger C42–C46; paper v1.4 (§5.12, tiêu đề mới). Nhãn người cho 20 server chưa có.
- [2026-10-13] HANDOFF — đọc [[projects/reliable-tool-using-ai-agents/HANDOFF-2026-10-13]] trước tiên. Paper v1.3 định vị lại sau prior art VP-Control/EFD: RQ1 replication, RQ2 điều kiện `J = r − φ > 0` (đã chứng minh + kiểm định đăng ký trước), RQ3 survey 42 MCP server (16% cặp chung upstream; L1 thiếu nhãn 70%; coder B κ 0.78/1.00). Survey 2 (78 server) đã sàng lọc, **đang chờ coder A gán nhãn**.

- [2026-10-05] INFLUENCE AUDIT — [[journal/2026-10-05-main-study-influence-audit]]: targeted Δ giữ âm sau 30 task/5 seed/6 stratum deletions; stratum range −24 đến −16 pp. Independent stratum range −0.8 đến +1.6 pp. Post-hoc descriptive ranges, không CI; zero treatment by construction vẫn là limitation. 7 tests/123 SQL cross-checks đạt; appendix §F/ledger C32 cập nhật, manuscript v0.9/21 frozen/3 figure hashes giữ nguyên. Không study episodes/model calls mới.
- [2026-10-04] WORKED EXAMPLES — bổ sung §6 vào [[projects/reliable-tool-using-ai-agents/paper/figure-guide]], không tạo note mới. INS-00062/seed101: shared-domain wrong agreement về refund 142.12 EUR; INS-00060/seed101: false denial bỏ lỡ refund 91.12 EUR trước gate; always-escalate là counterfactual, không measured K=2 baseline. Đối chiếu 7 raw rows/4 policy-regime aggregates, 3 page schemas/links. Paper v0.9, 21 frozen hashes và 3 figure artifacts unchanged; không episodes/model/tests/bootstrap hoặc author/human sign-off mới.
- [2026-10-04] PAPER v0.9 — [[journal/2026-10-04-clean-environment-core-reproduction]]: mới clone/cài pinned trajectory-judge base package trong Python 3.12.3 venv không system/user packages. Main/robustness replay 1,350/3,750 rows và bootstrap analyses; 10 selected files byte-identical, 15 focused tests đạt. Không tăng independent N, model calls hoặc live scaling; main PASS/wrong-metadata FAIL giữ nguyên. §8/package/ledger cập nhật, scientific Results không đổi. Same-host fresh venv không fresh-machine/independent reproduction.

## Active Thread

Hoàn thiện controlled empirical course paper; không bắt buộc live-agent effect. Main/robustness là decision simulation, không executed refund state. Targeted unsafe decisions random 30/150 vs provenance 0/150; clean correctness 150/150, nhưng targeted correct refunds đều 0/50. Main expectation 2/9 và provenance zero suy từ topology. Always-escalate bằng provenance dưới targeted faults, mất clean refund utility. Secondary 59/96 vs 24/96 tái dựng hoàn toàn từ schedule; utility false blocks 9/24 vs 18/24. Wrong-label robustness fail.

Paper vẫn MAJOR REVISION, novelty SURVIVES WITH REFINEMENT — PRELIMINARY; chưa human sign-off. Editorial/figures/local reanalysis pass không đóng substantive limitations. Giảng viên chỉ cần review RQ/methodology/contribution, không giả định audit từng case/oracle. Live diagnostic 16 cells có 0/4 matched unsafe-capable pairs: stop scaling, zero unsafe không effect evidence.

## Guardrails

- Không quay lại rejected recovery routing/early failure detection hoặc generic verification. Không dùng ToolBench-X primary.
- Không first/new-algorithm/generalization/production claims; exact feature conjunction không proof of novelty. Không superiority khi chưa head-to-head.
- Không gọi AI cross-review là human/teammate/peer review. Secondary contract vẫn candidate, P/S/I do project thêm, exploratory/internal.
- Main raw final_state_correct = action-oracle correctness; false_block gồm no-proposal abstention. Không đổi raw keys để sửa wording.
- K=2 là modeled observations tại refund proposals; không actual latency/token/API cost. Counterfactuals hậu nghiệm, không measured baseline episodes.
- Internal pre-specified notes/hashes không independent preregistration registry.
- Live unsafe-capable criterion cần positive amount khớp primary sai trước successful escalation và matched proposal. Current gate failed; không scale RTX hoặc tune seeds để cứu effect.
- INS-00030 đã recovered theo run ID; không dùng generic Downloads filenames tái sử dụng để audit.
- Inventory khóa selected files, không toàn dependency closure. v0.9 core generation đã replay trong clean venv cùng host; secondary/fresh-machine chưa kiểm, observed runtime pins không wheel/build lock. Defaults có overwrite risk: chỉ output mới.
- Historical WorkBench thiếu root license; indirect MIT attribution cần verify trước public redistribution. Vault chưa project-wide license, chưa tự cấp license mới.
- Không commit/push hoặc gọi package public release khi chưa được yêu cầu.

## Next Action

(1) Hạn nộp paper khoảng 2 tuần kể từ 2026-11-08. (2) RQ4 còn thiếu: phân tích theo loại thông tin và tỷ lệ `reason` nhắc nguồn (protocol §2/§7); xem lại tiêu đề paper (chưa nhắc RQ4), §5.1 và bảng §3.7. (3) Build lại `paper/latex/main.pdf`, supervisor-overview và gửi giảng viên; tác giả đọc bản tiếng Anh. (4) Hỏi tác giả trước khi commit/push (nhiều thay đổi chưa commit: rename 29 file, link rewrite, A2, `run_rq4.py`, journal, ledger, paper). (5) Xóa API key cũ trên dashboard OpenAI. Bối cảnh: [[projects/reliable-tool-using-ai-agents/HANDOFF-2026-11-08]].
