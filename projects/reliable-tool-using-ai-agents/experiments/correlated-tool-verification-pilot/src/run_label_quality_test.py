#!/usr/bin/env python3
"""Preregistered test of the label-quality (J = r - phi) condition.

Implements `synthesis/Protocol: Confirmatory Test of the Label-Quality Condition.md`
v1.0. Reuses the frozen fault map, evidence, gate and oracle code of the robustness
gate; only the corroborator-label model and the selector input differ.

Label model (§3.3): the primary's label is always correct. Each corroborator first has a
label with probability k (otherwise its label is missing); a present label says
"shares the primary's failure domain" with probability r for the truly shared tool and
phi for a truly independent tool. `provenance_k` picks uniformly among corroborators
labelled independent, falling back to all corroborators when none is.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any

from run_main_study import (
    CORROBORATORS,
    PRIMARY_TOOL,
    SOURCE_TOPOLOGY,
    evidence,
    outcome_correct,
    sha256,
    stable_seed,
    verification_decision,
)
from run_robustness_gate import build_fault_map

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = {  # name: (r, phi, k)
    "J_plus": (0.9, 0.1, 1.0),
    "J_zero": (0.5, 0.5, 1.0),
    "J_minus": (0.1, 0.6, 1.0),
    "survey_calibrated": (0.57, 0.0, 0.55),
}
LEAKAGE = 0.10
DEFAULT_SEEDS = (1103, 1217, 1307, 1409, 1511)
TASK_IDS = [f"INS-{index:05d}" for index in range(120, 180)]


def truly_shared(tool: str) -> bool:
    return SOURCE_TOPOLOGY[tool] == SOURCE_TOPOLOGY[PRIMARY_TOOL]


def draw_labels(task_id: str, seed: int, condition: str) -> dict[str, str]:
    """Per-corroborator label: 'shared', 'independent' or 'missing'."""
    r, phi, k = CONDITIONS[condition]
    labels = {}
    for tool in CORROBORATORS:
        rng = random.Random(stable_seed(task_id, seed, condition, tool, "label"))
        if rng.random() >= k:
            labels[tool] = "missing"
            continue
        p_shared = r if truly_shared(tool) else phi
        labels[tool] = "shared" if rng.random() < p_shared else "independent"
    return labels


def select_provenance(task_id: str, seed: int, condition: str, labels: dict[str, str]) -> tuple[str, bool]:
    candidates = [tool for tool in CORROBORATORS if labels[tool] == "independent"]
    fallback = not candidates
    if fallback:
        candidates = list(CORROBORATORS)
    rng = random.Random(stable_seed(task_id, seed, condition, "provenance-selector"))
    return rng.choice(candidates), fallback


def select_random(task_id: str, seed: int, condition: str) -> str:
    rng = random.Random(stable_seed(task_id, seed, condition, "random-selector"))
    return rng.choice(CORROBORATORS)


def run_episode(
    case: dict[str, Any], seed: int, regime: str, condition: str, policy: str,
    fault_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    primary_value = fault_map[PRIMARY_TOOL]
    observations = [evidence(PRIMARY_TOOL, primary_value, case)]
    refund_attempted = bool(primary_value["eligible"])
    requested_amount = float(primary_value["max_refund_eur"]) if refund_attempted else None
    labels = draw_labels(case["task_id"], seed, condition)
    corroborator, fallback = None, False
    conflict = blocked = False
    block_reason = None

    if not refund_attempted:
        final_action, final_amount = "escalate", None
    else:
        if policy == "provenance_k":
            corroborator, fallback = select_provenance(case["task_id"], seed, condition, labels)
        elif policy == "random_k":
            corroborator = select_random(case["task_id"], seed, condition)
        else:
            raise ValueError(f"unknown policy: {policy}")
        corroborator_value = fault_map[corroborator]
        observations.append(evidence(corroborator, corroborator_value, case))
        conflict, authorised, block_reason = verification_decision(
            primary_value, corroborator_value, float(requested_amount)
        )
        blocked = not authorised
        final_action, final_amount = ("refund", requested_amount) if authorised else ("escalate", None)

    correct = outcome_correct(case, final_action, final_amount)
    return {
        "task_id": case["task_id"],
        "difficulty": case["difficulty"],
        "expected_action": case["expected_action"],
        "seed": seed,
        "regime": regime,
        "condition": condition,
        "policy": policy,
        "labels": labels if policy == "provenance_k" else None,
        "selector_fallback": fallback,
        "corroborator": corroborator,
        "corroborator_truly_shared": truly_shared(corroborator) if corroborator else None,
        "refund_attempted": refund_attempted,
        "requested_amount_eur": requested_amount,
        "conflict": conflict,
        "blocked": blocked,
        "block_reason": block_reason,
        "final_action": final_action,
        "final_amount_eur": final_amount,
        "action_oracle_correct": correct,
        "unsafe_refund": final_action == "refund" and not correct,
    }


def load_cases(upstream: Path, tasks_path: Path) -> list[dict[str, Any]]:
    frozen = json.loads(tasks_path.read_text())
    sys.path.insert(0, str(upstream / "src"))
    from trajectory_judge.env.world import World, generate_instances

    instances = generate_instances(180, seed=20260914)[120:180]
    by_id = {instance.instance_id: instance for instance in instances}
    cases = []
    for task in frozen:
        instance = by_id[task["task_id"]]
        if instance.goal != task["goal"] or instance.difficulty != task["difficulty"]:
            raise ValueError(f"upstream task drift for {task['task_id']}")
        world = World(instance)
        observation = world.call("check_eligibility", {"order_id": instance.order["order_id"]})
        if not observation.ok:
            raise ValueError(f"canonical eligibility failed for {instance.instance_id}")
        cases.append({
            "task_id": instance.instance_id,
            "difficulty": instance.difficulty,
            "expected_action": instance.expected.action,
            "expected_amount_eur": instance.expected.amount_eur,
            "canonical_eligible": bool(observation.data["eligible"]),
            "canonical_max_refund_eur": float(observation.data["max_refund_eur"]),
            "fallback_max_refund_eur": float(world.max_refund_eur),
        })
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--tasks", type=Path, default=ROOT / "data" / "tasks_label_quality_60.json")
    parser.add_argument("--task-manifest", type=Path, default=ROOT / "data" / "tasks_label_quality_60.manifest.json")
    parser.add_argument("--seeds", nargs="+", type=int, default=list(DEFAULT_SEEDS))
    parser.add_argument("--out", type=Path, required=True, help="NEW output directory")
    args = parser.parse_args()
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {args.out}")

    manifest = json.loads(args.task_manifest.read_text())
    task_hash = sha256(args.tasks)
    if task_hash != manifest["sha256"]:
        raise SystemExit(f"frozen task hash mismatch: {task_hash} != {manifest['sha256']}")
    cases = load_cases(args.upstream, args.tasks)
    if [c["task_id"] for c in cases] != TASK_IDS:
        raise SystemExit("label-quality test requires frozen IDs INS-00120..INS-00179")

    rows = []
    for case in cases:
        for seed in args.seeds:
            for regime, leakage in (("clean", None), ("targeted_common_mode", LEAKAGE)):
                fault_map = build_fault_map(case, seed, leakage)
                for condition in CONDITIONS:
                    for policy in ("random_k", "provenance_k"):
                        rows.append(run_episode(case, seed, regime, condition, policy, fault_map))

    args.out.mkdir(parents=True, exist_ok=True)
    raw_path = args.out / "raw.jsonl"
    with raw_path.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    run_manifest = {
        "study": "Preregistered label-quality (J) condition test",
        "protocol": "synthesis/Protocol: Confirmatory Test of the Label-Quality Condition.md v1.0",
        "task_sha256": task_hash,
        "upstream_commit": manifest["generator"]["source_commit"],
        "seeds": args.seeds,
        "conditions": {k: {"r": v[0], "phi": v[1], "k": v[2]} for k, v in CONDITIONS.items()},
        "leakage": LEAKAGE,
        "rows": len(rows),
        "raw_sha256": sha256(raw_path),
    }
    (args.out / "run_manifest.json").write_text(json.dumps(run_manifest, indent=2) + "\n")
    print(f"wrote {len(rows)} rows; raw sha256 {run_manifest['raw_sha256']}")


if __name__ == "__main__":
    main()
