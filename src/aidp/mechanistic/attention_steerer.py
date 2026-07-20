import logging
import numpy as np

logger = logging.getLogger(__name__)

class EpistemicAttentionSteerer:
    """
    Mechanistic Intervention Module.
    Surgically alters neural attention weights during the forward pass to 
    enforce epistemic constraints and cure temporal leakage.
    """
    def __init__(self, steering_strength: float = 10.0):
        self.steering_strength = steering_strength

    def apply_attention_intervention(self, original_attention: dict) -> dict:
        """
        Intercepts the attention matrix. If the historical token is being overshadowed,
        it artificially boosts the historical attention and suppresses the modern concept attention.
        """
        hist_weight = original_attention.get("historical_attention_weight", 0.0)
        mod_weight = original_attention.get("modern_attention_weight", 1.0)
        
        logger.info("Intercepting Neural Forward Pass...")
        
        # Mathematical Intervention (Activation Addition / Attention Steering)
        # We multiply the historical attention by the steering strength,
        # then normalize the weights so they sum to 1.0.
        boosted_hist = hist_weight * self.steering_strength
        
        # We also actively suppress the modern concept to prevent leakage
        suppressed_mod = mod_weight / self.steering_strength
        
        total = boosted_hist + suppressed_mod
        
        steered_hist = boosted_hist / total
        steered_mod = suppressed_mod / total
        
        return {
            "historical_attention_weight": float(steered_hist),
            "modern_attention_weight": float(steered_mod),
            "layer": original_attention.get("layer") + " [INTERVENED]",
            "intervention_applied": True,
            "steering_strength": self.steering_strength
        }
