import json
import sys
import time
import traceback
from pathlib import Path

import yaml

try:
    import litellm
except ImportError:
    litellm = None

from aidp.discovery.scientific_planning import AblationConfig
from aidp.discovery.workflow import AutonomousDiscoveryOrchestrator
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

def preflight_checks(config, dataset_size, evidence_dir):
    print("Running execution preflight checks...")
    
    if not litellm:
        print("PREFLIGHT FAILED: litellm is not installed. Semantic evaluator unavailable.")
        sys.exit(1)
        
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
            
    cache_file = evidence_dir / "BENCHMARK_CORPUS_CACHE.json"
    if not cache_file.exists():
        print("PREFLIGHT FAILED: Frozen retrieval cache file missing.")
        sys.exit(1)
        
    with open(cache_file) as f:
        cache = json.load(f)
        if len(cache) < dataset_size:
            print(f"PREFLIGHT FAILED: Cache incomplete. Found {len(cache)} entries, need {dataset_size}.")
            sys.exit(1)
            
    print("Preflight checks passed.")

def main():
    base_dir = Path(__file__).parent.parent
    config_path = base_dir / "scripts" / "benchmark_execution_config.yaml"
    dataset_path = base_dir / "src" / "aidp" / "evaluation" / "data" / "discovery_bench_v1.json"
    evidence_dir = base_dir / "docs" / "evaluation" / "evidence"
    
    config = load_config(str(config_path))
    dataset = load_dataset(str(dataset_path))
    
    # Run a small subset for ablation testing (e.g. 3 cases)
    pilot_subset = dataset[:3]
    
    preflight_checks(config, len(pilot_subset), evidence_dir)
    
    print(f"Starting Phase 6 Ablation Evaluation ({len(pilot_subset)} cases).")
    
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
    
    # Freeze retrieval
    try:
        from aidp.knowledge.connectors.pubmed_connector import PubMedConnector
        
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
            return []
            
        PubMedConnector.fetch_literature_provenance = mock_fetch
    except ImportError:
        pass

    ablations = [
        ("Full_AIDP", AblationConfig(enable_spl=True, enable_schema_sync=True, enable_falsifiability=True, enable_power_analyzer=True)),
        ("No_SPL", AblationConfig(enable_spl=False, enable_schema_sync=True, enable_falsifiability=True, enable_power_analyzer=True)),
        ("No_Falsifiability", AblationConfig(enable_spl=True, enable_schema_sync=True, enable_falsifiability=False, enable_power_analyzer=True)),
        ("No_Power_Analyzer", AblationConfig(enable_spl=True, enable_schema_sync=True, enable_falsifiability=True, enable_power_analyzer=False)),
        ("No_Schema_Sync", AblationConfig(enable_spl=True, enable_schema_sync=False, enable_falsifiability=True, enable_power_analyzer=True)),
    ]

    results = []
    
    # Track reviewer rejections per configuration
    reviewer_rejections = {name: [] for name, _ in ablations}

    for name, config_obj in ablations:
        print("\n======================================")
        print(f"Running Ablation: {name}")
        print("======================================")
        
        orchestrator = AutonomousDiscoveryOrchestrator(gateway=gateway, ablation_config=config_obj)
        
        total_runtime = 0.0
        successes = 0
        failures = 0
        
        for case in pilot_subset:
            case_id = case["id"]
            print(f"  -> Executing case: {case_id}")
            
            start_time = time.time()
            session = orchestrator.run_discovery_cycle(
                question=case["query"], 
                historical_cutoff_date=case.get("historical_cutoff_date")
            )
            runtime = time.time() - start_time
            total_runtime += runtime
            
            if session.state.value == "APPROVED":
                successes += 1
            else:
                failures += 1
                if session.debate_record and "critiques" in session.debate_record:
                    for critique in session.debate_record["critiques"]:
                        if critique.get("decision") in ["reject", "approve with conditions"]:
                            reviewer_rejections[name].extend(critique.get("blockingIssues", []))
                
        results.append({
            "ablation": name,
            "successes": successes,
            "failures": failures,
            "total_runtime_s": total_runtime,
            "approval_rate": successes / len(pilot_subset),
            "rejections": reviewer_rejections[name]
        })

    print("\n\n=== ABLATION RESULTS ===")
    for r in results:
        print(f"{r['ablation']}: Approval Rate={r['approval_rate']*100:.1f}% | Runtime={r['total_runtime_s']:.2f}s | Rejections={len(r['rejections'])}")
        
    with open(base_dir / "docs" / "evaluation" / "evidence" / "ABLATION_RESULTS.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
