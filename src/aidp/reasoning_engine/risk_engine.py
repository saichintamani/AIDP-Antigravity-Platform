from dataclasses import dataclass


@dataclass
class RiskProfile:
    scientific_risk: float  # e.g., low probability of success
    economic_risk: float  # e.g., high cost
    execution_risk: float  # e.g., requires complex setup
    overall_risk: float


class RiskEngine:
    """
    Scores the multi-dimensional risk of an experiment.
    """

    def evaluate_risk(self, probability_of_success: float, cost_usd: float) -> RiskProfile:
        sci_risk = 1.0 - probability_of_success

        # Assume max comfortable spend for a single experiment is $1000
        eco_risk = min(cost_usd / 1000.0, 1.0)

        # Mock execution risk
        exe_risk = 0.5

        overall = (sci_risk * 0.5) + (eco_risk * 0.3) + (exe_risk * 0.2)

        return RiskProfile(sci_risk, eco_risk, exe_risk, overall)
