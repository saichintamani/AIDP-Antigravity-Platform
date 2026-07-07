from typing import Any


class DiscoveryTelemetry:
    """
    Captures discovery-specific metrics such as EIG, reviewer disagreement,
    and hypothesis generation rates, elevating telemetry beyond simple engineering metrics.
    """

    def __init__(self) -> None:
        self.metrics = {
            "hypotheses_generated": 0,
            "hypotheses_rejected": 0,
            "contradictions_discovered": 0,
            "counterfactuals_evaluated": 0,
            "total_information_gain": 0.0,
            "reviewer_disagreement_count": 0,
            "causal_graph_revisions": 0,
        }

    def record_hypothesis_generation(self, count: int = 1) -> None:
        self.metrics["hypotheses_generated"] += count

    def record_hypothesis_rejection(self, count: int = 1) -> None:
        self.metrics["hypotheses_rejected"] += count

    def record_contradiction(self, count: int = 1) -> None:
        self.metrics["contradictions_discovered"] += count

    def record_counterfactual(self, count: int = 1) -> None:
        self.metrics["counterfactuals_evaluated"] += count

    def record_information_gain(self, gain: float) -> None:
        self.metrics["total_information_gain"] += gain

    def record_reviewer_disagreement(self, count: int = 1) -> None:
        self.metrics["reviewer_disagreement_count"] += count

    def record_causal_graph_revision(self, count: int = 1) -> None:
        self.metrics["causal_graph_revisions"] += count

    def get_summary(self) -> dict[str, Any]:
        avg_eig = 0.0
        if self.metrics["hypotheses_generated"] > 0:
            avg_eig = self.metrics["total_information_gain"] / self.metrics["hypotheses_generated"]

        return {
            "raw_metrics": self.metrics,
            "derived_metrics": {
                "average_information_gain": avg_eig,
                "rejection_rate": self.metrics["hypotheses_rejected"]
                / max(1, self.metrics["hypotheses_generated"]),
            },
        }
