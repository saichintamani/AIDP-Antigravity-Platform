from aidp.meta_learning.adaptation_models import AdaptationRecord
from aidp.meta_learning.evolution_governor import EvolutionGovernanceLayer
from aidp.meta_learning.governance_models import HypothesisStatus, MetricPrediction, SystemMetrics
from aidp.meta_learning.policy_registry import AdaptivePolicyRegistry


def test_evolution_governance_success():
    registry = AdaptivePolicyRegistry()
    registry.reviewer_weights["Statistician"] = 1.0
    
    egl = EvolutionGovernanceLayer(registry)
    
    # Baseline
    baseline = SystemMetrics(verification_pass_rate=0.5)
    
    # Proposed adaptation: lower weight to 0.7
    adapt = AdaptationRecord(
        source_signal="Test", target_component="ReviewerWeights", target_key="Statistician",
        adaptation_type="WeightReduction", previous_state=1.0, new_state=0.7
    )
    
    # Prediction: Verification pass rate goes up by 0.20
    pred = MetricPrediction(metric_name="verification_pass_rate", expected_delta=0.20)
    
    hyp = egl.propose_adaptation(adapt, [pred], baseline, observation_window_runs=10)
    
    # Weight should be updated immediately
    assert registry.get_reviewer_weight("Statistician") == 0.7
    
    # Simulate 9 runs (no evaluation yet)
    for _ in range(9):
        egl.log_run(SystemMetrics(verification_pass_rate=0.6))
        
    assert hyp.status == HypothesisStatus.EVALUATING
    
    # Run 10 (Evaluation happens)
    # The actual pass rate goes to 0.8 (delta is +0.3, which beats the prediction of +0.2)
    egl.log_run(SystemMetrics(verification_pass_rate=0.8))
    
    assert hyp.status == HypothesisStatus.ACCEPTED
    assert registry.get_reviewer_weight("Statistician") == 0.7 # Change remains

def test_evolution_governance_failure_rollback():
    registry = AdaptivePolicyRegistry()
    registry.reviewer_weights["Statistician"] = 1.0
    
    egl = EvolutionGovernanceLayer(registry)
    
    # Baseline
    baseline = SystemMetrics(contradiction_rate=0.5)
    
    # Proposed adaptation
    adapt = AdaptationRecord(
        source_signal="Test", target_component="ReviewerWeights", target_key="Statistician",
        adaptation_type="WeightReduction", previous_state=1.0, new_state=0.7
    )
    
    # Prediction: Contradiction rate goes DOWN by 0.10
    pred = MetricPrediction(metric_name="contradiction_rate", expected_delta=-0.10)
    
    hyp = egl.propose_adaptation(adapt, [pred], baseline, observation_window_runs=10)
    
    # Simulate 10 runs
    for _i in range(10):
        # The contradiction rate actually goes UP to 0.6 (delta is +0.10)
        egl.log_run(SystemMetrics(contradiction_rate=0.6))
        
    # Evaluation should fail
    assert hyp.status == HypothesisStatus.REJECTED
    
    # Rollback should occur
    assert registry.get_reviewer_weight("Statistician") == 1.0
    
    # Adaptation added to anti-patterns
    assert len(egl.anti_pattern_registry) == 1
