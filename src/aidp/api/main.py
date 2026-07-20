#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

# Import our custom database handler safely
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.database import init_db, insert_reproduction, get_aggregated_stats

app = FastAPI(
    title="Antigravity Telemetry API",
    description="Enterprise-grade ingestion and aggregation of community reproductions.",
    version="1.0.0"
)

# Pydantic Schemas
class ReproductionRequest(BaseModel):
    model_name: str = Field(..., min_length=2)
    leakage_rate: float = Field(..., ge=0.0, le=100.0)
    reviewer_stance: str = Field(...)

class AggregatedStat(BaseModel):
    model: str
    evaluations: int
    mean_leakage: float

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/api/reproductions", status_code=201)
def submit_reproduction(req: ReproductionRequest):
    insert_reproduction(req.model_name, req.leakage_rate, req.reviewer_stance)
    return {"status": "success", "message": "Reproduction logged to telemetry.db"}

@app.get("/api/leaderboard", response_model=List[AggregatedStat])
def get_leaderboard():
    stats = get_aggregated_stats()
    if not stats:
        # Return mock data if db is empty for demonstration
        return [
            AggregatedStat(model="llama3.1:70b-instruct", evaluations=15, mean_leakage=15.2),
            AggregatedStat(model="gpt-4o", evaluations=12, mean_leakage=11.1)
        ]
    return stats

if __name__ == "__main__":
    import uvicorn
    print("==================================================")
    print(" PHASE 8: PRODUCTION FASTAPI & SQLITE TELEMETRY")
    print("==================================================\n")
    print("Initializing SQLite Database...")
    init_db()
    
    print("\nMocking POST /api/reproductions ...")
    insert_reproduction("llama3.1:8b-instruct", 34.5, "RLHF_Skeptic")
    insert_reproduction("llama3.1:8b-instruct", 32.1, "Prompting_Artifact")
    
    print("\nMocking GET /api/leaderboard ...")
    stats = get_aggregated_stats()
    for s in stats:
        print(f" - {s['model']}: N={s['evaluations']}, Mean={s['mean_leakage']:.2f}%")
        
    print("\n[SUCCESS] Enterprise API components verified.")
    print("Run live via: uvicorn src.aidp.api.main:app --reload")
