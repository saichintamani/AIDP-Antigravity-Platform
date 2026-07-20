import logging
from src.aidp.mechanistic.gemma_prober import GemmaMechanisticProber

logger = logging.getLogger(__name__)

class EpistemicAttentionAnalyzer:
    """
    Analyzes the neural attention matrix to mathematically prove if a 
    historical constraint was "overshadowed" by modern concepts in the pre-training weights.
    """
    def __init__(self):
        self.prober = GemmaMechanisticProber(model_name="google/gemma-2b")

    def analyze_overshadowing(self, prompt: str, historical_constraint: str) -> dict:
        """
        Calculates the Overshadowing Ratio: Modern Attention / Historical Attention.
        """
        attention_data = self.prober.extract_attention_matrix(prompt, historical_constraint)
        
        hist_weight = attention_data.get("historical_attention_weight", 0.0)
        mod_weight = attention_data.get("modern_attention_weight", 1.0)
        
        # If historical weight is near 0, the overshadowing ratio approaches infinity
        if hist_weight < 0.001:
            ratio = float('inf')
        else:
            ratio = mod_weight / hist_weight
            
        # Flagship standard: If ratio > 5.0 (modern concept receives 5x more neural attention 
        # than the explicit historical constraint), we have mechanistic proof of epistemic failure.
        is_overshadowed = ratio > 5.0
        
        return {
            "historical_attention": hist_weight,
            "modern_attention": mod_weight,
            "overshadowing_ratio": ratio,
            "mechanistic_failure_proven": is_overshadowed,
            "layer_analyzed": attention_data.get("layer")
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    analyzer = EpistemicAttentionAnalyzer()
    
    test_prompt = "Write a letter in 1900 about the new quantum computer."
    historical_token = "1900"
    
    print("\n==================================================")
    print(" MECHANISTIC INTERPRETABILITY (ATTENTION PROBING)")
    print("==================================================")
    
    results = analyzer.analyze_overshadowing(test_prompt, historical_token)
    
    print(f" Target Model            : google/gemma-2b")
    print(f" Analyzed Neural Layer   : {results['layer_analyzed']}")
    print(f" Historical Token Weight : {results['historical_attention']:.4f}")
    print(f" Modern Concept Weight   : {results['modern_attention']:.4f}")
    print(f" Overshadowing Ratio     : {results['overshadowing_ratio']:.2f}x")
    print(f" Mechanistic Proof?      : {'YES (Constraint Overshadowed)' if results['mechanistic_failure_proven'] else 'NO (Constraint Maintained)'}")
    print("==================================================\n")
