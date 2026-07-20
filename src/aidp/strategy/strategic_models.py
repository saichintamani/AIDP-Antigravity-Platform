from pydantic import BaseModel, Field


class ResearchOpportunity(BaseModel):
    """
    A prioritized gap in knowledge representing where the system should focus its attention next.
    """
    opportunity_id: str = Field(...)
    target_claim_id: str = Field(..., description="The ID of the unresolved claim or hypothesis to investigate.")
    
    # Core Metrics
    uncertainty: float = Field(..., description="Current epistemic uncertainty (0.0 to 1.0)")
    impact: float = Field(..., description="Estimated downstream value if this uncertainty is resolved (0.0 to 1.0)")
    cost: float = Field(..., description="Estimated cost of investigation (e.g., compute, time) (0.1 to 1.0)")
    
    # Calculated Intelligence
    expected_information_gain: float = Field(..., description="How much uncertainty is mathematically expected to disappear (EIG)")
    
    # Final Output
    priority: float = Field(default=0.0, description="The final ranking score, calculated dynamically by the engine.")
