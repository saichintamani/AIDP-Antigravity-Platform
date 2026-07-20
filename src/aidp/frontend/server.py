#!/usr/bin/env python3
import json
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="AIDP Track E - Human Evaluation Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BENCHMARK_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'benchmarks', 'constraint_bench_100.json')
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'ANTIGRAVITY_EVIDENCE_V1')

os.makedirs(RESULTS_DIR, exist_ok=True)

class RankingSubmission(BaseModel):
    evaluator_id: str
    case_id: str
    ranked_candidates: List[str]
    confidence: str
    reasoning: str
    rubric_scores: dict
    feedback: str

@app.get("/api/cases")
def get_cases():
    """Serves the constraint_bench_100 dataset to the React UI."""
    try:
        with open(BENCHMARK_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        cases = data.get('cases', [])
        
        # Format the cases for the UI (the UI expects 'case_id', 'title', 'context', 'candidates')
        ui_cases = []
        for c in cases:
            ui_cases.append({
                "case_id": c.get('id', 'unknown'),
                "title": f"{c.get('domain', 'Unknown')} Paradigm Shift",
                "year": c.get('historical_cutoff_date', 'Unknown').split('-')[0],
                "context": c.get('prompt', ''),
                "candidates": [
                    {"id": "A", "description": c.get('ground_truth_discovery', '')},
                    {"id": "B", "description": "Alternative hypothesis based on contemporary theories."},
                    {"id": "C", "description": "A hallucinated hypothesis that sounds plausible but is wrong."}
                ]
            })
            
        return {"cases": ui_cases}
    except FileNotFoundError:
        print(f"File not found: {BENCHMARK_PATH}")
        raise HTTPException(status_code=404, detail="Benchmark dataset not found.")
    except Exception as e:
        print(f"Error loading cases: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/submit_ranking")
def submit_ranking(submission: RankingSubmission):
    """Saves human evaluator rankings locally to the Evidence Vault."""
    filename = f"human_eval_{submission.evaluator_id}.json"
    filepath = os.path.join(RESULTS_DIR, filename)
    
    # Load existing submissions if any
    data = {"evaluations": []}
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            pass
            
    # Append new submission
    data["evaluations"].append(submission.dict())
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    return {"status": "success"}

if __name__ == "__main__":
    print("Starting Track E Human Evaluation Server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
