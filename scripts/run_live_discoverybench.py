import json
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

import yaml

try:
    import litellm
except ImportError:
    litellm = None

from aidp.discovery.workflow import AutonomousDiscoveryOrchestrator
from aidp.evaluation.discovery_bench import BenchmarkCase
from aidp.evaluation.metrics import MetricEvaluator
from aidp.governance.engine import ScientificGovernanceEngine
from aidp.intelligence.providers.capabilities import ProviderCapabilities, ReasoningTier
from aidp.intelligence.providers.llm import LLMProvider
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.routing import RoutingPolicy


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)

def load_dataset(dataset_path: str) -> list:
    with open(dataset_path, encoding="utf-8") as f:
        return json.load(f)

def format_failure(exception, response_obj=None):
    return {
        "root_cause": str(exception),
        "stack_trace": traceback.format_exc(),
        "provider_response": str(response_obj) if response_obj else "No response",
        "recovery_recommendation": "Verify API keys and network connectivity."
    }

def run_live_llm(model: str, prompt: str, config: dict):
    if not litellm:
        raise ImportError("litellm is required for live execution.")
        
    start_time = time.time()
    response = None
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.get("temperature", 0.1),
            max_tokens=config.get("max_tokens", 1000),
            num_ctx=4096
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
    
    return {
        "status": "success",
        "output": response.choices[0].message.content,
        "runtime": runtime,
        "cost": cost,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "model": response.model
    }

def preflight_checks(config, dataset_size, evidence_dir):
    print("Running execution preflight checks...")
    
    # 1. Semantic Evaluator check
    if not litellm:
        print("PREFLIGHT FAILED: litellm is not installed. Semantic evaluator unavailable.")
        sys.exit(1)
        
    # 2. Ollama model check
    reasoning_model = config["models"]["baseline_c_aidp"]["reasoning_model"]
    if "ollama" in reasoning_model:
        model_name = reasoning_model.replace("ollama/", "")
        try:
            import urllib.request
            req = urllib.request.Request("http://localhost:11434/api/tags")
            with urllib.request.urlopen(req, timeout=5) as response:
                tags = json.loads(response.read().decode())
                models = [m["name"] for m in tags.get("models", [])]
                if model_name not in models and model_name + ":latest" not in models:
                    print(f"PREFLIGHT FAILED: Required model '{model_name}' missing from Ollama.")
                    sys.exit(1)
        except Exception as e:
            print(f"PREFLIGHT FAILED: Ollama service unavailable. {e}")
            sys.exit(1)
            
    # 3. Cache Completeness check
    cache_file = evidence_dir / "BENCHMARK_CORPUS_CACHE.json"
    if not cache_file.exists():
        print("PREFLIGHT FAILED: Frozen retrieval cache file missing.")
        sys.exit(1)
        
    with open(cache_file) as f:
        cache = json.load(f)
        # Checking if it has at least as many keys as the dataset size
        if len(cache) < dataset_size:
            print(f"PREFLIGHT FAILED: Cache incomplete. Found {len(cache)} entries, need {dataset_size}.")
            sys.exit(1)
            
    print("Preflight checks passed.")

def load_or_init(file_path):
    if file_path.exists():
        with open(file_path) as f:
            return json.load(f)
    return []

def main():
    base_dir = Path(__file__).parent.parent
    config_path = base_dir / "scripts" / "benchmark_execution_config.yaml"
    dataset_path = base_dir / "src" / "aidp" / "evaluation" / "data" / "discovery_bench_v1.json"
    evidence_dir = base_dir / "docs" / "evaluation" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    config = load_config(str(config_path))
    dataset = load_dataset(str(dataset_path))
    
    pilot_subset = dataset
    
    # Run preflight checks before anything else
    preflight_checks(config, len(pilot_subset), evidence_dir)
    
    print(f"Starting Live M11.6.11 Full AIDP Scientific Evaluation ({len(pilot_subset)} cases).")
    
    # Setup AIDP Pipeline components
    routing_policy = RoutingPolicy()
    
    reasoning_model = config["models"]["baseline_c_aidp"]["reasoning_model"]
    llm_provider = LLMProvider(model_name=reasoning_model, api_key="dummy" if "ollama" in reasoning_model else None)
    
    caps = ProviderCapabilities(
        structured_output=True,
        tool_calling=False,
        streaming=False,
        vision=False,
        max_context=8000,
        supports_json_schema=True,
        reasoning_tier=ReasoningTier.EXPERT,
        cost_per_1m_input_tokens=0.0,
        cost_per_1m_output_tokens=0.0
    )
    routing_policy.register_provider("primary_local", llm_provider, caps)
    
    gateway = IntelligenceGateway(routing_policy=routing_policy)
    orchestrator = AutonomousDiscoveryOrchestrator(gateway=gateway)
    governance = ScientificGovernanceEngine()

    # P0-3: Reproducibility - Freeze benchmark retrieval context via monkey-patching
    try:
        from aidp.knowledge.connectors.pubmed_connector import PubMedConnector
        original_fetch = PubMedConnector.fetch_literature_provenance
        
        cache_file = evidence_dir / "BENCHMARK_CORPUS_CACHE.json"
        retrieval_cache = {}
        if cache_file.exists():
            with open(cache_file) as f:
                retrieval_cache = json.load(f)
                
        def mock_fetch(self, query, max_date=None):
            cache_key = f"{query}_{max_date}"
            if cache_key in retrieval_cache:
                from aidp.knowledge.provenance import ProvenanceEntry
                entries = []
                for item in retrieval_cache[cache_key]:
                    entries.append(ProvenanceEntry(**item))
                return entries
                
            results = original_fetch(self, query, max_date=max_date)
            from dataclasses import asdict
            retrieval_cache[cache_key] = [asdict(r) for r in results]
            with open(cache_file, "w") as f:
                json.dump(retrieval_cache, f, indent=2)
            return results
            
        PubMedConnector.fetch_literature_provenance = mock_fetch
    except ImportError:
        pass

    # Incremental persistence setup
    provenance_file = evidence_dir / "LIVE_BENCHMARK_EXECUTION_PROVENANCE.json"
    raw_outputs_file = evidence_dir / "LIVE_RAW_OUTPUTS.json"
    retrieval_evidence_file = evidence_dir / "LIVE_RETRIEVAL_EVIDENCE.json"
    governance_audit_file = evidence_dir / "LIVE_GOVERNANCE_AUDIT.json"
    runtime_metrics_file = evidence_dir / "LIVE_RUNTIME_METRICS.json"
    
    provenance_records = load_or_init(provenance_file)
    raw_outputs = load_or_init(raw_outputs_file)
    retrieval_evidence = load_or_init(retrieval_evidence_file)
    governance_audit = load_or_init(governance_audit_file)
    runtime_metrics = load_or_init(runtime_metrics_file)

    completed_cases = {record["case_id"] for record in raw_outputs}
    print(f"Found {len(completed_cases)} already completed cases.")
    
    def save_incremental():
        with open(provenance_file, "w") as f:
            json.dump(provenance_records, f, indent=2)
        with open(raw_outputs_file, "w") as f:
            json.dump(raw_outputs, f, indent=2)
        with open(retrieval_evidence_file, "w") as f:
            json.dump(retrieval_evidence, f, indent=2)
        with open(governance_audit_file, "w") as f:
            json.dump(governance_audit, f, indent=2)
        with open(runtime_metrics_file, "w") as f:
            json.dump(runtime_metrics, f, indent=2)
            
    for case in pilot_subset:
        case_id = case["id"]
        
        if case_id in completed_cases:
            print(f"\n--- Skipping case: {case_id} (already completed) ---")
            continue
            
        print(f"\n--- Executing case: {case_id} using AIDP Orchestrator ---")
        
        start_time = time.time()
        session = None
        governance_passed = False
        governance_reason = ""
        
        try:
            session = orchestrator.run_discovery_cycle(
                question=case["query"], 
                historical_cutoff_date=case.get("historical_cutoff_date")
            )
            
            # Run governance
            if session.hypothesis:
                governance_passed, governance_reason = governance.evaluate_hypothesis(session.hypothesis)
            else:
                governance_passed, governance_reason = False, "No hypothesis generated."
                
        except Exception as e:
            runtime = time.time() - start_time
            print(f"Failed {case_id}. Exception: {e}")
            run_identifier = f"run_{case_id}_{int(time.time())}"
            
            provenance_records.append({
                "case_id": case_id,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "FAILED",
                "run_identifier": run_identifier,
                "runtime": runtime
            })
            
            raw_outputs.append({
                "case_id": case_id,
                "status": "FAILED",
                "failure_details": format_failure(e)
            })
            save_incremental()
            continue

        runtime = time.time() - start_time
        cost = 0.0
        input_tokens = sum(t.input_tokens for t in gateway.traces)
        output_tokens = sum(t.output_tokens for t in gateway.traces)
        
        run_identifier = f"run_{case_id}_{int(time.time())}"
        
        baseline_model = config["models"]["baseline_a"]["primary"]
        retrieved_docs = session.knowledge_context.get("documents", []) if session else []
        context_str = "\n".join([str(d) for d in retrieved_docs])
        prompt = f"Context:\n{context_str}\n\nSolve this scientific query: {case['query']}"
        baseline_result = run_live_llm(baseline_model, prompt, config["models"]["baseline_a"])
        
        baseline_output = baseline_result.get("output", "Baseline FAILED")
        aidp_output = orchestrator.generate_report(session)
        
        evaluator = MetricEvaluator()
        bm_case = BenchmarkCase(**case)
        
        aidp_metrics = evaluator.evaluate(bm_case, {
            "output": aidp_output,
            "evidence_used": session.hypothesis.get("evidence_links", []) if session.hypothesis else []
        })
        
        baseline_metrics = evaluator.evaluate(bm_case, {
            "output": baseline_output,
            "evidence_used": []
        })
        
        provenance_records.append({
            "case_id": case_id,
            "timestamp": datetime.utcnow().isoformat(),
            "provider": "ollama",
            "model": reasoning_model,
            "runtime": runtime,
            "token_usage": {"input": input_tokens, "output": output_tokens},
            "cost": cost,
            "run_identifier": run_identifier
        })
        
        raw_outputs.append({
            "case_id": case_id,
            "baseline_output": baseline_output,
            "rag_output": "Executed internally",
            "aidp_output": aidp_output
        })
        
        runtime_metrics.append({
            "case_id": case_id,
            "aidp_metrics": aidp_metrics,
            "baseline_metrics": baseline_metrics,
            "aidp_runtime": runtime,
            "baseline_runtime": baseline_result.get("runtime", 0.0),
            "aidp_token_usage": input_tokens + output_tokens,
            "baseline_token_usage": baseline_result.get("input_tokens", 0) + baseline_result.get("output_tokens", 0)
        })
        
        retrieval_evidence.append({
            "case_id": case_id,
            "papers_retrieved": session.knowledge_context.get("documents", []),
            "evidence_quality_scores": []
        })
        
        governance_audit.append({
            "case_id": case_id,
            "governance_checks_executed": [c.__class__.__name__ for c in governance.checkers],
            "decisions": [
                {"passed": governance_passed, "reason": governance_reason}
            ]
        })
        
        print(f"Completed {case_id}. Final State: {session.state.value}")
        save_incremental()
            
    print("\nLive Execution finished.")
    print(f"Evidence artifacts saved incrementally to {evidence_dir}")

if __name__ == "__main__":
    main()
