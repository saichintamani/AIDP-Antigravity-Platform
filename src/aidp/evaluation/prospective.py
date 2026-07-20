import hashlib
from datetime import datetime

from pydantic import BaseModel


class ProspectiveChallenge(BaseModel):
    challenge_id: str
    domain: str
    current_date: str
    unresolved_question: str
    candidate_experiments: list[str]

class PredictionRecord(BaseModel):
    challenge_id: str
    timestamp: str
    ranked_predictions: list[str]
    cryptographic_hash: str

class ProspectivePredictionEngine:
    """
    Evaluates open scientific questions and generates a cryptographically 
    verifiable prediction for what experiment should be conducted next.
    """
    def generate_prediction(self, challenge: ProspectiveChallenge, aidp_rankings: list[str]) -> PredictionRecord:
        timestamp = datetime.now().isoformat()
        
        # We hash the predictions and the timestamp to create a verifiable record
        payload = f"{challenge.challenge_id}|{timestamp}|{'|'.join(aidp_rankings)}"
        signature = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        
        return PredictionRecord(
            challenge_id=challenge.challenge_id,
            timestamp=timestamp,
            ranked_predictions=aidp_rankings,
            cryptographic_hash=signature
        )
