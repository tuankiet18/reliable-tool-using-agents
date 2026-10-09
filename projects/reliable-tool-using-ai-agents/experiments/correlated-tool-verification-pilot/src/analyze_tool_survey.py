#!/usr/bin/env python3
"""Analysis for the real-tool failure-domain metadata survey (protocol §5).

Reads `data/tool_survey/coding.csv` (coder A) and, when it has been filled in,
`data/tool_survey/coder_b_template.csv` (coder B). Builds every within-category pair of
servers and reports, per category and pooled:

  rho  share of pairs that truly share an upstream provider (code ground truth)
  m    share of pairs whose declared sharing label is missing (a side is `unknown`)
  r    P(declared shared | truly shared), over pairs with a declared label
  phi  P(declared shared | truly independent), over pairs with a declared label
  J    r - phi

for L1 (agent-visible: server/tool names and tool descriptions; primary) and
L2 (L1 + README; sensitivity). Raw counts are always reported. A server-level bootstrap
within categories gives a percentile interval for pooled rho.

Sensitivity analyses: (b) drop servers with a user-switchable provider; (c) treat the
AMBIGUOUS self-hosted SearXNG pair as not shared. Protocol sensitivity (a) ("any provider
the code can call") is NOT computed: the coding recorded default providers only.

Also projects observed (r, phi) onto the selector model of `analyze_hidden_dependency.py`.
This projection is not a measurement of agent behaviour.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from analyze_hidden_dependency import p_select_shared_exact

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tool_survey"
UNKNOWN = {"", "unknown"}


def providers(value: str) -> frozenset[str]:
    return frozenset(p.strip() for p in value.split(";") if p.strip() and p.strip().lower() not in UNKNOWN)


def load_coding(path: Path) -> list[dict]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    for row in rows:
        row["truth"] = providers(row["upstream_providers"])
        row["l1"] = providers(row["l1_declared_provider"])
        row["l2"] = providers(row["l2_declared_provider"])
        row["configurable"] = row["configurable_upstream"].strip().lower() == "true"
        row["ambiguous"] = "AMBIGUOUS" in row["notes"]
    return rows


def build_pairs(rows: list[dict], ambiguous_as_independent: bool = False) -> list[dict]:
    by_category = defaultdict(list)
    for row in rows:
        by_category[row["category"]].append(row)
    pairs = []
    for category, members in sorted(by_category.items()):
        for a, b in itertools.combinations(members, 2):
            shared = bool(a["truth"] & b["truth"])
            if ambiguous_as_independent and a["ambiguous"] and b["ambiguous"]:
                shared = False
            pair = {"category": category, "a": a["server_id"], "b": b["server_id"], "truly_shared": shared}
            for level in ("l1", "l2"):
                if not a[level] or not b[level]:
                    pair[level] = "missing"
                else:
                    pair[level] = "shared" if a[level] & b[level] else "independent"
            pairs.append(pair)
    return pairs


def metrics(pairs: list[dict], level: str) -> dict:
    n = len(pairs)
    shared = sum(p["truly_shared"] for p in pairs)
    missing = sum(p[level] == "missing" for p in pairs)
    labelled = [p for p in pairs if p[level] != "missing"]
    ts = [p for p in labelled if p["truly_shared"]]
    ti = [p for p in labelled if not p["truly_shared"]]
    tp = sum(p[level] == "shared" for p in ts)
    fp = sum(p[level] == "shared" for p in ti)
    r = tp / len(ts) if ts else None
    phi = fp / len(ti) if ti else None
    return {
        "pairs": n, "truly_shared": shared, "rho": shared / n if n else None,
        "missing": missing, "m": missing / n if n else None,
        "labelled": len(labelled),
        "labelled_truly_shared": len(ts), "declared_shared_among_truly_shared": tp,
        "labelled_truly_independent": len(ti), "declared_shared_among_truly_independent": fp,
        "r": r, "phi": phi, "J": (r - phi) if r is not None and phi is not None else None,
    }


def table(pairs: list[dict]) -> dict:
    out = {}
    for level in ("l1", "l2"):
        cats = sorted({p["category"] for p in pairs})
        out[level] = {c: metrics([p for p in pairs if p["category"] == c], level) for c in cats}
        out[level]["POOLED"] = metrics(pairs, level)
    return out


def bootstrap_rho(rows: list[dict], resamples: int, seed: int) -> tuple[float, float]:
    rng = random.Random(seed)
    by_category = defaultdict(list)
    for row in rows:
        by_category[row["category"]].append(row)
    values = []
    for _ in range(resamples):
        shared = total = 0
        for members in by_category.values():
            draw = [rng.choice(members) for _ in members]
            for a, b in itertools.combinations(range(len(draw)), 2):
                if draw[a]["server_id"] == draw[b]["server_id"]:
                    continue  # a server is not paired with a copy of itself
                total += 1
                shared += bool(draw[a]["truth"] & draw[b]["truth"])
        if total:
            values.append(shared / total)
    values.sort()
    return values[int(0.025 * len(values))], values[int(0.975 * len(values)) - 1]


def projection(rows: list[dict], r: float | None, phi: float | None) -> dict | None:
    """Mean P(select a truly shared corroborator) over primaries that have >=1 shared peer."""
    if r is None or phi is None:
        return None
    by_category = defaultdict(list)
    for row in rows:
        by_category[row["category"]].append(row)
    prov, rand, used = [], [], 0
    for members in by_category.values():
        for primary in members:
            peers = [m for m in members if m is not primary]
            s = sum(bool(primary["truth"] & m["truth"]) for m in peers)
            if s == 0:
                continue
            used += 1
            prov.append(p_select_shared_exact(len(peers), s, r, phi))
            rand.append(s / len(peers))
    if not used:
        return None
    return {"primaries_with_shared_peer": used,
            "mean_p_select_shared_provenance": sum(prov) / used,
            "mean_p_select_shared_random": sum(rand) / used}


def p_select_shared_with_missing(n: int, s: int, r: float, phi: float, k: float) -> float:
    """Exact P(select a shared peer) when each label is known with probability k.

    Primary label unknown -> uniform fallback. A peer is a candidate only if its label is
    known and says independent (shared peer: prob 1-r; independent peer: prob 1-phi).
    No candidate -> uniform fallback over all n peers.
    """
    fallback = s / n
    states = []  # per peer: list of (is_candidate, prob)
    for shared in [True] * s + [False] * (n - s):
        p_cand = k * ((1 - r) if shared else (1 - phi))
        states.append((shared, p_cand))
    total = 0.0
    for mask in itertools.product((0, 1), repeat=n):
        prob = 1.0
        for (shared, p_cand), bit in zip(states, mask):
            prob *= p_cand if bit else (1 - p_cand)
        candidates = [shared for (shared, _), bit in zip(states, mask) if bit]
        total += prob * (sum(candidates) / len(candidates) if candidates else fallback)
    return (1 - k) * fallback + k * total


def projection_with_missing(rows: list[dict], level: str, r: float | None, phi: float | None) -> dict | None:
    if r is None or phi is None:
        return None
    k = sum(bool(row[level]) for row in rows) / len(rows)
    by_category = defaultdict(list)
    for row in rows:
        by_category[row["category"]].append(row)
    prov, rand = [], []
    for members in by_category.values():
        for primary in members:
            peers = [m for m in members if m is not primary]
            s = sum(bool(primary["truth"] & m["truth"]) for m in peers)
            if s == 0:
                continue
            prov.append(p_select_shared_with_missing(len(peers), s, r, phi, k))
            rand.append(s / len(peers))
    return {"server_label_known_share_k": k, "primaries_with_shared_peer": len(prov),
            "mean_p_select_shared_provenance": sum(prov) / len(prov),
            "mean_p_select_shared_random": sum(rand) / len(rand)}


def kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def agreement(coding: list[dict], coder_b_path: Path) -> dict:
    if not coder_b_path.exists():
        return {"status": "coder B file not found"}
    b_rows = [r for r in csv.DictReader(coder_b_path.open(encoding="utf-8")) if r.get("upstream_providers", "").strip()]
    if not b_rows:
        return {"status": "coder B labels not yet submitted"}
    a_by_id = {r["server_id"]: r for r in coding}
    common = [r for r in b_rows if r["server_id"] in a_by_id]
    up_a = ["|".join(sorted(a_by_id[r["server_id"]]["truth"])) for r in common]
    up_b = ["|".join(sorted(providers(r["upstream_providers"]))) for r in common]
    l1_a = ["|".join(sorted(a_by_id[r["server_id"]]["l1"])) or "unknown" for r in common]
    l1_b = ["|".join(sorted(providers(r["l1_declared_provider"]))) or "unknown" for r in common]
    return {
        "status": "computed", "servers": len(common),
        "upstream_percent_agreement": sum(x == y for x, y in zip(up_a, up_b)) / len(common),
        "upstream_kappa": kappa(up_a, up_b),
        "l1_percent_agreement": sum(x == y for x, y in zip(l1_a, l1_b)) / len(common),
        "l1_kappa": kappa(l1_a, l1_b),
        "note": "exact-string agreement after splitting on ';'; provider name variants must be reconciled before interpreting",
    }


def fmt(x: float | None) -> str:
    return "  n/a" if x is None else f"{x:5.2f}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coding", type=Path, default=DATA / "coding.csv")
    parser.add_argument("--coder-b", type=Path, default=DATA / "coder_b_template.csv")
    parser.add_argument("--out", type=Path, required=True, help="NEW output directory")
    parser.add_argument("--resamples", type=int, default=2000)
    args = parser.parse_args()
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {args.out}")
    args.out.mkdir(parents=True, exist_ok=True)

    rows = load_coding(args.coding)
    pairs = build_pairs(rows)
    main_table = table(pairs)
    lo, hi = bootstrap_rho(rows, args.resamples, seed=20261009)
    sens_b_rows = [r for r in rows if not r["configurable"]]
    sens = {
        "b_drop_configurable": {"servers": len(sens_b_rows), "table": table(build_pairs(sens_b_rows))},
        "c_searxng_not_shared": {"table": table(build_pairs(rows, ambiguous_as_independent=True))},
        "a_any_callable_provider": "not computed: coding recorded default providers only",
    }
    proj = {}
    for level in ("l1", "l2"):
        r, phi = main_table[level]["POOLED"]["r"], main_table[level]["POOLED"]["phi"]
        proj[level] = {"labels_complete": projection(rows, r, phi),
                       "with_observed_missing_labels": projection_with_missing(rows, level, r, phi)}

    summary = {
        "scope": "descriptive survey of 42 open-source MCP servers; coder A = AI-assisted",
        "coding_sha256": hashlib.sha256(args.coding.read_bytes()).hexdigest(),
        "servers": len(rows), "pairs": len(pairs),
        "main": main_table,
        "pooled_rho_server_bootstrap_95": [lo, hi],
        "sensitivity": sens,
        "projection_onto_selector_model": proj,
        "inter_rater": agreement(rows, args.coder_b),
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    with (args.out / "pairs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(pairs[0]))
        writer.writeheader()
        writer.writerows(pairs)

    print(f"servers={len(rows)} pairs={len(pairs)}  coding sha256={summary['coding_sha256'][:12]}")
    for level in ("l1", "l2"):
        print(f"\n[{level.upper()}] category            pairs shared   rho     m   r(n)        phi(n)       J")
        for cat, mt in main_table[level].items():
            print(f"  {cat:<22}{mt['pairs']:>5}{mt['truly_shared']:>7} {fmt(mt['rho'])} {fmt(mt['m'])}"
                  f"  {fmt(mt['r'])}({mt['labelled_truly_shared']:>2})  {fmt(mt['phi'])}({mt['labelled_truly_independent']:>2})  {fmt(mt['J'])}")
    print(f"\npooled rho 95% server-bootstrap: [{lo:.3f}, {hi:.3f}]")
    for name in ("b_drop_configurable", "c_searxng_not_shared"):
        t = sens[name]["table"]
        print(f"sensitivity {name}: rho={fmt(t['l1']['POOLED']['rho'])}  L1 m={fmt(t['l1']['POOLED']['m'])} "
              f"r={fmt(t['l1']['POOLED']['r'])} phi={fmt(t['l1']['POOLED']['phi'])}")
    for level, variants in proj.items():
        for name, p in variants.items():
            if p:
                extra = f" k={p['server_label_known_share_k']:.2f}" if "server_label_known_share_k" in p else ""
                print(f"projection {level} {name}:{extra} P(select shared) provenance="
                      f"{p['mean_p_select_shared_provenance']:.3f} vs random={p['mean_p_select_shared_random']:.3f}"
                      f" over {p['primaries_with_shared_peer']} primaries")
    print("inter-rater:", summary["inter_rater"]["status"])


if __name__ == "__main__":
    main()
