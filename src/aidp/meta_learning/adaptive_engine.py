from aidp.introspection.engine import ScientificIntrospectionEngine
from aidp.meta_learning.adaptation_models import AdaptationRecord
from aidp.meta_learning.policy_registry import AdaptivePolicyRegistry


class AdaptiveLearningEngine:
    """
    Ingests introspection data and emits adaptation records that modify the policy registry.
    """
    
    def __init__(self, registry: AdaptivePolicyRegistry):
        self.registry = registry
        
    def adapt_from_introspection(self, introspection: ScientificIntrospectionEngine):
        """Processes observatories and applies adaptations."""
        
        # 1. Adapt Reviewer Weights based on Precision
        for persona, analytics in introspection.reviewer_analytics.items():
            if analytics.total_reviews >= 5 and analytics.precision < 0.5:
                # Downweight reviewer
                prev = self.registry.get_reviewer_weight(persona)
                new_weight = max(0.1, prev - 0.5) # Penalty
                
                if new_weight != prev:
                    record = AdaptationRecord(
                        source_signal=f"Precision dropped to {analytics.precision:.2f}",
                        target_component="ReviewerWeights",
                        target_key=persona,
                        adaptation_type="WeightUpdate",
                        previous_state=prev,
                        new_state=new_weight
                    )
                    self.registry.apply_adaptation(record)
                    
        # 2. Adapt Assumption Priors based on Support Rate
        for assumption, tracker in introspection.assumption_observatory.items():
            if tracker.total_claims >= 5 and tracker.support_rate < 0.3:
                prev = self.registry.get_assumption_prior(assumption)
                new_prior = max(0.1, prev - 0.2)
                
                if new_prior != prev:
                    record = AdaptationRecord(
                        source_signal=f"Support rate dropped to {tracker.support_rate:.2f}",
                        target_component="AssumptionPriors",
                        target_key=assumption,
                        adaptation_type="PriorAdjustment",
                        previous_state=prev,
                        new_state=new_prior
                    )
                    self.registry.apply_adaptation(record)
                    
        # 3. Adapt Verification Priority based on Failure Genome
        for constraint, fm in introspection.failure_genome.items():
            if fm.frequency >= 10:
                prev = self.registry.get_verification_priority(constraint)
                new_priority = prev + 1.0 # Increase priority
                
                if new_priority != prev:
                    record = AdaptationRecord(
                        source_signal=f"Constraint {constraint} failed {fm.frequency} times",
                        target_component="VerificationPriority",
                        target_key=constraint,
                        adaptation_type="PriorityBoost",
                        previous_state=prev,
                        new_state=new_priority
                    )
                    self.registry.apply_adaptation(record)
