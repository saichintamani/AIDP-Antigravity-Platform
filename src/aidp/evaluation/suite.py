from typing import Any


class ScientificEvaluationSuite:
    """
    Automates the quantification of AIDP's performance across campaigns.
    """

    def __init__(self) -> None:
        self.metrics: dict[str, Any] = {
            "discovery_quality_novelty": [],
            "discovery_quality_validity": [],
            "evidence_quality_score": [],
            "calibration_error": [],
            "cost_efficiency_eig_per_usd": [],
            "reproducibility_variance": [],
        }

    def evaluate_campaign_mock(self, domain: str) -> dict[str, float]:
        """
        Mocks the evaluation of a completed campaign.
        In production, this would parse the DebateGraph and final output.
        """
        # Simulated metrics based on domain
        base_novelty = 0.85 if domain == "Oncology" else 0.75

        result = {
            "novelty": base_novelty,
            "validity": 0.90,
            "evidence": 0.88,
            "calibration": 0.05,  # Low error is good
            "cost_efficiency": 0.45,  # EIG / USD
            "reproducibility": 0.02,  # Variance
        }

        self.metrics["discovery_quality_novelty"].append(result["novelty"])
        self.metrics["discovery_quality_validity"].append(result["validity"])
        self.metrics["evidence_quality_score"].append(result["evidence"])
        self.metrics["calibration_error"].append(result["calibration"])
        self.metrics["cost_efficiency_eig_per_usd"].append(result["cost_efficiency"])
        self.metrics["reproducibility_variance"].append(result["reproducibility"])

        return result

    def aggregate_metrics(self) -> dict[str, float]:
        """
        Returns the averaged metrics across all evaluated campaigns.
        """

        def _avg(l: list[float]) -> float:
            return sum(l) / len(l) if l else 0.0

        return {k: _avg(v) for k, v in self.metrics.items()}
