---
title: "External-validity artifact gate — EnvTrustBench and ProvenanceGuard"
category: journal
tags: [research-log, reproducibility, benchmark, verification, external-validity]
sources:
  - "https://github.com/EnvTrustBench/EnvTrustBench"
  - "https://huggingface.co/datasets/Str1ck/envtrustbench-results"
  - "https://github.com/cmu-soda/ProvenanceGuard"
  - "https://arxiv.org/abs/2607.01236"
created: 2026-09-15T16:27:33+07:00
updated: 2026-09-15T16:27:33+07:00
summary: >-
  EnvTrustBench fail executable-artifact gate vì chỉ public aggregate data; ProvenanceGuard artifact chạy offline được nhưng chỉ PARTIAL fit cho correlated-failure RQ.
---

# External-validity artifact gate

## Mục tiêu

Kiểm tra xem có public benchmark thứ hai đủ executable để external-validate RQ về failure-domain-independent verification hay không. Gate ưu tiên [[references/envtrustbench]]; sau khi EnvTrustBench fail, kiểm tra [[references/provenanceguard-misalignment-provenance-analysis]] như phương án thay thế.

## Gate 1 — EnvTrustBench

### Artifact đã kiểm tra

- GitHub commit: `0763e9cf3da33076c103f69bf049172752c0bad5`.
- Hugging Face dataset commit: `2dbb49caf22703ecc0f06fd36b619e8ccbd5f6b0`.
- Đã fetch toàn bộ Git history, branches, tags và kiểm tra Git LFS; không có executable case bị bỏ sót do shallow clone.
- GitHub repository ghi MIT license; Hugging Face dataset card ghi `cc-by-nc-nd-4.0`. Đây là hai phạm vi artifact khác nhau và phải giữ nguyên distinction.

### Có gì công khai?

- Project documentation và benchmark definitions ở mức khái niệm.
- Aggregate matrix: 11 scenarios × 14 stacks.
- Leaderboard snapshot và paper-facing summary.
- Một uploader script cho Hugging Face; đây không phải benchmark runner.

### Kiểm tra dữ liệu

Từ public CSV có `154` scenario–stack cells, mỗi cell `25` runs. Tái tính được:

- total: `3,850` runs;
- false paths: `3,206`;
- pass: `644`;
- FPCR: `0.8327`, làm tròn `83.3%`.

### Thiếu gì?

Không public:

- scenario definitions có thể thực thi;
- `W0`, `E0`, `q`, `Omega` của từng case;
- case generator và oracle implementation;
- raw trajectories;
- benchmark runner/provider configuration.

Repository tự ghi rõ đây chưa phải complete reproducibility archive. Hình `database-migration-gate-decision` chỉ cho case shape, không đủ tái tạo official case.

### Verdict

`FAIL — NOT EXECUTABLE FOR THIS PROJECT NOW`.

Tự viết lại case từ hình minh họa sẽ tạo một synthetic adaptation mới, không phải external reproduction. EnvTrustBench chỉ được dùng làm motivation/aggregate evidence cho tới khi authors release cases và runner.

## Gate 2 — ProvenanceGuard replication artifact

### Artifact đã kiểm tra

- Commit: `3ad7141db44096e1440718618bdb24fa46c003ff`.
- Python 3.11 temporary environment; toàn bộ pinned requirements cài thành công.
- `compileall` pass; CLI load/help pass.
- License: Apache-2.0 cho source và author annotations; Agent-SafetyBench/WorkBench materials giữ upstream MIT terms.

### Data và offline reproduction

- Agent-SafetyBench: 194 traces, evaluation population `182`; 188 precomputed plans nhưng `2` selected cases có plan missing/invalid theo artifact validator.
- WorkBench: `388` traces/cases; `388/388` plans hợp lệ.
- Ba notebooks về misalignment detection, intervention rate và cost/latency đều execute offline thành công từ included results, không gọi API.
- Replayed locally một deterministic `HomeAssistant.search_guests` observation từ case `55`; environment code hoạt động.

### Suitability audit cho RQ

Trong 182 Agent-SafetyBench evaluation cases:

- `148` có prior tool evidence trước selected action;
- `140` có ít nhất một read-like tool call;
- `116` có pattern heuristic `read-before-likely-write`;
- chỉ `11` có từ hai distinct read-like tool names trở lên;
- manual inspection cho thấy các distinct reads thường lấy **khác loại facts**, không phải hai nguồn độc lập xác minh cùng claim.

Không tìm thấy `failure_domain`, `dependency_group`, correlated-fault injector hoặc redundant-source ground truth trong benchmark data. Provenance graph của paper mô tả justification dependency giữa context và action, không phải backend failure topology.

Static traces cũng cố định agent action. Nếu chỉ sửa observation trong trace, ta không thể đo agent task completion/recovery sau intervention; chỉ có thể đo guardrail allow/block. Muốn dùng cho exact RQ phải chạy lại agent hoặc tạo benchmark-derived deterministic wrapper.

### Verdict

`PASS TECHNICAL ARTIFACT; PARTIAL RQ FIT`.

Artifact phù hợp làm nguồn external task semantics, action boundaries và alignment labels. Nó không phải direct benchmark cho correlated tool failures hoặc provenance-independent corroboration.

## Kết luận nghiên cứu

`FACT:` Hiện chưa có external executable benchmark được xác minh là direct fit cho exact RQ.

`INFERENCE:` Phương án khả thi nhất trong 12 tuần là giữ `trajectory-judge`-derived controlled study làm primary evidence và dùng một subset Agent-SafetyBench/WorkBench làm **benchmark-derived secondary pilot**, với tuyên bố rõ rằng redundant sources và failure domains là adaptation của project.

`RISK:` Nếu adaptation tạo source topology quá thủ công, external-validity gain sẽ nhỏ và reviewer vẫn có thể xem toàn bộ effect là by construction.

## Bước tiếp theo duy nhất

Trước khi viết code, manual-audit và freeze một subset `12` read-before-write cases từ Agent-SafetyBench/WorkBench, trải trên ít nhất `6` domains. Với mỗi case phải ghi: decisive claim, irreversible action, canonical truth, primary evidence, same-domain replica khả dĩ, independent corroborator khả dĩ và programmatic oracle. Nếu không tìm đủ 12 cases mà không bóp méo task semantics, bỏ secondary adaptation.

## Related

- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]
- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]]
- [[references/envtrustbench]]

