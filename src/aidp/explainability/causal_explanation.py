
from pydantic import BaseModel, Field


class AcceptanceExplanation(BaseModel):
    """Explains why a claim is believed."""
    type: str = Field(default="acceptance")
    supporting_evidence_ids: list[str] = Field(default_factory=list)
    has_contradictions: bool = Field(default=False)
    reviewer_consensus: float = Field(default=1.0)
    individual_reviewer_scores: dict[str, float] = Field(default_factory=dict, description="Scores given by individual reviewer personas")
    summary: str = Field(..., description="Human-readable explanation of acceptance.")

class RejectionExplanation(BaseModel):
    """Explains why a claim failed, using mathematical proofs."""
    type: str = Field(default="rejection")
    unsat_core: list[str] = Field(..., description="The variables/constraints that caused the failure.")
    observed_values: dict = Field(default_factory=dict, description="The values that were observed in the claim.")
    counterfactual: str | None = Field(None, description="What minimal change would have reversed this decision?")
    summary: str = Field(..., description="Human-readable explanation of rejection.")

class BeliefRevisionExplanation(BaseModel):
    """Explains dynamic shifts in confidence over time."""
    type: str = Field(default="belief_revision")
    previous_confidence: float = Field(...)
    new_confidence: float = Field(...)
    delta: float = Field(...)
    causal_event: str = Field(..., description="The specific newly introduced evidence/claim that caused the shift.")
    summary: str = Field(..., description="Human-readable explanation of belief revision.")

class CausalExplanation(BaseModel):
    """A wrapper for the different types of explainability objects."""
    acceptance: AcceptanceExplanation | None = None
    rejection: RejectionExplanation | None = None
    revisions: list[BeliefRevisionExplanation] = Field(default_factory=list)
