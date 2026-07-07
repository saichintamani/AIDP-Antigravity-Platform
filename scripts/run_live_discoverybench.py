import json
import os
import time
import yaml
import traceback
from pathlib import Path
from datetime import datetime

try:
    import litellm
except ImportError:
    litellm = None

def load_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def load_dataset(dataset_path: str) -> list:
    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)

class ExecutionSafetyController:
    def __init__(self, budget_cap: float):
        self.budget_cap = budget_cap
        self.current_cost = 0.0

    def add_cost(self, cost: float):
        self.current_cost += cost
        if self.current_cost > self.budget_cap:
            raise RuntimeError(f"BUDGET CAP EXCEEDED. Cumulative cost: ${self.current_cost:.4f}")

def format_failure(exception, response_obj=None):
    return {
        "root_cause": str(exception),
        "stack_trace": traceback.format_exc(),
        "provider_response": str(response_obj) if response_obj else "No response",
        "recovery_recommendation": "Verify API keys in environment variables and network connectivity."
    }

def run_live_llm(model: str, prompt: str, config: dict, safety_controller: ExecutionSafetyController):
    if not litellm:
        raise ImportError("litellm is required for live execution.")
        
    start_time = time.time()
    response = None
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.get("temperature", 0.1),
            max_tokens=config.get("max_tokens", 1000)
        )
    except Exception as e:
        runtime = time.time() - start_time
        return {
            "status": "failure",
            "runtime": runtime,
            "failure_details": format_failure(e, response)
        }
        
    runtime = time.time() - start_time
    cost = litellm.completion_cost(completion_response=response) or 0.0
    
    safety_controller.add_cost(cost)
    
    return {
        "status": "success",
        "output": response.choices[0].message.content,
        "runtime": runtime,
        "cost": cost,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "model": response.model
    }

def main():
    base_dir = Path(__file__).parent.parent
    config_path = base_dir / "scripts" / "benchmark_execution_config.yaml"
    dataset_path = base_dir / "src" / "aidp" / "evaluation" / "data" / "discovery_bench_v1.json"
    evidence_dir = base_dir / "docs" / "evaluation" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    config = load_config(str(config_path))
    budget_cap = config.get("live_execution", {}).get("budget_cap_usd", 10.0)
    
    safety = ExecutionSafetyController(budget_cap)
    dataset = load_dataset(str(dataset_path))
    
    # 1 Easy, 1 Medium, 1 Hard case
    pilot_subset = [
        case for case in dataset if case["id"] in ["case-oncology-001", "case-oncology-002", "case-oncology-003"]
    ][:3]
    if not pilot_subset:
        pilot_subset = dataset[:3]
        
    print(f"Starting Live M11.6.2 Execution. Budget Cap: ${budget_cap}")
    
    provenance_records = []
    raw_outputs = []
    retrieval_evidence = []
    governance_audit = []
    runtime_metrics = []
    
    for case in pilot_subset:
        case_id = case["id"]
        print(f"\n--- Executing case: {case_id} ---")
        
        # Simulate Live LLM Call for Baseline A
        model = config["models"]["baseline_a"]["primary"]
        prompt = f"Solve this scientific query: {case['query']}"
        
        result = run_live_llm(model, prompt, config["models"]["baseline_a"], safety)
        
        run_identifier = f"run_{case_id}_{int(time.time())}"
        
        if result["status"] == "success":
            provenance_records.append({
                "case_id": case_id,
                "timestamp": datetime.utcnow().isoformat(),
                "provider": "openai",
                "model": result["model"],
                "runtime": result["runtime"],
                "token_usage": {"input": result["input_tokens"], "output": result["output_tokens"]},
                "cost": result["cost"],
                "run_identifier": run_identifier
            })
            
            raw_outputs.append({
                "case_id": case_id,
                "baseline_output": result["output"],
                "rag_output": "Not executed (Baseline A only)",
                "aidp_output": "Not executed (Baseline A only)"
            })
            
            runtime_metrics.append({
                "case_id": case_id,
                "scientific_correctness": 0.0,  # Needs post-evaluation against expected
                "evidence_quality": 0.0,
                "hallucination_rate": 0.0,
                "calibration": 0.0,
                "runtime": result["runtime"],
                "token_usage": result["input_tokens"] + result["output_tokens"],
                "cost": result["cost"]
            })
            print(f"Completed {case_id} using {model}. Cost: ${result['cost']:.4f}")
            
        else:
            # Handle strict failure reporting requirements
            provenance_records.append({
                "case_id": case_id,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "FAILED",
                "run_identifier": run_identifier
            })
            
            # Store failure trace natively in the raw outputs structure
            raw_outputs.append({
                "case_id": case_id,
                "status": "FAILED",
                "failure_details": result["failure_details"]
            })
            print(f"Failed {case_id}. Trace recorded in evidence JSON.")
            
        # Record empty/failed retrieval and governance since it failed or didn't run C
        retrieval_evidence.append({
            "case_id": case_id,
            "papers_retrieved": [],
            "evidence_quality_scores": []
        })
        governance_audit.append({
            "case_id": case_id,
            "governance_checks_executed": [],
            "decisions": []
        })
            
    # Write the 5 required Live Evidence artifacts
    with open(evidence_dir / "LIVE_BENCHMARK_EXECUTION_PROVENANCE.json", "w") as f:
        json.dump(provenance_records, f, indent=2)
        
    with open(evidence_dir / "LIVE_RAW_OUTPUTS.json", "w") as f:
        json.dump(raw_outputs, f, indent=2)
        
    with open(evidence_dir / "LIVE_RETRIEVAL_EVIDENCE.json", "w") as f:
        json.dump(retrieval_evidence, f, indent=2)
        
    with open(evidence_dir / "LIVE_GOVERNANCE_AUDIT.json", "w") as f:
        json.dump(governance_audit, f, indent=2)
        
    with open(evidence_dir / "LIVE_RUNTIME_METRICS.json", "w") as f:
        json.dump(runtime_metrics, f, indent=2)

    print(f"\nLive Execution finished. Total cost: ${safety.current_cost:.4f}")
    print(f"Evidence artifacts written to {evidence_dir}")

if __name__ == "__main__":
    main()
