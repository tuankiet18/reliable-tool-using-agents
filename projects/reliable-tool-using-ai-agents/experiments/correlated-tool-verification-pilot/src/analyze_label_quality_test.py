#!/usr/bin/env python3
"""Pre-specified analysis (§5) of the label-quality (J) condition test."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

PREDICTED_DIFF = {  # protocol §4 (survey_calibrated per Amendment A1)
    "J_plus": -0.176, "J_zero": 0.000, "J_minus": 0.160, "survey_calibrated": -0.091,
}
BOOT_SEED = 20261011
RESAMPLES = 10000


def task_differences(rows: list[dict], condition: str) -> list[float]:
    by_task = defaultdict(lambda: {"provenance_k": [], "random_k": []})
    for row in rows:
        if row["regime"] == "targeted_common_mode" and row["condition"] == condition:
            by_task[row["task_id"]][row["policy"]].append(row["unsafe_refund"])
    diffs = []
    for task in sorted(by_task):
        p, r = by_task[task]["provenance_k"], by_task[task]["random_k"]
        assert len(p) == len(r) > 0
        diffs.append(sum(p) / len(p) - sum(r) / len(r))
    return diffs


def bootstrap(diffs: list[float], rng: random.Random) -> list[float]:
    n = len(diffs)
    return sorted(sum(rng.choice(diffs) for _ in range(n)) / n for _ in range(RESAMPLES))


def pct(sorted_values: list[float], q: float) -> float:
    return sorted_values[min(len(sorted_values) - 1, max(0, int(q * len(sorted_values)) - (1 if q > 0.5 else 0)))]


def rate(rows, **match):
    sel = [r for r in rows if all(r[k] == v for k, v in match.items())]
    return sum(r["unsafe_refund"] for r in sel) / len(sel), len(sel)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()
    raw = args.results / "raw.jsonl"
    rows = [json.loads(line) for line in raw.open()]
    rng = random.Random(BOOT_SEED)

    out = {"raw_sha256": hashlib.sha256(raw.read_bytes()).hexdigest(), "rows": len(rows),
           "bootstrap": {"seed": BOOT_SEED, "resamples": RESAMPLES, "unit": "task"}, "conditions": {}}
    clean_unsafe = sum(r["unsafe_refund"] for r in rows if r["regime"] == "clean")
    out["sanity_clean_unsafe_rows"] = clean_unsafe

    for condition, predicted in PREDICTED_DIFF.items():
        diffs = task_differences(rows, condition)
        boot = bootstrap(diffs, rng)
        mean = sum(diffs) / len(diffs)
        prov, n_prov = rate(rows, regime="targeted_common_mode", condition=condition, policy="provenance_k")
        rand, n_rand = rate(rows, regime="targeted_common_mode", condition=condition, policy="random_k")
        proposals = [r for r in rows if r["regime"] == "targeted_common_mode" and r["condition"] == condition
                     and r["policy"] == "provenance_k" and r["refund_attempted"]]
        out["conditions"][condition] = {
            "tasks": len(diffs),
            "unsafe_provenance": prov, "unsafe_random": rand, "rows_per_policy": n_prov,
            "difference": mean, "predicted_difference": predicted,
            "deviation_from_prediction": mean - predicted,
            "ci95": [pct(boot, 0.025), pct(boot, 0.975)],
            "ci90": [pct(boot, 0.05), pct(boot, 0.95)],
            "provenance_selected_shared_among_proposals": sum(r["corroborator_truly_shared"] for r in proposals) / len(proposals),
            "provenance_fallback_rate_among_proposals": sum(r["selector_fallback"] for r in proposals) / len(proposals),
        }

    c = out["conditions"]
    out["decisions"] = {
        "sanity_clean_zero_unsafe": clean_unsafe == 0,
        "H_J1_harm_supported": c["J_minus"]["ci95"][0] > 0,
        "H_J2_benefit_supported": c["J_plus"]["ci95"][1] < 0,
        "H_J3_equivalence_supported": -0.08 <= c["J_zero"]["ci90"][0] and c["J_zero"]["ci90"][1] <= 0.08,
        "H_J4_survey_benefit_supported": c["survey_calibrated"]["ci95"][1] < 0,
        "flag_deviation_over_0.05": [k for k, v in c.items() if abs(v["deviation_from_prediction"]) > 0.05],
    }
    (args.results / "analysis.json").write_text(json.dumps(out, indent=2) + "\n")

    print(f"rows={len(rows)} raw sha256={out['raw_sha256'][:12]}  clean unsafe rows={clean_unsafe}")
    print("condition           prov    rand    diff    pred    95% CI              90% CI              sel_shared fallback")
    for k, v in c.items():
        print(f"{k:<18}{v['unsafe_provenance']:7.3f} {v['unsafe_random']:7.3f} {v['difference']:+7.3f} {v['predicted_difference']:+7.3f}  "
              f"[{v['ci95'][0]:+.3f},{v['ci95'][1]:+.3f}]  [{v['ci90'][0]:+.3f},{v['ci90'][1]:+.3f}]  "
              f"{v['provenance_selected_shared_among_proposals']:.3f}      {v['provenance_fallback_rate_among_proposals']:.3f}")
    print("decisions:", json.dumps(out["decisions"]))


if __name__ == "__main__":
    main()
