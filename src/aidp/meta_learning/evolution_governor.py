import uuid
from datetime import UTC, datetime

from aidp.meta_learning.adaptation_models import AdaptationRecord
from aidp.meta_learning.governance_models import (
    AdaptationHypothesis,
    HypothesisStatus,
    MetricPrediction,
    SystemMetrics,
)
from aidp.meta_learning.policy_registry import AdaptivePolicyRegistry


class EvolutionGovernanceLayer:
    """
    Second-order learning orchestrator. Evaluates if adaptations actually improved the system.
    """
    
    def __init__(self, policy_registry: AdaptivePolicyRegistry):
        self.policy_registry = policy_registry
        self.active_hypotheses: dict[str, AdaptationHypothesis] = {}
        self.anti_pattern_registry: list[AdaptationRecord] = []
        
    def propose_adaptation(
        self, 
        adaptation: AdaptationRecord, 
        predictions: list[MetricPrediction], 
        current_metrics: SystemMetrics,
        observation_window_runs: int = 100
    ) -> AdaptationHypothesis:
        """
        Wraps a proposed adaptation into a testable scientific hypothesis.
        Applies the adaptation and begins observation.
        """
        
        hypothesis = AdaptationHypothesis(
            hypothesis_id=f"HYP-{uuid.uuid4().hex[:8].upper()}",
            adaptation=adaptation,
            predictions=predictions,
            observation_window_runs=observation_window_runs,
            baseline_metrics=current_metrics,
            status=HypothesisStatus.EVALUATING
        )
        
        self.active_hypotheses[hypothesis.hypothesis_id] = hypothesis
        
        # Apply the policy
        self.policy_registry.apply_adaptation(adaptation)
            
        return hypothesis
        
    def log_run(self, current_metrics: SystemMetrics):
        """
        Called after every run. Advances the observation window for all active hypotheses.
        If a window completes, the hypothesis is evaluated.
        """
        completed = []
        for hyp in self.active_hypotheses.values():
            if hyp.status == HypothesisStatus.EVALUATING:
                hyp.runs_elapsed += 1
                if hyp.runs_elapsed >= hyp.observation_window_runs:
                    self._evaluate_hypothesis(hyp, current_metrics)
                    completed.append(hyp.hypothesis_id)
                    
        for _hid in completed:
            # We keep them in memory for the PoC, in reality they'd move to the EvolutionLedger
            pass
            
    def _evaluate_hypothesis(self, hypothesis: AdaptationHypothesis, final_metrics: SystemMetrics):
        """
        Compares the actual metrics against the predictions.
        """
        success = True
        
        for pred in hypothesis.predictions:
            baseline_val = getattr(hypothesis.baseline_metrics, pred.metric_name)
            final_val = getattr(final_metrics, pred.metric_name)
            
            actual_delta = final_val - baseline_val
            hypothesis.actual_deltas[pred.metric_name] = actual_delta
            
            # Simple evaluation: Did it move in the expected direction by at least half the expected amount?
            if pred.expected_delta > 0:
                if actual_delta < (pred.expected_delta * 0.5):
                    success = False
            else:
                if actual_delta > (pred.expected_delta * 0.5):
                    success = False
                    
        hypothesis.evaluated_at = datetime.now(UTC)
        
        if success:
            hypothesis.status = HypothesisStatus.ACCEPTED
        else:
            hypothesis.status = HypothesisStatus.REJECTED
            self._rollback_adaptation(hypothesis.adaptation)
            self.anti_pattern_registry.append(hypothesis.adaptation)
            
    def _rollback_adaptation(self, adaptation: AdaptationRecord):
        """
        Reverts the system to its prior state.
        """
        self.policy_registry.rollback_adaptation(adaptation.record_id)
