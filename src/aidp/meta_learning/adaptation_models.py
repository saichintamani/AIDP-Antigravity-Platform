import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class AdaptationRecord(BaseModel):
    """
    An immutable, auditable record of a system parameter changing based on evidence.
    """
    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    # What caused this adaptation?
    source_signal: str = Field(..., description="The lesson, frequency count, or metric that triggered this.")
    
    # What are we changing?
    target_component: str = Field(..., description="E.g., ReviewerWeights, AssumptionPriors, VerificationPriority")
    target_key: str = Field(..., description="E.g., 'Statistician', 'Protein A activates Protein B'")
    adaptation_type: str = Field(..., description="E.g., 'WeightUpdate', 'PriorAdjustment'")
    
    # The Delta
    previous_state: Any = Field(...)
    new_state: Any = Field(...)
