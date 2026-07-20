#!/usr/bin/env python3
import json
import os
try:
    from fastapi import FastAPI, HTTPException
except ImportError:
    print("FastAPI not installed. Mocking for demonstration...")
    FastAPI = lambda: type("MockAPI", (), {"get": lambda self, path: lambda f: f})

app = FastAPI()

def load_community_evidence():
    path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "ANTIGRAVITY_EVIDENCE_V1", "community_evidence.json")
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.get("/api/leaderboard")
def get_leaderboard():
    """
    Phase 8/9: Real-time telemetry router.
    Serves live benchmark aggregation to public researchers via REST.
    """
    evidence = load_community_evidence()
    if not evidence:
        raise HTTPException(status_code=404, detail="No evidence found.")
        
    models = {}
    for entry in evidence:
        model = entry.get("model")
        leak = entry.get("leakage_rate")
        if not model or leak is None: continue
        
        if model not in models:
            models[model] = {"evals": 0, "sum_leakage": 0.0}
        models[model]["evals"] += 1
        models[model]["sum_leakage"] += leak
        
    response = []
    for m, stats in models.items():
        response.append({
            "model": m,
            "evals": stats["evals"],
            "avg_leakage": stats["sum_leakage"] / stats["evals"]
        })
        
    return sorted(response, key=lambda x: x["avg_leakage"])

if __name__ == "__main__":
    print("==================================================")
    print(" PHASE 8: FASTAPI TELEMETRY ROUTER")
    print("==================================================\n")
    print("[SUCCESS] API Router configured. Run with: uvicorn src.aidp.api.benchmark_router:app --reload")
    
    # Mocking a live request
    print("\nMocking request to /api/leaderboard:")
    try:
        res = get_leaderboard()
        print(json.dumps(res, indent=2))
    except Exception as e:
        print(f"API Error: {e}")
