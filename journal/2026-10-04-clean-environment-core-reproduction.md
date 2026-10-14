---
title: "2026-10-04 — Tái tạo core study trong clean Python environment"
category: journal
tags: [research-log, reproducibility, paper-draft, evidence, research-methods]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_clean_env_reproduction_20261004/run-report.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_clean_env_reproduction_20261004/requirements-environment.txt"
  - "projects/reliable-tool-using-ai-agents/paper/artifact-inventory.json"
  - "projects/reliable-tool-using-ai-agents/paper/reproducibility-package.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_main_study.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/run_robustness_gate.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_main_study.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_robustness_gate.py"
  - "https://github.com/mohammadi-hadi/trajectory-judge/tree/d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5"
created: 2026-10-04T16:40:00+07:00
updated: 2026-10-04T16:40:00+07:00
summary: >-
  Fresh clone/base install và core replay trong clean venv cùng host: 10 files khớp frozen, 15 tests đạt. Không independent samples hoặc fresh-machine validation.
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
base_confidence: 0.59
lifecycle: draft
lifecycle_changed: 2026-10-04
tier: supporting
---

# Core experiment có phụ thuộc môi trường cũ không?

## Mục tiêu và kết quả

**FACT — LOCAL CLEAN-VENV REPRODUCTION PASS:** Main và robustness generators/analyses chạy được sau khi clone pinned upstream và cài dependencies vào Python environment mới. 10 selected files khớp byte-for-byte với bản frozen; 15 focused tests đạt. Main vẫn PASS, robustness vẫn FAIL ROBUSTNESS. Không dùng GPU hoặc model/API calls.

**INFERENCE:** Evidence mới giảm lo ngại rằng results chỉ chạy được nhờ packages đã cài sẵn trong môi trường cũ. Nó không chứng minh portability trên máy/OS khác, novelty, population generalization hoặc live-agent effectiveness.

Đây là bước bổ sung về reproducibility trong lúc course template/author readback/supervisor feedback còn mở; không thay việc tác giả đọc và hiểu paper.

## 1. Setup thực tế

- Host: Linux x86_64, Python 3.12.3; `uv` 0.12.12.
- Tạo riêng `/tmp/reliable-core-repro-w7jCJR/`; giữ nguyên mọi clone và môi trường cũ.
- Clone mới `trajectory-judge`, detached HEAD `d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5`; tracked worktree sạch sau install/run.
- Venv mới không system site-packages; user site disabled. Trước install, `pydantic` không có.
- Đọc pinned pyproject, World/trace và package entry point trước chạy. Không có upstream AGENTS.md. Cài **base package**, không dev/serve/report extras, bằng `uv pip install --python .../venv/bin/python .../upstream`.
- Quan sát 19 installed distributions gồm `trajectory-judge` 0.1.0; pydantic 2.13.5, httpx 0.28.1, typer 0.27.2. 18 third-party versions nằm trong `requirements-environment.txt`.
- Runner/analyzer dùng explicit venv Python với `-s`, bỏ `PYTHONPATH`/`PYTHONHOME`; không dùng environment API keys. `PYTHONDONTWRITEBYTECODE=1` cho các lượt core chạy.
- Pinned source và installed wheel có `world.py`, `trace.py`, `__init__.py` byte-identical (3/3); không suy rằng đã audit toàn installed package.

Installation dùng network/GitHub/package registry. Generation/analysis không gọi model; không diễn giải “API cost = 0” thành setup không cần internet.

**Giới hạn isolation:** Cùng kernel/host/CPU/Python base và researcher; research scripts lấy từ current dirty working tree, không clean committed research snapshot. Build isolation có thể cài build dependencies; versions/hashes của build environment chưa khóa. Không nói full dependency closure, minimal-dependency proof hoặc fresh-machine reproduction đã pass.

## 2. Những gì đã chạy

| Bước | Outcome | Phạm vi |
|---|---|---|
| Main generator | 1,350 replayed decision rows | Cùng 30 tasks/five seeds/config, không LLM/refund execution |
| Robustness generator | 3,750 replayed decision rows | Cùng metadata/fault conditions/tasks/seeds |
| Main analyzer | PASS; raw/manifest/summary/inference/decision khớp | Tính lại cùng bootstrap algorithm/seeds |
| Robustness analyzer | FAIL ROBUSTNESS; năm files khớp | Giữ required wrong-label condition fail |
| `test_main_study.py` | 7/7 | Focused unit tests |
| `test_robustness_gate.py` | 8/8 | Focused unit tests, không full suite |
| Frozen integrity | 21/21 inventory hashes giữ nguyên | Không đổi source/raw/analysis frozen |

Hai raw hashes giữ nguyên:

- Main: `a51aebcb207f996e7a4d065b2e424fe794346d685d5f37a615d0de6bcb872234`.
- Robustness: `f22e7f29c97a89eda20bdb57f9e59fa43581adb3d3b6475ee40e926492ab1982`.

Per-file hashes/paths và environment metadata ở `run-report.json`. “10/10” chỉ năm selected files mỗi study, không tuyên bố mọi file trong output hoặc toàn repo byte-identical. Outputs mới được giữ tại `results_clean_env_reproduction_20261004/`, không overwrite frozen paths.

## 3. Recipe core đã thực thi

Từ experiment directory trong Linux/WSL2, dùng paths mới cho từng lần. Không dùng block này để overwrite frozen results; không clone toàn vault lên NTFS nếu có filenames chứa dấu hai chấm.

```bash
set -euo pipefail
task_core_replay=$(mktemp -d /tmp/reliable-core-repro-XXXXXX)
git clone --no-checkout https://github.com/mohammadi-hadi/trajectory-judge.git "$task_core_replay/upstream"
git -C "$task_core_replay/upstream" checkout --detach d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5
test "$(git -C "$task_core_replay/upstream" rev-parse HEAD)" = d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5

UV_CACHE_DIR="$task_core_replay/cache" uv venv --python /usr/bin/python3 "$task_core_replay/venv"
UV_CACHE_DIR="$task_core_replay/cache" uv pip install --python "$task_core_replay/venv/bin/python" "$task_core_replay/upstream"

env -u PYTHONPATH -u PYTHONHOME "$task_core_replay/venv/bin/python" -s src/run_main_study.py --upstream "$task_core_replay/upstream" --out "$task_core_replay/main"
env -u PYTHONPATH -u PYTHONHOME "$task_core_replay/venv/bin/python" -s src/run_robustness_gate.py --upstream "$task_core_replay/upstream" --out "$task_core_replay/robustness"
env -u PYTHONPATH -u PYTHONHOME "$task_core_replay/venv/bin/python" -s src/analyze_main_study.py --results "$task_core_replay/main"
env -u PYTHONPATH -u PYTHONHOME "$task_core_replay/venv/bin/python" -s src/analyze_robustness_gate.py --results "$task_core_replay/robustness"

for task_replay_file in raw.jsonl run_manifest.json summary.json inference.json decision.json; do
  cmp "results_main_study/$task_replay_file" "$task_core_replay/main/$task_replay_file"
  cmp "results_robustness_gate/$task_replay_file" "$task_core_replay/robustness/$task_replay_file"
done

env -u PYTHONPATH -u PYTHONHOME "$task_core_replay/venv/bin/python" -s -m unittest discover -s tests -p test_main_study.py -v
env -u PYTHONPATH -u PYTHONHOME "$task_core_replay/venv/bin/python" -s -m unittest discover -s tests -p test_robustness_gate.py -v
```

Base dependency ranges sẽ resolve theo registry ở lúc install. Observed pins giúp ghi nhận môi trường đã pass; chưa phải portable/hash-locked installation recipe. Không dùng `python -I` trực tiếp cho robustness runner vì nó cần sibling-module imports; isolation hiện dùng fresh venv/`-s`/unset Python overrides.

## 4. Điều này có làm paper mạnh hơn không?

**FACT:** Core setup/generation/analysis được kiểm chứng thêm, không chỉ reanalysis từ raw có sẵn. Claim C31 và paper v0.9 §8 ghi chính xác mức evidence này.

**INFERENCE:** Paper mạnh hơn ở **khả năng kiểm tra và tái tạo (reproducibility)**. Không mạnh hơn ở novelty hoặc external validity. 5,100 replayed rows không được cộng vào sample size; CIs/estimates khớp kết quả cũ, không cung cấp independent replication của H1.

Các kết luận âm còn nguyên: targeted valid refunds 0/50, wrong-metadata robustness FAIL, secondary topology/schedule constructed, live opportunity 0/4 matched pairs. Không có human sign-off hoặc commit/push.

## 5. Gate còn mở và next action

**FACT — DOCUMENTATION/INTEGRITY CHECK:** 9/9 updated/created research-page frontmatters, local sources, path-qualified wikilinks và images hợp lệ; summaries ≤200 ký tự. RQ/H1 parity 3/3; 15 citation IDs, bibliography và chín scientific sections ngoài §8 giữ nguyên. Ba figure hashes không đổi. Recorded distributions khớp 19/19, third-party version pins khớp 18/18 với actual venv. `git diff --check` đạt. Đây không full-vault lint hoặc full-suite tests.

- Secondary generation/import closure chưa thử trong môi trường sạch.
- Fresh-machine/OS portability, independent reviewer/researcher reproduction chưa thực hiện.
- Public release snapshot/build/wheel lock/licensing chưa đóng.
- Author readback, course format/export và supervisor methodology/contribution feedback còn mở.

**Bước tiếp theo:** Hoàn thiện bản giải thích phương pháp để tác giả đọc và bảo vệ: một worked example cho common-mode faults, no-proposal false denial và always-escalate trade-off, dựa trên frozen raw. Không thêm thí nghiệm cùng seeds để tăng N; không viết thay phản hồi cá nhân của tác giả cho năm câu readiness.

## Related

- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]
- [[projects/reliable-tool-using-ai-agents/paper/reproducibility-package]]
- [[projects/reliable-tool-using-ai-agents/paper/submission-readiness]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
