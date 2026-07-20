from datetime import datetime

from pydantic import BaseModel, Field


class EvidenceTrustScore(BaseModel):
    score: float = Field(ge=0.0, le=1.0, description="Normalized trust score")
    is_retracted: bool = False
    penalties_applied: list[str] = Field(default_factory=list)
    bonuses_applied: list[str] = Field(default_factory=list)

class EpistemicScorer:
    """
    Evaluates evidence quality before it reaches the reasoning layer.
    """
    
    def __init__(self):
        # In a real system, this connects to the Retraction Watch database
        self._mock_retracted_pmids = {"1001", "1002", "retracted_123"}
        
    def score_document(self, pmid: str, title: str, year: int) -> EvidenceTrustScore:
        """
        Generates a trust score based on metadata.
        """
        score = 0.8  # Base starting score
        penalties = []
        bonuses = []
        is_retracted = False
        
        # 1. Retraction Check (Fatal)
        if pmid in self._mock_retracted_pmids or "retracted" in title.lower():
            is_retracted = True
            score = 0.0
            penalties.append("FATAL: Document is in retraction database.")
            return EvidenceTrustScore(score=score, is_retracted=is_retracted, penalties_applied=penalties, bonuses_applied=bonuses)
            
        # 2. Recency Decay
        current_year = datetime.now().year
        age = current_year - year
        if age > 10:
            penalty = min(0.3, (age - 10) * 0.02)
            score -= penalty
            penalties.append(f"Age penalty (-{penalty:.2f}): Document is {age} years old.")
        elif age <= 3:
            score += 0.1
            bonuses.append("Recency bonus (+0.10): Document is highly current.")
            
        # 3. Simulated Citation Impact (Mocked deterministically for stability)
        # In production, query Semantic Scholar for actual citation count
        pseudo_citation_count = sum(ord(c) for c in title) % 1000 
        if pseudo_citation_count > 800:
            score += 0.15
            bonuses.append("High impact bonus (+0.15): Widely cited.")
        elif pseudo_citation_count < 10:
            score -= 0.1
            penalties.append("Low impact penalty (-0.10): Sparse citations.")
            
        # Bound score
        score = max(0.1, min(1.0, score))
        
        return EvidenceTrustScore(
            score=round(score, 3),
            is_retracted=is_retracted,
            penalties_applied=penalties,
            bonuses_applied=bonuses
        )
