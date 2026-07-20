
class AdversarialQueryGenerator:
    """
    Simulates Gemma-driven logic to invert a scientific query.
    Instead of searching for 'Drug X efficacy', it searches for 'Drug X toxicity'.
    This forces the system to confront negative evidence, breaking confirmation bias.
    """
    
    def __init__(self, gateway=None):
        self.gateway = gateway
        # Pre-computed adversarial mappings for MVP. 
        # In full production, Gemma would dynamically generate these antonyms.
        self._antonym_map = {
            "efficacy": ["toxicity", "adverse events", "ineffectiveness", "failure"],
            "upregulates": ["downregulates", "inhibits", "suppresses"],
            "activates": ["deactivates", "blocks", "antagonizes"],
            "causes": ["prevents", "cures", "ameliorates"],
            "increases": ["decreases", "reduces", "diminishes"],
            "safe": ["toxic", "lethal", "dangerous", "harmful"],
            "treats": ["worsens", "exacerbates", "fails to treat"]
        }
        
    def generate_adversarial_queries(self, base_query: str) -> list[str]:
        """
        Takes a base query (e.g., "Does Acetaminophen increase blood pressure")
        and returns adversarial variants (e.g., "Acetaminophen decreases blood pressure")
        """
        adversarial_queries = []
        words = base_query.lower().split()
        
        for i, word in enumerate(words):
            if word in self._antonym_map:
                for antonym in self._antonym_map[word]:
                    # Create a new query by substituting the word with its antonym
                    new_words = list(words)
                    new_words[i] = antonym
                    adversarial_queries.append(" ".join(new_words))
                    
        # If no explicit verbs were found, default to a broad toxicity search
        if not adversarial_queries:
            adversarial_queries.append(f"{base_query} toxicity OR adverse events OR failure")
            
        return adversarial_queries[:3]  # Cap at 3 to prevent query explosion
