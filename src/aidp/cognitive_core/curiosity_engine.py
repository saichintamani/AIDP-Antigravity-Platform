from dataclasses import dataclass


@dataclass
class ResearchDirection:
    id: str
    description: str
    target_entity: str
    related_entities: list[str]


class CuriosityEngine:
    """
    Scores potential research directions based on a Curiosity Heuristic.
    """

    def __init__(
        self,
        novelty_weight: float = 1.0,
        uncertainty_weight: float = 1.0,
        impact_weight: float = 1.0,
        eig_weight: float = 1.0,
        cost_weight: float = 1.0,
    ):
        self.w_novelty = novelty_weight
        self.w_uncertainty = uncertainty_weight
        self.w_impact = impact_weight
        self.w_eig = eig_weight
        self.w_cost = cost_weight

    def _estimate_novelty(self, direction: ResearchDirection) -> float:
        # In full system, checks WorldModel for existence of similar relationships
        return 0.8

    def _estimate_uncertainty(self, direction: ResearchDirection) -> float:
        # Checks subjective logic confidence of existing related edges
        return 0.9

    def _estimate_impact(self, direction: ResearchDirection) -> float:
        # Based on user feedback: relies on semantic level (e.g., Disease > Protein > Gene)
        # Can also be supplemented by LLM scoring
        return 0.7

    def _estimate_eig(self, direction: ResearchDirection) -> float:
        # Expected Information Gain (reduction in entropy of the world model)
        return 0.6

    def _estimate_cost(self, direction: ResearchDirection) -> float:
        # Estimated cost of experiments required to validate the direction
        return 0.4

    def score_direction(self, direction: ResearchDirection) -> float:
        """
        Calculates the Curiosity Score.
        Score = (Novelty + Uncertainty + Potential Impact + Expected Information Gain) - Research Cost
        """
        novelty = self._estimate_novelty(direction)
        uncertainty = self._estimate_uncertainty(direction)
        impact = self._estimate_impact(direction)
        eig = self._estimate_eig(direction)
        cost = self._estimate_cost(direction)

        score = (
            (self.w_novelty * novelty)
            + (self.w_uncertainty * uncertainty)
            + (self.w_impact * impact)
            + (self.w_eig * eig)
        ) - (self.w_cost * cost)

        return max(0.0, score)
