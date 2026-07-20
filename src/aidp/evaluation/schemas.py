from pydantic import BaseModel, Field

from aidp.intelligence.epistemic_models import EpistemicEvidence


class HistoricalReplayCase(BaseModel):
    case_id: str = Field(..., description="Unique identifier for the historical case")
    domain: str = Field(..., description="Biology, materials science, physics, medicine, etc.")
    time_window: str = Field(..., description="Start and cutoff date before the breakthrough")
    known_evidence: list[EpistemicEvidence] = Field(..., description="Evidence available at the cutoff")
    constraints: list[str] = Field(default_factory=list, description="Explicit scientific constraints that cannot be violated")
    hidden_outcome: str = Field(..., description="Discovery intentionally withheld")
    candidate_experiments: list[str] = Field(..., description="Plausible next investigations available at the time")
    historical_winner: str = Field(..., description="What actually led to the breakthrough")
    evaluation_metric: str = Field(..., description="Top-1, Top-3, percentile rank, EIG score, etc.")
    difficulty_rating: str = Field(..., description="Easy, medium, hard, paradigm-shift")
