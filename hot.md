---
title: Hot Cache
updated: 2026-10-13T14:00:00+07:00
---

# Hot Cache

## Recent Activity

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

Theo [[projects/reliable-tool-using-ai-agents/HANDOFF-2026-10-13]] §4: (1) hỏi tác giả trước khi push `4d2b1dd`; (2) coder A gán nhãn 78 server survey 2 theo §5 của [[synthesis/Protocol: Expanded Real-Tool Metadata Survey]], lưu tiến độ vào repo sau mỗi nhóm; (3) phân tích P1–P6; (4) ledger rồi paper. Các mục Active Thread/Guardrails phía trên là lịch sử đến v0.9; nơi có hiệu lực là ledger và handoff.
