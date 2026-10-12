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
updated: 2026-10-13T12:00:00+07:00
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

## Inter-rater agreement — cập nhật 2026-10-13

Coder B (con người, thành viên nhóm) nộp nhãn cho 10 server được giao: đủ 10 dòng, không trống cột bắt buộc, commit và URL khớp, mỗi nhãn có bằng chứng file:dòng. `src/analyze_coder_agreement.py`, output `results_coder_agreement_20261013/`.

| Trường | Khớp nguyên chữ | Sau chuẩn hóa tên |
|---|---|---|
| Upstream provider | 0.40 (κ = 0.38) | **0.80 (κ = 0.78)** |
| L1 declared provider | 0.80 (κ = 0.68) | **1.00 (κ = 1.00)** |
| L2 declared provider | 0.40 (κ = 0.38) | **1.00 (κ = 1.00)** |
| L1 có/không có nhãn | 1.00 | 1.00 |

Bảng chuẩn hóa chỉ gộp các cách viết của **cùng một** tổ chức (ví dụ "Sina" và "Sina Finance", "Microsoft" là bên vận hành "Bing"). Nó được viết **sau** khi thấy cả hai file, vì protocol survey 1 không định trước, nên kết quả khớp nguyên chữ được báo cáo song song.

**Hai bất đồng thật, đều do codebook chưa rõ:**
1. `adem1409/Currency-Exchange-MCP-Server`: coder B ghi bên vận hành host (jsDelivr; Cloudflare), **đúng theo chữ của hướng dẫn**; coder A ghi chủ bộ dữ liệu (fawazahmed0 exchange-api), theo một làm rõ được đưa ra trong lúc gán nhãn nhưng không có trong hướng dẫn gửi coder B.
2. `Pascalrjt/SearXNG-Websearch-MCP`: coder B ghi `ambiguous`; coder A ghi `SearXNG (self-hosted)` kèm cờ AMBIGUOUS. Cả hai đều thấy là mơ hồ.

**Tác động lên kết quả:** không đổi nhãn cặp nào ở mức chính. Không server tỷ giá nào khác dùng jsDelivr hay fawazahmed0, nên cặp của `adem1409` không đổi. Cặp SearXNG đã được xét ở phân tích độ nhạy (c) (ρ 0.15).

Coder B còn phát hiện điều coder A bỏ sót ở `niuheilong/stock-mcp-server`: Dockerfile chạy `server.py` (trả giá 0.0) thay vì `mcp_server.py`, và README trỏ tới `main.py` không tồn tại. Đây là bằng chứng rằng việc kiểm tra của con người có giá trị thật.

## POST-HOC — Độ nhạy theo mức nguồn dữ liệu gốc

**Không có trong protocol; làm sau khi thấy `r = 1`.** Script `src/analyze_tool_survey_origin.py`, output `results_tool_survey_origin_posthoc_20261009/`. Chỉ thêm các liên kết bên vận hành → nguồn gốc có **bằng chứng ngay trong các repo đã khảo sát**: Nominatim và Photon → OpenStreetMap; Frankfurter → ECB; cbr-xml-daily.ru → Bank of Russia; Algolia HN Search → Hacker News; SearXNG tự host → tập engine mặc định {Google, DuckDuckGo, Brave Search, Startpage, Wikipedia, Wiby} (lấy từ `settings.yml` của slinusc; với Pascalrjt là **suy luận** vì repo dùng mặc định của SearXNG). Phụ thuộc chỉ được ghi ngoài repo (ví dụ một engine dùng lại index của engine khác) **không** được thêm, nên đây vẫn là cận dưới.

**FACT — kết quả gộp:**

| Biến thể | Mức | ρ | m | r | φ | P(chọn nhầm) provenance vs random |
|---|---|---:|---:|---|---|---|
| Mức bên vận hành (chính) | L1 | 0.16 | 0.70 | 1.00 (8/8) | 0.00 (0/24) | 0.176 vs 0.340 |
| Mức bên vận hành (chính) | L2 | 0.16 | 0.05 | 1.00 (17/17) | 0.00 (0/83) | 0.008 vs 0.340 |
| Nguồn gốc, đọc tên theo chữ | L1 | 0.27 | 0.70 | 0.57 (8/14) | 0.00 (0/18) | 0.473 vs 0.533 |
| Nguồn gốc, đọc tên theo chữ | L2 | 0.27 | 0.05 | 0.61 (17/28) | 0.00 (0/72) | 0.406 vs 0.533 |
| Nguồn gốc, biết ánh xạ | L2 | 0.27 | 0.05 | 1.00 (28/28) | 0.00 (0/72) | 0.292 vs 0.533 |

Theo nhóm (đọc tên theo chữ, L2): web_search `ρ = 1.00` (cả 15 cặp chung ít nhất một engine), `r = 7/15`; geocoding `ρ = 0.40`, `r = 3/6`.

**INFERENCE:**
1. **`r = 1` không bền.** Khi xét nguồn gốc dữ liệu, gần **40%** cặp thật sự chung không được tên provider tiết lộ (`r ≈ 0.6`). `J` vẫn dương vì `φ = 0`, nên theo quy tắc `J > 0` metadata vẫn không làm hại, nhưng lợi ích giảm mạnh: 0.406 so với 0.533, thay vì 0.008 so với 0.340.
2. **Giới hạn thứ hai là thiếu nguồn độc lập (availability), không phải metadata.** Ngay cả khi selector biết đầy đủ ánh xạ, xác suất chọn nhầm vẫn là 0.292, vì trong web_search **không có cặp server nào độc lập về nguồn gốc**: mọi server đều dùng chung ít nhất một trong Google, DuckDuckGo hoặc Brave. Không metadata nào giúp được khi không tồn tại nguồn độc lập. Điều này khớp với điều kiện "có independent corroborator khả dụng" mà paper đã nêu ở §6.2, và với hiện tượng sụp ở `K=3` của RIVA.
3. **Cảnh báo về cách đo:** quy tắc "giao tập khác rỗng thì là chung" coi chung một engine trong số nhiều engine (aggregator) là chung hoàn toàn, nên phóng đại mức phụ thuộc ở web_search. Kết quả này nên được trình bày như cận trên ở chiều đó và cận dưới ở chiều phụ thuộc ngoài repo.

## Tiếp theo

- Chạy lại `analyze_tool_survey.py` sau khi coder B nộp để có agreement/kappa.
- Quyết định có làm phân tích độ nhạy mức nguồn gốc dữ liệu (post-hoc) không.
- Đưa kết quả vào paper: thay vì claim "provenance tốt hơn random" (đã có trong VP-Control), claim mới là về **chất lượng và mức hiện diện của metadata thực tế** và hệ quả cho selector.

## Liên quan

- [[synthesis/Protocol: Real-Tool Failure-Domain Metadata Survey]]
- [[journal/2026-10-06-prior-art-refresh-vp-control-and-efd]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
