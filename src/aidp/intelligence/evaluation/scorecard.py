import time
from dataclasses import dataclass, field

from aidp.intelligence.evaluation.harness import EvaluationResult


@dataclass
class ProviderScorecard:
    provider_name: str
    historical_evaluations: list[EvaluationResult] = field(default_factory=list)
    last_updated: float = field(default_factory=time.time)

    @property
    def aggregate_success_rate(self) -> float:
        if not self.historical_evaluations:
            return 0.0
        return sum(e.success_rate for e in self.historical_evaluations) / len(
            self.historical_evaluations
        )

    @property
    def aggregate_avg_latency_ms(self) -> float:
        if not self.historical_evaluations:
            return 0.0
        return sum(e.avg_latency_ms for e in self.historical_evaluations) / len(
            self.historical_evaluations
        )


class ScorecardRegistry:
    _scorecards: dict[str, ProviderScorecard] = {}

    @classmethod
    def record_evaluation(cls, result: EvaluationResult) -> None:
        if result.provider_name not in cls._scorecards:
            cls._scorecards[result.provider_name] = ProviderScorecard(
                provider_name=result.provider_name
            )

        scorecard = cls._scorecards[result.provider_name]
        scorecard.historical_evaluations.append(result)
        scorecard.last_updated = time.time()

    @classmethod
    def get_scorecard(cls, provider_name: str) -> ProviderScorecard | None:
        return cls._scorecards.get(provider_name)
