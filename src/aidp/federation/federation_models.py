from datetime import UTC, datetime

from pydantic import BaseModel, Field

from aidp.intelligence.epistemic_models import Claim, EpistemicEvidence


class FederatedEpistemicObject(BaseModel):
    """
    The transmission primitive for federation.
    Exchanges claims and evidence, but purposefully isolates confidence and verification status
    so the receiving node must independently verify.
    """
    federation_id: str = Field(...)
    sender_node_id: str = Field(...)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    # The actual payload
    claim: Claim = Field(...)
    evidence: list[EpistemicEvidence] = Field(default_factory=list)
    
    # Context that might be useful for local evaluation
    assumptions: list[str] = Field(default_factory=list)
    
    # We include the sender's confidence lineage for transparency/auditing, 
    # but the receiver should NOT use this to bypass local verification.
    sender_confidence: float = Field(default=0.0)
