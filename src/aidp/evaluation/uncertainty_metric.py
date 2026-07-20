
from aidp.intelligence.epistemic_models import ConfidenceLineageEvent, ConfidenceOntology


class UncertaintyMetricsEngine:
    """
    Calculates the flagship metric: Epistemic Uncertainty Reduction.
    Uncertainty = 1.0 - Confidence.
    """
    
    @staticmethod
    def calculate_uncertainty_reduction(initial_confidence: ConfidenceOntology, final_confidence: ConfidenceOntology) -> float:
        """
        Returns the absolute reduction in uncertainty. 
        Positive value means uncertainty was reduced (system gained confidence).
        Negative value means uncertainty increased (system lost confidence).
        """
        initial_uncertainty = 1.0 - initial_confidence.overall_confidence
        final_uncertainty = 1.0 - final_confidence.overall_confidence
        
        return initial_uncertainty - final_uncertainty

    @staticmethod
    def identify_largest_uncertainty_reducer(lineage: list[ConfidenceLineageEvent]) -> str:
        """
        Analyzes the lineage to determine which system component reduced uncertainty the most.
        """
        if not lineage:
            return "None"
            
        # Group deltas by reason/component
        component_deltas = {}
        for event in lineage:
            if event.dimension == "overall_confidence":
                component_deltas[event.reason] = component_deltas.get(event.reason, 0.0) + event.delta
                
        if not component_deltas:
            return "None"
            
        # Return the component that had the largest positive delta (most confidence gained)
        return max(component_deltas.items(), key=lambda x: x[1])[0]
