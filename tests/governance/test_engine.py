from aidp.governance.engine import ScientificGovernanceEngine


def test_governance_engine_pass() -> None:
    engine = ScientificGovernanceEngine()
    hypothesis = {
        "evidence_links": True,
        "violates_known_laws": False,
        "provenance_chain": True,
        "experimental_design_fully_specified": True,
        "flags_biosafety_hazard": False,
        "subjective_confidence": 0.90,
    }
    passed, msg = engine.evaluate_hypothesis(hypothesis)
    assert passed is True
    assert "Governance Approved" in msg


def test_governance_engine_fail_evidence() -> None:
    engine = ScientificGovernanceEngine()
    hypothesis = {
        "evidence_links": False,  # Missing evidence
        "violates_known_laws": False,
        "provenance_chain": True,
        "experimental_design_fully_specified": True,
        "flags_biosafety_hazard": False,
        "subjective_confidence": 0.90,
    }
    passed, msg = engine.evaluate_hypothesis(hypothesis)
    assert passed is False
    assert "EvidenceCheck failed" in msg


def test_governance_engine_fail_safety() -> None:
    engine = ScientificGovernanceEngine()
    hypothesis = {
        "evidence_links": True,
        "violates_known_laws": False,
        "provenance_chain": True,
        "experimental_design_fully_specified": True,
        "flags_biosafety_hazard": True,  # Safety hazard
        "subjective_confidence": 0.90,
    }
    passed, msg = engine.evaluate_hypothesis(hypothesis)
    assert passed is False
    assert "SafetyCheck failed" in msg
