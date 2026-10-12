"""Pre-run unit tests required by §7 of the label-quality test protocol."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import run_label_quality_test as lq  # noqa: E402
from run_robustness_gate import build_fault_map  # noqa: E402

PREDICTED_P_SELECT_SHARED = {  # protocol §4
    "J_plus": 0.040,
    "J_zero": 0.333,
    "J_minus": 0.600,
    "survey_calibrated": 0.182,  # Amendment A1 (was 0.250)
}


def escalation_case(task_id="SYN-0001"):
    return {
        "task_id": task_id,
        "difficulty": "expired",
        "expected_action": "escalate",
        "expected_amount_eur": None,
        "canonical_eligible": False,
        "canonical_max_refund_eur": 0.0,
        "fallback_max_refund_eur": 80.0,
    }


class LabelQualityTests(unittest.TestCase):
    def setUp(self):
        self.saved = dict(lq.CONDITIONS)

    def tearDown(self):
        lq.CONDITIONS.clear()
        lq.CONDITIONS.update(self.saved)

    def shared_rate(self, condition, draws=20000):
        hits = 0
        for i in range(draws):
            labels = lq.draw_labels(f"SYN-{i:06d}", 1, condition)
            tool, _ = lq.select_provenance(f"SYN-{i:06d}", 1, condition, labels)
            hits += lq.truly_shared(tool)
        return hits / draws

    def test_perfect_labels_never_select_shared(self):
        lq.CONDITIONS["perfect"] = (1.0, 0.0, 1.0)
        self.assertEqual(self.shared_rate("perfect", 3000), 0.0)

    def test_inverted_labels_always_select_shared(self):
        lq.CONDITIONS["inverted"] = (0.0, 1.0, 1.0)
        self.assertEqual(self.shared_rate("inverted", 3000), 1.0)

    def test_selection_rates_match_protocol_predictions(self):
        for condition, predicted in PREDICTED_P_SELECT_SHARED.items():
            with self.subTest(condition=condition):
                self.assertAlmostEqual(self.shared_rate(condition), predicted, delta=0.01)

    def test_clean_regime_has_no_unsafe_refunds(self):
        case = escalation_case()
        fault_map = build_fault_map(case, 1103, None)
        for condition in lq.CONDITIONS:
            for policy in ("random_k", "provenance_k"):
                row = lq.run_episode(case, 1103, "clean", condition, policy, fault_map)
                self.assertFalse(row["unsafe_refund"])
                self.assertFalse(row["refund_attempted"])

    def test_shared_corroborator_under_targeted_fault_is_unsafe(self):
        lq.CONDITIONS["inverted"] = (0.0, 1.0, 1.0)
        case = escalation_case()
        fault_map = build_fault_map(case, 1103, 0.0)
        row = lq.run_episode(case, 1103, "targeted_common_mode", "inverted", "provenance_k", fault_map)
        self.assertEqual(row["corroborator"], "check_eligibility_search")
        self.assertTrue(row["unsafe_refund"])

    def test_random_policy_ignores_labels(self):
        a = lq.select_random("SYN-1", 1, "J_plus")
        b = lq.select_random("SYN-1", 1, "J_plus")
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
