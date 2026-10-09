---
title: "2026-10-09 — Kết quả survey metadata failure-domain trên 42 MCP server"
category: journal
tags: [research-log, provenance, external-validity, tool-use, evidence]
sources:
  - "synthesis/Protocol: Real-Tool Failure-Domain Metadata Survey.md"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/data/tool_survey/coding.csv"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/results_tool_survey_20261009/summary.json"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_tool_survey.py"
created: 2026-10-09T18:00:00+07:00
updated: 2026-10-09T18:00:00+07:00
summary: >-
  16% cặp MCP server cùng loại dùng chung upstream; metadata agent thấy (L1) thiếu nhãn ở 70% cặp nhưng khi có thì đúng (8/8, 0/24). Vấn đề thực tế là thiếu nhãn hơn là sai nhãn.
provenance:
  extracted: 0.70
  inferred: 0.30
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-10-09
---

# Kết quả survey metadata failure-domain — 2026-10-09

**Phạm vi:** descriptive survey theo [[synthesis/Protocol: Real-Tool Failure-Domain Metadata Survey]]. 42 MCP server mã nguồn mở, 7 nhóm thông tin, 105 cặp cùng nhóm. **Coder A là AI-assisted**; nhãn của coder B (10 server) chưa nộp nên chưa có inter-rater agreement. Không gọi API, không chạy server, không đo hành vi agent.

## FACT — kết quả chính (L1 = metadata agent thấy lúc chạy)

| Nhóm | Cặp | Chung upstream | ρ | Thiếu nhãn L1 (m) |
|---|---:|---:|---:|---:|
| web_search | 15 | 7 | 0.47 | 0.33 |
| news | 15 | 3 | 0.20 | 0.60 |
| geocoding | 15 | 3 | 0.20 | 0.93 |
| crypto_prices | 15 | 2 | 0.13 | 0.80 |
| stock_quotes | 15 | 1 | 0.07 | 0.33 |
| weather | 15 | 1 | 0.07 | 0.93 |
| currency_exchange | 15 | 0 | 0.00 | 0.93 |
| **Gộp** | **105** | **17** | **0.16** | **0.70** |

- ρ gộp `17/105 = 0.16`, bootstrap theo server trong từng nhóm 95% `[0.075, 0.281]`.
- Trong các cặp có nhãn L1: `r = 8/8 = 1.00`, `φ = 0/24 = 0.00`, `J = 1.00`. Với L2 (thêm README): `m = 0.05`, `r = 17/17`, `φ = 0/83`.
- Độ nhạy: bỏ server có provider đổi được (b) cho ρ 0.16, m 0.68; coi cặp SearXNG tự host là không chung (c) cho ρ 0.15, `φ = 0.04`.

## Đối chiếu kỳ vọng ghi trước

- **E1 (ít nhất hai nhóm có > 20% cặp chung): KHÔNG ĐẠT theo đúng chữ.** Chỉ web_search vượt (0.47); news và geocoding đúng bằng 0.20, không lớn hơn.
- **E2 (L1 thiếu nhãn ở hơn nửa số cặp): ĐẠT**, `m = 0.70`.
- **E3 (J > 0 trong các cặp có nhãn): ĐẠT**, nhưng mẫu số nhỏ (8 cặp chung có nhãn ở L1).

## INFERENCE — ý nghĩa

1. **Rủi ro thực tế ở mẫu này là thiếu nhãn, không phải sai nhãn.** Khi tên provider xuất hiện trong metadata thì nó đúng; nhưng ở L1 phần lớn server không nêu provider. Theo quy tắc `J > 0` của [[journal/2026-10-06-prior-art-refresh-vp-control-and-efd]], metadata hiện có không làm hại provenance selection; nó chỉ làm selector phải fallback ngẫu nhiên thường xuyên.
2. **Phép chiếu lên mô hình selector** (không phải đo hành vi agent; 20 primary có ít nhất một peer chung): xác suất chọn nhầm nguồn chung là `0.340` nếu chọn ngẫu nhiên, `0.176` với metadata L1 như hiện có (`k = 0.55` server có nhãn), và `0.008` nếu metadata mức README được đưa vào tool description (`k = 0.98`).
3. **Hàm ý Software Engineering (cần thận trọng):** chỉ việc đưa tên provider upstream vào description của tool đã có thể đưa provenance selection gần mức metadata hoàn hảo trong mô hình này. Đây là đề xuất thực hành cụ thể, rẻ, có thể kiểm chứng.

## Giới hạn quan trọng

- **`r = 1` một phần do cách định nghĩa ground truth ở mức bên vận hành API.** Ở mức nguồn dữ liệu gốc, có các phụ thuộc mà nhãn không bắt được: Photon và Nominatim cùng dữ liệu OpenStreetMap; Frankfurter phân phối dữ liệu ECB; một server ghi "AKShare" (thư viện) thay vì Eastmoney (nguồn thật). Một phân tích độ nhạy theo mức nguồn gốc dữ liệu sẽ cho `r` thấp hơn; phân tích đó **chưa ghi trong protocol** nên nếu làm phải dán nhãn post-hoc.
- 105 cặp không độc lập (mỗi server nằm trong 5 cặp); mẫu số của `r` nhỏ.
- Mẫu thiên về repo phổ biến trên GitHub; MCP không đại diện cho mọi hệ sinh thái tool.
- Chưa có kiểm tra bởi con người (coder B).

## Tiếp theo

- Chạy lại `analyze_tool_survey.py` sau khi coder B nộp để có agreement/kappa.
- Quyết định có làm phân tích độ nhạy mức nguồn gốc dữ liệu (post-hoc) không.
- Đưa kết quả vào paper: thay vì claim "provenance tốt hơn random" (đã có trong VP-Control), claim mới là về **chất lượng và mức hiện diện của metadata thực tế** và hệ quả cho selector.

## Liên quan

- [[synthesis/Protocol: Real-Tool Failure-Domain Metadata Survey]]
- [[journal/2026-10-06-prior-art-refresh-vp-control-and-efd]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
