#!/usr/bin/env python3
"""Render the RQ2 and RQ3 paper figures from stored results; no new statistics.

Figure A  problem illustration (common-mode failure through a shared provider).
Figure B  RQ2: (left) closed-form P(select shared) - s/n over (r, phi) for the main topology
          (n = 3 corroborators, s = 1 shared); (right) the preregistered label-quality test:
          observed difference with stored 95% CI and the pre-registered prediction.
Figure C  RQ3: per-category operator-level shared-pair rate rho and L1 missing-label rate m
          for survey 1 and survey 2, with the stored pooled bootstrap interval.

Inputs are pinned by SHA-256; the only computation is the closed form of
`verify_j_theorem.closed_form` for the theoretical heatmap.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from html import escape
from pathlib import Path

from verify_j_theorem import closed_form

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT.parent.parent / "paper"
INPUTS = {
    "results_label_quality_20261012/analysis.json": "3496ed947d692b58d2f37a61256d0b5843c562b3047506787e2ae7bb6ad48587",
    "results_label_quality_20261012/run_manifest.json": "2320b732faa353531b93ceeab137320d812bffd735d5c87d6f1aabc3e8b87f16",
    "results_tool_survey_20261009/summary.json": "966f43b8aa7ec4c8dbe18cb6041303ceedb43bad72a28ad5a39c4c8e91f74e6c",
    "results_tool_survey2_20261014/summary.json": "4fea2137faba40bdd85ddeabfa8bae61ecf03a269f53d19c023a148e5c64f2b7",
}
CONDITIONS = ("J_minus", "J_zero", "survey_calibrated", "J_plus")  # ordered by J
LABELS = {"J_minus": "J = −0.5", "J_zero": "J = 0", "survey_calibrated": "survey (k = 0.55)", "J_plus": "J = +0.8"}
CATEGORIES = ("weather", "currency_exchange", "stock_quotes", "crypto_prices", "geocoding", "web_search",
              "news", "translation", "movies", "books", "air_quality")
S1, S2, GOOD, BAD, INK, GRID = "#355c9a", "#16806a", "#1d6b2f", "#a33333", "#222", "#d8dde3"
FONT = 'font-family="Noto Sans, DejaVu Sans, sans-serif"'


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_inputs(root: Path) -> dict:
    data = {}
    for rel, expected in INPUTS.items():
        raw = (root / rel).read_bytes()
        check(hashlib.sha256(raw).hexdigest() == expected, f"input hash mismatch: {rel}")
        data[rel] = json.loads(raw)
    return data


def text(x, y, s, size=11, anchor="start", weight="normal", fill=INK, extra="") -> str:
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" fill="{fill}" {extra}>{escape(s)}</text>')


def svg(width, height, body) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" {FONT}><rect width="100%" height="100%" fill="#fff"/>'
            + "".join(body) + "</svg>\n")


def figure_a() -> str:
    b = []
    box = lambda x, y, w, h, fill, stroke: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}"/>'
    line = lambda x1, y1, x2, y2, c, w=1.2: f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"/>'
    b += [box(10, 55, 90, 40, "#e6edf5", "#1f4e79"), text(55, 79, "Agent", anchor="middle")]
    for y, name in ((10, "weather_A (primary)"), (58, "weather_pro"), (106, "forecast_x")):
        b += [box(160, y, 130, 34, "#fff", "#555"), text(225, y + 21, name, anchor="middle")]
        b.append(line(100, 75, 160, y + 17, "#555"))
    b += [box(370, 30, 130, 40, "#fbe9e9", BAD), text(435, 48, "Provider P", anchor="middle"),
          text(435, 62, "returns wrong data", 10, "middle", fill=BAD),
          box(370, 100, 130, 40, "#e8f4ea", GOOD), text(435, 124, "Provider Q", anchor="middle"),
          line(290, 27, 370, 45, BAD, 1.8), line(290, 75, 370, 55, BAD, 1.8), line(290, 123, 370, 120, GOOD, 1.8),
          text(512, 46, "same failure domain", 10, fill=BAD), text(512, 59, "→ wrong agreement", 10, fill=BAD),
          text(512, 116, "independent", 10, fill=GOOD), text(512, 129, "→ disagreement detected", 10, fill=GOOD)]
    return svg(650, 150, b)


def heat_color(v: float, vmax: float) -> str:
    t = max(-1.0, min(1.0, v / vmax))
    end = (0x1d, 0x6b, 0x2f) if t < 0 else (0xa3, 0x33, 0x33)
    w = abs(t) ** 0.8
    rgb = [round(255 + (c - 255) * w) for c in end]
    return "#%02x%02x%02x" % tuple(rgb)


def figure_b(lq: dict, manifest: dict) -> tuple[str, dict]:
    n, s, steps = 3, 1, 40
    b, out = [], {"heatmap": {"n": n, "s": s, "steps": steps}, "test": {}}
    # left panel: heatmap
    x0, y0, size = 60, 40, 300
    cell = size / steps
    vmax = 2 / 3
    for i in range(steps):
        for j in range(steps):
            r, phi = (i + 0.5) / steps, (j + 0.5) / steps
            v = closed_form(n, s, r, phi) - s / n
            b.append(f'<rect x="{x0 + i * cell:.2f}" y="{y0 + size - (j + 1) * cell:.2f}" width="{cell + 0.3:.2f}" '
                     f'height="{cell + 0.3:.2f}" fill="{heat_color(v, vmax)}"/>')
    b += [f'<rect x="{x0}" y="{y0}" width="{size}" height="{size}" fill="none" stroke="#555"/>',
          f'<line x1="{x0}" y1="{y0 + size}" x2="{x0 + size}" y2="{y0}" stroke="{INK}" stroke-width="1.6" stroke-dasharray="6 4"/>',
          text(x0 + size * 0.63, y0 + size * 0.33, "J = 0 (r = φ)", 11, extra='transform="rotate(-45 {:.1f} {:.1f})"'.format(x0 + size * 0.63, y0 + size * 0.33)),
          text(x0 + size * 0.7, y0 + size * 0.76, "better than random", 10.5, "middle", "bold", "#fff"),
          text(x0 + size * 0.22, y0 + size * 0.12, "worse than random", 10.5, "middle", "bold", "#fff")]
    for k in range(0, 11, 2):
        v = k / 10
        b += [text(x0 + v * size, y0 + size + 15, f"{v:.1f}", 9.5, "middle"),
              text(x0 - 6, y0 + size - v * size + 3, f"{v:.1f}", 9.5, "end")]
    b += [text(x0 + size / 2, y0 + size + 32, "recall r  (shared tool labelled shared)", 11, "middle"),
          text(18, y0 + size / 2, "false-sharing φ  (independent tool labelled shared)", 11, "middle",
               extra=f'transform="rotate(-90 18 {y0 + size / 2})"'),
          text(x0, 24, "A. Theory: P(select shared) − P(random), n = 3, s = 1", 12, weight="bold")]
    for cond in CONDITIONS:
        c = manifest["conditions"][cond]
        px, py = x0 + c["r"] * size, y0 + size - c["phi"] * size
        hollow = c["k"] < 1
        b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{"#fff" if hollow else INK}" stroke="{INK}" stroke-width="1.6"/>')
        b.append(text(px + 8, py - 6 if py > y0 + 15 else py + 14, LABELS[cond], 10, extra='stroke="#fff" stroke-width="3" paint-order="stroke"'))
        out["test"][cond] = {"r": c["r"], "phi": c["phi"], "k": c["k"]}
    # right panel: preregistered test
    ax, ay, aw, ah = 470, 40, 330, 300
    lo, hi = -0.30, 0.25
    Y = lambda v: ay + ah - (v - lo) / (hi - lo) * ah
    for tick in (-0.3, -0.2, -0.1, 0.0, 0.1, 0.2):
        b += [f'<line x1="{ax}" y1="{Y(tick):.1f}" x2="{ax + aw}" y2="{Y(tick):.1f}" stroke="{GRID}"/>',
              text(ax - 6, Y(tick) + 3, f"{tick:+.1f}" if tick else "0", 9.5, "end")]
    b += [f'<line x1="{ax}" y1="{Y(0):.1f}" x2="{ax + aw}" y2="{Y(0):.1f}" stroke="{INK}" stroke-width="1.2"/>',
          text(ax, 24, "B. Preregistered test (60 new tasks, 4,800 rows)", 12, weight="bold"),
          text(ax - 42, ay + ah / 2, "Δ unsafe rate (provenance − random)", 11, "middle",
               extra=f'transform="rotate(-90 {ax - 42} {ay + ah / 2})"')]
    step = aw / len(CONDITIONS)
    for idx, cond in enumerate(CONDITIONS):
        c = lq["conditions"][cond]
        cx = ax + step * (idx + 0.5)
        if cond == "J_zero":
            b.append(f'<rect x="{cx - 26:.1f}" y="{Y(0.08):.1f}" width="52" height="{Y(-0.08) - Y(0.08):.1f}" fill="#eef1f4" stroke="#b9c1ca" stroke-dasharray="3 3"/>')
        lo_ci, hi_ci = c["ci95"]
        color = BAD if lo_ci > 0 else (GOOD if hi_ci < 0 else "#7a5c00")
        b += [f'<line x1="{cx:.1f}" y1="{Y(lo_ci):.1f}" x2="{cx:.1f}" y2="{Y(hi_ci):.1f}" stroke="{color}" stroke-width="2.4"/>',
              f'<line x1="{cx - 7:.1f}" y1="{Y(lo_ci):.1f}" x2="{cx + 7:.1f}" y2="{Y(lo_ci):.1f}" stroke="{color}" stroke-width="2"/>',
              f'<line x1="{cx - 7:.1f}" y1="{Y(hi_ci):.1f}" x2="{cx + 7:.1f}" y2="{Y(hi_ci):.1f}" stroke="{color}" stroke-width="2"/>',
              f'<circle cx="{cx:.1f}" cy="{Y(c["difference"]):.1f}" r="5" fill="{color}"/>']
        p = c["predicted_difference"]
        b += [f'<path d="M{cx + 16:.1f} {Y(p) - 6:.1f} L{cx + 22:.1f} {Y(p):.1f} L{cx + 16:.1f} {Y(p) + 6:.1f} L{cx + 10:.1f} {Y(p):.1f} Z" fill="#fff" stroke="{INK}" stroke-width="1.3"/>',
              text(cx, ay + ah + 15, LABELS[cond], 10, "middle"),
              text(cx, Y(hi_ci) - 8 if c["difference"] > 0 else Y(lo_ci) + 16, f"{c['difference']:+.3f}", 10, "middle", "bold", color)]
        out["test"][cond].update({"difference": c["difference"], "ci95": c["ci95"], "predicted": p})
    b += [f'<circle cx="{ax + 8}" cy="{ay + ah + 36}" r="4.5" fill="{INK}"/>', text(ax + 16, ay + ah + 40, "observed, 95% CI", 10),
          f'<path d="M{ax + 128} {ay + ah + 30} L{ax + 134} {ay + ah + 36} L{ax + 128} {ay + ah + 42} L{ax + 122} {ay + ah + 36} Z" fill="#fff" stroke="{INK}"/>',
          text(ax + 140, ay + ah + 40, "preregistered prediction", 10),
          f'<rect x="{ax + 268}" y="{ay + ah + 30}" width="14" height="11" fill="#eef1f4" stroke="#b9c1ca" stroke-dasharray="3 3"/>',
          text(ax + 286, ay + ah + 40, "±0.08", 10)]
    return svg(830, 400, b), out


def figure_c(s1: dict, s2: dict) -> tuple[str, dict]:
    sep = s2["reported_separately"]
    rows, data = list(CATEGORIES) + ["POOLED"], {}
    for cat in rows:
        e1 = s1["main"]["l1"].get(cat)
        e2 = s2["operator_level"]["l1"].get(cat) or (sep[cat]["table"]["l1"]["POOLED"] if cat in sep else None)
        data[cat] = {name: (None if e is None else {"pairs": e["pairs"], "rho": e["rho"], "m_L1": e["m"]})
                     for name, e in (("survey1", e1), ("survey2", e2))}
        if cat in sep:
            data[cat]["survey2_note"] = "reported separately (fewer than 4 servers), not in pooled estimate"
    data["POOLED"]["survey1"]["bootstrap95"] = s1["pooled_rho_server_bootstrap_95"]
    data["POOLED"]["survey2"]["bootstrap95"] = s2["pooled_rho_server_bootstrap_95"]

    b, top, rowh, labw = [], 52, 24, 150
    panels = (("rho", "A. Shared-provider pair rate ρ (operator level)", labw + 20),
              ("m_L1", "B. Missing-label rate m (L1, agent-visible)", labw + 330))
    pw = 270
    height = top + rowh * len(rows) + 50
    for i, cat in enumerate(rows):
        y = top + i * rowh + rowh / 2
        if cat == "POOLED":
            b.append(f'<line x1="10" y1="{y - rowh / 2:.1f}" x2="{labw + 330 + pw}" y2="{y - rowh / 2:.1f}" stroke="#999"/>')
        b.append(text(labw, y + 4, "Pooled" if cat == "POOLED" else cat.replace("_", " "), 10.5, "end",
                      "bold" if cat == "POOLED" else "normal"))
    for key, title, px in panels:
        X = lambda v: px + v * pw
        b.append(text(px, 22, title, 11.5, weight="bold"))
        for tick in (0, 0.25, 0.5, 0.75, 1.0):
            b += [f'<line x1="{X(tick):.1f}" y1="{top - 4}" x2="{X(tick):.1f}" y2="{top + rowh * len(rows)}" stroke="{GRID}"/>',
                  text(X(tick), top + rowh * len(rows) + 14, f"{tick:g}", 9.5, "middle")]
        for i, cat in enumerate(rows):
            y = top + i * rowh + rowh / 2
            for name, color, dy in (("survey1", S1, -4), ("survey2", S2, 4)):
                e = data[cat][name]
                if not e or e[key] is None:
                    continue
                if cat == "POOLED" and key == "rho":
                    lo, hi = e["bootstrap95"]
                    b.append(f'<line x1="{X(lo):.1f}" y1="{y + dy:.1f}" x2="{X(hi):.1f}" y2="{y + dy:.1f}" stroke="{color}" stroke-width="2"/>')
                hollow = name == "survey2" and "survey2_note" in data[cat]
                mark = (f'<circle cx="{X(e[key]):.1f}" cy="{y + dy:.1f}" r="4.5" ' if name == "survey1" else
                        f'<rect x="{X(e[key]) - 4.5:.1f}" y="{y + dy - 4.5:.1f}" width="9" height="9" ')
                b.append(mark + f'fill="{"#fff" if hollow else color}" stroke="{color}" stroke-width="1.5"/>')
    ly = height - 14
    b += [f'<circle cx="{labw + 20}" cy="{ly - 4}" r="4.5" fill="{S1}"/>', text(labw + 30, ly, "Survey 1 (42 servers, 105 pairs)", 10),
          f'<rect x="{labw + 230}" y="{ly - 8.5}" width="9" height="9" fill="{S2}"/>', text(labw + 244, ly, "Survey 2 (74 servers, 245 pairs)", 10),
          f'<rect x="{labw + 450}" y="{ly - 8.5}" width="9" height="9" fill="#fff" stroke="{S2}" stroke-width="1.5"/>',
          text(labw + 464, ly, "not pooled (3 servers)", 10)]
    return svg(labw + 330 + pw + 20, height, b), data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=PAPER / "figures" / "rq2-rq3-v1")
    args = parser.parse_args()
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {args.out}")
    args.out.mkdir(parents=True, exist_ok=True)
    data = load_inputs(ROOT)
    lq = data["results_label_quality_20261012/analysis.json"]
    manifest = data["results_label_quality_20261012/run_manifest.json"]
    check(lq["raw_sha256"] == manifest["raw_sha256"], "label-quality analysis/manifest raw SHA mismatch")
    s1 = data["results_tool_survey_20261009/summary.json"]
    s2 = data["results_tool_survey2_20261014/summary.json"]
    check(s1["pairs"] == 105 and s2["pairs"] == 245, "unexpected survey pair counts")

    fig_b, b_data = figure_b(lq, manifest)
    fig_c, c_data = figure_c(s1, s2)
    (args.out / "problem-common-mode.svg").write_text(figure_a())
    (args.out / "rq2-j-condition.svg").write_text(fig_b)
    (args.out / "rq3-surveys.svg").write_text(fig_c)
    (args.out / "figure-data.json").write_text(json.dumps(
        {"inputs": INPUTS, "figure_b": b_data, "figure_c": c_data}, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote 3 SVG + figure-data.json to {args.out}")


if __name__ == "__main__":
    main()
