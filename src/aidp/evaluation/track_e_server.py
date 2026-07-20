import json
import os
import random
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from tests.evaluation.datasets.historical_cases import ALL_CASES

app = FastAPI(title="AIDP Track E Human Evaluation API")

# Allow CORS for the Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RESULTS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "..", "tests", "evaluation", "results", "track_e_rankings.json"
)

# Ensure results file exists
os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "w") as f:
        json.dump([], f)

class RankingSubmission(BaseModel):
    evaluator_id: str
    field_of_expertise: str
    years_experience: str
    affiliation: str
    specialization: str
    case_id: str
    ranked_candidates: list[str]
    confidence: int
    reasoning: str
    rubric_scores: dict[str, int]
    feedback: str

@app.get("/api/cases")
def get_cases():
    cases_response = []
    for c in ALL_CASES:
        # Extract constraints vs evidence
        evidence = [ev.extracted_text for ev in c.known_evidence if not ev.extracted_text.startswith("CONSTRAINT:")]
        constraints = [ev.extracted_text for ev in c.known_evidence if "constraint" in ev.extracted_text.lower() or "limit" in ev.extracted_text.lower()]
        
        # Scramble the candidates to prevent ordering bias
        shuffled_candidates = list(c.candidate_experiments)
        random.shuffle(shuffled_candidates)
        
        cases_response.append({
            "case_id": c.case_id,
            "domain": c.domain,
            "time_window": c.time_window,
            "evidence": evidence,
            "constraints": constraints,
            "candidates": shuffled_candidates
        })
    return {"cases": cases_response}

@app.post("/api/rankings")
def submit_ranking(submission: RankingSubmission):
    try:
        with open(RESULTS_FILE) as f:
            data = json.load(f)
    except Exception:
        data = []
        
    data.append(submission.model_dump())
    
    with open(RESULTS_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
