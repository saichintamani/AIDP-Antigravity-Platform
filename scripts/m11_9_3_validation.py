import json
import re
import os
import sys

# Ensure src is in path if not already
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.llm import LLMProvider
from aidp.intelligence.providers.capabilities import ProviderCapabilities, ReasoningTier
from aidp.intelligence.providers.routing import RoutingPolicy
from aidp.intelligence.reasoning_planner import ReasoningPlanner
from aidp.discovery.scientific_planning import ScientificPlanningLayer
from aidp.discovery.debate import ScientificDebateEngine

def extract_hypothesis(aidp_output: str) -> dict:
    claim_match = re.search(r'\*\*Claim:\*\* (.*?)\n', aidp_output)
    rationale_match = re.search(r'\*\*Rationale:\*\* (.*?)\n', aidp_output)
    
    claim = claim_match.group(1) if claim_match else "N/A"
    rationale = rationale_match.group(1) if rationale_match else "N/A"
    
    return {
        "claim": claim, 
        "rationale": rationale
    }

def main():
    target_cases = [
        "case-oncology-004",
        "case-genetics-002",
        "case-genetics-003",
        "case-neuroscience-003",
        "case-immunology-003",
        "case-materials-002"
    ]
    
    # Load old traces
    raw_outputs_path = os.path.join("docs", "evaluation", "evidence", "LIVE_RAW_OUTPUTS.json")
    with open(raw_outputs_path, "r", encoding="utf-8") as f:
        raw_outputs = json.load(f)
        
    retrieval_path = os.path.join("docs", "evaluation", "evidence", "LIVE_RETRIEVAL_EVIDENCE.json")
    with open(retrieval_path, "r", encoding="utf-8") as f:
        retrieval_evidence = json.load(f)
        
    # Build maps
    old_traces = {item["case_id"]: item for item in raw_outputs if item["case_id"] in target_cases}
    old_evidence = {item["case_id"]: item for item in retrieval_evidence if item.get("case_id") in target_cases}

    # Setup Routing and Gateway
    routing_policy = RoutingPolicy()
    llm_provider = LLMProvider(model_name="ollama/llama3.2:3b", api_key="dummy")
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

    # ScientificPlanningLayer expects a gateway, not a planner!
    spl = ScientificPlanningLayer(gateway)
    debate = ScientificDebateEngine(gateway)

    results = []
    
    print("Starting SPL Validation across 6 cases...")

    for case_id in target_cases:
        print(f"\nEvaluating {case_id}...")
        
        if case_id not in old_traces:
            print(f"Skipping {case_id}, not found in RAW OUTPUTS.")
            continue
        
        hypothesis = extract_hypothesis(old_traces[case_id]["aidp_output"])
        
        papers = []
        if case_id in old_evidence:
            papers = old_evidence[case_id].get("papers_retrieved", [])
            
        knowledge_context = {"documents": papers}
        ledger_entry = {
            "case_id": case_id,
            "readiness": "readyForExperiment"
        }
        
        try:
            print(f"  Running SPL for {case_id}...")
            new_design = spl.design_experiment(hypothesis, ledger_entry, knowledge_context)
            
            print(f"  Running Debate for {case_id}...")
            debate_result = debate.evaluate_design(new_design, hypothesis)
            debate_decision = debate_result["finalDecision"]
            critiques = debate_result["critiques"]
            
            results.append({
                "case_id": case_id,
                "hypothesis": hypothesis,
                "old_critiques": old_traces[case_id]["aidp_output"].split("## 4. Scientific Review & Consensus")[1] if "## 4. Scientific Review & Consensus" in old_traces[case_id]["aidp_output"] else "N/A",
                "new_design": new_design,
                "new_decision": debate_decision,
                "new_critiques": critiques
            })
            print(f"  Decision: {debate_decision}")
        except Exception as e:
            print(f"  Error processing {case_id}: {e}")

    report_path = os.path.join(os.path.dirname(__file__), "..", "scratch", "spl_validation_results.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"\nValidation complete. Raw results saved to {report_path}")

if __name__ == "__main__":
    main()
