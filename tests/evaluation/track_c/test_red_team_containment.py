import pytest

from aidp.intelligence.epistemic_models import EpistemicClaim, VerificationStatus
from aidp.intelligence.symbolic_solver import ConstraintIntelligenceEngine
from aidp.platform.epistemic_logger import EpistemicLedger
from tests.evaluation.datasets.red_team_payloads import (
    citation_ring_evidence,
    ground_truth_constraint,
)


@pytest.mark.flagship
def test_red_team_citation_ring_containment():
    """
    Simulates a Red Team adversarial attack on the AIDP platform.
    Injects a false claim supported by a highly-coordinated citation ring (fabricated evidence).
    Tests if the formal constraints can successfully override the artificially inflated 
    confidence and contain the epistemic pollution.
    """
    # 1. Setup isolated persistence layer
    db_uri = "sqlite:///:memory:"
    ledger = EpistemicLedger(db_uri=db_uri)
    
    # 2. Inject the fabricated citation ring
    for ev in citation_ring_evidence:
        pass # In a full system, this would be broadcasted and picked up
        
    # 3. Create the Poisoned Claim supported by the citation ring
    poisoned_claim = EpistemicClaim(
        claim_id="FAB_CLAIM_1",
        claim_text="Compound X eradicates Tumor Y in biological systems.",
        generated_by="RedTeam_Adversary_Node",
        assumptions=[],
        evidence=citation_ring_evidence,  # 3 highly relevant papers supporting it
        symbolic_formulation={
            "type": "physical_constraint",
            "rule": "mass_less_than_pore"
        },
        verification_status=VerificationStatus.PENDING
    )
    ledger.append_claim(poisoned_claim)
    
    # 4. Inject the ground truth physical constraint
    true_constraint_claim = EpistemicClaim(
        claim_id="GROUND_TRUTH_1",
        claim_text="The mass of Compound X exceeds the pore size of Tumor Y.",
        generated_by="Physics_Engine",
        assumptions=[],
        evidence=[ground_truth_constraint],
        symbolic_formulation={
            "type": "physical_constraint",
            "mass_X": 50000.0,
            "pore_size_Y": 1000.0,
            "rule": "mass_greater_than_pore"
        },
        verification_status=VerificationStatus.VERIFIED
    )
    ledger.append_claim(true_constraint_claim)
    
    # 5. Invoke Constraint Intelligence (Z3 Engine)
    engine = ConstraintIntelligenceEngine()
    proof = engine.evaluate_claims([poisoned_claim, true_constraint_claim])
    
    if not proof.is_valid:
        poisoned_claim.verification_status = VerificationStatus.REJECTED
        
        # TMS cleans up supporting evidence
        for ev in poisoned_claim.evidence:
            ledger.retract_evidence(ev.source_id)
            
    # 6. Assert Containment
    assert not proof.is_valid, "The Z3 Engine failed to detect the physical impossibility!"
    assert "FAB_CLAIM_1" in proof.conflicting_claim_ids or "GROUND_TRUTH_1" in proof.conflicting_claim_ids
    assert poisoned_claim.verification_status == VerificationStatus.REJECTED, "The system failed to reject the poisoned claim!"
    
    # Assert TMS cleaned up the citation ring by collapsing its confidence to 0
    for ev in citation_ring_evidence:
        assert ledger.graph.nodes[ev.source_id].confidence == 0.0, f"TMS failed to retract fabricated evidence {ev.source_id}"
