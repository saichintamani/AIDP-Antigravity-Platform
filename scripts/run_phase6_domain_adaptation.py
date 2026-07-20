import json
from pathlib import Path

try:
    import litellm
except ImportError:
    litellm = None

from aidp.discovery.workflow import AutonomousDiscoveryOrchestrator
from aidp.intelligence.providers.capabilities import ProviderCapabilities, ReasoningTier
from aidp.intelligence.providers.llm import LLMProvider
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.routing import RoutingPolicy


def main():
    base_dir = Path(__file__).parent.parent
    discovery_bench_path = base_dir / "src" / "aidp" / "evaluation" / "data" / "discovery_bench_v1.json"
    clinical_bench_path = base_dir / "src" / "aidp" / "evaluation" / "data" / "clinical_trials_bench_v1.json"
    
    with open(discovery_bench_path, encoding="utf-8") as f:
        discovery_case = json.load(f)[0]
        
    with open(clinical_bench_path, encoding="utf-8") as f:
        clinical_case = json.load(f)[0]
        
    print("Testing Domain-Aware Planning (Phase 6)")
    
    routing_policy = RoutingPolicy()
    # Mock API key for ollama, or real one if configured
    llm_provider = LLMProvider(model_name="ollama/llama3.1:8b", api_key="dummy")
    
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
    
    cases = [
        ("DiscoveryBench (Wet Lab)", discovery_case),
        ("ClinicalTrialsBench (Clinical)", clinical_case)
    ]
    
    results = []
    
    for bench_name, case in cases:
        print(f"\n--- Running: {bench_name} ---")
        print(f"Query: {case['query']}")
        
        session = orchestrator.run_discovery_cycle(
            question=case["query"], 
            historical_cutoff_date=case.get("historical_cutoff_date")
        )
        
        # Extract detected domain from trace
        detected_domain = "UNKNOWN"
        for trace in session.trace:
            if trace["event"].startswith("Domain Detected:"):
                detected_domain = trace["event"].split(": ")[1]
                
        print(f"Detected Domain: {detected_domain}")
        print(f"Final State: {session.state.value}")
        
        if session.experiment_design:
            print("Experiment Design Output Sample:")
            print(json.dumps(session.experiment_design, indent=2)[:500] + "...\n")
        
        results.append({
            "benchmark": bench_name,
            "detected_domain": detected_domain,
            "state": session.state.value,
        })
        
    print("\n=== SUMMARY ===")
    for r in results:
        print(f"{r['benchmark']} -> Routed to: {r['detected_domain']} | Final State: {r['state']}")

if __name__ == "__main__":
    main()
