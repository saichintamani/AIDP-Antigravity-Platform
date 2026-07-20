from typing import Any

import requests


class GenerativeHarness:
    """
    Unlike the SelectionHarness, which asks the AI to rank pre-written candidates,
    the GenerativeHarness forces the AI to invent a novel experimental approach 
    based solely on the provided EpistemicEvidence.
    """
    def __init__(self, model_name: str = "llama3.1:8b", endpoint: str = "http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.endpoint = endpoint

    def generate_hypothesis(self, case) -> dict[str, Any]:
        """
        Sends the strict SciKG constraints to the model and requests a generated hypothesis.
        """
        prompt = self._build_generative_prompt(case)
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3, # Low temperature for highly logical reasoning
                "seed": 42
            }
        }
        
        try:
            response = requests.post(self.endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            return {
                "generated_hypothesis": data.get("response", "").strip(),
                "status": "success",
                "raw_response": data
            }
        except Exception as e:
            return {
                "generated_hypothesis": None,
                "status": "error",
                "error_message": str(e)
            }

    def _build_generative_prompt(self, case) -> str:
        prompt = "System: You are an elite scientific hypothesis generator. The year is the cutoff date for this case. You must NOT use any knowledge discovered after this time period.\n\n"
        prompt += f"Domain: {case.domain}\n"
        prompt += f"Time Window: {case.time_window}\n\n"
        prompt += "Based STRICTLY on the following evidence and mathematical constraints, formulate a single highly specific experimental or theoretical proposal that is most likely to lead to a breakthrough.\n\n"
        
        for i, ev in enumerate(case.known_evidence):
            prompt += f"Evidence {i+1}: {ev.extracted_text}\n"
            if hasattr(ev, 'mathematical_constraints') and ev.mathematical_constraints:
                prompt += f"Constraints: {', '.join(ev.mathematical_constraints)}\n"
            if hasattr(ev, 'entity_relationships') and ev.entity_relationships:
                prompt += f"Relationships: {', '.join(ev.entity_relationships)}\n"
            prompt += "\n"
            
        prompt += "Task: Output a 2-3 paragraph experimental proposal. Your proposal MUST explicitly address the mathematical constraints provided above.\n"
        prompt += "Proposal:"
        
        return prompt
