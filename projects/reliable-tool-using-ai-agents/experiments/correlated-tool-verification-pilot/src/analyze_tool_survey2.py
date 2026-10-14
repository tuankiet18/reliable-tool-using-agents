#!/usr/bin/env python3
"""Survey 2 analysis (protocol "Expanded Real-Tool Metadata Survey" §7, Amendment A2).

A thin wrapper: pair building, metrics, bootstrap, sensitivity and projection are imported
unchanged from `analyze_tool_survey.py`. What is new here, all fixed in Amendment A2 before any
metric was computed:

  * estimate set: `coding.csv` minus categories with fewer than 4 included servers (§4), which
    are reported separately; `coding_agreement_only.csv` is never read here.
  * origin level (pre-registered, evidence (a) only): a server's origin truth is its `origin_a`
    column when filled, otherwise its operator providers mapped through ORIGIN_GLOBAL (provider-
    level facts stated in the surveyed repos). Variants as in survey 1: `naive` (declared names
    compared literally) and `informed` (declared names mapped the same way; a declared name equal
    to one of the server's own operator providers is replaced by that server's `origin_a`).
  * P1-P6 evaluated with the exact rules of protocol §2 (P4 uses the naive variant).
  * descriptive comparison with survey 1 on the 7 shared categories.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from analyze_tool_survey import (bootstrap_rho, build_pairs, load_coding, projection,
                                 projection_with_missing, providers, table)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tool_survey_2"
SURVEY1 = ROOT / "results_tool_survey_20261009" / "summary.json"
MIN_SERVERS = 4
ORIGIN_GLOBAL = {
    "Frankfurter": (frozenset({"ECB"}), "vivart README.md:5; NotNull92 README.md:15; boy-373 exchange_mcp_server.py:85; stock-vibes worker.js:319"),
    "Algolia HN Search": (frozenset({"Hacker News (Y Combinator)"}), "joeswann/hackernews-mcp src/tools/search.ts:16"),
}


def map_global(names: frozenset[str]) -> frozenset[str]:
    out: set[str] = set()
    for name in names:
        out |= ORIGIN_GLOBAL[name][0] if name in ORIGIN_GLOBAL else {name}
    return frozenset(out)


def origin_rows(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    naive, informed = [], []
    for r in rows:
        own = providers(r["origin_a"])
        truth = own if own else map_global(r["truth"])

        def informed_label(names: frozenset[str]) -> frozenset[str]:
            if own and names & r["truth"]:
                names = (names - r["truth"]) | own
            return map_global(names)

        naive.append(dict(r, truth=truth))
        informed.append(dict(r, truth=truth, l1=informed_label(r["l1"]), l2=informed_label(r["l2"])))
    return naive, informed


def evaluate(op: dict, naive: dict) -> dict:
    p_op, l2_op, l2_or = op["l1"]["POOLED"], op["l2"]["POOLED"], naive["l2"]["POOLED"]
    cats = {c: m["rho"] for c, m in naive["l2"].items() if c != "POOLED"}

    def verdict(ok: bool | None) -> str:
        return "not evaluable" if ok is None else ("MET" if ok else "NOT MET")

    r_or, r_op = l2_or["r"], l2_op["r"]
    return {
        "P1": {"rule": "0.05 <= pooled operator rho <= 0.30", "value": p_op["rho"], "verdict": verdict(0.05 <= p_op["rho"] <= 0.30)},
        "P2": {"rule": "m_L1 > 0.50", "value": p_op["m"], "verdict": verdict(p_op["m"] > 0.50)},
        "P3": {"rule": "phi_L1 <= 0.05 (operator)", "value": p_op["phi"],
               "counts": f"{p_op['declared_shared_among_truly_independent']}/{p_op['labelled_truly_independent']}",
               "verdict": verdict(None if p_op["phi"] is None else p_op["phi"] <= 0.05)},
        "P4": {"rule": "r_origin,L2 (naive) < r_operator,L2", "value": [r_or, r_op],
               "counts": [f"{l2_or['declared_shared_among_truly_shared']}/{l2_or['labelled_truly_shared']}",
                          f"{l2_op['declared_shared_among_truly_shared']}/{l2_op['labelled_truly_shared']}"],
               "verdict": verdict(None if r_or is None or r_op is None else r_or < r_op)},
        "P5": {"rule": "some category has origin-level rho >= 0.80", "value": cats,
               "verdict": verdict(any(v is not None and v >= 0.80 for v in cats.values()))},
        "P6": {"rule": "J_operator,L2 > 0", "value": l2_op["J"],
               "verdict": verdict(None if l2_op["J"] is None else l2_op["J"] > 0)},
    }


def fmt(x: float | None) -> str:
    return "  n/a" if x is None else f"{x:5.2f}"


def print_table(name: str, t: dict) -> None:
    for level in ("l1", "l2"):
        print(f"\n[{name} {level.upper()}] category           pairs shared   rho     m   r(n)        phi(n)       J")
        for cat, mt in t[level].items():
            print(f"  {cat:<21}{mt['pairs']:>5}{mt['truly_shared']:>7} {fmt(mt['rho'])} {fmt(mt['m'])}"
                  f"  {fmt(mt['r'])}({mt['labelled_truly_shared']:>2})  {fmt(mt['phi'])}({mt['labelled_truly_independent']:>2})  {fmt(mt['J'])}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coding", type=Path, default=DATA / "coding.csv")
    parser.add_argument("--survey1", type=Path, default=SURVEY1)
    parser.add_argument("--out", type=Path, required=True, help="NEW output directory")
    parser.add_argument("--resamples", type=int, default=2000)
    args = parser.parse_args()
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {args.out}")
    args.out.mkdir(parents=True, exist_ok=True)

    rows_all = load_coding(args.coding)
    counts = Counter(r["category"] for r in rows_all)
    small = sorted(c for c, n in counts.items() if n < MIN_SERVERS)
    rows = [r for r in rows_all if r["category"] not in small]
    small_rows = [r for r in rows_all if r["category"] in small]

    pairs = build_pairs(rows)
    op = table(pairs)
    lo, hi = bootstrap_rho(rows, args.resamples, seed=20261014)
    sens_b_rows = [r for r in rows if not r["configurable"]]
    sens = {
        "b_drop_configurable": {"servers": len(sens_b_rows), "table": table(build_pairs(sens_b_rows))},
        "c_ambiguous_not_shared": {"table": table(build_pairs(rows, ambiguous_as_independent=True))},
    }
    proj = {}
    for level in ("l1", "l2"):
        r, phi = op[level]["POOLED"]["r"], op[level]["POOLED"]["phi"]
        proj[level] = {"labels_complete": projection(rows, r, phi),
                       "with_observed_missing_labels": projection_with_missing(rows, level, r, phi)}

    naive_rows, informed_rows = origin_rows(rows)
    origin = {}
    for name, orows in (("origin_naive", naive_rows), ("origin_informed", informed_rows)):
        t = table(build_pairs(orows))
        origin[name] = {"table": t, "projection_with_missing": {
            lv: projection_with_missing(orows, lv, t[lv]["POOLED"]["r"], t[lv]["POOLED"]["phi"]) for lv in ("l1", "l2")}}

    predictions = evaluate(op, origin["origin_naive"]["table"])

    comparison = {}
    if args.survey1.exists():
        s1 = json.loads(args.survey1.read_text())["main"]
        for cat in sorted(set(s1["l1"]) & set(op["l1"]) - {"POOLED"}):
            comparison[cat] = {f"survey{i}": {"pairs": t["l1"][cat]["pairs"], "rho": t["l1"][cat]["rho"],
                                              "m_L1": t["l1"][cat]["m"], "m_L2": t["l2"][cat]["m"]}
                               for i, t in ((1, s1), (2, op))}

    summary = {
        "scope": "survey 2: descriptive survey of open-source MCP servers; coder A = AI-assisted; human labels not yet included",
        "coding_sha256": hashlib.sha256(args.coding.read_bytes()).hexdigest(),
        "servers_in_coding": len(rows_all), "servers_in_estimates": len(rows), "pairs": len(pairs),
        "reported_separately": {c: {"servers": counts[c], "table": table(build_pairs([r for r in small_rows if r["category"] == c]))}
                                for c in small},
        "operator_level": op,
        "pooled_rho_server_bootstrap_95": [lo, hi],
        "sensitivity": sens,
        "projection_onto_selector_model": proj,
        "origin_level": {"evidence": "(a) repo-internal only; (a)+(b) secondary analysis not computed (no provider-doc evidence collected)",
                         "global_map": {k: {"origins": sorted(v[0]), "evidence": v[1]} for k, v in ORIGIN_GLOBAL.items()},
                         "servers_with_origin_a": sum(bool(r["origin_a"].strip()) for r in rows), **origin},
        "predictions": predictions,
        "survey1_comparison_7_categories": comparison,
        "inter_rater": "human-coder labels not yet received; not human-validated",
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    for name, prs in (("pairs.csv", pairs), ("pairs_origin_naive.csv", build_pairs(naive_rows))):
        with (args.out / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(prs[0]))
            writer.writeheader()
            writer.writerows(prs)

    print(f"coding sha256={summary['coding_sha256'][:12]}  servers={len(rows_all)} estimates={len(rows)} "
          f"pairs={len(pairs)}  reported separately: {small}")
    print_table("operator", op)
    print(f"\npooled rho 95% server-bootstrap: [{lo:.3f}, {hi:.3f}]")
    for name, s in sens.items():
        t = s["table"]
        print(f"sensitivity {name}: rho={fmt(t['l1']['POOLED']['rho'])}  L1 m={fmt(t['l1']['POOLED']['m'])} "
              f"r={fmt(t['l1']['POOLED']['r'])} phi={fmt(t['l1']['POOLED']['phi'])}  L2 J={fmt(t['l2']['POOLED']['J'])}")
    for level, variants in proj.items():
        for name, p in variants.items():
            if p:
                extra = f" k={p['server_label_known_share_k']:.2f}" if "server_label_known_share_k" in p else ""
                print(f"projection {level} {name}:{extra} P(select shared) provenance="
                      f"{p['mean_p_select_shared_provenance']:.3f} vs random={p['mean_p_select_shared_random']:.3f}"
                      f" over {p['primaries_with_shared_peer']} primaries")
    for name, res in origin.items():
        print_table(name, res["table"])
    for c, info in summary["reported_separately"].items():
        p = info["table"]["l1"]["POOLED"]
        print(f"separately {c}: servers={info['servers']} pairs={p['pairs']} shared={p['truly_shared']}")
    print("\npredictions:")
    for k, v in predictions.items():
        print(f"  {k} {v['verdict']:<14} {v['rule']}  value={v['value']}" + (f"  counts={v['counts']}" if "counts" in v else ""))
    print("\nsurvey 1 vs 2 (7 shared categories): rho / m_L1")
    for cat, v in comparison.items():
        print(f"  {cat:<20} s1 {fmt(v['survey1']['rho'])} / {fmt(v['survey1']['m_L1'])} ({v['survey1']['pairs']})   "
              f"s2 {fmt(v['survey2']['rho'])} / {fmt(v['survey2']['m_L1'])} ({v['survey2']['pairs']})")


if __name__ == "__main__":
    main()
