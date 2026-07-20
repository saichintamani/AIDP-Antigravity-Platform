from aidp.explainability.causal_explanation import (
    AcceptanceExplanation,
    CausalExplanation,
    RejectionExplanation,
)
from aidp.intelligence.epistemic_models import Claim, VerificationStatus
from aidp.introspection.engine import ScientificIntrospectionEngine


def test_introspection_engine():
    engine = ScientificIntrospectionEngine()
    
    claims = []
    
    # Create 15 failing claims to trigger lessons learned
    for i in range(15):
        # We simulate a "Statistician" persona approving a claim that later fails Z3 validation
        acc = AcceptanceExplanation(
            summary="Approved by Statistician",
            individual_reviewer_scores={"Statistician": 1.0, "Engineer": 0.4} # Engineer rejects
        )
        rej = RejectionExplanation(
            unsat_core=["rule_pwr_claim_X"],
            summary="Power constraint failed"
        )
        
        c = Claim(
            claim_id=f"FAIL_{i}",
            claim_text="This protocol will work",
            assumptions=["Protein A activates Protein B"],
            generated_by="Planner X",
            verification_status=VerificationStatus.REJECTED,
            explanation=CausalExplanation(acceptance=acc, rejection=rej)
        )
        claims.append(c)
        
    # Create 5 passing claims
    for i in range(5):
        acc = AcceptanceExplanation(
            summary="Approved",
            individual_reviewer_scores={"Statistician": 1.0, "Engineer": 1.0}
        )
        
        c = Claim(
            claim_id=f"PASS_{i}",
            claim_text="This protocol will work",
            assumptions=["Protein A activates Protein B"],
            generated_by="Planner Y",
            verification_status=VerificationStatus.VERIFIED,
            explanation=CausalExplanation(acceptance=acc)
        )
        claims.append(c)
        
    engine.analyze_claims(claims)
    
    # 1. Check Failure Genome
    assert "rule_pwr_claim_X" in engine.failure_genome
    assert engine.failure_genome["rule_pwr_claim_X"].frequency == 15
    
    # 2. Check Reviewer Analytics
    # Statistician approved all 20, but 15 failed. Precision = 5/20 = 0.25
    assert "Statistician" in engine.reviewer_analytics
    assert engine.reviewer_analytics["Statistician"].precision == 0.25
    assert engine.reviewer_analytics["Statistician"].false_positives == 15
    
    # Engineer approved 5 (and all 5 passed). Engineer precision = 5/5 = 1.0
    assert "Engineer" in engine.reviewer_analytics
    assert engine.reviewer_analytics["Engineer"].precision == 1.0
    
    # 3. Check Assumption Observatory
    assert "Protein A activates Protein B" in engine.assumption_observatory
    obs = engine.assumption_observatory["Protein A activates Protein B"]
    assert obs.total_claims == 20
    assert obs.support_rate == 0.25
    
    # 4. Check Learning Signals
    lessons = [l.lesson for l in engine.lessons_learned]
    assert any("rule_pwr_claim_X" in l for l in lessons)
    assert any("Statistician" in l for l in lessons)
    assert any("Protein A activates Protein B" in l for l in lessons)
