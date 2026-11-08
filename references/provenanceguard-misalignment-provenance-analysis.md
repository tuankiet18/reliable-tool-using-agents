---
title: "Safeguarding LLM Agents from Misalignment through Provenance Analysis"
category: reference
tags: [ai-agents, runtime-monitoring, provenance, safety, prior-art]
sources:
  - "https://arxiv.org/abs/2607.01236"
  - "https://doi.org/10.1145/3832783.3837535"
  - "https://github.com/cmu-soda/ProvenanceGuard"
created: 2026-09-15T15:34:48+07:00
updated: 2026-09-15T16:27:33+07:00
summary: >-
  ASE 2026 runtime guardrail kiểm tra provenance của proposed tool call trước execution; provenance ở đây là justification trace, không phải độ độc lập của data source.
---

# Safeguarding LLM Agents from Misalignment through Provenance Analysis

> [!warning] Không nhầm paper này với [[references/provenanceguard-source-aware-factuality]]. Hai work khác nhau cùng đặt tên system là `ProvenanceGuard`.

## Problem và setting

Agent có thể đề xuất tool call không phù hợp user intent, dùng argument không có căn cứ, hoặc diễn giải tùy tiện khi query thiếu thông tin. Hậu quả đáng lo nhất là environment-changing action khó đảo ngược.

## Method

Runtime monitor chặn proposed tool call trước execution và kiểm tra provenance ở ba mức: tool selection, parameter và interpretation. Evidence đầu vào gồm user query, tool documentation, execution history và agent plan. Action chỉ được allow khi có justification traceable về context.

## Main results

Trên `Agent-SafetyBench` và `WorkBench`, paper báo error trên misaligned traces giảm mạnh so với direct LLM-as-a-judge, đồng thời giảm intervention burden trên task-successful traces. Paper được ghi nhận tại ASE 2026; replication package công khai chứa source, traces/labels và analysis notebooks, dùng Apache-2.0 cho phần đóng góp của authors và giữ upstream MIT terms cho benchmark materials.

## Assumptions và limitations

- Tool developer cung cấp metadata cho biết tool nào thay đổi environment.
- Agent plan trong benchmark phải được GPT-5 reconstruct; lỗi reconstruction có thể ảnh hưởng verdict.
- Guard kiểm tra action tương đối với chính plan của agent. Nếu plan đã sai user intent, action cục bộ vẫn có thể được coi là justified.
- Không đánh giá tool output có bị silent corruption hay hai tools có chung failure domain.

## Research implication

Broad claim “provenance-aware action-boundary guardrail là mới” bị **REJECTED**. Điểm khác biệt còn có thể bảo vệ chỉ là **loại provenance**: failure-domain/source independence, không phải justification provenance.

## Local artifact gate

Replication artifact commit `3ad7141db44096e1440718618bdb24fa46c003ff` pass setup trên temporary Python 3.11 environment. Benchmark loaders đọc được 182 Agent-SafetyBench evaluation traces và 388 WorkBench traces; ba included analysis notebooks execute offline thành công. Một Agent-SafetyBench environment cũng replay tool observation locally được.

Tuy nhiên data không có failure-domain metadata, correlated-fault injector hoặc independent corroborators. Traces cố định proposed actions nên không trực tiếp đo task completion sau observation corruption. Verdict: `PASS TECHNICAL ARTIFACT; PARTIAL RQ FIT`. Xem [[journal/2026-09-15-external-validity-artifact-gate]].

## Related

- [[synthesis/Prior-Art Threat - Provenance Metadata and Source Selection]]
- [[synthesis/Preliminary Gap - Provenance-Aware Verification under Correlated Tool Failures]]
