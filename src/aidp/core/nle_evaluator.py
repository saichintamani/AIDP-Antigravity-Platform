import logging

logger = logging.getLogger(__name__)

class NLE_Evaluator:
    """
    Natural Language Explanation (NLE) Evaluator.
    Forces the AI Judge to write a logical proof of why a text contains temporal leakage,
    preventing black-box scoring and exposing evaluator bias.
    """
    def __init__(self):
        pass

    def evaluate_with_nle(self, prompt: str, generated_text: str, historical_constraint: str) -> dict:
        """
        Simulates an LLM-as-a-judge extracting an NLE before scoring.
        In production, this would call an API like GPT-4 or Claude.
        """
        # We mathematically simulate the NLE extraction based on keyword presence
        # to guarantee execution without API keys.
        modern_terms = ["quantum", "internet", "modern", "computer", "relativity"]
        
        found_terms = [t for t in modern_terms if t in generated_text.lower()]
        
        if found_terms:
            nle = (f"The constraint was set to '{historical_constraint}'. "
                   f"However, the generated text explicitly references '{found_terms[0]}'. "
                   f"This concept did not exist in {historical_constraint}, constituting a severe temporal leak.")
            score = 1  # 1 = Biased / Leaked
        else:
            nle = (f"The text maintains strict coherence with the '{historical_constraint}' constraint. "
                   "No anachronistic terminology was detected.")
            score = 0  # 0 = Unbiased / Clean

        return {
            "nle_reasoning": nle,
            "bias_score": score
        }
