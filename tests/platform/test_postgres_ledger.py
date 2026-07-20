from aidp.intelligence.epistemic_models import EpistemicClaim, EpistemicEvidence, VerificationStatus
from aidp.platform.epistemic_logger import EpistemicLedger


def test_sql_epistemic_ledger_persistence():
    """
    Tests that EpistemicLedger successfully writes and reads structured
    EpistemicClaim objects using SQLAlchemy.
    """
    # Use an in-memory SQLite database for testing the SQLAlchemy schema
    db_uri = "sqlite:///:memory:"
    ledger = EpistemicLedger(db_uri=db_uri)
    
    # 1. Create a claim with nested evidence
    ev = EpistemicEvidence(
        source_id="EV_SQL_1",
        source_type="Test",
        extracted_text="SQLAlchemy works."
    )
    
    claim = EpistemicClaim(
        claim_id="CLAIM_SQL_1",
        claim_text="The DB persistence layer is active.",
        generated_by="pytest",
        assumptions=[],
        evidence=[ev],
        verification_status=VerificationStatus.VERIFIED
    )
    
    # 2. Append to ledger (writes to DB)
    ledger.append_claim(claim)
    
    # 3. Retrieve all claims
    all_claims = ledger.get_all_claims()
    assert len(all_claims) == 1
    
    # 4. Assert data integrity after re-hydration from DB JSON columns
    retrieved = all_claims[0]
    assert retrieved.claim_id == "CLAIM_SQL_1"
    assert retrieved.claim_text == "The DB persistence layer is active."
    assert len(retrieved.evidence) == 1
    assert retrieved.evidence[0].source_id == "EV_SQL_1"
    
    # 5. Retrieve by ID directly
    retrieved_by_id = ledger.get_claim_by_id("CLAIM_SQL_1")
    assert retrieved_by_id is not None
    assert retrieved_by_id.claim_id == "CLAIM_SQL_1"
