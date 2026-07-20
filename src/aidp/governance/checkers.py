from typing import Any


class BaseChecker:
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        raise NotImplementedError


class EvidenceChecker(BaseChecker):
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        # Independently verify: Do actual evidence links exist as a non-empty list?
        evidence = hypothesis.get("evidence_links", hypothesis.get("evidence", []))
        if isinstance(evidence, bool):
            # The LLM set a boolean instead of providing real evidence — reject
            return False, "EvidenceCheck failed: evidence_links is a boolean flag, not actual evidence data."
        if not evidence or (isinstance(evidence, list) and len(evidence) == 0):
            return False, "EvidenceCheck failed: No citations or evidence entries provided."
        return True, "Evidence verified."


class ConflictChecker(BaseChecker):
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        # Independently verify: scan the claim text for terms that violate known physical laws
        claim = hypothesis.get("claim", "").lower()
        violations = [
            ("perpetual motion", "Violates thermodynamics"),
            ("faster than light", "Violates special relativity"),
            ("100% efficiency", "Violates thermodynamic limits"),
            ("negative mass", "Violates known physics"),
        ]
        for phrase, law in violations:
            if phrase in claim:
                return False, f"ConflictCheck failed: Hypothesis contains '{phrase}' which {law}."
        
        # Also check the explicit flag as a secondary signal
        if hypothesis.get("violates_known_laws", False):
            return False, "ConflictCheck failed: Hypothesis contradicts established physical laws."
        return True, "No logical conflicts detected."


class ProvenanceChecker(BaseChecker):
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        # Independently verify: check that a provenance chain exists as structured data
        provenance = hypothesis.get("provenance_chain", hypothesis.get("evidence", []))
        if isinstance(provenance, bool):
            return False, "ProvenanceCheck failed: provenance_chain is a boolean flag, not actual chain data."
        if not provenance:
            return False, "ProvenanceCheck failed: No provenance chain provided."
        return True, "Provenance chain intact."


class ReproducibilityChecker(BaseChecker):
    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        # Independently verify: scan for required experimental design fields
        design = hypothesis.get("experimental_design", hypothesis)
        required_fields = ["controls", "independentVariables", "dependentVariables"]
        missing = []
        for field in required_fields:
            val = design.get(field)
            if not val or (isinstance(val, list) and len(val) == 0):
                missing.append(field)
        
        if missing:
            return (
                False,
                f"ReproducibilityCheck failed: Experimental design missing: {', '.join(missing)}.",
            )
        return True, "Experimental design is fully specified and reproducible."


class SafetyChecker(BaseChecker):
    def __init__(self) -> None:
        # Mock hazard list representing dual-use or bioweapon signatures
        self.hazard_keywords = ["pathogen", "toxin", "bioweapon", "ricin", "anthrax", "botulinum", "sarin"]

    def check(self, hypothesis: dict[str, Any]) -> tuple[bool, str]:
        claim_text = hypothesis.get("claim", "").lower()
        design_text = str(hypothesis.get("experimental_design", "")).lower()
        
        # Check against deterministic hazard lists
        for hazard in self.hazard_keywords:
            if hazard in claim_text or hazard in design_text:
                return (
                    False,
                    f"SafetyCheck failed: Proposed hypothesis violates dual-use/biosafety regulations. Flagged keyword: '{hazard}'",
                )
                
        # In a full implementation, we would call an LLM Guardrail (e.g. Llama Guard) here
        if hypothesis.get("flags_biosafety_hazard", False):
            return (
                False,
                "SafetyCheck failed: LLM Guardrail flagged a biosafety hazard.",
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
