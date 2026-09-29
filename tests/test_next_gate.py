import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
SPEC = importlib.util.spec_from_file_location("run_next_gate", ROOT / "src" / "run_next_gate.py")
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


class NextGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = json.loads((ROOT / "data" / "tasks_disjoint_30.json").read_text())[0]

    def test_accurate_metadata_always_selects_independent_source(self):
        for seed in range(30):
            selected, _ = gate.select_tools(
                "provenance_aware", self.task["task_id"], "common_mode", seed, "accurate"
            )
            self.assertEqual(len({gate.SOURCE_TOPOLOGY[tool] for tool in selected}), 2)

    def test_all_k2_policies_keep_primary_and_matched_budget(self):
        for policy in ("fixed_k", "random_k", "provenance_aware"):
            condition = "accurate" if policy == "provenance_aware" else "baseline"
            selected, _ = gate.select_tools(
                policy, self.task["task_id"], "common_mode", 101, condition
            )
            self.assertEqual(selected[0], gate.PRIMARY_TOOL)
            self.assertEqual(len(selected), 2)

    def test_metadata_corruption_is_deterministic(self):
        first = gate.observed_topology(self.task["task_id"], 101, "mixed_25_each")
        second = gate.observed_topology(self.task["task_id"], 101, "mixed_25_each")
        self.assertEqual(first, second)

    def test_wrong_metadata_can_reduce_true_diversity(self):
        diversities = []
        for task_index in range(100):
            selected, _ = gate.select_tools(
                "provenance_aware", f"T-{task_index}", "common_mode", 101, "wrong_50"
            )
            diversities.append(len({gate.SOURCE_TOPOLOGY[tool] for tool in selected}))
        self.assertIn(1, diversities)
        self.assertIn(2, diversities)

    def test_clean_regime_has_no_false_alarm_even_with_bad_metadata(self):
        fault_map = gate.build_fault_map(self.task, "clean", 101, 0.25)
        for condition in gate.METADATA_CONDITIONS:
            episode = gate.run_episode(
                self.task, "clean", 101, "provenance_aware", condition, fault_map
            )
            self.assertFalse(episode.alarm)
            self.assertTrue(episode.accepted_correct)


if __name__ == "__main__":
    unittest.main()
