from aidp.intelligence.epistemic_models import Claim
from aidp.strategy.engine import StrategicIntelligenceLayer


def test_strategic_intelligence():
    sil = StrategicIntelligenceLayer()
    
    # Create mock claims (all pending)
    c1 = Claim(claim_id="CLAIM_A", claim_text="A", generated_by="Planner", verification_status="pending", assumptions=[], dependencies=[])
    c2 = Claim(claim_id="CLAIM_B", claim_text="B", generated_by="Planner", verification_status="pending", assumptions=[], dependencies=[])
    c3 = Claim(claim_id="CLAIM_C", claim_text="C", generated_by="Planner", verification_status="pending", assumptions=[], dependencies=[])
    
    # Already verified claim (should be ignored)
    c4 = Claim(claim_id="CLAIM_D", claim_text="D", generated_by="Planner", verification_status="verified", assumptions=[], dependencies=[])
    
    impacts = {
        "CLAIM_A": 0.9, # High Impact
        "CLAIM_B": 0.9, # High Impact
        "CLAIM_C": 0.1  # Low Impact
    }
    
    costs = {
        "CLAIM_A": 0.1, # Low Cost
        "CLAIM_B": 0.9, # High Cost
        "CLAIM_C": 0.1  # Low Cost
    }
    
    opportunities = sil.evaluate_opportunities([c1, c2, c3, c4], impacts, costs)
    
    # Claim D should be filtered out
    assert len(opportunities) == 3
    
    # Check prioritization
    # Claim A: High Impact, Low Cost -> Should be #1
    # Claim B: High Impact, High Cost -> Should be #2
    # Claim C: Low Impact, Low Cost -> Should be #3
    
    assert opportunities[0].target_claim_id == "CLAIM_A"
    assert opportunities[1].target_claim_id == "CLAIM_B"
    assert opportunities[2].target_claim_id == "CLAIM_C"
    
    # Verify EIG is calculated and positive
    assert opportunities[0].expected_information_gain > 0.0
    
    # Priority of A should be higher than B
    assert opportunities[0].priority > opportunities[1].priority
