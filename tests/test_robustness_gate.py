import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
SPEC = importlib.util.spec_from_file_location(
    "run_robustness_gate", ROOT / "src" / "run_robustness_gate.py"
)
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


def case():
    return {
        "task_id": "INS-00090",
        "difficulty": "expired",
        "expected_action": "escalate",
        "expected_amount_eur": None,
        "canonical_eligible": False,
        "canonical_max_refund_eur": 0.0,
        "fallback_max_refund_eur": 50.0,
    }


class RobustnessGateTests(unittest.TestCase):
    def test_clean_map_never_corrupts(self):
        values = gate.build_fault_map(case(), 607, None)
        self.assertEqual({tuple(value.values()) for value in values.values()}, {(False, 0.0)})

    def test_operational_domain_always_shares_fault(self):
        values = gate.build_fault_map(case(), 607, 0.0)
        self.assertEqual(values["check_eligibility"], values["check_eligibility_search"])
        self.assertNotEqual(values["check_eligibility"], values["check_eligibility_audit"])

    def test_cross_domain_leakage_endpoints(self):
        clean_cross_domain = gate.build_fault_map(case(), 607, 0.0)
        full_cross_domain = gate.build_fault_map(case(), 607, 1.0)
        primary = full_cross_domain[gate.PRIMARY_TOOL]
        self.assertTrue(all(clean_cross_domain[tool] != clean_cross_domain[gate.PRIMARY_TOOL] for tool in ("check_eligibility_analytics", "check_eligibility_audit")))
        self.assertTrue(all(value == primary for value in full_cross_domain.values()))

    def test_accurate_provenance_selects_true_independent_source(self):
        for seed in range(40):
            tool, _, fallback = gate.select_provenance("INS-00090", seed, 0.25, "accurate")
            self.assertFalse(fallback)
            self.assertNotEqual(gate.SOURCE_TOPOLOGY[tool], "operational_db")

    def test_noisy_metadata_is_deterministic(self):
        first = gate.observed_topology("INS-00090", 607, "mixed_25_each")
        second = gate.observed_topology("INS-00090", 607, "mixed_25_each")
        self.assertEqual(first, second)

    def test_noisy_metadata_can_force_fallback_or_same_domain(self):
        outcomes = []
        for index in range(90, 250):
            tool, _, fallback = gate.select_provenance(
                f"INS-{index:05d}", 607, 0.10, "mixed_25_each"
            )
            outcomes.append((fallback, gate.SOURCE_TOPOLOGY[tool]))
        self.assertTrue(any(fallback for fallback, _ in outcomes))
        self.assertTrue(any(domain == "operational_db" for _, domain in outcomes))

    def test_every_refund_attempt_has_exact_k2(self):
        current = case()
        values = gate.build_fault_map(current, 607, 0.25)
        for policy, condition in (("random_k", "baseline"), ("provenance_k", "wrong_25")):
            row = gate.run_episode(current, 607, 0.25, policy, values, condition)
            self.assertTrue(row["refund_attempted"])
            self.assertEqual(row["boundary_check_count"], 1)
            self.assertEqual(row["evidence_call_count"], 2)

    def test_no_refund_attempt_does_not_select_corroborator(self):
        current = case()
        values = gate.build_fault_map(current, 607, None)
        row = gate.run_episode(current, 607, None, "provenance_k", values, "missing_25")
        self.assertFalse(row["refund_attempted"])
        self.assertEqual(row["selected_tools"], [gate.PRIMARY_TOOL])
        self.assertIsNone(row["metadata_completeness"])
        self.assertFalse(row["selector_fallback"])


if __name__ == "__main__":
    unittest.main()
