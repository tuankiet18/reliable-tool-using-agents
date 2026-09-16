---
title: "Which Tool Response Should I Trust? Tool-Expertise-Aware Chest X-ray Agent with Multimodal Agentic Learning"
category: reference
tags: [ai-agents, tool-use, verification, uncertainty, prior-art]
sources:
  - "https://arxiv.org/abs/2602.21517"
created: 2026-09-15T15:34:48+07:00
updated: 2026-09-15T15:34:48+07:00
summary: >-
  TEA-CXA học độ đáng tin theo loại câu hỏi của hai medical tools và chọn phản hồi nên tin khi chúng xung đột; đây là prior art trực tiếp chống claim rộng về dynamic tool-response selection.
---

# Which Tool Response Should I Trust? Tool-Expertise-Aware Chest X-ray Agent with Multimodal Agentic Learning

## Problem

Các medical tools có expertise khác nhau và có thể trả lời mâu thuẫn. Paper hỏi agent nên tin tool nào theo từng loại truy vấn, thay vì coi mọi tool đáng tin như nhau.

## Method và evidence

TEA-CXA dùng agentic reinforcement learning để học practical trustworthiness của `MedGemma-4B` và `Lingshu-7B`. Khi hai tool bất đồng, agent có thể chấp nhận hoặc bác phản hồi và nhận reward. Trên `CheXbench` gồm 618 câu hỏi, paper báo overall accuracy `73.8%`; riêng conflict tool-response selection đạt `63.8%`, cao hơn `Agent-ensemble` (`54.0%`) và `MedRAX*` (`57.5%`).

## Giới hạn liên quan RQ hiện tại

- Đây là **dynamic selection** dựa trên query type và learned tool expertise: broad claim “chưa ai học tool nào nên tin” bị bác bỏ.
- Paper không mô hình hóa `failure_domain_id`, shared backend, common-mode silent corruption hay metadata sai.
- Không kiểm tra safety gate ngay trước irreversible action và không so sánh matched `K=2` independent-source với random-source verification.
- Training dùng 8 NVIDIA H800; paper ghi code “will be released”, chưa có public artifact được xác minh tại thời điểm kiểm tra.

## Phân loại

`PARTIAL` novelty threat rất mạnh. Nó phủ **tool trust selection**, nhưng chưa phủ **failure-domain-independent corroboration under correlated failures**.

## Related

- [[synthesis/Prior-Art Threat: Provenance Metadata and Source Selection]]
- [[synthesis/Candidate RQ: Provenance-Aware Verification under Correlated Tool Failures]]

