import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "run_live_agent_gate", ROOT / "src" / "run_live_agent_gate.py"
)
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


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


if __name__ == "__main__":
    unittest.main()
