from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from aidp.meta_learning.adaptation_models import AdaptationRecord


class SystemMetrics(BaseModel):
    """A snapshot of global health for evaluating adaptations."""
    verification_pass_rate: float = Field(default=0.0)
    contradiction_rate: float = Field(default=0.0)
    avg_reviewer_precision: float = Field(default=0.0)

class MetricPrediction(BaseModel):
    metric_name: str = Field(...)
    expected_delta: float = Field(...)

class HypothesisStatus(StrEnum):
    PENDING = "pending"
    EVALUATING = "evaluating"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class AdaptationHypothesis(BaseModel):
    hypothesis_id: str = Field(...)
    adaptation: AdaptationRecord = Field(...)
    
    # Second-order learning parameters
    predictions: list[MetricPrediction] = Field(default_factory=list)
    observation_window_runs: int = Field(default=100)
    
    # State tracking
    status: HypothesisStatus = Field(default=HypothesisStatus.PENDING)
    baseline_metrics: SystemMetrics | None = None
    runs_elapsed: int = Field(default=0)
    
    # Outcome
    actual_deltas: dict[str, float] = Field(default_factory=dict)
    evaluated_at: datetime | None = None
