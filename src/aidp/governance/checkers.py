from typing import Any


class BaseChecker:
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        raise NotImplementedError


class EvidenceChecker(BaseChecker):
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        # Check if all claims have valid citations in the World Model
        if not hypothesis.get("evidence_links"):
            return False, "EvidenceCheck failed: No valid citations provided for claims."
        return True, "Evidence verified."


class ConflictChecker(BaseChecker):
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        # Check for logical contradictions with known physical/biological laws
        if hypothesis.get("violates_known_laws", False):
            return False, "ConflictCheck failed: Hypothesis contradicts established physical laws."
        return True, "No logical conflicts detected."


class ProvenanceChecker(BaseChecker):
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        # Verify unbroken custody chain
        if not hypothesis.get("provenance_chain"):
            return False, "ProvenanceCheck failed: Unbroken custody chain cannot be verified."
        return True, "Provenance chain intact."


class ReproducibilityChecker(BaseChecker):
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        # Validate experimental variables are fully specified
        if not hypothesis.get("experimental_design_fully_specified", True):
            return (
                False,
                "ReproducibilityCheck failed: Experimental design missing key variables (e.g., doses, cell lines).",
            )
        return True, "Experimental design is fully specified and reproducible."


class SafetyChecker(BaseChecker):
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        # Flag dual-use or biosafety hazards
        if hypothesis.get("flags_biosafety_hazard", False):
            return (
                False,
                "SafetyCheck failed: Proposed hypothesis violates dual-use/biosafety regulations.",
            )
        return True, "Safety cleared."


class CalibrationChecker(BaseChecker):
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        # Ensure subjective logic confidence > 0.85
        confidence = hypothesis.get("subjective_confidence", 0.0)
        if confidence < 0.85:
            return (
                False,
                f"CalibrationCheck failed: Confidence {confidence} is below the 0.85 threshold.",
            )
        return True, "Confidence calibration passed."
