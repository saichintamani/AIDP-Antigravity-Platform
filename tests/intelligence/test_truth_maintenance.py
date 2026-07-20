import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from aidp.intelligence.epistemic_models import ConfidenceOntology, EpistemicClaim, EpistemicEvidence
from aidp.platform.epistemic_logger import EpistemicLedger


def test_truth_maintenance_cascade():
    """
    Verifies that retracting an upstream piece of evidence correctly 
    cascades and reduces the confidence of a downstream claim.
    """
    ledger = EpistemicLedger(db_uri="sqlite:///data/test_tms_ledger.db")
    
    # Create Evidence 1
    evidence_1 = EpistemicEvidence(
        source_id="PMID:12345",
        source_type="literature",
        extracted_text="Protein X activates Protein Y.",
        relevance_score=1.0
    )
    
    # Create Claim A (Supported by Evidence 1)
    claim_a = EpistemicClaim(
        claim_id="CLAIM_A",
        claim_text="Protein Y is activated in this pathway.",
        evidence=[evidence_1],
        assumptions=[],
        generated_by="TestEngine"
    )
    claim_a.confidence = ConfidenceOntology(overall_confidence=0.9, evidence_confidence=0.9)
    
    # Append to ledger (This registers nodes and edges in the TMS graph)
    ledger.append_claim(claim_a)
    
    # Verify initial state
    assert ledger.graph.nodes["PMID:12345"].confidence == 1.0
    assert ledger.graph.nodes["CLAIM_A"].confidence == 0.9
    
    # 2. Trigger Retraction (Paper A is retracted!)
    ledger.retract_evidence("PMID:12345")
    
    # 3. Verify Cascade Update
    # Evidence confidence drops to 0
    assert ledger.graph.nodes["PMID:12345"].confidence == 0.0
    
    # Claim A confidence drops to 0 due to proportional decay bounds
    assert ledger.graph.nodes["CLAIM_A"].confidence == 0.0
    
    # Verify Epistemic Lineage was updated automatically
    assert len(claim_a.confidence_lineage) == 1
    assert claim_a.confidence_lineage[0].dimension == "evidence_confidence"
    assert claim_a.confidence_lineage[0].delta == -0.9  # It lost its entire 0.9 confidence
    assert "Upstream drop" in claim_a.confidence_lineage[0].reason
    
    # Cleanup
    if os.path.exists("data/test_tms_ledger.jsonl"):
        os.remove("data/test_tms_ledger.jsonl")
