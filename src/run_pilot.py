#!/usr/bin/env python3
"""Controlled pilot for verification under independent and common-mode tool faults."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SOURCE_TOPOLOGY = {
    "order_api": "operational_db",
    "order_search": "operational_db",
    "analytics_dashboard": "analytics_replica",
    "warehouse_query": "analytics_replica",
    "audit_log": "audit_ledger",
}
TOOLS = tuple(SOURCE_TOPOLOGY)
FAILURE_DOMAINS = tuple(dict.fromkeys(SOURCE_TOPOLOGY.values()))
REGIMES = ("clean", "independent", "common_mode")
POLICIES = ("single", "fixed_k", "random_k", "provenance_aware")


@dataclass(frozen=True)
class Observation:
    tool: str
    failure_domain: str
    value: Any
    corrupted: bool


@dataclass(frozen=True)
class Episode:
    task_id: str
    difficulty: str
    fact_key: str
    regime: str
    seed: int
    policy: str
    selected_tools: tuple[str, ...]
    observations: tuple[Observation, ...]
    alarm: bool
    accepted: bool
    accepted_value: Any | None
    accepted_correct: bool
    unsafe_accept: bool
    selected_fault: bool
    extra_tool_calls: int


def stable_seed(*parts: object) -> int:
    payload = "|".join(map(str, parts)).encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def wrong_value(task: dict[str, Any], rng: random.Random) -> Any:
    """Return a schema-valid, plausible alternative to the canonical fact."""
    key, value = task["fact_key"], task["true_value"]
    if isinstance(value, bool):
        return not value
    if isinstance(value, (int, float)):
        alternatives = {
            "total_eur": [round(value * 0.9, 2), round(value * 1.1, 2)],
            "days_since_purchase": [max(0, value - 7), value + 7],
            "refund_window_days": [14, 60] if value == 30 else [30, 60],
            "restocking_fee_pct": [0.0, 10.0, 15.0],
            "max_refund_eur": [19.99, 49.99],
        }.get(key, [value + 1, value + 2])
        candidates = [item for item in alternatives if item != value]
        return rng.choice(candidates)
    alternatives = {
        "order_status": ["pending", "refunded"],
        "customer_id": ["CUS-9001", "CUS-7001"],
        "sku": ["SKU-CHAIR-42", "SKU-PHONE-88"],
    }.get(key, [f"alternative-{value}"])
    candidates = [item for item in alternatives if item != value]
    return rng.choice(candidates)


def build_fault_map(task: dict[str, Any], regime: str, seed: int, p: float) -> dict[str, Any]:
    """Create one fault map reused by every policy in a paired comparison."""
    rng = random.Random(stable_seed(task["task_id"], regime, seed, "fault-map"))
    truth = task["true_value"]
    values = {tool: truth for tool in TOOLS}
    if regime == "clean":
        return values
    if regime == "common_mode":
        failed_domain = rng.choice(FAILURE_DOMAINS)
        shared_wrong = wrong_value(task, rng)
        for tool, domain in SOURCE_TOPOLOGY.items():
            if domain == failed_domain:
                values[tool] = shared_wrong
        return values
    if regime == "independent":
        for tool in TOOLS:
            if rng.random() < p:
                values[tool] = wrong_value(task, rng)
        return values
    raise ValueError(f"unknown regime: {regime}")


def select_tools(policy: str, task_id: str, regime: str, seed: int) -> tuple[str, ...]:
    if policy == "single":
        return (TOOLS[0],)
    if policy == "fixed_k":
        return (TOOLS[0], TOOLS[1])
    if policy == "random_k":
        rng = random.Random(stable_seed(task_id, regime, seed, policy))
        return tuple(rng.sample(TOOLS, 2))
    if policy == "provenance_aware":
        # Same K=2 budget as fixed/random; select different known failure domains.
        return ("order_api", "audit_log")
    raise ValueError(f"unknown policy: {policy}")


def run_episode(
    task: dict[str, Any], regime: str, seed: int, policy: str, fault_map: dict[str, Any]
) -> Episode:
    selected = select_tools(policy, task["task_id"], regime, seed)
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
    accepted_correct = accepted and accepted_value == truth
    unsafe_accept = accepted and accepted_value != truth
    return Episode(
        task_id=task["task_id"],
        difficulty=task["difficulty"],
        fact_key=task["fact_key"],
        regime=regime,
        seed=seed,
        policy=policy,
        selected_tools=selected,
        observations=observations,
        alarm=alarm,
        accepted=accepted,
        accepted_value=accepted_value,
        accepted_correct=accepted_correct,
        unsafe_accept=unsafe_accept,
        selected_fault=any(item.corrupted for item in observations),
        extra_tool_calls=max(0, len(selected) - 1),
    )


def summarize(episodes: list[Episode]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[Episode]] = defaultdict(list)
    for episode in episodes:
        groups[(episode.regime, episode.policy)].append(episode)
    rows = []
    for (regime, policy), group in sorted(groups.items()):
        n = len(group)
        fault_cases = sum(item.selected_fault for item in group)
        alarms = sum(item.alarm for item in group)
        detected_faults = sum(item.alarm and item.selected_fault for item in group)
        unsafe = sum(item.unsafe_accept for item in group)
        correct = sum(item.accepted_correct for item in group)
        accepted = sum(item.accepted for item in group)
        extra = sum(item.extra_tool_calls for item in group)
        rows.append(
            {
                "regime": regime,
                "policy": policy,
                "episodes": n,
                "selected_fault_cases": fault_cases,
                "alarm_rate": alarms / n,
                "detection_recall": detected_faults / fault_cases if fault_cases else None,
                "unsafe_accept_rate": unsafe / n,
                "unsafe_accept_given_selected_fault": unsafe / fault_cases if fault_cases else None,
                "correct_accept_rate": correct / n,
                "selective_accuracy": correct / accepted if accepted else None,
                "abstention_rate": alarms / n,
                "mean_extra_tool_calls": extra / n,
                "detections_per_extra_call": detected_faults / extra if extra else None,
            }
        )
    return rows


def fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def markdown_summary(
    rows: list[dict[str, Any]], episodes: list[Episode], seeds: list[int], p: float
) -> str:
    columns = [
        "regime",
        "policy",
        "episodes",
        "selected_fault_cases",
        "detection_recall",
        "unsafe_accept_rate",
        "correct_accept_rate",
        "selective_accuracy",
        "abstention_rate",
        "mean_extra_tool_calls",
    ]
    lines = [
        "# Pilot summary",
        "",
        f"Seeds: `{seeds}`; independent corruption probability per tool: `{p}`.",
        "",
        "| " + " | ".join(columns) + " |",
        "|" + "|".join(["---"] * len(columns)) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row[key]) for key in columns) + " |")
    lines.extend(["", "## Safety–utility sensitivity under common-mode faults", ""])
    lines.append("Expected loss = `unsafe_accept_rate + abstention_cost × abstention_rate`; wrong accept cost được chuẩn hóa bằng `1`.")
    lines.extend(["", "| abstention cost | fixed_k | random_k | provenance_aware | best |", "|---:|---:|---:|---:|---|"])
    common = {row["policy"]: row for row in rows if row["regime"] == "common_mode"}
    for cost in (0.0, 0.1, 0.25, 0.5, 0.75, 1.0):
        losses = {
            policy: common[policy]["unsafe_accept_rate"]
            + cost * common[policy]["abstention_rate"]
            for policy in ("fixed_k", "random_k", "provenance_aware")
        }
        best = min(losses, key=losses.get)
        lines.append(
            f"| {cost:.2f} | {losses['fixed_k']:.3f} | {losses['random_k']:.3f} | "
            f"{losses['provenance_aware']:.3f} | {best} |"
        )
    lines.extend(["", "## Common-mode effect by task stratum", ""])
    lines.extend(["| difficulty | episodes/policy | fixed unsafe | provenance unsafe | provenance alarms |", "|---|---:|---:|---:|---:|"])
    strata = sorted({item.difficulty for item in episodes})
    for difficulty in strata:
        fixed = [item for item in episodes if item.regime == "common_mode" and item.policy == "fixed_k" and item.difficulty == difficulty]
        provenance = [item for item in episodes if item.regime == "common_mode" and item.policy == "provenance_aware" and item.difficulty == difficulty]
        lines.append(
            f"| {difficulty} | {len(fixed)} | {sum(x.unsafe_accept for x in fixed)} | "
            f"{sum(x.unsafe_accept for x in provenance)} | {sum(x.alarm for x in provenance)} |"
        )
    lines.extend(
        [
            "",
            "`detection_recall` chỉ dùng các episode nơi ít nhất một selected tool bị corrupt.",
            "`unsafe_accept_rate` là tỷ lệ accept một giá trị sai trên toàn bộ episode.",
            "`selective_accuracy` chỉ chấm các episode policy đã accept, nên phải đọc cùng coverage/abstention.",
            "Kết quả này chỉ kiểm tra fault-model mechanics; chưa phải live-agent evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=[11, 23, 37, 51, 79])
    parser.add_argument("--independent-probability", type=float, default=0.25)
    parser.add_argument("--out", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    tasks = json.loads((ROOT / "data" / "tasks.json").read_text())
    episodes: list[Episode] = []
    for task in tasks:
        for regime in REGIMES:
            for seed in args.seeds:
                fault_map = build_fault_map(task, regime, seed, args.independent_probability)
                for policy in POLICIES:
                    episodes.append(run_episode(task, regime, seed, policy, fault_map))

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "raw.jsonl").open("w") as handle:
        for episode in episodes:
            handle.write(json.dumps(asdict(episode), ensure_ascii=False) + "\n")
    rows = summarize(episodes)
    (args.out / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")
    (args.out / "summary.md").write_text(
        markdown_summary(rows, episodes, args.seeds, args.independent_probability)
    )
    print(f"wrote {len(episodes)} paired episodes to {args.out}")


if __name__ == "__main__":
    main()
