import math
from dataclasses import dataclass


@dataclass
class SimulationResult:
    expected_information_gain: float
    risk_of_failure: float
    prior_probability_of_success: float
    variance: float = 0.0


class SimulationEngine:
    """
    Calculates mathematical metrics like Expected Information Gain (EIG)
    from the Digital Twin's predicted outcomes.
    """

    def _calculate_shannon_entropy(self, probabilities: list[float]) -> float:
        entropy = 0.0
        for p in probabilities:
            if p > 0.0:
                entropy -= p * math.log2(p)
        return entropy

    def evaluate_outcomes(
        self, prior_probs: list[float], post_probs: list[float], success_prob: float
    ) -> SimulationResult:
        prior_entropy = self._calculate_shannon_entropy(prior_probs)
        post_entropy = self._calculate_shannon_entropy(post_probs)

        eig = max(0.0, prior_entropy - post_entropy)

        # Max entropy for 3 states is ~1.58
        normalized_eig = min(max(eig / 1.58, 0.0), 1.0)

        return SimulationResult(
            expected_information_gain=normalized_eig,
            risk_of_failure=1.0 - success_prob,
            prior_probability_of_success=success_prob,
        )
