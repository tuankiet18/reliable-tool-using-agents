---
title: "Chứng minh điều kiện J = r − φ cho chọn corroborator theo failure domain"
category: project
tags: [paper-draft, provenance, verification, research-methods, evidence]
sources:
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/verify_j_theorem.py"
  - "projects/reliable-tool-using-ai-agents/experiments/correlated-tool-verification-pilot/src/analyze_hidden_dependency.py"
  - "journal/2026-10-12-label-quality-test-results.md"
created: 2026-10-12T18:00:00+07:00
updated: 2026-10-12T18:00:00+07:00
summary: >-
  Chứng minh chính xác: chọn theo failure domain ít chọn nhầm tool chung hơn chọn ngẫu nhiên khi và chỉ khi J = r − φ > 0, kèm công thức đóng cho độ lớn và hệ quả cho nhãn thiếu.
provenance:
  extracted: 0.20
  inferred: 0.80
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: 2026-10-12
---

# Chứng minh điều kiện $J = r - \varphi$

**Trạng thái:** chứng minh viết với sự hỗ trợ của AI, chưa có người độc lập kiểm tra. Công thức đóng được kiểm tra bằng số với phép liệt kê đầy đủ: sai số lớn nhất $6.7 \times 10^{-16}$ trên 3.087 điểm (7 topology), và $5.6 \times 10^{-16}$ khi có nhãn thiếu (`src/verify_j_theorem.py`). Điều này thay cho ghi chú "chưa chứng minh" ở ledger C35, **trong phạm vi giả định dưới đây**.

## 1. Mô hình

Primary có $n$ corroborator. Trong đó $s$ tool thật sự chung failure domain với primary ("tool chung") và $n - s$ tool độc lập, với $1 \le s \le n - 1$.

**Giả định:**

- **(A1) Nhãn primary đúng.** Selector biết đúng domain của primary.
- **(A2) Nhãn độc lập, chỉ phụ thuộc lớp.** Mỗi corroborator, độc lập với các tool khác, là **ứng viên** (được gắn nhãn "độc lập") với xác suất
  - $a = 1 - r$ nếu là tool chung ($r$ là recall phát hiện phụ thuộc chung),
  - $b = 1 - \varphi$ nếu là tool độc lập ($\varphi$ là tỷ lệ gán nhầm là chung).
- **(A3) Chọn đều.** Selector chọn đều trong tập ứng viên $C$. Nếu $C = \emptyset$, chọn đều trong cả $n$ tool.

Chọn ngẫu nhiên (random) chọn đều trong cả $n$ tool, nên chọn trúng tool chung với xác suất $s/n$.

Đặt $J = r - \varphi = b - a$.

## 2. Định lý

$$
P(\text{chọn tool chung}) - \frac{s}{n} \;=\; -\,\frac{s(n-s)}{n}\, J\; \mathbb{E}\!\left[\frac{1}{1+K}\right],
$$

trong đó $K = K_S + K_I$, với $K_S \sim \mathrm{Bin}(s-1, a)$ và $K_I \sim \mathrm{Bin}(n-s-1, b)$ độc lập.

Vì $\mathbb{E}[1/(1+K)] > 0$ và $s(n-s)/n > 0$:

> **Chọn theo failure domain chọn nhầm tool chung ít hơn chọn ngẫu nhiên khi và chỉ khi $J > 0$, bằng khi $J = 0$, và nhiều hơn khi $J < 0$.**

## 3. Chứng minh

**Bước 1 — Quy về so sánh hai tool.** Theo (A2) và (A3), mọi tool chung có cùng xác suất được chọn, gọi là $p_S$, và mọi tool độc lập có cùng xác suất $p_I$. Selector luôn chọn đúng một tool, nên

$$
s\,p_S + (n-s)\,p_I = 1. \tag{1}
$$

Từ (1), $p_S = \tfrac{1}{n} - \tfrac{n-s}{n}(p_I - p_S)$. Nhân với $s$:

$$
P(\text{chọn tool chung}) - \frac{s}{n} \;=\; s\,p_S - \frac{s}{n} \;=\; -\,\frac{s(n-s)}{n}\,(p_I - p_S). \tag{2}
$$

Vậy chỉ cần tính $p_I - p_S$.

**Bước 2 — Ghép một tool chung $x$ với một tool độc lập $y$.** Gọi $O$ là $n - 2$ tool còn lại ($s-1$ tool chung, $n-s-1$ tool độc lập), và $K$ là số ứng viên trong $O$. **Phân phối của $K$ giống nhau** dù ta đang tính cho $x$ hay cho $y$. Đây là điểm mấu chốt của chứng minh.

Xác suất $x$ được chọn, xét theo $y$ có là ứng viên hay không:

$$
p_S = a\,\mathbb{E}\!\left[\frac{b}{2+K} + \frac{1-b}{1+K}\right] + (1-a)(1-b)\,P(K=0)\,\frac{1}{n}.
$$

Số hạng đầu là khi $x$ là ứng viên: $x$ được chọn đều trong $C$, mà $C$ có $2+K$ phần tử nếu $y$ cũng là ứng viên, hoặc $1+K$ nếu không. Số hạng cuối là khi cả $x$ và $y$ đều không là ứng viên và $O$ cũng không có ứng viên, nên selector fallback và chọn $x$ với xác suất $1/n$. Mọi trường hợp khác cho $p = 0$ với $x$.

Tương tự, đổi vai $a \leftrightarrow b$:

$$
p_I = b\,\mathbb{E}\!\left[\frac{a}{2+K} + \frac{1-a}{1+K}\right] + (1-b)(1-a)\,P(K=0)\,\frac{1}{n}.
$$

**Bước 3 — Trừ hai biểu thức.** Số hạng fallback giống hệt nhau nên triệt tiêu. Số hạng $ab/(2+K)$ cũng triệt tiêu. Còn lại:

$$
p_I - p_S = \mathbb{E}\!\left[\frac{b(1-a) - a(1-b)}{1+K}\right] = (b - a)\,\mathbb{E}\!\left[\frac{1}{1+K}\right] = J\,\mathbb{E}\!\left[\frac{1}{1+K}\right].
$$

Thay vào (2) ta được định lý. $\blacksquare$

## 4. Trực giác

Selector chỉ chọn trong nhóm được gắn nhãn "độc lập". Một tool chung lọt vào nhóm này với xác suất $1 - r$, một tool độc lập với xác suất $1 - \varphi$. Nếu tool độc lập lọt vào **dễ hơn** ($1 - \varphi > 1 - r$, tức $J > 0$) thì nhóm được chọn "sạch" hơn ngẫu nhiên. Nếu ngược lại thì nhóm đó "bẩn" hơn ngẫu nhiên. Chứng minh cho thấy cơ chế fallback không làm lệch kết luận, vì tool chung và tool độc lập bị fallback như nhau.

**Ví dụ kiểm tra:** $n = 3$, $s = 1$, $r = 0$, $\varphi = 0.5$. Ta có $a = 1$, $b = 0.5$, $J = -0.5$, và $K \sim \mathrm{Bin}(1, 0.5)$ nên $\mathbb{E}[1/(1+K)] = 0.75$. Công thức cho $P = \tfrac13 + \tfrac{2}{3} \times 0.5 \times 0.75 \approx 0.583$, so với $1/3$ khi chọn ngẫu nhiên. Với leakage $\ell = 0.1$, unsafe là $0.583 + 0.1 \times 0.417 = 0.625$, đúng bằng con số trong bảng §5.8 của paper. (Đính chính: trong một lần giải thích trước, con số 0.625 bị gọi nhầm là xác suất chọn nhầm; xác suất chọn nhầm là 0.583.)

## 5. Hệ quả

**H1 — Quyết định unsafe.** Dưới targeted fault, tool chung luôn đồng ý với primary sai, còn tool độc lập sai với xác suất leakage $\ell$. Khi đó unsafe $= P + \ell(1-P)$, nên

$$
\text{unsafe}_{\text{prov}} - \text{unsafe}_{\text{rand}} = (1 - \ell)\Big(P(\text{chọn tool chung}) - \tfrac{s}{n}\Big).
$$

Cùng dấu với $-J$ khi $\ell < 1$.

**H2 — Nhãn thiếu không bao giờ đảo dấu.** Nếu mỗi corroborator có nhãn với xác suất $k$ (nhãn thiếu thì không là ứng viên), thì $a = k(1-r)$ và $b = k(1-\varphi)$, nên $b - a = kJ$. Nếu thêm nhãn của primary thiếu với xác suất $1 - k_P$ (khi đó fallback ngẫu nhiên, không chênh lệch), toàn bộ chênh lệch được nhân với $k_P$:

$$
P - \frac{s}{n} = -\,k_P\,\frac{s(n-s)}{n}\, k J\, \mathbb{E}\!\left[\frac{1}{1+K}\right], \quad K \sim \mathrm{Bin}(s-1, k(1-r)) + \mathrm{Bin}(n-s-1, k(1-\varphi)).
$$

Vậy **nhãn thiếu chỉ làm nhỏ độ lớn, không đổi hướng**. Điều này giải thích kết quả survey: L1 thiếu nhãn ở 70% cặp nhưng vẫn có lợi.

**H3 — Trường hợp biên.** Nếu $s = 0$ hoặc $s = n$, hai policy như nhau. Nếu $a = b = 0$ ($r = \varphi = 1$), $C$ luôn rỗng nên luôn fallback và hai policy như nhau, khớp với $J = 0$.

## 6. Giới hạn — định lý **không** nói gì

- **Nhãn tương quan giữa các tool** (vi phạm A2), ví dụ cả nhóm tool cùng bị gán nhầm vì cùng một tài liệu sai, không được bao phủ.
- **Nhãn primary có thể sai** (vi phạm A1). Mô hình nhãn domain của robustness gate thuộc loại này: tool được so với domain *quan sát* của primary, có thể sai. **Đính chính:** trước đây chúng tôi viết rằng mô hình đó "luôn có $J > 0$" để giải thích vì sao provenance không bao giờ tệ hơn random. Lời giải thích đó **không** được định lý này chứng minh. Ví dụ, khi $m = 0$, $w = 0.9$ và nhãn primary đúng, ta có $a = 0.9 > b = 0.55$, tức nhánh đó tệ hơn random; kết quả tổng thể vẫn tốt hơn ($P = 0.274 < 1/3$) nhờ nhánh nhãn primary sai. Kết quả "không bao giờ tệ hơn random" của mô hình đó vẫn đúng **trên lưới đã liệt kê**, nhưng chưa có chứng minh.
- **Chọn không đều, hoặc chọn nhiều hơn một corroborator** ($K > 2$) chưa được xét.
- Định lý nói về **mô hình**, không nói gì về agent hay tool thật.

## Liên quan

- [[projects/reliable-tool-using-ai-agents/paper/paper-draft]]
- [[projects/reliable-tool-using-ai-agents/paper/claim-evidence-ledger]]
- [[journal/2026-10-12-label-quality-test-results]]
- [[journal/2026-10-06-prior-art-refresh-vp-control-and-efd]]
