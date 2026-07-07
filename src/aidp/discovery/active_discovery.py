import uuid
from typing import Any


class ActiveDiscoveryPlanner:
    """
    Ranks experimental designs based on Expected Information Gain (EIG) rather than base confidence.
    This implements a mock Bayesian Experimental Design / Thompson Sampling routing logic.
    """

    def __init__(self) -> None:
        pass

    def prioritize_experiments(
        self, hypotheses: list[dict[str, Any]], designs: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Calculates EIG for each experiment based on the uncertainty (risk) of its hypothesis.
        Higher uncertainty * structural integrity = Higher EIG.
        """
        tasks = []

        hyp_map = {h.get("id"): h for h in hypotheses}

        for design in designs:
            hyp_id = design.get("hypothesisId")
            hypothesis = hyp_map.get(hyp_id, {})

            # Expected Information Gain is a function of current uncertainty (risk) and the potential payoff
            # An experiment on a 99% confident hypothesis has low EIG.
            # An experiment on a 50% confident hypothesis with high impact has high EIG.
            confidence = hypothesis.get("confidence", 0.5)
            risk = hypothesis.get("risk", 0.5)

            # Simple mock heuristic for EIG: Variance * Base Impact
            # Variance is highest when confidence is near 0.5
            variance = 4.0 * confidence * (1.0 - confidence)  # peaks at 1.0 when conf=0.5

            base_impact = hypothesis.get("expectedInformationGain", 1.0)

            calculated_eig = variance * base_impact * (1.0 + risk)

            tasks.append(
                {
                    "id": f"task-{uuid.uuid4()}",
                    "experimentalDesignId": design.get("id"),
                    "expectedInformationGain": calculated_eig,
                    "executionCost": 100.0,  # Mock cost
                }
            )

        # Sort by EIG descending
        tasks.sort(key=lambda x: x["expectedInformationGain"], reverse=True)
        return tasks
