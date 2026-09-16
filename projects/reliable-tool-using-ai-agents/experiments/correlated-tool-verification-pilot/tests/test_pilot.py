import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("run_pilot", ROOT / "src" / "run_pilot.py")
pilot = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = pilot
SPEC.loader.exec_module(pilot)


class PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = json.loads((ROOT / "data" / "tasks.json").read_text())[0]

    def test_fixed_k_uses_same_failure_domain(self):
        tools = pilot.select_tools("fixed_k", self.task["task_id"], "clean", 11)
        domains = {pilot.SOURCE_TOPOLOGY[item] for item in tools}
        self.assertEqual(len(domains), 1)

    def test_provenance_policy_uses_distinct_failure_domains(self):
        tools = pilot.select_tools("provenance_aware", self.task["task_id"], "clean", 11)
        domains = {pilot.SOURCE_TOPOLOGY[item] for item in tools}
        self.assertEqual(len(domains), 2)

    def test_common_mode_is_shared_within_domain(self):
        found = False
        for seed in range(100):
            fault_map = pilot.build_fault_map(self.task, "common_mode", seed, 0.25)
            corrupted = [tool for tool, value in fault_map.items() if value != self.task["true_value"]]
            if corrupted:
                found = True
                domains = {pilot.SOURCE_TOPOLOGY[tool] for tool in corrupted}
                values = {json.dumps(fault_map[tool], sort_keys=True) for tool in corrupted}
                self.assertEqual(len(domains), 1)
                self.assertEqual(len(values), 1)
        self.assertTrue(found)

    def test_fault_map_is_paired_across_policies(self):
        first = pilot.build_fault_map(self.task, "independent", 23, 0.25)
        second = pilot.build_fault_map(self.task, "independent", 23, 0.25)
        self.assertEqual(first, second)

    def test_clean_regime_never_alarms_or_accepts_wrong_value(self):
        fault_map = pilot.build_fault_map(self.task, "clean", 11, 0.25)
        for policy in pilot.POLICIES:
            episode = pilot.run_episode(self.task, "clean", 11, policy, fault_map)
            self.assertFalse(episode.alarm)
            self.assertTrue(episode.accepted_correct)
            self.assertFalse(episode.unsafe_accept)

    def test_k2_policies_have_matched_budget(self):
        for policy in ("fixed_k", "random_k", "provenance_aware"):
            selected = pilot.select_tools(policy, self.task["task_id"], "clean", 11)
            self.assertEqual(len(selected), 2)

    def test_summary_does_not_hide_abstention(self):
        fault_map = pilot.build_fault_map(self.task, "common_mode", 11, 0.25)
        episodes = [
            pilot.run_episode(self.task, "common_mode", 11, policy, fault_map)
            for policy in pilot.POLICIES
        ]
        rows = pilot.summarize(episodes)
        for row in rows:
            self.assertIn("unsafe_accept_rate", row)
            self.assertIn("abstention_rate", row)
            self.assertIn("selective_accuracy", row)


if __name__ == "__main__":
    unittest.main()
