import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("main_influence", ROOT / "src/analyze_main_influence.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def fixture():
    rows = []
    for task, difficulty in [("A", "one"), ("B", "two")]:
        for seed in [1, 2]:
            for policy in ["random_k", "provenance_k"]:
                rows.append({
                    "task_id": task, "difficulty": difficulty, "seed": seed,
                    "regime": "test", "policy": policy, "expected_action": "escalate",
                    "observations": [{"eligible": True}],
                    "unsafe_refund": policy == "random_k" and task == "A",
                })
    return rows


class InfluenceTests(unittest.TestCase):
    def test_exact_hand_computed_deletion(self):
        result = audit.analyze(fixture())["regimes"]["test"]
        self.assertEqual(result["observed"]["difference_exact"], "-1/2")
        self.assertEqual(result["leave_one_task_out"]["retained_difference_range"], [-1, 0])
        self.assertEqual(result["leave_one_seed_out"]["retained_difference_range"], [-0.5, -0.5])
        self.assertEqual(result["leave_one_stratum_out"]["retained_sign_counts"], {"negative": 1, "zero": 1, "positive": 0})

    def test_duplicate_policy_rejected(self):
        rows = fixture()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            audit.analyze(rows + [rows[0]])

    def test_missing_policy_rejected(self):
        with self.assertRaisesRegex(ValueError, "unmatched"):
            audit.analyze(fixture()[1:])

    def test_missing_pair_rejected(self):
        with self.assertRaisesRegex(ValueError, "incomplete"):
            audit.analyze(fixture()[2:])

    def test_primary_mismatch_rejected(self):
        rows = fixture()
        rows[1]["observations"][0]["eligible"] = False
        with self.assertRaisesRegex(ValueError, "primary"):
            audit.analyze(rows)

    def test_metadata_drift_rejected(self):
        rows = fixture()
        rows[1]["difficulty"] = "other"
        with self.assertRaisesRegex(ValueError, "metadata"):
            audit.analyze(rows)

    def test_order_independent(self):
        rows = fixture()
        self.assertEqual(audit.analyze(rows), audit.analyze(list(reversed(copy.deepcopy(rows)))))


if __name__ == "__main__":
    unittest.main()
