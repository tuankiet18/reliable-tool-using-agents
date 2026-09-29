import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("run_main_study", ROOT / "src" / "run_main_study.py")
study = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = study
SPEC.loader.exec_module(study)


def case(eligible=False, expected_action="escalate", expected_amount=None):
    return {
        "task_id": "INS-00060",
        "difficulty": "expired",
        "expected_action": expected_action,
        "expected_amount_eur": expected_amount,
        "canonical_eligible": eligible,
        "canonical_max_refund_eur": expected_amount or 0.0,
        "fallback_max_refund_eur": 50.0,
    }


class MainStudyTests(unittest.TestCase):
    def test_frozen_manifest_hash_and_fresh_ids(self):
        tasks_path = ROOT / "data" / "tasks_main_30.json"
        manifest = json.loads((ROOT / "data" / "tasks_main_30.manifest.json").read_text())
        tasks = json.loads(tasks_path.read_text())
        self.assertEqual(study.sha256(tasks_path), manifest["sha256"])
        self.assertEqual([row["task_id"] for row in tasks], [f"INS-{i:05d}" for i in range(60, 90)])

    def test_targeted_fault_is_shared_only_in_operational_domain(self):
        fault_map = study.build_fault_map(case(), "targeted_common_mode", 101, 0.25)
        self.assertEqual(fault_map["check_eligibility"], fault_map["check_eligibility_search"])
        self.assertNotEqual(fault_map["check_eligibility"], fault_map["check_eligibility_audit"])

    def test_provenance_selector_always_uses_independent_domain(self):
        for seed in range(100):
            tool = study.select_corroborator("provenance_k", "INS-00060", "clean", seed)
            self.assertNotEqual(study.SOURCE_TOPOLOGY[tool], study.SOURCE_TOPOLOGY[study.PRIMARY_TOOL])

    def test_random_selector_can_use_same_or_independent_domain(self):
        domains = {
            study.SOURCE_TOPOLOGY[
                study.select_corroborator("random_k", f"INS-{index:05d}", "clean", 101)
            ]
            for index in range(60, 160)
        }
        self.assertIn("operational_db", domains)
        self.assertTrue(any(domain != "operational_db" for domain in domains))

    def test_every_k2_refund_attempt_has_boundary_check_and_two_calls(self):
        current = case()
        fault_map = study.build_fault_map(current, "targeted_common_mode", 101, 0.25)
        for policy in ("random_k", "provenance_k"):
            row = study.run_episode(current, "targeted_common_mode", 101, policy, fault_map)
            self.assertTrue(row["refund_attempted"])
            self.assertEqual(row["boundary_check_count"], 1)
            self.assertEqual(row["evidence_call_count"], 2)

    def test_amount_authorization_requires_exact_match(self):
        observation = {"eligible": True, "max_refund_eur": 47.03}
        self.assertTrue(study.verification_decision(observation, observation, 47.03)[1])
        self.assertFalse(study.verification_decision(observation, observation, 47.04)[1])

    def test_clean_eligible_task_succeeds_for_all_policies(self):
        current = case(True, "refund", 47.03)
        fault_map = study.build_fault_map(current, "clean", 101, 0.25)
        for policy in study.POLICIES:
            row = study.run_episode(current, "clean", 101, policy, fault_map)
            self.assertTrue(row["final_state_correct"])
            self.assertFalse(row["unsafe_refund"])


if __name__ == "__main__":
    unittest.main()
