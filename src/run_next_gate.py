#!/usr/bin/env python3
"""Holdout experiment with incomplete and incorrect provenance metadata."""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from run_pilot import (
    FAILURE_DOMAINS,
    SOURCE_TOPOLOGY,
    TOOLS,
    Observation,
    build_fault_map,
    stable_seed,
)

ROOT = Path(__file__).resolve().parents[1]
PRIMARY_TOOL = "order_api"
BASE_POLICIES = ("single", "fixed_k", "random_k")
METADATA_CONDITIONS = {
    "accurate": (0.0, 0.0),
    "missing_25": (0.25, 0.0),
    "wrong_25": (0.0, 0.25),
    "mixed_25_each": (0.25, 0.25),
    "wrong_50": (0.0, 0.50),
}


@dataclass(frozen=True)
class GateEpisode:
    task_id: str
    difficulty: str
    fact_key: str
    regime: str
    seed: int
    policy: str
    metadata_condition: str
    metadata_completeness: float
    metadata_accuracy: float | None
    selected_tools: tuple[str, ...]
    selected_true_domains: tuple[str, ...]
    true_domain_diversity: int
    observations: tuple[Observation, ...]
    alarm: bool
    accepted: bool
    accepted_value: Any | None
    accepted_correct: bool
    unsafe_accept: bool
    selected_fault: bool
    extra_tool_calls: int


def observed_topology(task_id: str, seed: int, condition: str) -> dict[str, str | None]:
    missing_p, wrong_p = METADATA_CONDITIONS[condition]
    rng = random.Random(stable_seed(task_id, seed, condition, "observed-topology"))
    observed: dict[str, str | None] = {}
    for tool, true_domain in SOURCE_TOPOLOGY.items():
        draw = rng.random()
        if draw < missing_p:
            observed[tool] = None
        elif draw < missing_p + wrong_p:
            observed[tool] = rng.choice([d for d in FAILURE_DOMAINS if d != true_domain])
        else:
            observed[tool] = true_domain
    return observed


def metadata_quality(observed: dict[str, str | None]) -> tuple[float, float | None]:
    known = [tool for tool, domain in observed.items() if domain is not None]
    completeness = len(known) / len(SOURCE_TOPOLOGY)
    accuracy = (
        sum(observed[tool] == SOURCE_TOPOLOGY[tool] for tool in known) / len(known)
        if known
        else None
    )
    return completeness, accuracy


def select_tools(
    policy: str,
    task_id: str,
    regime: str,
    seed: int,
    condition: str = "baseline",
) -> tuple[tuple[str, ...], dict[str, str | None]]:
    if policy == "single":
        return (PRIMARY_TOOL,), dict(SOURCE_TOPOLOGY)
    if policy == "fixed_k":
        return (PRIMARY_TOOL, "order_search"), dict(SOURCE_TOPOLOGY)
    if policy == "random_k":
        rng = random.Random(stable_seed(task_id, regime, seed, policy))
        candidates = [tool for tool in TOOLS if tool != PRIMARY_TOOL]
        return (PRIMARY_TOOL, rng.choice(candidates)), dict(SOURCE_TOPOLOGY)
    if policy != "provenance_aware":
        raise ValueError(f"unknown policy: {policy}")

    observed = observed_topology(task_id, seed, condition)
    rng = random.Random(stable_seed(task_id, regime, seed, condition, "selector"))
    primary_domain = observed[PRIMARY_TOOL]
    candidates = [
        tool
        for tool in TOOLS
        if tool != PRIMARY_TOOL
        and primary_domain is not None
        and observed[tool] is not None
        and observed[tool] != primary_domain
    ]
    if not candidates:
        candidates = [tool for tool in TOOLS if tool != PRIMARY_TOOL]
    return (PRIMARY_TOOL, rng.choice(candidates)), observed


def run_episode(
    task: dict[str, Any],
    regime: str,
    seed: int,
    policy: str,
    condition: str,
    fault_map: dict[str, Any],
) -> GateEpisode:
    selected, observed = select_tools(policy, task["task_id"], regime, seed, condition)
    completeness, accuracy = metadata_quality(observed)
    truth = task["true_value"]
    observations = tuple(
        Observation(
            tool=tool,
            failure_domain=SOURCE_TOPOLOGY[tool],
            value=fault_map[tool],
            corrupted=fault_map[tool] != truth,
        )
        for tool in selected
    )
    values = [item.value for item in observations]
    alarm = len(values) > 1 and any(value != values[0] for value in values[1:])
    accepted = not alarm
    accepted_value = values[0] if accepted else None
    true_domains = tuple(SOURCE_TOPOLOGY[tool] for tool in selected)
    return GateEpisode(
        task_id=task["task_id"],
        difficulty=task["difficulty"],
        fact_key=task["fact_key"],
        regime=regime,
        seed=seed,
        policy=policy,
        metadata_condition=condition,
        metadata_completeness=completeness,
        metadata_accuracy=accuracy,
        selected_tools=selected,
        selected_true_domains=true_domains,
        true_domain_diversity=len(set(true_domains)),
        observations=observations,
        alarm=alarm,
        accepted=accepted,
        accepted_value=accepted_value,
        accepted_correct=accepted and accepted_value == truth,
        unsafe_accept=accepted and accepted_value != truth,
        selected_fault=any(item.corrupted for item in observations),
        extra_tool_calls=max(0, len(selected) - 1),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=[101, 211, 307, 401, 503])
    parser.add_argument("--independent-probability", type=float, default=0.25)
    parser.add_argument("--tasks", type=Path, default=ROOT / "data" / "tasks_disjoint_30.json")
    parser.add_argument("--out", type=Path, default=ROOT / "results_next_gate")
    args = parser.parse_args()

    tasks = json.loads(args.tasks.read_text())
    episodes: list[GateEpisode] = []
    for task in tasks:
        for regime in ("clean", "independent", "common_mode"):
            for seed in args.seeds:
                fault_map = build_fault_map(task, regime, seed, args.independent_probability)
                for policy in BASE_POLICIES:
                    episodes.append(run_episode(task, regime, seed, policy, "baseline", fault_map))
                for condition in METADATA_CONDITIONS:
                    episodes.append(
                        run_episode(task, regime, seed, "provenance_aware", condition, fault_map)
                    )

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "raw.jsonl").open("w") as handle:
        for episode in episodes:
            handle.write(json.dumps(asdict(episode), ensure_ascii=False) + "\n")
    print(f"wrote {len(episodes)} holdout episodes to {args.out}")


if __name__ == "__main__":
    main()
