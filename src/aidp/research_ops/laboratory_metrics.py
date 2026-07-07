from dataclasses import dataclass


@dataclass
class LaboratoryMetrics:
    total_spend_usd: float = 0.0
    total_tokens_consumed: int = 0
    research_throughput: int = 0
    hypotheses_generated: int = 0
    experiments_completed: int = 0
    novel_discoveries: int = 0
    average_confidence_gain: float = 0.0

    @property
    def cost_per_discovery(self) -> float:
        if self.novel_discoveries == 0:
            return 0.0
        return self.total_spend_usd / self.novel_discoveries

    @property
    def cost_per_hypothesis(self) -> float:
        if self.hypotheses_generated == 0:
            return 0.0
        return self.total_spend_usd / self.hypotheses_generated


class KPIDashboard:
    """
    Maintains a real-time view of the laboratory's operational and scientific health.
    """

    def __init__(self) -> None:
        self.metrics = LaboratoryMetrics()

    def log_discovery(self) -> None:
        self.metrics.novel_discoveries += 1

    def log_spend(self, usd: float, tokens: int) -> None:
        self.metrics.total_spend_usd += usd
        self.metrics.total_tokens_consumed += tokens

    def get_snapshot(self) -> LaboratoryMetrics:
        return self.metrics
