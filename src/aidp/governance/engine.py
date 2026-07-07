from typing import Any

from aidp.governance.checkers import (
    CalibrationChecker,
    ConflictChecker,
    EvidenceChecker,
    ProvenanceChecker,
    ReproducibilityChecker,
    SafetyChecker,
)


class ScientificGovernanceEngine:
    """
    The 'Constitution of Science' pipeline.
    Acts as an unbypassable gatekeeper for all hypotheses before execution or publication.
    """

    def __init__(self) -> None:
        self.checkers = [
            EvidenceChecker(),
            ConflictChecker(),
            ProvenanceChecker(),
            ReproducibilityChecker(),
            SafetyChecker(),
            CalibrationChecker(),
        ]

    def evaluate_hypothesis(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        """
        Runs the constitutional gauntlet. Fails fast on the first negative check.
        """
        for checker in self.checkers:
            passed, reason = checker.check(hypothesis)
            if not passed:
                return False, f"Governance Rejected: {reason}"

        return True, "Governance Approved: Constitution of Science satisfied."
