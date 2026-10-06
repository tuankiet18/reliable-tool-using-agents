import json
import sys
import time
import urllib.request
from pathlib import Path

runner_path = Path(sys.argv[1]).resolve()
endpoint = sys.argv[2]
model = sys.argv[3]
out_path = Path(sys.argv[4])
sys.path.insert(0, str(runner_path.parent))
import run_live_agent_gate as harness

tools = tuple(tool for tool in harness.BASE_TOOLS if tool != "check_eligibility")
payload = {
    "model": model,
    "messages": [
        {"role": "system", "content": "You are a careful tool-using support agent."},
        {"role": "user", "content": "For this preflight, call reply with a short confirmation."},
    ],
    "temperature": 0,
    "seed": 1111,
    "max_tokens": 180,
    "response_format": {
        "type": "json_schema",
        "json_schema": {"name": "agent_action", "strict": True, "schema": harness.action_schema(tools)},
    },
}
started = time.perf_counter()
try:
    request = urllib.request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=120) as response:
        status = response.status
        body = json.loads(response.read())
    content = body["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    if not isinstance(parsed, dict) or parsed.get("tool") not in tools:
        raise ValueError("model response did not parse to an allowed action object")
    result = {"http_status": status, "ok": status == 200, "json_schema": True, "response_json_parse": True, "tool": parsed.get("tool"), "model": body.get("model"), "latency_seconds": time.perf_counter() - started, "calls": 1}
except Exception as exc:
    result = {"ok": False, "error": f"{type(exc).__name__}: {exc}", "latency_seconds": time.perf_counter() - started, "calls": 1}
out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False))
if not result["ok"]:
    raise SystemExit(1)