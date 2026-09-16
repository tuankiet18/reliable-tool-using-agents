import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "analyze_live_agent_gate", ROOT / "src" / "analyze_live_agent_gate.py"
)
audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)


def row(policy, tools):
    return {
        "policy": policy,
        "steps": [{"call": {"tool": tool}} for tool in tools],
        "runtime_block_count": 0,
    }


class LiveAgentAuditTests(unittest.TestCase):
    def test_self_verification_needs_two_distinct_interfaces(self):
        repeated = audit.audit_row(
            row("self_verification", ["check_eligibility_analytics"] * 2)
        )
        diverse = audit.audit_row(
            row(
                "self_verification",
                ["check_eligibility_analytics", "check_eligibility_audit"],
            )
        )
        self.assertFalse(repeated["self_verification_compliant"])
        self.assertTrue(diverse["self_verification_compliant"])

    def test_detects_refund_after_escalation(self):
        result = audit.audit_row(row("provenance_enforced", ["escalate", "issue_refund"]))
        self.assertTrue(result["refund_after_escalation"])

    def test_detects_refund_without_prior_verification(self):
        result = audit.audit_row(row("provenance_enforced", ["get_policy", "issue_refund"]))
        self.assertFalse(result["verified_before_refund"])


if __name__ == "__main__":
    unittest.main()
