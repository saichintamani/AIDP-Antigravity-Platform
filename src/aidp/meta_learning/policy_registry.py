
from aidp.meta_learning.adaptation_models import AdaptationRecord


class AdaptivePolicyRegistry:
    """
    Central, auditable store for dynamic system weights.
    Agents query this at runtime.
    """
    
    def __init__(self):
        # Default policies
        self.reviewer_weights: dict[str, float] = {}
        self.assumption_priors: dict[str, float] = {}
        self.verification_priorities: dict[str, float] = {}
        
        self.adaptation_history: list[AdaptationRecord] = []
        
    def get_reviewer_weight(self, persona: str) -> float:
        return self.reviewer_weights.get(persona, 1.0)
        
    def get_assumption_prior(self, assumption: str) -> float:
        return self.assumption_priors.get(assumption, 0.5)
        
    def get_verification_priority(self, constraint: str) -> float:
        return self.verification_priorities.get(constraint, 1.0)
        
    def apply_adaptation(self, record: AdaptationRecord):
        """Applies an adaptation and stores the record for auditability."""
        if record.target_component == "ReviewerWeights":
            self.reviewer_weights[record.target_key] = record.new_state
        elif record.target_component == "AssumptionPriors":
            self.assumption_priors[record.target_key] = record.new_state
        elif record.target_component == "VerificationPriority":
            self.verification_priorities[record.target_key] = record.new_state
        else:
            raise ValueError(f"Unknown target component: {record.target_component}")
            
        self.adaptation_history.append(record)
        
    def rollback_adaptation(self, record_id: str):
        """Reverses an adaptation based on its ID."""
        record_to_revert = None
        for record in self.adaptation_history:
            if record.record_id == record_id:
                record_to_revert = record
                break
                
        if not record_to_revert:
            raise ValueError(f"Record {record_id} not found in history.")
            
        # Revert the state
        if record_to_revert.target_component == "ReviewerWeights":
            self.reviewer_weights[record_to_revert.target_key] = record_to_revert.previous_state
        elif record_to_revert.target_component == "AssumptionPriors":
            self.assumption_priors[record_to_revert.target_key] = record_to_revert.previous_state
        elif record_to_revert.target_component == "VerificationPriority":
            self.verification_priorities[record_to_revert.target_key] = record_to_revert.previous_state
            
        # Remove from history
        self.adaptation_history.remove(record_to_revert)
