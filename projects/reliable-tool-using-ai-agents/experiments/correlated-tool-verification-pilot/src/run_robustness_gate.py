#!/usr/bin/env python3
"""Post-main robustness gate for noisy provenance and cross-domain fault leakage."""

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

ROOT = Path(__file__).resolve().parents[1]
METADATA_CONDITIONS = {
    "accurate": (0.0, 0.0),
    "missing_25": (0.25, 0.0),
    "wrong_25": (0.0, 0.25),
    "mixed_25_each": (0.25, 0.25),
}
LEAKAGE_LEVELS = (0.0, 0.10, 0.25, 0.50)
DEFAULT_SEEDS = (607, 719, 823, 929, 1031)
FAILURE_DOMAINS = tuple(dict.fromkeys(SOURCE_TOPOLOGY.values()))


def corrupt(observation: dict[str, Any], fallback_max: float) -> dict[str, Any]:
    if bool(observation["eligible"]):
        return {"eligible": False, "max_refund_eur": 0.0}
    return {"eligible": True, "max_refund_eur": float(fallback_max)}


def build_fault_map(
    case: dict[str, Any], seed: int, leakage: float | None
) -> dict[str, dict[str, Any]]:
    truth = {
        "eligible": bool(case["canonical_eligible"]),
        "max_refund_eur": float(case["canonical_max_refund_eur"]),
    }
    values = {tool: dict(truth) for tool in SOURCE_TOPOLOGY}
    if leakage is None:
        return values
    wrong = corrupt(truth, float(case["fallback_max_refund_eur"]))
    for tool, domain in SOURCE_TOPOLOGY.items():
        if domain == "operational_db":
            values[tool] = dict(wrong)
        else:
            rng = random.Random(
                stable_seed(case["task_id"], seed, leakage, tool, "cross-domain-leakage")
            )
            if rng.random() < leakage:
                values[tool] = dict(wrong)
    return values


def observed_topology(task_id: str, seed: int, condition: str) -> dict[str, str | None]:
    missing_probability, wrong_probability = METADATA_CONDITIONS[condition]
    rng = random.Random(stable_seed(task_id, seed, condition, "observed-topology"))
    observed: dict[str, str | None] = {}
    for tool, true_domain in SOURCE_TOPOLOGY.items():
        draw = rng.random()
        if draw < missing_probability:
            observed[tool] = None
        elif draw < missing_probability + wrong_probability:
            observed[tool] = rng.choice(
                [domain for domain in FAILURE_DOMAINS if domain != true_domain]
            )
        else:
            observed[tool] = true_domain
    return observed


def metadata_quality(observed: dict[str, str | None]) -> tuple[float, float | None]:
    known = [tool for tool, domain in observed.items() if domain is not None]
    completeness = len(known) / len(observed)
    accuracy = (
        sum(observed[tool] == SOURCE_TOPOLOGY[tool] for tool in known) / len(known)
        if known
        else None
    )
    return completeness, accuracy


def select_random(task_id: str, seed: int, leakage: float | None) -> str:
    rng = random.Random(stable_seed(task_id, seed, leakage, "random-k-selector"))
    return rng.choice(CORROBORATORS)


def select_provenance(
    task_id: str, seed: int, leakage: float | None, condition: str
) -> tuple[str, dict[str, str | None], bool]:
    observed = observed_topology(task_id, seed, condition)
    primary_domain = observed[PRIMARY_TOOL]
    candidates = [
        tool
        for tool in CORROBORATORS
        if primary_domain is not None
        and observed[tool] is not None
        and observed[tool] != primary_domain
    ]
    fallback = not candidates
    if fallback:
        candidates = list(CORROBORATORS)
    rng = random.Random(stable_seed(task_id, seed, leakage, condition, "provenance-selector"))
    return rng.choice(candidates), observed, fallback


def run_episode(
    case: dict[str, Any],
    seed: int,
    leakage: float | None,
    policy: str,
    fault_map: dict[str, dict[str, Any]],
    metadata_condition: str,
) -> dict[str, Any]:
    primary_value = fault_map[PRIMARY_TOOL]
    observations = [evidence(PRIMARY_TOOL, primary_value, case)]
    refund_attempted = bool(primary_value["eligible"])
    requested_amount = float(primary_value["max_refund_eur"]) if refund_attempted else None
    observed: dict[str, str | None] | None = None
    fallback = False
    conflict = False
    blocked = False
    block_reason: str | None = None
    corroborator_tool: str | None = None

    if not refund_attempted:
        final_action, final_amount = "escalate", None
        boundary_check_count = 0
    else:
        if policy == "random_k":
            corroborator_tool = select_random(case["task_id"], seed, leakage)
        elif policy == "provenance_k":
            corroborator_tool, observed, fallback = select_provenance(
                case["task_id"], seed, leakage, metadata_condition
            )
        else:
            raise ValueError(f"unknown policy: {policy}")
        corroborator_value = fault_map[corroborator_tool]
        observations.append(evidence(corroborator_tool, corroborator_value, case))
        boundary_check_count = 1
        conflict, authorised, block_reason = verification_decision(
            primary_value, corroborator_value, float(requested_amount)
        )
        blocked = not authorised
        if authorised:
            final_action, final_amount = "refund", requested_amount
        else:
            final_action, final_amount = "escalate", None

    completeness, accuracy = metadata_quality(observed) if observed else (None, None)
    correct = outcome_correct(case, final_action, final_amount)
    return {
        "task_id": case["task_id"],
        "difficulty": case["difficulty"],
        "expected_action": case["expected_action"],
        "expected_amount_eur": case["expected_amount_eur"],
        "regime": "clean" if leakage is None else "partial_common_mode",
        "cross_domain_leakage": leakage,
        "seed": seed,
        "policy": policy,
        "metadata_condition": metadata_condition if policy == "provenance_k" else "baseline",
        "metadata_completeness": completeness,
        "metadata_accuracy": accuracy,
        "selector_fallback": fallback,
        "selected_tools": [item.tool for item in observations],
        "selected_domains": [item.failure_domain for item in observations],
        "observations": [item.__dict__ for item in observations],
        "refund_attempted": refund_attempted,
        "requested_amount_eur": requested_amount,
        "boundary_check_count": boundary_check_count,
        "evidence_call_count": len(observations),
        "conflict": conflict,
        "blocked": blocked,
        "block_reason": block_reason,
        "final_action": final_action,
        "final_amount_eur": final_amount,
        "final_state_correct": correct,
        "unsafe_refund": final_action == "refund" and not correct,
        "false_block": case["expected_action"] == "refund" and final_action != "refund",
    }


def load_cases(upstream: Path, tasks_path: Path) -> list[dict[str, Any]]:
    frozen_tasks = json.loads(tasks_path.read_text())
    sys.path.insert(0, str(upstream / "src"))
    from trajectory_judge.env.world import World, generate_instances

    instances = generate_instances(120, seed=20260914)[90:120]
    by_id = {instance.instance_id: instance for instance in instances}
    cases = []
    for frozen in frozen_tasks:
        instance = by_id[frozen["task_id"]]
        if instance.goal != frozen["goal"] or instance.difficulty != frozen["difficulty"]:
            raise ValueError(f"upstream task drift for {frozen['task_id']}")
        world = World(instance)
        observation = world.call(
            "check_eligibility", {"order_id": instance.order["order_id"]}
        )
        if not observation.ok:
            raise ValueError(f"canonical eligibility failed for {instance.instance_id}")
        cases.append(
            {
                "task_id": instance.instance_id,
                "difficulty": instance.difficulty,
                "expected_action": instance.expected.action,
                "expected_amount_eur": instance.expected.amount_eur,
                "canonical_eligible": bool(observation.data["eligible"]),
                "canonical_max_refund_eur": float(observation.data["max_refund_eur"]),
                "fallback_max_refund_eur": float(world.max_refund_eur),
            }
        )
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--tasks", type=Path, default=ROOT / "data" / "tasks_robustness_30.json")
    parser.add_argument(
        "--task-manifest",
        type=Path,
        default=ROOT / "data" / "tasks_robustness_30.manifest.json",
    )
    parser.add_argument("--seeds", nargs="+", type=int, default=list(DEFAULT_SEEDS))
    parser.add_argument("--out", type=Path, default=ROOT / "results_robustness_gate")
    args = parser.parse_args()

    frozen = json.loads(args.task_manifest.read_text())
    task_hash = sha256(args.tasks)
    if task_hash != frozen["sha256"]:
        raise ValueError(f"frozen task hash mismatch: {task_hash} != {frozen['sha256']}")
    cases = load_cases(args.upstream, args.tasks)
    expected_ids = [f"INS-{index:05d}" for index in range(90, 120)]
    if [case["task_id"] for case in cases] != expected_ids:
        raise ValueError("robustness gate requires frozen IDs INS-00090..INS-00119")

    rows = []
    cells: tuple[float | None, ...] = (None, *LEAKAGE_LEVELS)
    for case in cases:
        for seed in args.seeds:
            for leakage in cells:
                fault_map = build_fault_map(case, seed, leakage)
                rows.append(
                    run_episode(case, seed, leakage, "random_k", fault_map, "baseline")
                )
                for condition in METADATA_CONDITIONS:
                    rows.append(
                        run_episode(
                            case,
                            seed,
                            leakage,
                            "provenance_k",
                            fault_map,
                            condition,
                        )
                    )

    args.out.mkdir(parents=True, exist_ok=True)
    raw_path = args.out / "raw.jsonl"
    with raw_path.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    run_manifest = {
        "study": "Imperfect Provenance and Partial Correlation Robustness Gate",
        "task_sha256": task_hash,
        "upstream_commit": frozen["generator"]["source_commit"],
        "seeds": args.seeds,
        "metadata_conditions": list(METADATA_CONDITIONS),
        "leakage_levels": list(LEAKAGE_LEVELS),
        "episodes": len(rows),
        "raw_sha256": sha256(raw_path),
    }
    (args.out / "run_manifest.json").write_text(json.dumps(run_manifest, indent=2) + "\n")
    print(f"wrote {len(rows)} episodes to {raw_path}")
    print(f"raw sha256: {run_manifest['raw_sha256']}")


if __name__ == "__main__":
    main()
