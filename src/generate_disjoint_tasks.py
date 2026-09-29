#!/usr/bin/env python3
"""Generate the preregistered 30-task holdout from trajectory-judge."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260914)
    parser.add_argument("--offset", type=int, default=30)
    parser.add_argument("--count", type=int, default=30)
    parser.add_argument("--out", type=Path, default=ROOT / "data" / "tasks_disjoint_30.json")
    args = parser.parse_args()

    sys.path.insert(0, str(args.upstream / "src"))
    from trajectory_judge.env.world import World, generate_instances

    instances = generate_instances(args.offset + args.count, seed=args.seed)[args.offset :]
    fact_names = (
        "order_status",
        "customer_id",
        "sku",
        "total_eur",
        "days_since_purchase",
        "refundable",
        "refund_window_days",
        "restocking_fee_pct",
        "eligible",
        "max_refund_eur",
    )
    tasks: list[dict[str, Any]] = []
    for position, instance in enumerate(instances):
        eligibility = World(instance).call(
            "check_eligibility", {"order_id": instance.order["order_id"]}
        ).data
        facts = {
            "order_status": instance.order["status"],
            "customer_id": instance.customer["customer_id"],
            "sku": instance.order["sku"],
            "total_eur": instance.order["total_eur"],
            "days_since_purchase": instance.order["days_since_purchase"],
            "refundable": instance.policy["refundable"],
            "refund_window_days": instance.policy["refund_window_days"],
            "restocking_fee_pct": instance.policy["restocking_fee_pct"],
            "eligible": eligibility["eligible"],
            "max_refund_eur": eligibility["max_refund_eur"],
        }
        fact_key = fact_names[position % len(fact_names)]
        tasks.append(
            {
                "task_id": instance.instance_id,
                "difficulty": instance.difficulty,
                "goal": instance.goal,
                "fact_key": fact_key,
                "true_value": facts[fact_key],
                "generator_seed": args.seed,
                "source_commit": "d0ee54aadcaa69ea7368c2dcae71fa181cffa3f5",
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(tasks, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(tasks)} disjoint tasks to {args.out}")


if __name__ == "__main__":
    main()
