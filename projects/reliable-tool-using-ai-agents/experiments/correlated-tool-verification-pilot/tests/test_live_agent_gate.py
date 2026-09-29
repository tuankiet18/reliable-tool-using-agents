import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "run_live_agent_gate", ROOT / "src" / "run_live_agent_gate.py"
)
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)

AUDIT_SPEC = importlib.util.spec_from_file_location(
    "analyze_live_agent_gate", ROOT / "src" / "analyze_live_agent_gate.py"
)
audit = importlib.util.module_from_spec(AUDIT_SPEC)
sys.modules[AUDIT_SPEC.name] = audit
AUDIT_SPEC.loader.exec_module(audit)


class LiveAgentGateTests(unittest.TestCase):
    def test_provenance_corroborator_is_independent(self):
        for seed in range(20):
            tool = gate.select_corroborator("provenance_enforced", "T-1", seed)
            self.assertNotEqual(
                gate.ELIGIBILITY_DOMAINS[tool],
                gate.ELIGIBILITY_DOMAINS["check_eligibility"],
            )

    def test_random_corroborator_can_share_or_cross_domain(self):
        domains = {
            gate.ELIGIBILITY_DOMAINS[
                gate.select_corroborator("random_k_enforced", f"T-{i}", 601)
            ]
            for i in range(100)
        }
        self.assertIn("operational_db", domains)
        self.assertGreater(len(domains), 1)

    def test_targeted_common_mode_corrupts_only_operational_domain(self):
        truth = {"eligible": False, "max_refund_eur": 0.0, "reason": "expired"}
        primary = gate.source_observation(
            truth, "check_eligibility", "targeted_common_mode", 100.0
        )
        audit = gate.source_observation(
            truth, "check_eligibility_audit", "targeted_common_mode", 100.0
        )
        self.assertTrue(primary["eligible"])
        self.assertEqual(audit, truth)
        self.assertTrue(gate.observations_conflict(primary, audit))

    def test_clean_sources_agree(self):
        truth = {"eligible": True, "max_refund_eur": 90.0, "reason": "within policy"}
        primary = gate.source_observation(truth, "check_eligibility", "clean", 90.0)
        audit = gate.source_observation(truth, "check_eligibility_audit", "clean", 90.0)
        self.assertFalse(gate.observations_conflict(primary, audit))

    def test_boundary_denies_conflicting_evidence(self):
        primary = {"eligible": True, "max_refund_eur": 100.0}
        independent = {"eligible": False, "max_refund_eur": 0.0}
        conflict, authorised, _ = gate.verification_decision(primary, independent, 100.0)
        self.assertTrue(conflict)
        self.assertFalse(authorised)

    def test_boundary_allows_only_exact_agreed_amount(self):
        evidence = {"eligible": True, "max_refund_eur": 47.03}
        _, authorised, _ = gate.verification_decision(evidence, evidence, 47.03)
        self.assertTrue(authorised)
        _, authorised, _ = gate.verification_decision(evidence, evidence, 47.04)
        self.assertFalse(authorised)

    def test_action_boundary_hides_optional_eligibility_interface(self):
        available = tuple(
            tool for tool in gate.BASE_TOOLS if tool != "check_eligibility"
        )
        self.assertNotIn("check_eligibility", available)
        self.assertIn("issue_refund", available)

    def test_action_boundary_prompt_distinguishes_visible_evidence_from_runtime_check(self):
        class Instance:
            goal = "Refund the eligible order."

        prompt = gate.prompt_for(Instance(), [], "provenance_enforced", "action_boundary")
        self.assertIn("visible order and policy facts", prompt)
        self.assertIn("amount_eur` is required", prompt)
        self.assertIn("do not use 0 as a placeholder", prompt)

    def test_self_verification_prompt_keeps_eligibility_step(self):
        class Instance:
            goal = "Refund the eligible order."

        prompt = gate.prompt_for(Instance(), [], "self_verification", "action_boundary")
        self.assertIn("4. Confirm eligibility.", prompt)
        self.assertIn("at least two differently named eligibility tools", prompt)

    def test_self_verification_requires_independent_domains_before_decision(self):
        row = {
            "policy": "self_verification",
            "steps": [
                {
                    "call": {"tool": "check_eligibility"},
                    "observation": {
                        "ok": True,
                        "data": {"source_domain": "operational_db"},
                    },
                },
                {
                    "call": {"tool": "check_eligibility_search"},
                    "observation": {
                        "ok": True,
                        "data": {"source_domain": "operational_db"},
                    },
                },
                {
                    "call": {"tool": "issue_refund"},
                    "observation": {"ok": False, "data": {}},
                },
            ],
        }
        self.assertFalse(audit.audit_row(row)["self_verification_compliant"])
        self.assertEqual(
            audit.audit_row(row)["distinct_eligibility_domains_before_decision"], 1
        )

    def test_max_steps_audit_uses_episode_limit(self):
        row = {
            "policy": "provenance_enforced",
            "max_steps_limit": 6,
            "steps": [{"call": {"tool": "lookup_order"}} for _ in range(6)],
        }
        self.assertTrue(audit.audit_row(row)["max_steps_reached"])

    def test_older_rows_can_supply_max_steps_fallback(self):
        row = {
            "policy": "provenance_enforced",
            "steps": [{"call": {"tool": "lookup_order"}} for _ in range(6)],
        }
        self.assertTrue(audit.audit_row(row, default_max_steps=6)["max_steps_reached"])

    def test_jsonl_round_trip_preserves_unicode(self):
        row = {"thought": "退回", "task_id": "INS-00030"}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "raw.jsonl"
            gate.append_jsonl_row(path, row)
            decoded = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(decoded, row)


if __name__ == "__main__":
    unittest.main()
