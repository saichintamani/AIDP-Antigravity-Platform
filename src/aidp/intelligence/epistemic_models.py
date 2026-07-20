import uuid
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from aidp.explainability.causal_explanation import CausalExplanation


class VerificationStatus(StrEnum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    UNCERTAIN = "uncertain"

class ConfidenceOntology(BaseModel):
    evidence_confidence: float = Field(0.0, description="Is there sufficient evidence?")
    verification_confidence: float = Field(0.0, description="Did deterministic checks pass?")
    assumption_confidence: float = Field(0.0, description="How many assumptions remain unverified?")
    consensus_confidence: float = Field(0.0, description="Do reviewers agree?")
    knowledge_confidence: float = Field(0.0, description="Does the knowledge graph support or contradict it?")
    reproducibility_confidence: float = Field(0.0, description="Would another run likely reach the same conclusion?")
    overall_confidence: float = Field(0.0, description="Aggregate confidence score")

class ConfidenceLineageEvent(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    dimension: str = Field(..., description="The ontology dimension that changed")
    delta: float = Field(..., description="The numerical change (+ or -)")
    reason: str = Field(..., description="Human-readable explanation for the shift")

class EpistemicEvidence(BaseModel):
    source_id: str = Field(..., description="Unique identifier for the source (e.g., PubMed ID, URL, or Internal DB ID)")
    source_type: str = Field(..., description="Type of source (e.g., 'literature', 'database_query', 'statistical_rule')")
    extracted_text: str = Field(..., description="The exact text or data snippet relied upon")
    relevance_score: float = Field(1.0, description="Confidence in the relevance of this evidence to the claim")
    ontology_tags: list[str] = Field(default_factory=list, description="Semantic ontology tags (e.g., 'Astrophysics', 'GeneralRelativity')")
    mathematical_constraints: list[str] = Field(default_factory=list, description="Explicit equations or numerical bounds extracted (e.g., 'strain < 10^-21')")
    entity_relationships: list[str] = Field(default_factory=list, description="Knowledge graph triples (e.g., 'LIGO -> measures -> Strain')")

class EpistemicReview(BaseModel):
    reviewer_role: str = Field(..., description="The persona/role of the reviewer (e.g., 'Statistician', 'Ethicist')")
    vote: str = Field(..., description="Approve, Reject, or Abstain")
    rationale: str = Field(..., description="Detailed explanation for the vote")
    identified_confounds: list[str] = Field(default_factory=list, description="Any confounding variables or flaws identified")

class EpistemicClaim(BaseModel):
    claim_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    claim_text: str = Field(..., description="The core assertion, hypothesis, or proposed plan")
    evidence: list[EpistemicEvidence] = Field(default_factory=list, description="The explicit evidence backing this claim")
    symbolic_formulation: dict | None = Field(None, description="Serialized constraint representation for Z3")
    assumptions: list[str] = Field(..., description="Explicit assumptions made by the generator that are not fully backed by evidence")
    explanation: CausalExplanation | None = Field(None, description="The causal trace for why this claim was accepted, rejected, or revised.")
    confidence: ConfidenceOntology | None = Field(None, description="Mathematically auditable confidence ontology")
    confidence_lineage: list[ConfidenceLineageEvent] = Field(default_factory=list, description="Auditable history of belief revision")
    verification_status: VerificationStatus = Field(default=VerificationStatus.PENDING)
    generated_by: str = Field(..., description="The module or agent that generated this claim (e.g., 'ClinicalTrialPlanner')")
    reviewed_by: list[EpistemicReview] = Field(default_factory=list)

    def update_confidence(self, dimension: str, delta: float, reason: str):
        if not self.confidence:
            self.confidence = ConfidenceOntology()
        
        # apply delta
        current_val = getattr(self.confidence, dimension, self.confidence.overall_confidence)
        new_val = max(0.0, min(1.0, current_val + delta))
        setattr(self.confidence, dimension, new_val)
        
        # update overall
        self.confidence.overall_confidence = new_val
        
        # track lineage
        self.confidence_lineage.append(
            ConfidenceLineageEvent(dimension=dimension, delta=delta, reason=reason)
        )

Claim = EpistemicClaim
