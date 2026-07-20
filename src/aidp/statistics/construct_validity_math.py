import logging
import math

logger = logging.getLogger(__name__)

class ConstructValidityMath:
    """
    Mathematical framework to calculate the Construct Validity of the Antigravity hypothesis.
    It isolates the effect of the RLHF Optimizer from the Base Neural Representation.
    """
    
    @staticmethod
    def calculate_delta(base_stats: dict, rlhf_stats: dict) -> dict:
        """
        Calculates the delta between Base Model leakage and RLHF Model leakage.
        """
        base_mean = base_stats.get('mean_bias', 0.0)
        rlhf_mean = rlhf_stats.get('mean_bias', 0.0)
        
        # Avoid division by zero
        if rlhf_mean == 0:
            return {"delta": 0.0, "construct_validity_score": 0.0, "verdict": "No Leakage"}
            
        # Delta: How much MORE does the RLHF model leak than the base model?
        # If delta is high, the leakage is heavily driven by RLHF.
        delta = rlhf_mean - base_mean
        
        # Construct Validity Score (CVS) ranges from 0.0 to 1.0
        # 1.0 = Base model leaks exactly as much as RLHF (Flaw is fundamental)
        # 0.0 = Base model doesn't leak at all, only RLHF leaks (Flaw is an RLHF artifact)
        cvs = max(0.0, min(1.0, (base_mean / rlhf_mean) if rlhf_mean > 0 else 1.0))
        
        verdict = "Strong Validity (Structural Flaw)" if cvs > 0.6 else "Weak Validity (RLHF Artifact)"
        
        return {
            "base_mean": base_mean,
            "rlhf_mean": rlhf_mean,
            "absolute_delta": delta,
            "construct_validity_score": cvs,
            "verdict": verdict
        }

    @staticmethod
    def check_hdi_overlap(base_stats: dict, rlhf_stats: dict) -> bool:
        """
        Checks if the 95% HDI bounds of the Base model overlap with the RLHF model.
        If they overlap, the difference between Base and RLHF is not statistically significant.
        """
        base_lower = base_stats.get('hdi_lower', 0.0)
        base_upper = base_stats.get('hdi_upper', 0.0)
        
        rlhf_lower = rlhf_stats.get('hdi_lower', 0.0)
        rlhf_upper = rlhf_stats.get('hdi_upper', 0.0)
        
        # Overlap occurs if the start of one is before the end of the other, and vice versa
        overlap = (base_lower <= rlhf_upper) and (rlhf_lower <= base_upper)
        return overlap
