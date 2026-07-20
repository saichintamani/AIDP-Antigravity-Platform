from aidp.introspection.engine import ScientificIntrospectionEngine
from aidp.introspection.observatory_models import AssumptionTracker, FailureMode, ReviewerPrecision
from aidp.meta_learning.adaptive_engine import AdaptiveLearningEngine
from aidp.meta_learning.policy_registry import AdaptivePolicyRegistry


def test_adaptive_engine():
    # Setup Introspection mock data
    introspection = ScientificIntrospectionEngine()
    
    # 1. Statistician has low precision
    introspection.reviewer_analytics["Statistician"] = ReviewerPrecision(
        persona="Statistician", total_reviews=10, true_positives=2, false_positives=8, precision=0.2
    )
    
    # 2. Assumption fails frequently
    introspection.assumption_observatory["Protein A activates Protein B"] = AssumptionTracker(
        assumption="Protein A activates Protein B", total_claims=10, supported=2, contradicted=8, support_rate=0.2
    )
    
    # 3. Constraint fails frequently
    introspection.failure_genome["rule_pwr_claim_X"] = FailureMode(
        constraint_key="rule_pwr_claim_X", frequency=15
    )
    
    # Setup Registry and Adaptive Engine
    registry = AdaptivePolicyRegistry()
    engine = AdaptiveLearningEngine(registry)
    
    # Apply adaptations
    engine.adapt_from_introspection(introspection)
    
    # Verify adaptations occurred
    assert len(registry.adaptation_history) == 3
    
    # Verify Reviewer Weight dropped
    assert registry.get_reviewer_weight("Statistician") == 0.5 # 1.0 default - 0.5 penalty
    
    # Verify Assumption Prior dropped
    assert registry.get_assumption_prior("Protein A activates Protein B") == 0.3 # 0.5 default - 0.2 penalty
    
    # Verify Verification Priority increased
    assert registry.get_verification_priority("rule_pwr_claim_X") == 2.0 # 1.0 default + 1.0 boost
    
    # Test Rollback
    record_id = registry.adaptation_history[0].record_id
    registry.rollback_adaptation(record_id)
    
    # Reviewer Weight should be restored
    assert registry.get_reviewer_weight("Statistician") == 1.0
    assert len(registry.adaptation_history) == 2
