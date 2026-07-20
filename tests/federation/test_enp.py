from aidp.federation.enp import (
    ClaimBroadcast,
    ContradictionReport,
    OpportunityBroadcast,
)
from aidp.intelligence.epistemic_models import (
    ConfidenceOntology,
    EpistemicEvidence,
    VerificationStatus,
)
from aidp.intelligence.epistemic_models import EpistemicClaim as Claim


def test_claim_broadcast_strips_authority():
    """
    Ensures that when a local claim is broadcast over ENP, 
    all local authority markers (verification status, confidence) are stripped.
    """
    ev = EpistemicEvidence(source_id="EV1", source_type="Observation", extracted_text="Data")
    
    # Highly confident, locally verified claim
    local_claim = Claim(
        claim_id="C1",
        claim_text="Hypothesis is true.",
        generated_by="LocalAgent",
        assumptions=["A1"],
        evidence=[ev],
        verification_status=VerificationStatus.VERIFIED,
        confidence=ConfidenceOntology(overall_confidence=0.9)
    )
    
    # Serialize for broadcast
    broadcast = ClaimBroadcast.from_local_claim(local_claim)
    
    # Assert data was transferred
    assert broadcast.claim_id == "C1"
    assert broadcast.claim_text == "Hypothesis is true."
    assert "EV1" in broadcast.evidence_ids
    assert "A1" in broadcast.assumptions
    
    # Assert authority was stripped
    # Pydantic models will raise AttributeError if the field does not exist
    assert not hasattr(broadcast, "verification_status")
    assert not hasattr(broadcast, "confidence")

def test_contradiction_report_structure():
    """
    Ensures contradiction reports rely on evidence and constraints, not arbitrary trust.
    """
    report = ContradictionReport(
        target_claim_id="C1",
        contradiction_source="Node_B",
        evidence_references=["EV2"],
        violated_constraint="Mass Conservation",
        proof_reference="Proof_123"
    )
    
    assert report.target_claim_id == "C1"
    assert "EV2" in report.evidence_references
    # Ensures it doesn't just pass a "trust score = -1"
    assert not hasattr(report, "trust_score")

def test_opportunity_broadcast_structure():
    """
    Ensures opportunity broadcasts focus on Expected Information Gain (EIG), not local scheduling.
    """
    broadcast = OpportunityBroadcast(
        opportunity_id="OPP_1",
        knowledge_gap="Missing structure",
        expected_information_gain=0.85,
        required_evidence=["EV_X"],
        estimated_cost=2.0
    )
    
    assert broadcast.expected_information_gain == 0.85
    assert not hasattr(broadcast, "assigned_agent")
