import copy
import importlib.util
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("generate_paper_figures", ROOT / "src/generate_paper_figures.py")
figures = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(figures)


class PaperFigureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((figures.PAPER / "artifact-inventory.json").read_text(encoding="utf-8"))
        cls.data = figures.build_data(ROOT, cls.inventory)

    def test_five_frozen_hashes_verified(self):
        self.assertEqual(len(self.data["input_hashes"]), 5)
        self.assertFalse(self.data["new_bootstrap"])
        self.assertEqual(self.data["new_episodes"], 0)

    def test_wrong_hash_stops_before_render(self):
        bad = copy.deepcopy(self.inventory)
        next(r for r in bad["artifacts"] if r["path"] == figures.INPUTS[0])["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            figures.verify_inputs(ROOT, bad)

    def test_main_counts_and_conditional_denominators(self):
        rows = [r for r in self.data["main_counts"] if r["regime"] == "targeted_common_mode"]
        self.assertEqual([r["unsafe_decisions"]["numerator"] for r in rows], [30, 0, 0])
        for row in rows:
            self.assertEqual(row["unsafe_decisions"]["denominator"], 150)
            self.assertEqual(row["correct_expected_refund_decisions"], figures.ratio(0, 50))
        for row in rows[:2]:
            self.assertEqual((row["missed_no_proposal"], row["missed_gate_rejection"]), (50, 0))

    def test_counterfactual_not_mislabeled_measured_baseline(self):
        rows = [r for r in self.data["main_counts"] if r["policy"] == "always_escalate"]
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(r["status"] == "POST_HOC_COUNTERFACTUAL_NOT_RUN" for r in rows))

    def test_percentage_point_conversion_not_relative_reduction(self):
        row = next(r for r in self.data["effects"] if r["label"] == "targeted_common_mode")
        self.assertEqual(row["difference_pp"], -20.0)
        self.assertAlmostEqual(row["ci95_pp"][0], -27.33333333333334)

    def test_wrong_metadata_fail_preserved_before_rounding(self):
        row = next(r for r in self.data["effects"] if r["label"].startswith("wrong"))
        self.assertEqual(row["gate"], "FAIL")
        self.assertGreaterEqual(row["ci95"][1], 0)
        self.assertEqual(self.data["robustness_gate"], "FAIL ROBUSTNESS")

    def test_robustness_shared_control_not_multiplied_by_metadata_conditions(self):
        rows = [r for r in self.data["effects"] if r["study"] == "robustness"]
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1]["rates"]["random_k"], rows[2]["rates"]["random_k"])
        self.assertEqual(rows[1]["rates"]["random_k"], figures.ratio(38, 150))

    def test_svg_is_valid_and_contains_scope_warnings(self):
        first = figures.safety_utility_svg(self.data)
        second = figures.effects_svg(self.data)
        for document in [first, second]:
            self.assertEqual(ET.fromstring(document).tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("counterfactual", first)
        self.assertIn("0/50", first)
        self.assertIn("FAIL ROBUSTNESS", second)
        self.assertIn("không pool", second)

    def test_output_refuses_overwrite_and_roundtrips_utf8(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary) / "new"
            figures.write_outputs(out, self.data)
            self.assertEqual(json.loads((out / "figure-data.json").read_text(encoding="utf-8")), self.data)
            before = (out / "main-safety-utility.svg").read_bytes()
            with self.assertRaises(FileExistsError):
                figures.write_outputs(out, self.data)
            self.assertEqual((out / "main-safety-utility.svg").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
