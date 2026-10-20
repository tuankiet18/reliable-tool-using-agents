#!/usr/bin/env python3
"""Run the RQ4 corroborator-choice items against a local Ollama server (standard library only).

Usage:
  python3 run_rq4.py --model qwen2.5:7b-instruct-q4_K_M --out results_qwen.jsonl
  python3 run_rq4.py --model llama3.1:8b-instruct-q4_K_M --out results_llama.jsonl
  python3 run_rq4.py --dry-run --model fake --out fake.jsonl     # no Ollama needed; random answers

Resumable: items already in --out are skipped. Settings are fixed by the protocol
(temperature 0, seed 0, at most 200 output tokens, one retry on invalid output).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import random
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OPTIONS = {"temperature": 0, "seed": 0, "num_predict": 200}
EXPECTED_ITEMS_SHA256 = "e0b33c12039a86cc51d724084331aa22f336aa76bbf7c222bda9ef4acd1be086"


def post(url: str, payload: dict, timeout: float = 300) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def parse_choice(text: str) -> str | None:
    try:
        obj = json.loads(text)
        c = str(obj.get("choice", "")).strip().upper()
    except (json.JSONDecodeError, AttributeError):
        m = re.search(r'"choice"\s*:\s*"([ABC])"', text)
        c = m.group(1) if m else ""
    return c if c in ("A", "B", "C") else None


def environment(host: str, model: str, dry: bool) -> dict:
    env = {"python": sys.version.split()[0], "platform": platform.platform(), "model": model}
    if dry:
        env["dry_run"] = True
        return env
    try:
        env["ollama_version"] = json.loads(urllib.request.urlopen(f"{host}/api/version", timeout=10).read()).get("version")
        tags = json.loads(urllib.request.urlopen(f"{host}/api/tags", timeout=10).read())
        env["model_digest"] = next((m.get("digest") for m in tags.get("models", []) if m.get("name") == model), None)
    except Exception as e:  # recorded, not fatal
        env["ollama_info_error"] = str(e)
    try:
        env["gpu"] = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
                                    capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        env["gpu"] = None
    return env


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--host", default="http://localhost:11434")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    items_path = HERE / "items.jsonl"
    digest = hashlib.sha256(items_path.read_bytes()).hexdigest()
    if digest != EXPECTED_ITEMS_SHA256:
        raise SystemExit(f"items.jsonl changed (sha256 {digest}); refusing to run")
    items = [json.loads(l) for l in items_path.open(encoding="utf-8")]
    done = set()
    if args.out.exists():
        for line in args.out.open(encoding="utf-8"):
            row = json.loads(line)
            if "item_id" in row:
                done.add(row["item_id"])
    rng = random.Random(0)
    with args.out.open("a", encoding="utf-8") as out:
        if not done:
            out.write(json.dumps({"environment": environment(args.host, args.model, args.dry_run),
                                  "items_sha256": digest, "options": OPTIONS,
                                  "started": time.strftime("%Y-%m-%dT%H:%M:%S%z")}) + "\n")
        todo = [it for it in items if it["item_id"] not in done]
        for n, it in enumerate(todo, 1):
            attempts = []
            for attempt in (1, 2):
                t0 = time.time()
                if args.dry_run:
                    raw = json.dumps({"choice": rng.choice("ABC"), "reason": "dry run"})
                else:
                    resp = post(f"{args.host}/api/chat", {"model": args.model, "messages": it["messages"],
                                                          "stream": False, "format": "json", "options": OPTIONS})
                    raw = resp.get("message", {}).get("content", "")
                choice = parse_choice(raw)
                attempts.append({"attempt": attempt, "raw": raw, "choice": choice, "seconds": round(time.time() - t0, 2)})
                if choice:
                    break
            final = attempts[-1]["choice"]
            out.write(json.dumps({"item_id": it["item_id"], "model": args.model, "choice": final, "valid": final is not None,
                                  "chose_shared": (final == it["shared_letter"]) if final else None,
                                  "attempts": attempts}, ensure_ascii=False) + "\n")
            out.flush()
            if n % 50 == 0 or n == len(todo):
                print(f"{n}/{len(todo)} done", flush=True)


if __name__ == "__main__":
    main()
