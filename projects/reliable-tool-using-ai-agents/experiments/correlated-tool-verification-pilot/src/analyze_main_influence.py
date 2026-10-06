#!/usr/bin/env python3
"""Post-hoc deletion diagnostics for frozen main decisions; no policy runs or CIs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_SHA256 = "a51aebcb207f996e7a4d065b2e424fe794346d685d5f37a615d0de6bcb872234"
POLICIES = {"random_k", "provenance_k"}


def paired_cells(rows: list[dict]) -> dict[str, list[dict]]:
    """Reject duplicate, unmatched or unbalanced cells before averaging seeds."""
    pairs = {}
    task_metadata = {}
    for row in rows:
        if row["policy"] not in POLICIES:
            continue
        key = (row["regime"], row["task_id"], row["seed"])
        pair = pairs.setdefault(key, {})
        if row["policy"] in pair:
            raise ValueError(f"duplicate policy cell: {key}/{row['policy']}")
        if type(row["unsafe_refund"]) is not bool:
            raise ValueError("unsafe_refund must be a Boolean")
        metadata = (row["difficulty"], row["expected_action"])
        previous = task_metadata.setdefault(row["task_id"], metadata)
        if previous != metadata:
            raise ValueError(f"task metadata mismatch: {row['task_id']}")
        pair[row["policy"]] = row
    if not pairs:
        raise ValueError("no paired policy cells")
    regimes = sorted({key[0] for key in pairs})
    tasks = sorted({key[1] for key in pairs})
    seeds = sorted({key[2] for key in pairs})
    if set(pairs) != set(itertools.product(regimes, tasks, seeds)):
        raise ValueError("incomplete task/seed/regime grid")
    output = {regime: [] for regime in regimes}
    for (regime, task, seed), pair in sorted(pairs.items()):
        if set(pair) != POLICIES:
            raise ValueError(f"unmatched policies: {regime}/{task}/{seed}")
        control, treatment = pair["random_k"], pair["provenance_k"]
        if control["observations"][0] != treatment["observations"][0]:
            raise ValueError(f"different primary observations: {regime}/{task}/{seed}")
        output[regime].append({
            "task_id": task, "seed": seed, "difficulty": control["difficulty"],
            "expected_action": control["expected_action"],
            "random_unsafe": int(control["unsafe_refund"]),
            "provenance_unsafe": int(treatment["unsafe_refund"]),
        })
    return output


def metrics(cells: list[dict]) -> dict:
    if not cells:
        raise ValueError("empty retained sample")
    numerator = sum(c["provenance_unsafe"] - c["random_unsafe"] for c in cells)
    delta = Fraction(numerator, len(cells))
    return {
        "paired_cells": len(cells),
        "task_instances": len({c["task_id"] for c in cells}),
        "seeds": len({c["seed"] for c in cells}),
        "random_unsafe": sum(c["random_unsafe"] for c in cells),
        "provenance_unsafe": sum(c["provenance_unsafe"] for c in cells),
        "difference_numerator": numerator,
        "difference_denominator": len(cells),
        "difference_exact": str(delta),
        "difference": float(delta),
        "difference_percentage_points": float(100 * delta),
    }


def deletion_diagnostic(cells: list[dict], field: str) -> dict:
    groups = sorted({cell[field] for cell in cells})
    if len(groups) < 2:
        raise ValueError(f"need at least two {field} groups")
    results = []
    for group in groups:
        kept = [cell for cell in cells if cell[field] != group]
        removed = [cell for cell in cells if cell[field] == group]
        results.append({"removed_group": group, "removed": metrics(removed), "retained": metrics(kept)})
    deltas = [Fraction(r["retained"]["difference_exact"]) for r in results]
    return {
        "grouping": field, "deletions": results,
        "retained_difference_range": [float(min(deltas)), float(max(deltas))],
        "retained_sign_counts": {
            "negative": sum(d < 0 for d in deltas),
            "zero": sum(d == 0 for d in deltas),
            "positive": sum(d > 0 for d in deltas),
        },
        "interpretation": "Observed deletion range; not a confidence interval or hypothesis test.",
    }


def analyze(rows: list[dict]) -> dict:
    groups = paired_cells(rows)
    output = {}
    for regime, cells in groups.items():
        output[regime] = {
            "observed": metrics(cells),
            "leave_one_task_out": deletion_diagnostic(cells, "task_id"),
            "leave_one_seed_out": deletion_diagnostic(cells, "seed"),
            "leave_one_stratum_out": deletion_diagnostic(cells, "difficulty"),
        }
    return {
        "status": "POST_HOC_DESCRIPTIVE_SENSITIVITY",
        "scope": "Frozen main unsafe decision differences, provenance_k minus random_k; balanced paired grid.",
        "new_episodes": 0, "new_model_calls": 0, "new_confidence_intervals": 0,
        "limitations": [
            "No new tasks, seeds, topology or independent evidence.",
            "Deleting strata changes task composition; deletion ranges are not population uncertainty intervals.",
            "Targeted treatment zero follows from accurate metadata and uncorrupted independent sources.",
            "Seed groups are deterministic schedules, not sampled deployment environments.",
        ],
        "regimes": output,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, default=ROOT / "results_main_study/raw.jsonl")
    parser.add_argument("--out", type=Path, required=True, help="New directory; existing paths are refused")
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(f"refusing to overwrite {args.out}")
    payload = args.raw.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != RAW_SHA256:
        raise ValueError(f"frozen main raw hash mismatch: {digest}")
    rows = [json.loads(line) for line in payload.decode("utf-8").splitlines() if line.strip()]
    result = analyze(rows)
    cases = {r["task_id"]: r["difficulty"] for r in rows}
    if len(rows) != 1350 or len(cases) != 30 or sorted(Counter(cases.values()).values()) != [5] * 6:
        raise ValueError("unexpected frozen design dimensions")
    result["inputs"] = {
        "raw_relative_to_experiment": "results_main_study/raw.jsonl",
        "raw_sha256": digest,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "raw_rows": len(rows), "task_instances": len(cases),
        "tasks_per_stratum": dict(sorted(Counter(cases.values()).items())),
    }
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / "analysis.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for regime, data in result["regimes"].items():
        print(regime, data["observed"]["difference_exact"])
        for mode in ("leave_one_task_out", "leave_one_seed_out", "leave_one_stratum_out"):
            print(" ", mode, data[mode]["retained_difference_range"], data[mode]["retained_sign_counts"])


if __name__ == "__main__":
    main()
