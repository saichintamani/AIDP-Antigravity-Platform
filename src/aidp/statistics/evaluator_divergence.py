import logging
import numpy as np

logger = logging.getLogger(__name__)

class EvaluatorDivergenceMath:
    """
    Calculates the statistical divergence between Human Evaluators and the AI Judge 
    using Cohen's Kappa for Inter-Rater Reliability.
    """
    
    @staticmethod
    def calculate_cohens_kappa(human_scores: list[int], ai_scores: list[int]) -> dict:
        """
        Calculates Cohen's Kappa score to measure evaluation coherence.
        """
        assert len(human_scores) == len(ai_scores), "Mismatch in evaluation sample sizes."
        
        n = len(human_scores)
        if n == 0:
            return {"kappa": 0.0, "agreement": 0.0, "verdict": "Insufficient Data"}
            
        # Confusion matrix variables
        both_leak = sum(1 for h, a in zip(human_scores, ai_scores) if h == 1 and a == 1)
        both_clean = sum(1 for h, a in zip(human_scores, ai_scores) if h == 0 and a == 0)
        ai_false_leak = sum(1 for h, a in zip(human_scores, ai_scores) if h == 0 and a == 1)
        ai_missed_leak = sum(1 for h, a in zip(human_scores, ai_scores) if h == 1 and a == 0)
        
        # Observed Agreement (P_o)
        p_o = (both_leak + both_clean) / n
        
        # Expected Agreement (P_e)
        p_human_leak = sum(human_scores) / n
        p_human_clean = 1.0 - p_human_leak
        
        p_ai_leak = sum(ai_scores) / n
        p_ai_clean = 1.0 - p_ai_leak
        
        p_e = (p_human_leak * p_ai_leak) + (p_human_clean * p_ai_clean)
        
        # Cohen's Kappa
        if p_e == 1.0:
            kappa = 1.0
        else:
            kappa = (p_o - p_e) / (1 - p_e)
            
        # Interpretation based on DeepMind/Anthropic standards
        if kappa > 0.8:
            verdict = "Flawless Coherence (Flagship Standard)"
        elif kappa > 0.6:
            verdict = "Substantial Coherence"
        elif kappa > 0.4:
            verdict = "Moderate Coherence (Evaluator Bias Detected)"
        else:
            verdict = "Poor Coherence (Severe Evaluator Divergence)"
            
        return {
            "kappa_score": float(kappa),
            "observed_agreement": float(p_o),
            "ai_false_positive_rate": float(ai_false_leak / n),
            "verdict": verdict
        }
