from datetime import UTC, datetime

from pydantic import BaseModel, Field


class EvidenceBroadcast(BaseModel):
    """
    ENP Message Type: EvidenceBroadcast
    Shares raw observations or findings.
    """
    evidence_id: str
    source: str
    provenance: str = "Unknown"
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    payload: str
    is_retracted: bool = False

class ClaimBroadcast(BaseModel):
    """
    ENP Message Type: ClaimBroadcast
    Shares hypotheses or theories.
    Strictly omits VerificationStatus and Confidence.
    """
    claim_id: str
    claim_text: str
    evidence_ids: list[str]
    assumptions: list[str]
    lineage_reference: str | None = None
    
    @classmethod
    def from_local_claim(cls, local_claim):
        """
        Creates a ClaimBroadcast from a local Claim object, intentionally stripping 
        local authority metrics like verification_status and confidence.
        """
        return cls(
            claim_id=local_claim.claim_id,
            claim_text=local_claim.claim_text,
            evidence_ids=[ev.source_id for ev in local_claim.evidence],
            assumptions=local_claim.assumptions,
            lineage_reference=getattr(local_claim, "lineage_reference", None)
        )

class ContradictionReport(BaseModel):
    """
    ENP Message Type: ContradictionReport
    Shares evidence-backed objections.
    """
    target_claim_id: str
    contradiction_source: str
    evidence_references: list[str]
    violated_constraint: str
    proof_reference: str | None = None

class OpportunityBroadcast(BaseModel):
    """
    ENP Message Type: OpportunityBroadcast
    Shares strategic directions based on Expected Information Gain.
    """
    opportunity_id: str
    knowledge_gap: str
    expected_information_gain: float
    required_evidence: list[str]
    estimated_cost: float
