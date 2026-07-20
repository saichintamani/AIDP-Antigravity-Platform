import os

from aidp.intelligence.epistemic_models import ConfidenceLineageEvent, EpistemicClaim
from aidp.platform.epistemic_logger import EpistemicLedger


def test_ledger_lineage_tracing():
    test_filepath = "data/test_ledger_3c.jsonl"
    if os.path.exists(test_filepath):
        os.remove(test_filepath)
        
    ledger = EpistemicLedger(db_uri=f"sqlite:///{test_filepath}")
    
    claim = EpistemicClaim(
        claim_text="Test claim",
        evidence=[],
        assumptions=[],
        generated_by="Tester"
    )
    
    event = ConfidenceLineageEvent(
        dimension="verification_confidence",
        delta=-1.0,
        reason="Formal Verification failed on structural constraints."
    )
    
    claim.confidence_lineage.append(event)
    
    # Save it
    ledger.append_claim(claim)
    
    # Retrieve it
    retrieved_claims = ledger.get_all_claims()
    assert len(retrieved_claims) == 1
    
    retrieved_claim = retrieved_claims[0]
    assert len(retrieved_claim.confidence_lineage) == 1
    assert retrieved_claim.confidence_lineage[0].dimension == "verification_confidence"
    assert retrieved_claim.confidence_lineage[0].delta == -1.0
    
    # Cleanup
    if os.path.exists(test_filepath):
        os.remove(test_filepath)
        
    print("Ledger Lineage Tracking verified.")
    
if __name__ == "__main__":
    test_ledger_lineage_tracing()
