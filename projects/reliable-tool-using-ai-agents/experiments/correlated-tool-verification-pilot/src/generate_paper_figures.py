#!/usr/bin/env python3
"""Render frozen decision-level evidence; no episodes, calls or new bootstrap."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT.parent.parent / "paper"
INPUTS = (
    "results_main_study/raw.jsonl",
    "results_main_study/inference.json",
    "results_robustness_gate/raw.jsonl",
    "results_robustness_gate/inference.json",
    "results_robustness_gate/decision.json",
)
REGIMES = ("clean", "independent", "targeted_common_mode")
POLICIES = ("random_k", "provenance_k")
COLORS = {"random_k": "#355c9a", "provenance_k": "#16806a", "always_escalate": "#707780"}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verify_inputs(root: Path, inventory: dict) -> list[dict]:
    expected = {item["path"]: item["sha256"] for item in inventory["artifacts"]}
    checked = []
    for relative in INPUTS:
        check(relative in expected, f"missing inventory entry: {relative}")
        actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
        check(actual == expected[relative], f"frozen input hash mismatch: {relative}")
        checked.append({"path": relative, "sha256": actual})
    return checked


def ratio(numerator: int, denominator: int) -> dict:
    check(0 <= numerator <= denominator and denominator > 0, "invalid denominator/count")
    return {"numerator": numerator, "denominator": denominator, "rate": numerator / denominator}


def main_counts(rows: list[dict]) -> list[dict]:
    check(len(rows) == 1350, "main matrix must contain 1350 frozen rows")
    keys = [(r["task_id"], r["seed"], r["regime"], r["policy"]) for r in rows]
    check(len(set(keys)) == len(keys), "duplicate main row")
    result = []
    for regime in REGIMES:
        for policy in POLICIES:
            selected = [r for r in rows if r["regime"] == regime and r["policy"] == policy]
            refunds = [r for r in selected if r["expected_action"] == "refund"]
            check(len(selected) == 150 and len(refunds) == 50, "unexpected main group size")
            check(len({r["task_id"] for r in selected}) == 30, "expected 30 task clusters")
            missed = [r for r in refunds if r["final_action"] != "refund"]
            no_proposal = sum(not r["refund_attempted"] for r in missed)
            gate_rejected = sum(r["refund_attempted"] and r["blocked"] for r in missed)
            check(len(missed) == no_proposal + gate_rejected, "missed-refund decomposition fails")
            result.append({
                "regime": regime, "policy": policy, "status": "OBSERVED_FROZEN_DECISIONS",
                "unsafe_decisions": ratio(sum(r["unsafe_refund"] for r in selected), 150),
                "correct_expected_refund_decisions": ratio(sum(r["final_state_correct"] for r in refunds), 50),
                "missed_no_proposal": no_proposal, "missed_gate_rejection": gate_rejected,
            })
        result.append({
            "regime": regime, "policy": "always_escalate", "status": "POST_HOC_COUNTERFACTUAL_NOT_RUN",
            "unsafe_decisions": ratio(0, 150), "correct_expected_refund_decisions": ratio(0, 50),
            "budget": "not a measured matched-K=2 policy",
        })
    return result


def effect_row(inference: list[dict], selected: list[dict], label: str, study: str, **fields) -> dict:
    found = [r for r in inference if r["metric"] == "unsafe_refund" and all(r.get(k) == v for k, v in fields.items())]
    check(len(found) == 1, f"expected one inference row: {label}")
    row = found[0]
    check(row["treatment"] == "provenance_k" and row["control"] == "random_k", "effect direction mismatch")
    lo, hi = row["ci95"]
    check(all(math.isfinite(x) for x in (lo, hi, row["difference"])), "nonfinite effect")
    check(lo <= row["difference"] <= hi, "CI does not contain estimate")
    rates = {}
    pair_keys = []
    for policy in POLICIES:
        group = [r for r in selected if r["policy"] == policy]
        check(len(group) == 150 and len({r["task_id"] for r in group}) == 30, "unexpected effect sample")
        keys = {(r["task_id"], r["seed"]) for r in group}
        check(len(keys) == len(group), "duplicate effect row")
        pair_keys.append(keys)
        rates[policy] = ratio(sum(r["unsafe_refund"] for r in group), len(group))
    check(pair_keys[0] == pair_keys[1], "effect rows not paired")
    delta = rates["provenance_k"]["rate"] - rates["random_k"]["rate"]
    check(math.isclose(delta, row["difference"], abs_tol=1e-12), "raw/inference point mismatch")
    check(row["task_clusters"] == 30 and row["bootstrap_resamples"] == 10000, "inference design mismatch")
    return {"label": label, "study": study, "rates": rates,
            "difference": row["difference"], "ci95": row["ci95"],
            "difference_pp": row["difference"] * 100, "ci95_pp": [lo * 100, hi * 100],
            "task_clusters": 30, "bootstrap_resamples": 10000}


def build_data(root: Path, inventory: dict) -> dict:
    hashes = verify_inputs(root, inventory)
    def load(relative):
        return json.loads((root / relative).read_text(encoding="utf-8"))
    def jsonl(relative):
        return [json.loads(line) for line in (root / relative).read_text(encoding="utf-8").splitlines() if line.strip()]
    main = jsonl(INPUTS[0])
    robust = jsonl(INPUTS[2])
    check(len(robust) == 3750, "robustness matrix must contain 3750 rows")
    main_inference, robust_inference, decision = load(INPUTS[1]), load(INPUTS[3]), load(INPUTS[4])
    effects = []
    for regime in REGIMES:
        effects.append(effect_row(main_inference, [r for r in main if r["regime"] == regime],
                                  regime, "main", regime=regime))
    specifications = (
        ("accurate_at_leakage_0_25", "accurate", "leakage_0.25", "accurate; leakage .25"),
        ("missing_25_at_leakage_0_10", "missing_25", "leakage_0.10", "missing .25; leakage .10"),
        ("wrong_25_at_leakage_0_10", "wrong_25", "leakage_0.10", "wrong .25; leakage .10"),
    )
    for gate_key, condition, cell, label in specifications:
        # The control occurs once per leakage cell, not once per metadata condition.
        leakage = float(cell.removeprefix("leakage_"))
        selected = [r for r in robust if r["cross_domain_leakage"] == leakage
                    and (r["policy"] == "random_k" or r["metadata_condition"] == condition)]
        row = effect_row(robust_inference, selected, label, "robustness",
                         metadata_condition=condition, cell=cell)
        check(type(decision["conditions"][gate_key]) is bool, "gate status must be boolean")
        row["gate"] = "PASS" if decision["conditions"][gate_key] else "FAIL"
        check(row["gate"] == ("PASS" if row["difference"] < 0 and row["ci95"][1] < 0 else "FAIL"), "stored CI/gate mismatch")
        effects.append(row)
    return {"schema_version": "1.0", "scope": "FROZEN_DECISION_LEVEL_EVIDENCE_NOT_LIVE_AGENT_EFFECT",
            "new_episodes": 0, "new_model_calls": 0, "new_bootstrap": False,
            "input_hashes": hashes, "main_counts": main_counts(main), "effects": effects,
            "robustness_gate": decision["robustness_gate"],
            "notes": ["Bars are descriptive counts; existing task-cluster CIs appear in the forest plot.",
                      "Main and robustness have separate sets of 30 tasks; never pool them.",
                      "Metadata fractions are nominal probabilities, not realized fractions.",
                      "Zero observed unsafe decisions do not imply successful task recovery."]}


class SVG:
    def __init__(self, width: int, height: int, title: str, description: str):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
                      f'<title>{escape(title)}</title><desc>{escape(description)}</desc>',
                      '<style>text{font-family:Arial,"DejaVu Sans",sans-serif;fill:#172332}</style>',
                      f'<rect width="{width}" height="{height}" fill="white"/>']

    def text(self, x, y, value, size=16, anchor="start", weight="normal"):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(value))}</text>')

    def line(self, x1, y1, x2, y2, color="#dce2e8", width=1, dashed=False):
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{dash}/>')

    def rect(self, x, y, width, height, color):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{color}"/>')

    def point(self, x, y, color):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}"/>')

    def finish(self):
        return "\n".join(self.parts + ["</svg>"]) + "\n"


def safety_utility_svg(data: dict) -> str:
    svg = SVG(1200, 620, "Safety và utility trong main study",
              "Hai policies quan sát và always-escalate counterfactual; hai panel có mẫu số khác nhau, không phải giao dịch thật.")
    svg.text(30, 40, "Zero unsafe không đồng nghĩa phục hồi nhiệm vụ", 26, weight="bold")
    svg.text(30, 71, "Main: deterministic actor; 30 tasks × 5 seeds mỗi regime/policy. Không thực thi refund.")
    for index, policy in enumerate((*POLICIES, "always_escalate")):
        x = 30 + index * 365
        svg.rect(x, 94, 16, 16, COLORS[policy])
        label = policy if policy != "always_escalate" else "always-escalate (counterfactual; chưa run)"
        svg.text(x + 24, 108, label, 15)
    panels = ((75, "unsafe_decisions", "A. Quyết định refund sai /150", "Thấp hơn tốt hơn"),
              (665, "correct_expected_refund_decisions", "B. Refund đúng khi oracle yêu cầu refund /50", "Cao hơn tốt hơn"))
    for left, metric, title, direction in panels:
        svg.text(left, 161, title, 18, weight="bold")
        svg.text(left, 186, direction, 15)
        bottom, top, plot_width = 458, 224, 450
        for percent in range(0, 101, 25):
            y = bottom - (bottom - top) * percent / 100
            svg.line(left, y, left + plot_width, y)
            svg.text(left - 12, y + 5, f"{percent}%", 14, anchor="end")
        for group_index, regime in enumerate(REGIMES):
            center = left + 75 + group_index * 150
            for policy_index, policy in enumerate((*POLICIES, "always_escalate")):
                row = next(r for r in data["main_counts"] if r["regime"] == regime and r["policy"] == policy)
                value = row[metric]
                x = center - 53 + policy_index * 38
                height = value["rate"] * (bottom - top)
                svg.rect(x, bottom - height, 28, height, COLORS[policy])
                svg.text(x + 14, bottom - height - 10, f'{value["numerator"]}/{value["denominator"]}', 13, anchor="middle")
            label = "targeted" if regime == "targeted_common_mode" else regime
            svg.text(center, bottom + 30, label, 15, anchor="middle")
    svg.text(30, 535, "Targeted: cả hai policies chỉ đúng 0/50 expected-refund decisions; missed refunds do actor không tạo proposal.", 16)
    svg.text(30, 567, "Always-escalate là counterfactual hậu nghiệm, không measured baseline cùng K=2. Bars không có CI.", 15)
    svg.text(30, 595, "Tỷ lệ dùng hai mẫu số riêng. Không suy production safety, successful recovery hoặc live-agent effectiveness.", 15)
    return svg.finish()


def effects_svg(data: dict) -> str:
    svg = SVG(1200, 660, "Chênh lệch unsafe decisions và metadata sensitivity",
              "Forest plot của CIs đã lưu; main và robustness dùng hai tập 30 tasks khác nhau, không pooled inference.")
    svg.text(30, 40, "Advantage có điều kiện; wrong metadata không qua gate", 25, weight="bold")
    svg.text(30, 72, "Δ = provenance_k − random_k; đơn vị điểm phần trăm (percentage points). Âm: ít unsafe hơn.")
    left, right, lo, hi = 440, 850, -30, 10
    def x(value):
        return left + (value - lo) / (hi - lo) * (right - left)
    for value in range(lo, hi + 1, 10):
        svg.line(x(value), 125, x(value), 490, "#697789" if value == 0 else "#dce2e8", 2 if value == 0 else 1, value == 0)
        svg.text(x(value), 522, str(value), 14, anchor="middle")
    svg.text(30, 119, "MAIN — 30 frozen tasks", 17, weight="bold")
    svg.text(890, 119, "Δ [95% CI], pp", 16, weight="bold")
    ys = (165, 210, 255, 360, 405, 450)
    svg.text(30, 317, "ROBUSTNESS — 30 tasks mới (không pool)", 17, weight="bold")
    svg.line(30, 284, 1160, 284)
    for row, y in zip(data["effects"], ys):
        a, b = row["ci95_pp"]
        color = "#a04b19" if row.get("gate") == "FAIL" else "#16806a"
        svg.text(30, y + 5, row["label"], 16)
        svg.line(x(a), y, x(b), y, color, 3)
        svg.line(x(a), y - 6, x(a), y + 6, color, 2)
        svg.line(x(b), y - 6, x(b), y + 6, color, 2)
        svg.point(x(row["difference_pp"]), y, color)
        gate = f' — {row["gate"]}' if "gate" in row else ""
        svg.text(890, y + 5, f'{row["difference_pp"]:+.1f} [{a:.1f}, {b:.1f}]{gate}', 15)
    svg.text(30, 559, "CI đã lưu: paired task-cluster bootstrap, 10.000 resamples; không bootstrap mới hoặc population CI.", 15)
    svg.text(30, 588, "Wrong .25 là xác suất label noise danh nghĩa. FAIL lấy từ stored gate trên số chưa làm tròn.", 15)
    svg.text(30, 617, "Clean [0,0] chỉ mô tả frozen set, không equivalence proof. Overall robustness: FAIL ROBUSTNESS.", 15)
    return svg.finish()


def write_outputs(out: Path, data: dict) -> None:
    # Reject existing directories before any write, including otherwise empty ones.
    out.mkdir(parents=True, exist_ok=False)
    files = {"main-safety-utility.svg": safety_utility_svg(data),
             "effects-and-metadata.svg": effects_svg(data),
             "figure-data.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n"}
    for name, content in files.items():
        with (out / name).open("x", encoding="utf-8") as handle:
            handle.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="New directory only; refuses overwrite")
    args = parser.parse_args()
    inventory = json.loads((PAPER / "artifact-inventory.json").read_text(encoding="utf-8"))
    data = build_data(ROOT, inventory)
    write_outputs(args.out, data)
    print(f"Rendered 2 SVG figures and verified data into {args.out}; 0 new episodes/model calls.")


if __name__ == "__main__":
    main()
