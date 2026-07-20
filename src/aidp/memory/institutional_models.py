from datetime import UTC, datetime

from pydantic import BaseModel, Field

from aidp.meta_learning.adaptation_models import AdaptationRecord


class LongitudinalFailureMode(BaseModel):
    """Memory Layer 2: Failure Memory"""
    constraint_key: str = Field(...)
    total_occurrences: int = Field(default=0)
    first_seen: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_seen: datetime = Field(default_factory=lambda: datetime.now(UTC))

class LongitudinalAssumption(BaseModel):
    """Memory Layer 3: Assumption Memory"""
    assumption: str = Field(...)
    total_claims: int = Field(default=0)
    supported: int = Field(default=0)
    contradicted: int = Field(default=0)
    unresolved: int = Field(default=0)
    
    @property
    def support_rate(self) -> float:
        if self.total_claims == 0:
            return 0.0
        return self.supported / self.total_claims

class ReviewerSnapshot(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    precision: float = Field(...)

class LongitudinalReviewerStats(BaseModel):
    """Memory Layer 4: Reviewer Memory"""
    persona: str = Field(...)
    history: list[ReviewerSnapshot] = Field(default_factory=list)

class StrategyMemoryRecord(BaseModel):
    """Memory Layer 5: Strategy Memory"""
    question: str = Field(..., description="The original intent or goal")
    intervention: AdaptationRecord = Field(..., description="What the system changed to address this")
    outcome_metrics: dict[str, float] = Field(default_factory=dict, description="Measurable impacts")
    lesson_learned: str = Field(..., description="The reusable lesson from this strategy")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
