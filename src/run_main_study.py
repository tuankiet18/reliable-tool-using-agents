#!/usr/bin/env python3
"""Preregistered deterministic action-boundary verification main study."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRIMARY_TOOL = "check_eligibility"
SOURCE_TOPOLOGY = {
    PRIMARY_TOOL: "operational_db",
    "check_eligibility_search": "operational_db",
    "check_eligibility_analytics": "analytics_replica",
    "check_eligibility_audit": "audit_ledger",
}
CORROBORATORS = tuple(tool for tool in SOURCE_TOPOLOGY if tool != PRIMARY_TOOL)
POLICIES = ("single_source", "random_k", "provenance_k")
REGIMES = ("clean", "independent", "targeted_common_mode")
DEFAULT_SEEDS = (101, 211, 307, 401, 503)


@dataclass(frozen=True)
class Evidence:
    tool: str
    failure_domain: str
    eligible: bool
    max_refund_eur: float
    corrupted: bool


def stable_seed(*parts: object) -> int:
    payload = "|".join(map(str, parts)).encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def corrupt(observation: dict[str, Any], fallback_max: float) -> dict[str, Any]:
    if bool(observation["eligible"]):
        return {"eligible": False, "max_refund_eur": 0.0}
    return {"eligible": True, "max_refund_eur": float(fallback_max)}


def build_fault_map(
    case: dict[str, Any], regime: str, seed: int, independent_probability: float
) -> dict[str, dict[str, Any]]:
    truth = {
        "eligible": bool(case["canonical_eligible"]),
        "max_refund_eur": float(case["canonical_max_refund_eur"]),
    }
    values = {tool: dict(truth) for tool in SOURCE_TOPOLOGY}
    wrong = corrupt(truth, float(case["fallback_max_refund_eur"]))
    if regime == "clean":
        return values
    if regime == "targeted_common_mode":
        for tool, domain in SOURCE_TOPOLOGY.items():
            if domain == "operational_db":
                values[tool] = dict(wrong)
        return values
    if regime == "independent":
        rng = random.Random(stable_seed(case["task_id"], regime, seed, "fault-map"))
        for tool in SOURCE_TOPOLOGY:
            if rng.random() < independent_probability:
                values[tool] = dict(wrong)
        return values
    raise ValueError(f"unknown regime: {regime}")


def select_corroborator(policy: str, task_id: str, regime: str, seed: int) -> str:
    rng = random.Random(stable_seed(task_id, regime, seed, policy, "selector"))
    if policy == "random_k":
        return rng.choice(CORROBORATORS)
    if policy == "provenance_k":
        independent = [
            tool
            for tool in CORROBORATORS
            if SOURCE_TOPOLOGY[tool] != SOURCE_TOPOLOGY[PRIMARY_TOOL]
        ]
        return rng.choice(independent)
    raise ValueError(f"policy has no corroborator: {policy}")


def verification_decision(
    primary: dict[str, Any], corroborator: dict[str, Any], requested_amount: float
) -> tuple[bool, bool, str]:
    conflict = any(
        primary[key] != corroborator[key] for key in ("eligible", "max_refund_eur")
    )
    if conflict:
        return True, False, "conflict"
    if not bool(primary["eligible"]):
        return False, False, "not_eligible"
    if abs(float(primary["max_refund_eur"]) - requested_amount) > 1e-6:
        return False, False, "amount_mismatch"
    return False, True, "authorised"


def evidence(tool: str, value: dict[str, Any], case: dict[str, Any]) -> Evidence:
    truth = (
        bool(case["canonical_eligible"]),
        float(case["canonical_max_refund_eur"]),
    )
    observed = (bool(value["eligible"]), float(value["max_refund_eur"]))
    return Evidence(
        tool=tool,
        failure_domain=SOURCE_TOPOLOGY[tool],
        eligible=observed[0],
        max_refund_eur=observed[1],
        corrupted=observed != truth,
    )


def outcome_correct(case: dict[str, Any], action: str, amount: float | None) -> bool:
    if action != case["expected_action"]:
        return False
    expected_amount = case["expected_amount_eur"]
    if action != "refund":
        return True
    return expected_amount is not None and amount is not None and abs(amount - expected_amount) < 1e-6


def run_episode(
    case: dict[str, Any],
    regime: str,
    seed: int,
    policy: str,
    fault_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    primary_value = fault_map[PRIMARY_TOOL]
    observations = [evidence(PRIMARY_TOOL, primary_value, case)]
    refund_attempted = bool(primary_value["eligible"])
    requested_amount = float(primary_value["max_refund_eur"]) if refund_attempted else None
    boundary_check_count = 0
    conflict = False
    blocked = False
    block_reason: str | None = None

    if not refund_attempted:
        final_action, final_amount = "escalate", None
    elif policy == "single_source":
        final_action, final_amount = "refund", requested_amount
    else:
        corroborator_tool = select_corroborator(policy, case["task_id"], regime, seed)
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

    correct = outcome_correct(case, final_action, final_amount)
    unsafe_refund = final_action == "refund" and not correct
    false_block = case["expected_action"] == "refund" and final_action != "refund"
    return {
        "task_id": case["task_id"],
        "difficulty": case["difficulty"],
        "expected_action": case["expected_action"],
        "expected_amount_eur": case["expected_amount_eur"],
        "canonical_eligible": case["canonical_eligible"],
        "canonical_max_refund_eur": case["canonical_max_refund_eur"],
        "regime": regime,
        "seed": seed,
        "policy": policy,
        "observations": [asdict(item) for item in observations],
        "selected_tools": [item.tool for item in observations],
        "selected_domains": [item.failure_domain for item in observations],
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
        "unsafe_refund": unsafe_refund,
        "false_block": false_block,
    }


def load_cases(upstream: Path, tasks_path: Path) -> list[dict[str, Any]]:
    manifest_tasks = json.loads(tasks_path.read_text())
    sys.path.insert(0, str(upstream / "src"))
    from trajectory_judge.env.world import World, generate_instances

    instances = generate_instances(90, seed=20260914)[60:90]
    by_id = {instance.instance_id: instance for instance in instances}
    cases = []
    for frozen in manifest_tasks:
        instance = by_id[frozen["task_id"]]
        if instance.difficulty != frozen["difficulty"] or instance.goal != frozen["goal"]:
            raise ValueError(f"upstream task drift for {frozen['task_id']}")
        world = World(instance)
        eligibility = world.call(
            "check_eligibility", {"order_id": instance.order["order_id"]}
        )
        if not eligibility.ok:
            raise ValueError(f"canonical eligibility failed for {frozen['task_id']}")
        cases.append(
            {
                "task_id": instance.instance_id,
                "difficulty": instance.difficulty,
                "expected_action": instance.expected.action,
                "expected_amount_eur": instance.expected.amount_eur,
                "canonical_eligible": bool(eligibility.data["eligible"]),
                "canonical_max_refund_eur": float(eligibility.data["max_refund_eur"]),
                "fallback_max_refund_eur": float(world.max_refund_eur),
            }
        )
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--tasks", type=Path, default=ROOT / "data" / "tasks_main_30.json")
    parser.add_argument(
        "--task-manifest",
        type=Path,
        default=ROOT / "data" / "tasks_main_30.manifest.json",
    )
    parser.add_argument("--seeds", nargs="+", type=int, default=list(DEFAULT_SEEDS))
    parser.add_argument("--independent-probability", type=float, default=0.25)
    parser.add_argument("--out", type=Path, default=ROOT / "results_main_study")
    args = parser.parse_args()

    frozen = json.loads(args.task_manifest.read_text())
    actual_hash = sha256(args.tasks)
    if actual_hash != frozen["sha256"]:
        raise ValueError(f"frozen task hash mismatch: {actual_hash} != {frozen['sha256']}")
    cases = load_cases(args.upstream, args.tasks)
    if len(cases) != 30 or any(int(case["task_id"].split("-")[1]) < 60 for case in cases):
        raise ValueError("main study requires exactly 30 fresh task IDs starting at INS-00060")

    rows = []
    for case in cases:
        for regime in REGIMES:
            for seed in args.seeds:
                fault_map = build_fault_map(case, regime, seed, args.independent_probability)
                for policy in POLICIES:
                    rows.append(run_episode(case, regime, seed, policy, fault_map))

    args.out.mkdir(parents=True, exist_ok=True)
    raw_path = args.out / "raw.jsonl"
    with raw_path.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    run_manifest = {
        "study": "Action-Boundary Provenance Verification Main Study",
        "tasks_sha256": actual_hash,
        "upstream_commit": frozen["generator"]["source_commit"],
        "seeds": args.seeds,
        "regimes": list(REGIMES),
        "policies": list(POLICIES),
        "independent_probability": args.independent_probability,
        "episodes": len(rows),
        "raw_sha256": sha256(raw_path),
    }
    (args.out / "run_manifest.json").write_text(json.dumps(run_manifest, indent=2) + "\n")
    print(f"wrote {len(rows)} episodes to {raw_path}")
    print(f"raw sha256: {run_manifest['raw_sha256']}")


if __name__ == "__main__":
    main()
