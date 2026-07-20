
from pydantic import BaseModel, Field


class FailureMode(BaseModel):
    """Tracks the frequency and domain of specific unsat_core rejections."""
    constraint_key: str = Field(..., description="The Z3 constraint or rule that was violated")
    frequency: int = Field(default=0, description="Number of times this constraint failed")
    domains: dict[str, int] = Field(default_factory=dict, description="Counts of failures by domain/category")

class ReviewerPrecision(BaseModel):
    """Tracks correlation between a reviewer's approval and ultimate SAT/UNSAT outcome."""
    persona: str = Field(..., description="The reviewer persona (e.g., Statistician)")
    total_reviews: int = Field(default=0)
    true_positives: int = Field(default=0, description="Approved and SAT")
    false_positives: int = Field(default=0, description="Approved but UNSAT")
    precision: float = Field(default=0.0)

class AssumptionTracker(BaseModel):
    """Maps an assumption string to its historical success/failure rate."""
    assumption: str = Field(...)
    total_claims: int = Field(default=0)
    supported: int = Field(default=0)
    contradicted: int = Field(default=0)
    unresolved: int = Field(default=0)
    support_rate: float = Field(default=0.0)

class LessonLearned(BaseModel):
    """The flagship output containing actionable meta-knowledge."""
    lesson: str = Field(..., description="The generated lesson text")
    confidence: float = Field(..., description="Statistical confidence in this lesson")
    evidence_count: int = Field(..., description="Number of observations backing this lesson")
    related_constraints: list[str] = Field(default_factory=list)
