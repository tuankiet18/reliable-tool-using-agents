---
title: Tag Taxonomy
category: _meta
tags: [meta/taxonomy]
sources: [conversation]
created: 2026-10-06
updated: 2026-10-06
summary: Bộ tag chuẩn (controlled vocabulary) cho vault nghiên cứu Reliable Tool-Using AI Agents, kèm alias và quy tắc gắn tag.
---

# Tag Taxonomy

Quy tắc: tối đa 5 tag mỗi trang, chữ thường, nối bằng dấu gạch ngang, ưu tiên tag rộng hơn tag hẹp. Tag `visibility/*` là system tag, không tính vào giới hạn 5.

## Domain tags (chủ đề)

| Tag | Dùng cho |
|---|---|
| `ai-agents` | Agent dùng LLM nói chung |
| `tool-use` | Gọi tool/function, MCP, tool mediation |
| `tool-failure` | Lỗi tool, silent/common-mode failure, fault injection |
| `verification` | Xác minh, cross-tool verification, corroboration |
| `failure-detection` | Phát hiện/dự báo lỗi sớm, diagnosis |
| `runtime-monitoring` | Giám sát runtime, observability, runtime policy |
| `reliability` | Độ tin cậy, robustness, recovery |
| `provenance` | Provenance, failure domain, dependency metadata |
| `authorization` | Least privilege, capability control, permission |
| `security` | An toàn và bảo mật agent |
| `coding-agents` | Agent lập trình, software engineering |

## Type tags (loại trang)

| Tag | Dùng cho |
|---|---|
| `paper` | Trang tham khảo một paper |
| `research` | Tổng hợp nghiên cứu theo chủ đề |
| `research-log` | Journal/nhật ký nghiên cứu |
| `research-question` | Candidate RQ |
| `research-gap` | Gap analysis |
| `research-protocol` | Protocol, amendment, gate |
| `research-methods` | Phương pháp nghiên cứu |
| `prior-art` | Rà soát prior art, novelty threat |
| `experiment` | Thí nghiệm, pilot, kết quả |
| `benchmark` | Benchmark, dataset |
| `paper-draft` | Bản thảo paper và tài liệu đi kèm |
| `field-map` | Bản đồ lĩnh vực |
| `glossary` | Thuật ngữ |

## Project / epistemic tags

| Tag | Dùng cho |
|---|---|
| `reproducibility` | Artifact, package, tái lập |
| `external-validity` | Giá trị ngoại suy, secondary/live-agent gate |
| `evidence` | Claim–evidence, audit bằng chứng |
| `preliminary` | Kết quả/ý tưởng sơ bộ |
| `novelty` | Đánh giá tính mới |
| `supervisor-review` | Tài liệu cho giảng viên/reviewer |

## Aliases

| Alias | Canonical |
|---|---|
| `agent-verification` | `verification` |
| `monitoring`, `observability` | `runtime-monitoring` |
| `safety` | `security` |
| `evaluation` | `benchmark` |
| `least-privilege` | `authorization` |
| `failure-correlation` | `tool-failure` |
| `recovery` | `reliability` |
| `runtime-policy` | `runtime-monitoring` |

## Migration notes

- Các alias ở trên đang được dùng trong vault; chuẩn hóa dần khi sửa trang, không bulk rewrite.
- Tag chỉ xuất hiện 1 lần (ví dụ `automata`, `forecasting`, `ensembles`) là tag hẹp: giữ nếu cần, nhưng nên thay bằng tag chuẩn khi trang được cập nhật.
