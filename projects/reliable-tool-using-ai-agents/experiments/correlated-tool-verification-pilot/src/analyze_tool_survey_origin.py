#!/usr/bin/env python3
"""POST-HOC sensitivity: re-define "shared upstream" at the DATA-ORIGIN level.

Not in the survey protocol; written after seeing the main results (r = 1 at the
API-operator level). Every operator -> origin link below is supported by evidence inside
the surveyed repositories themselves (code, bundled config, README or tool description);
dependencies documented only outside the repos (e.g. a search engine licensing another's
index) are deliberately NOT added, so this is still a lower bound.

Two variants:
  naive    truth mapped to origins; declared labels compared literally (an agent that
           only reads names, without knowing e.g. that Photon serves OpenStreetMap data)
  informed truth AND declared names mapped through the same origin table (an agent that
           knows the mapping)
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from analyze_tool_survey import DATA, build_pairs, load_coding, projection_with_missing, table

SEARXNG_DEFAULT_WEB_ENGINES = frozenset(
    {"Google", "DuckDuckGo", "Brave Search", "Startpage", "Wikipedia", "Wiby"}
)
ORIGIN = {
    "OpenStreetMap Nominatim": (frozenset({"OpenStreetMap"}), "Nominatim is OpenStreetMap's geocoder (nominatim.openstreetmap.org)"),
    "Photon (Komoot)": (frozenset({"OpenStreetMap"}), "adelie-ai/geocode-mcp src/service.rs:69 'Photon geocoding API (powered by OpenStreetMap)'"),
    "Frankfurter": (frozenset({"ECB"}), "cyanheads/exchange-rates-mcp-server README.md:32 'ECB reference exchange rates via Frankfurter'"),
    "ECB": (frozenset({"ECB"}), "declared data origin"),
    "cbr-xml-daily.ru": (frozenset({"Bank of Russia"}), "cloud-ru lab README.md:7 'курсы валют от ЦБР (cbr-xml-daily.ru)'"),
    "Bank of Russia": (frozenset({"Bank of Russia"}), "declared data origin"),
    "Algolia HN Search": (frozenset({"Hacker News (Y Combinator)"}), "hn.algolia.com indexes Hacker News items (devabdultech/hn-mcp, karanb192/hn-mcp)"),
    "SearXNG (self-hosted)": (SEARXNG_DEFAULT_WEB_ENGINES, "slinusc/web-search-mcp-server config/settings.yml enabled general engines; Pascalrjt uses SearXNG defaults (use_default_settings: true) — INFERRED to be the same set"),
}


def to_origin(names: frozenset[str]) -> frozenset[str]:
    out: set[str] = set()
    for name in names:
        out |= ORIGIN[name][0] if name in ORIGIN else {name}
    return frozenset(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coding", type=Path, default=DATA / "coding.csv")
    parser.add_argument("--out", type=Path, required=True, help="NEW output directory")
    args = parser.parse_args()
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {args.out}")
    args.out.mkdir(parents=True, exist_ok=True)

    operator_rows = load_coding(args.coding)
    naive = [dict(r, truth=to_origin(r["truth"])) for r in operator_rows]
    informed = [dict(r, truth=to_origin(r["truth"]), l1=to_origin(r["l1"]), l2=to_origin(r["l2"])) for r in operator_rows]

    results = {}
    for name, rows in (("operator_level_main", operator_rows), ("origin_naive", naive), ("origin_informed", informed)):
        t = table(build_pairs(rows))
        proj = {}
        for level in ("l1", "l2"):
            pooled = t[level]["POOLED"]
            proj[level] = projection_with_missing(rows, level, pooled["r"], pooled["phi"])
        results[name] = {"table": t, "projection_with_missing": proj}

    summary = {
        "status": "POST-HOC sensitivity, not pre-specified in the survey protocol",
        "coding_sha256": hashlib.sha256(args.coding.read_bytes()).hexdigest(),
        "origin_map": {k: {"origins": sorted(v[0]), "evidence": v[1]} for k, v in ORIGIN.items()},
        "results": results,
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")

    print("variant              level  rho    m     r (tp/n)        phi (fp/n)      J      P(sel shared) prov vs rand")
    for name, res in results.items():
        for level in ("l1", "l2"):
            p = res["table"][level]["POOLED"]
            pr = res["projection_with_missing"][level]
            r_s = f"{p['r']:.2f} ({p['declared_shared_among_truly_shared']}/{p['labelled_truly_shared']})" if p["r"] is not None else "n/a"
            f_s = f"{p['phi']:.2f} ({p['declared_shared_among_truly_independent']}/{p['labelled_truly_independent']})" if p["phi"] is not None else "n/a"
            j_s = f"{p['J']:+.2f}" if p["J"] is not None else "n/a"
            pj = f"{pr['mean_p_select_shared_provenance']:.3f} vs {pr['mean_p_select_shared_random']:.3f} ({pr['primaries_with_shared_peer']})" if pr else "n/a"
            print(f"{name:<20} {level.upper():<5} {p['rho']:.2f}  {p['m']:.2f}  {r_s:<15} {f_s:<15} {j_s:<6} {pj}")
    for name in ("origin_naive",):
        print(f"\n{name} by category (L2):")
        for cat, mt in results[name]["table"]["l2"].items():
            print(f"  {cat:<20} rho={mt['rho']:.2f} r={mt['r'] if mt['r'] is None else round(mt['r'], 2)} "
                  f"({mt['declared_shared_among_truly_shared']}/{mt['labelled_truly_shared']})")


if __name__ == "__main__":
    main()
