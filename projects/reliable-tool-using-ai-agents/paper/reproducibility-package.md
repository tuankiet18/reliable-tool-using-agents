---
title: >-
  Reproducibility package — Controlled refund authorization study
category: project
tags: [reproducibility, paper-draft, evidence, research-methods, verification]
sources:
  - "journal/2026-10-04-clean-environment-core-reproduction.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_clean_env_reproduction_20261004/run-report.json"
  - "projects/reliable-tool-using-ai-agents/paper/figure-guide.md"
  - "projects/reliable-tool-using-ai-agents/paper/build_review_pdf.py"
  - "projects/reliable-tool-using-ai-agents/paper/review/paper-review-v0.9-2026-10-05.pdf"
  - "projects/reliable-tool-using-ai-agents/paper/artifact-inventory.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/README.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_main_study.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_robustness_gate.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_secondary_varied.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_secondary_varied.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_topology_diagnostics.py"
  - "https://raw.githubusercontent.com/mohammadi-hadi/trajectory-judge/d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5/pyproject.toml"
  - "https://raw.githubusercontent.com/mohammadi-hadi/trajectory-judge/d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5/LICENSE"
  - "https://raw.githubusercontent.com/cmu-soda/ProvenanceGuard/3ad7141db44096e1440718618bdb24fa46c003ff/README.md"
  - "https://api.github.com/repos/olly-styles/WorkBench/git/trees/00670510c8a476acd247925cefb17fee88500737"
created: 2026-10-03T22:26:57+07:00
updated: 2026-10-05T09:14:46+07:00
summary: >-
  Core replay trong clean venv cùng host: 10 files khớp frozen, 15 tests đạt; secondary/fresh-machine chưa kiểm, public release còn cần snapshot/license gate.
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.59
lifecycle: draft
lifecycle_changed: 2026-10-03
tier: supporting
---

# Reproducibility package

## 1. Phạm vi đã xác nhận

**FACT — LOCAL REANALYSIS, 2026-10-03 / v0.5:** Python 3.12.3 trên Linux, standard library; không model/API/GPU. Tái phân tích frozen main, robustness, secondary và analytical artifacts trong thư mục tạm cho **8/8 selected outputs byte-identical**: main/robustness mỗi bộ summary/inference/decision, secondary analysis-summary và topology analysis. Không tạo policy episodes hoặc CI mới; chỉ tính lại CIs đã có với cùng analyzer/seeds. Audit v0.8 ngày 2026-10-04 kiểm stored counts/hashes và tài liệu, không lặp lại reanalysis này.

**FACT — CORE GENERATION REPLAY, 2026-10-04 / v0.9:** Clone mới upstream pinned và cài base package vào venv mới; system/user site-packages không dùng, trước install chưa có pydantic. Main 1,350 và robustness 3,750 decisions được tái tạo với frozen tasks/seeds; 10 selected raw/manifest/summary/inference/decision files khớp byte-for-byte. 15 focused tests đạt. Không thêm independent samples, model/API calls hoặc live episodes. Report và observed runtime pins ở `results_clean_env_reproduction_20261004/`; [[journal/2026-10-04-clean-environment-core-reproduction]] giải thích setup/scope.

**Chưa xác nhận:** fresh-machine/independent reproduction, secondary generation trong venv mới, full dependency/wheel/build lock, optional live-agent execution, independent human case review hoặc public-release licensing clearance. Fresh venv không fresh host; historical checks giữ chronology riêng.

Package status: **CANDIDATE**, không public release freeze. Research HEAD 18bcf40e92755a6fed05ec2cdacb5cf863cd7410 đi kèm dirty working tree; HEAD riêng chưa identify paper/package hiện tại. Machine-readable [artifact-inventory.json](artifact-inventory.json) khóa 21 selected file hashes, không toàn bộ dependency closure. Hash manuscript/package được ghi ở vault manifest sau revision.

## 2. Artifact inventory và endpoints

Tất cả paths dưới đây relative với experiment directory:

| Evidence | Inputs chính | Raw / output | Phạm vi |
|---|---|---|---|
| Main | data/tasks_main_30.json + manifest; run_main_study.py | results_main_study/raw.jsonl, inference.json, decision.json | 1,350 decisions; 30 task clusters, không refund execution. |
| Robustness | data/tasks_robustness_30.json + manifest; run_robustness_gate.py | results_robustness_gate/raw.jsonl, inference.json, decision.json | 3,750 decisions; overall FAIL ROBUSTNESS, same environment. |
| Secondary | secondary_schema_contract_v1.json; secondary_varied_schedule_v1/schedule.jsonl | results_secondary_varied/episodes.jsonl, analysis-summary.json | 1,056 rows/528 pairs; 8 safety/6 domains, 2 utility, WB-295 ngoài denominator. |
| Analytical supplement | Sáu frozen inputs kiểm trong analyze_topology_diagnostics.py | results_topology_diagnostics_20261003/analysis.json | Post-hoc expectation/reconstruction/counterfactual, 0 new rows. |
| Live negative diagnostic | Run-specific archive/config/audits trong results_live_agent_opportunity_16cells_rtx4060_20261003/ | raw.jsonl + matched_pair_audit.json | 16 episodes, 0/4 matched opportunities; không effect estimate. |

Inventory không thay các run manifests/contracts gốc. Nếu hash mismatch, dừng; không sửa raw hoặc cập nhật expected hash chỉ để chạy pass.

## 3. Safe reanalysis — đã kiểm thử

Chạy từ experiment directory trong Linux/WSL2. Python cần khả năng đọc source hiện tại; 3.12.3 là phiên bản kiểm trong lượt này. Không cần pip install cho các analyzers dưới đây. Mỗi lần dùng một thư mục tạm **mới**, không results path đã freeze.

```bash
cd /path/to/research/projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot
set -euo pipefail
task_repro_dir=$(mktemp -d)
mkdir "$task_repro_dir/main" "$task_repro_dir/robustness"
cp results_main_study/raw.jsonl "$task_repro_dir/main/raw.jsonl"
cp results_robustness_gate/raw.jsonl "$task_repro_dir/robustness/raw.jsonl"

python3 src/analyze_main_study.py --results "$task_repro_dir/main"
python3 src/analyze_robustness_gate.py --results "$task_repro_dir/robustness"
python3 src/analyze_secondary_varied.py --out "$task_repro_dir/secondary.json"
python3 src/analyze_topology_diagnostics.py --output "$task_repro_dir/topology.json"

cmp results_main_study/summary.json "$task_repro_dir/main/summary.json"
cmp results_main_study/inference.json "$task_repro_dir/main/inference.json"
cmp results_main_study/decision.json "$task_repro_dir/main/decision.json"
cmp results_robustness_gate/summary.json "$task_repro_dir/robustness/summary.json"
cmp results_robustness_gate/inference.json "$task_repro_dir/robustness/inference.json"
cmp results_robustness_gate/decision.json "$task_repro_dir/robustness/decision.json"
cmp results_secondary_varied/analysis-summary.json "$task_repro_dir/secondary.json"
cmp results_topology_diagnostics_20261003/analysis.json "$task_repro_dir/topology.json"
```

Không có output từ cmp và exit 0 nghĩa là files khớp. Analyst vẫn phải dùng metric mapping paper §2.5: raw final_state_correct của main/robustness là action-oracle correctness; false_block gồm no-proposal abstention. Script output PASS không xác nhận novelty/external validity.

**Overwrite warning:** Main/robustness runner và analyzers có thể overwrite output mặc định. Secondary analyzer cũng có write_text không exclusive-create. Chỉ topology analyzer và varied runner có explicit existing-output rejection. Recipe dùng paths mới cho tất cả, không sửa scripts trong lượt này.

## 4. Generation rerun — core đã kiểm trong fresh venv cùng host

Upstream repos phải clone vào Linux filesystem nếu dùng WSL2; đừng materialize cả vault vào NTFS khi có filenames chứa dấu hai chấm. Dùng clone riêng, giữ nguyên working tree cũ.

| Repo | URL | Required HEAD |
|---|---|---|
| trajectory-judge | https://github.com/mohammadi-hadi/trajectory-judge | d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5 |
| ProvenanceGuard | https://github.com/cmu-soda/ProvenanceGuard | 3ad7141db44096e1440718618bdb24fa46c003ff |
| WorkBench | https://github.com/olly-styles/WorkBench | 00670510c8a476acd247925cefb17fee88500737 |

Kiểm git rev-parse HEAD trước chạy. Main/robustness manifest **ghi** upstream commit nhưng không thay manual HEAD check; secondary validator kiểm commit/hash. Không dùng latest main.

Pinned trajectory-judge pyproject yêu cầu Python >=3.12, pydantic>=2.7, httpx>=0.27 và typer>=0.12. Đây là ranges. Lượt v0.9 cài base package bằng `uv pip install --python /path/to/new-venv/bin/python /path/to/pinned-upstream`, không dev/serve/report extras. Quan sát 19 installed distributions gồm upstream; `requirements-environment.txt` ghi 18 third-party versions. Đây là **observed version pins**, chưa hash-locked wheels/build environment hoặc thử mọi dependency combination. Không claim đã tìm minimal dependencies; package `__init__` còn import judge modules.

Main/robustness CLI bên dưới đã thực thi trong fresh venv trên Linux bằng explicit venv Python, `-s`, bỏ PYTHONPATH/PYTHONHOME; cần --upstream và **--out mới**. Analyzer nhận --results cùng thư mục đó. Installation cần network/package registry; core generation/analysis không gọi model/API.

```bash
# Chạy trong môi trường Python đã cài upstream dependencies.
task_generation_dir=$(mktemp -d)
python src/run_main_study.py --upstream /path/to/trajectory-judge --out "$task_generation_dir/main"
python src/analyze_main_study.py --results "$task_generation_dir/main"
python src/run_robustness_gate.py --upstream /path/to/trajectory-judge --out "$task_generation_dir/robustness"
python src/analyze_robustness_gate.py --results "$task_generation_dir/robustness"
cmp results_main_study/raw.jsonl "$task_generation_dir/main/raw.jsonl"
cmp results_robustness_gate/raw.jsonl "$task_generation_dir/robustness/raw.jsonl"
```

Varied secondary runner giữ existing 704-row artifact làm integrity input; không xóa nó. CLI đã đối chiếu code nhưng **không rerun**:

```bash
task_secondary_dir=$(mktemp -d)
python src/validate_secondary_schema_contract.py --provenanceguard /path/to/ProvenanceGuard --workbench /path/to/WorkBench
python src/run_secondary_varied.py --provenanceguard /path/to/ProvenanceGuard --workbench /path/to/WorkBench --out-dir "$task_secondary_dir/varied"
python src/analyze_secondary_varied.py --rows "$task_secondary_dir/varied/episodes.jsonl" --out "$task_secondary_dir/analysis.json"
cmp results_secondary_varied/episodes.jsonl "$task_secondary_dir/varied/episodes.jsonl"
```

Typed secondary executor imports selected upstream tool classes; không khẳng định chỉ standard library cho full executor nếu chưa kiểm import closure/dependencies. Giữ source notices theo từng origin.

## 5. License và release gate

**FACT — SOURCE CHECK, không legal advice:**

- trajectory-judge pinned pyproject/LICENSE ghi MIT; URL ở frontmatter.
- ProvenanceGuard pinned README phân biệt Apache-2.0 cho code/author annotations và upstream MIT attribution cho benchmark-derived materials. Không đồng nhất toàn bộ artifact thành một license.
- Historical WorkBench commit tree không có LICENSE ở root; direct pinned LICENSE URL trả 404. MIT attribution trong ProvenanceGuard README là evidence **gián tiếp**, chưa independently verified license/notice cho đúng historical fixture. Không kết luận “unlicensed” hoặc “chắc chắn được redistribute”.
- Research vault hiện không có LICENSE/LICENSE.md ở root. Tác giả chưa chọn project-wide release license; không tự thêm hoặc gán MIT cho toàn bộ package.

**OPEN QUESTION / PUBLIC-RELEASE BLOCKER:** Xác minh đúng upstream licensing notices và quyền redistribution của materials trước public dataset/archive release. Private course review/reanalysis hiện tại không phải một quyết định cấp license mới. Không cần giải quyết bằng đổi scientific outcomes.

## 6. Derived figures — riêng với frozen study inventory

Hai SVG và figure-data.json tại `paper/figures/frozen-evidence-v1/` được thêm từ v0.6 và giữ nguyên ở v0.9. Script `src/generate_paper_figures.py` kiểm năm selected input hashes từ inventory, đối chiếu point estimates với raw, dùng stored CIs/gates và từ chối output directory đã tồn tại. Generator không rerun study episodes hoặc bootstrap; lượt v0.9 chạy core generators/analyzers riêng để reproduce existing estimates. Recipe và interpretation trong [[projects/reliable-tool-using-ai-agents/paper/figure-guide]].

9/9 figure tests, 7/7 main và 8/8 robustness focused tests đã đạt trong lượt figure revision; không full suite. Hai SVG đã render/kiểm trực quan trên Linux. Derived figure outputs không thay hoặc mở rộng inventory 21 frozen artifacts; generator/tests/output hashes được ghi riêng trong manifest revision.

## 6b. RQ4 / RQ3 trong paper — thí nghiệm LLM (2026-11-08)

Khác phần core, thí nghiệm này **cần OpenAI API** và dùng model đóng, nên chạy lại sẽ không cho đúng từng dòng (OpenAI không bảo đảm seed hoàn toàn xác định; mỗi lời gọi ghi `system_fingerprint`).

- **Chạy lại lời gọi:** `python data/rq4_agent_choice/runner/run_rq4.py --backend openai --model <tên model> --out <file mới>` với `OPENAI_API_KEY` trong môi trường; runner từ chối chạy nếu `items.jsonl` khác SHA-256 `e0b33c12…be086`. Resumable theo `item_id`.
- **Phân tích lại từ raw, không cần API:** `python src/rq4_analyze.py --results <hai file raw> --out <thư mục mới>` và `python src/rq4_breakdowns.py --results <hai file raw> --out <thư mục mới>`.
- **Hash:** raw `gpt-4o-mini` `20e6de8d…df0a`, raw `gpt-4.1-mini` `02d2f7d9…fe59`; `breakdowns.json` `d0b1d705…51d0`; `rq4_breakdowns.py` `67ccb128…5acd`.
- **Giới hạn:** hai model cùng hãng, đóng; model đổi sau khi khóa protocol v1.0 (Amendment A2, trước lời gọi đầu tiên); chưa nằm trong inventory 21 file đã khóa.

## 7. Tiêu chí bàn giao

Danh sách này chứa cả việc hoàn thiện bài môn học và public artifact release. Hai đích không tương đương; checklist được tách theo đích và owner tại [[projects/reliable-tool-using-ai-agents/paper/submission-readiness]]. Không mặc định giảng viên yêu cầu live-agent effect hoặc independent case audit. Những claim đó vẫn bị giới hạn nếu thiếu evidence.

- [x] Selected 21-file inventory với SHA-256 và origins/pins.
- [x] Main/robustness/secondary/topology reanalysis: 8 selected outputs byte-identical.
- [x] Same-host fresh-venv core installation/generation/analysis: 10 selected files byte-identical; 15 focused tests.
- [x] Expected endpoints/denominators và negative results được ghi riêng.
- [x] Commands dùng output mới, tránh overwrite frozen results.
- [ ] Commit/snapshot xác định package hiện hành — chưa commit/push theo yêu cầu.
- [ ] Fresh-machine generation/dependency audit nếu muốn independent reproduction claim.
- [ ] License/notice clearance trước public redistribution.
- [ ] Giảng viên review RQ/methodology/contribution.
- [x] Hai frozen-data figures với mẫu số, counterfactual và negative evidence rõ.
- [ ] Course-template layout, citation export và final author proofreading.

## 8. Bản PDF đọc để review

Đã tạo [[projects/reliable-tool-using-ai-agents/paper/review/paper-review-v0.9-2026-10-05.pdf]], một bản A4 24 trang gồm manuscript v0.9 đến References, supplementary appendix bắt đầu trang mới và danh sách đường dẫn hồ sơ nội bộ. Đây là bản đọc để tác giả/giảng viên góp ý RQ, methodology, baseline và mức contribution; chưa theo template môn học.

Builder `build_review_pdf.py` chỉ chuyển Markdown hiện có sang PDF; nó không sửa source paper hoặc tính lại metrics. Source paper SHA-256 `0e9855c81f0d4d91bb78b3c51944954a191cf1368713f163f47b730469403087`; PDF SHA-256 `a19c39ae50a7c85396319cf3b288ba32fba48d1e270f62092c716abd18af3a1a`. Bản render được kiểm tra bằng `pdfinfo`, `pdftotext` và xem trực quan trang đầu, hai trang figure, trang appendix đại diện và contact sheet toàn PDF.

Tái xuất từ vault root bằng:

```bash
python3 projects/reliable-tool-using-ai-agents/paper/build_review_pdf.py
```

Builder cần Python package `markdown`, LibreOffice và ImageMagick `convert`; các dependency này chỉ dùng cho dàn trang artifact. Nếu source Markdown thay đổi, tạo snapshot mới và kiểm tra lại hash/render trước khi dùng bản đó.

## Related

- [[journal/2026-10-04-clean-environment-core-reproduction]]
- [[projects/reliable-tool-using-ai-agents/paper/submission-readiness]]
- [[projects/reliable-tool-using-ai-agents/paper/figure-guide]]
- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]
- [[projects/reliable-tool-using-ai-agents/paper/supplementary-appendix]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
- [[projects/reliable-tool-using-ai-agents/paper/supervisor-methodology-rq-briefing]]
