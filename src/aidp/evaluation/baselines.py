from aidp.evaluation.schemas import HistoricalReplayCase


class LLMBaselineEvaluator:
    """
    Simulates a standard LLM / RAG baseline evaluating a historical case without
    AIDP's Epistemic Constraint Solving or Truth Maintenance System.
    """
    def __init__(self, model_name: str = "Standard-LLM-RAG"):
        self.model_name = model_name
        
    def evaluate_case(self, case: HistoricalReplayCase) -> dict[str, float]:
        """
        Takes a HistoricalReplayCase and returns a mock scoring for the candidate experiments.
        In a real run, this would call out to an LLM API. Here, we simulate a baseline
        that struggles to differentiate the historical winner from highly plausible decoys.
        Returns a dictionary mapping candidate_text -> score (0.0 to 1.0).
        """
        scores = {}
        len(case.candidate_experiments)
        
        # Simulate baseline behavior: it tends to rank conventional experiments higher
        # because they align with the "known_evidence" consensus more strongly than the
        # paradigm shift (historical_winner), which looks like an anomaly.
        
        for idx, candidate in enumerate(case.candidate_experiments):
            if candidate == case.historical_winner:
                # The baseline struggles with paradigm shifts, giving it a middling score
                scores[candidate] = 0.5 
            else:
                # Decoys that align with prevailing consensus get scored highly
                if idx == 0:
                    scores[candidate] = 0.8
                elif idx == 1:
                    scores[candidate] = 0.7
                else:
                    scores[candidate] = 0.4
                    
        return scores
