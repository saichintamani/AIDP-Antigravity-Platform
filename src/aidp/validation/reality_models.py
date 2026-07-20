
from pydantic import BaseModel

from aidp.intelligence.epistemic_models import EpistemicEvidence


class RealWorldEvidence(EpistemicEvidence):
    """
    Evidence subclassed to include real-world publication reality markers.
    """
    is_retracted: bool = False
    citation_bias_score: float = 0.0 # 0.0 = neutral, 1.0 = highly biased toward popular consensus
    expert_consensus_score: float = 0.5 # 0.0 = rejected by experts, 1.0 = universally accepted
    
class HistoricalCase(BaseModel):
    """
    A specific moment in scientific history to replay.
    """
    case_id: str
    description: str
    prevailing_assumptions: list[str]
    prevailing_evidence: list[RealWorldEvidence]
    anomalous_evidence: list[RealWorldEvidence]
    historical_resolution_claim: str
