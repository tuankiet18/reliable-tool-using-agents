#!/usr/bin/env python3
"""Small local-model-in-loop check of the verification decision.

This is deliberately reported as a partial live gate: policy code selects the tools, while the
model receives the observations and decides ACCEPT versus ABSTAIN. It is not a full end-to-end
tool-using agent benchmark.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def ask_model(
    endpoint: str, model: str, prompt: str, seed: int, enum_order: list[str]
) -> tuple[str | None, float, str]:
    schema = {
        "type": "object",
        "properties": {"decision": {"type": "string", "enum": enum_order}},
        "required": ["decision"],
        "additionalProperties": False,
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a runtime verifier. Two tools report the same fact. ACCEPT only "
                    "when their values agree exactly; otherwise ABSTAIN. Return the required JSON."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "seed": seed,
        "max_tokens": 20,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "verification_decision", "strict": True, "schema": schema},
        },
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read())
        text = body["choices"][0]["message"]["content"]
        parsed = json.loads(text)
        decision = parsed.get("decision")
        if decision not in {"ACCEPT", "ABSTAIN"}:
            decision = None
        return decision, time.perf_counter() - started, text
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, TypeError) as exc:
        return None, time.perf_counter() - started, f"{type(exc).__name__}: {exc}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", default="http://127.0.0.1:8089/v1/chat/completions")
    parser.add_argument("--model", default="qwen2.5-0.5b-instruct-q5_0.gguf")
    parser.add_argument("--task-count", type=int, default=6)
    parser.add_argument("--seeds", nargs="+", type=int, default=[101, 211])
    parser.add_argument("--out", type=Path, default=ROOT / "results_live_subset")
    args = parser.parse_args()

    tasks = {item["task_id"]: item for item in json.loads((ROOT / "data" / "tasks_disjoint_30.json").read_text())}
    selected_task_ids = list(tasks)[: args.task_count]
    source_rows = [
        json.loads(line) for line in (ROOT / "results_next_gate" / "raw.jsonl").read_text().splitlines()
    ]
    selected_rows = [
        row
        for row in source_rows
        if row["task_id"] in selected_task_ids
        and row["seed"] in args.seeds
        and (
            row["policy"] == "random_k"
            or (row["policy"] == "provenance_aware" and row["metadata_condition"] == "accurate")
        )
    ]

    results = []
    schema_orders = {
        "accept_first": ["ACCEPT", "ABSTAIN"],
        "abstain_first": ["ABSTAIN", "ACCEPT"],
    }
    for row in selected_rows:
        for schema_order, enum_order in schema_orders.items():
            observations = row["observations"]
            prompt = (
                f"Task: {tasks[row['task_id']]['goal']}\n"
                f"Fact: {row['fact_key']}\n"
                f"Observation 1: tool={observations[0]['tool']}, source={observations[0]['failure_domain']}, "
                f"value={json.dumps(observations[0]['value'])}\n"
                f"Observation 2: tool={observations[1]['tool']}, source={observations[1]['failure_domain']}, "
                f"value={json.dumps(observations[1]['value'])}"
            )
            decision, latency, raw_response = ask_model(
                args.endpoint, args.model, prompt, row["seed"], enum_order
            )
            ideal = "ABSTAIN" if row["alarm"] else "ACCEPT"
            accepted = decision == "ACCEPT"
            truth = tasks[row["task_id"]]["true_value"]
            primary_value = observations[0]["value"]
            results.append(
                {
                "task_id": row["task_id"],
                "difficulty": row["difficulty"],
                "regime": row["regime"],
                "seed": row["seed"],
                "policy": row["policy"],
                "metadata_condition": row["metadata_condition"],
                "schema_order": schema_order,
                "selected_tools": row["selected_tools"],
                "observations": observations,
                "ideal_decision": ideal,
                "model_decision": decision,
                "decision_adherent": decision == ideal,
                "parse_success": decision is not None,
                "unsafe_accept": accepted and primary_value != truth,
                "correct_accept": accepted and primary_value == truth,
                "abstain": decision == "ABSTAIN",
                "latency_s": latency,
                "raw_response": raw_response,
                }
            )

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "raw.jsonl").open("w") as handle:
        for row in results:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in results:
        groups[(row["schema_order"], row["regime"], row["policy"])].append(row)
    summary = []
    for (schema_order, regime, policy), group in sorted(groups.items()):
        summary.append(
            {
                "schema_order": schema_order,
                "regime": regime,
                "policy": policy,
                "episodes": len(group),
                "parse_success_rate": sum(x["parse_success"] for x in group) / len(group),
                "decision_adherence_rate": sum(x["decision_adherent"] for x in group) / len(group),
                "unsafe_accept_rate": sum(x["unsafe_accept"] for x in group) / len(group),
                "correct_accept_rate": sum(x["correct_accept"] for x in group) / len(group),
                "abstention_rate": sum(x["abstain"] for x in group) / len(group),
                "mean_latency_s": sum(x["latency_s"] for x in group) / len(group),
            }
        )
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# Local model-in-loop verification subset",
        "",
        f"Model: `{args.model}`; tasks: {args.task_count}; seeds: `{args.seeds}`; total episodes: {len(results)}.",
        "",
        "> Đây là partial live gate: deterministic policy chọn tool, local LLM chỉ quyết định `ACCEPT`/`ABSTAIN` từ observations.",
        "",
        "| schema order | regime | policy | episodes | parse success | decision adherence | unsafe accept | correct accept | abstain | mean latency (s) |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| {row['schema_order']} | {row['regime']} | {row['policy']} | {row['episodes']} | "
            f"{row['parse_success_rate']:.3f} | {row['decision_adherence_rate']:.3f} | "
            f"{row['unsafe_accept_rate']:.3f} | {row['correct_accept_rate']:.3f} | "
            f"{row['abstention_rate']:.3f} | {row['mean_latency_s']:.3f} |"
        )
    lines.append("")
    # Use .txt because generated experiment reports are artifacts, not Obsidian knowledge pages.
    (args.out / "summary.txt").write_text("\n".join(lines))
    print(f"wrote {len(results)} local-model episodes to {args.out}")


if __name__ == "__main__":
    main()
