from dataclasses import dataclass


@dataclass
class ScientificTaskProposal:
    id: str
    name: str
    expected_impact: float  # 0.0 to 1.0
    information_gain: float  # 0.0 to 1.0
    novelty: float  # 0.0 to 1.0
    estimated_cost_usd: float
    estimated_time_hours: float
    risk_of_failure: float  # 0.0 to 1.0


class EconomicsEngine:
    """
    Scores proposed tasks based on their expected scientific Return on Investment (ROI).
    """

    def calculate_priority_score(self, task: ScientificTaskProposal) -> float:
        """
        Priority = (Expected Impact × Information Gain × Novelty) / (Cost × Time × Risk)
        """
        # Add epsilon to denominators to prevent division by zero
        numerator = task.expected_impact * task.information_gain * task.novelty

        # Risk is a penalty. High risk = high penalty. We use (1 + risk) or similar.
        # Cost and Time could be extremely small, use max to prevent blowup
        cost_factor = max(task.estimated_cost_usd, 0.01)
        time_factor = max(task.estimated_time_hours, 0.1)
        risk_factor = max(task.risk_of_failure, 0.05)

        denominator = cost_factor * time_factor * risk_factor

        return numerator / denominator
