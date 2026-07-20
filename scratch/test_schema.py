import json
import asyncio
from aidp.discovery.debate import ScientificDebateEngine
from aidp.intelligence.providers.middleware import IntelligenceGateway
import dotenv

dotenv.load_dotenv()

async def test_domain_expert_schema():
    with open('C:/Users/saich/.gemini/antigravity-ide/brain/d017cc73-ba47-455a-8b4f-ae4d9a0b014b/SPL_VALIDATION_EVIDENCE.json') as f:
        data = json.load(f)

    # Pick case-oncology-004
    test_case = data[0]
    
    hypothesis = test_case["hypothesis"]
    # Ensure old evidence is 'Not provided' for the OLD test
    old_hypothesis = hypothesis.copy()
    old_hypothesis["evidence"] = "Not provided"
    
    from aidp.intelligence.providers.middleware import IntelligenceGateway
    from aidp.intelligence.providers.llm import LLMProvider
    from aidp.intelligence.providers.capabilities import ProviderCapabilities, ReasoningTier
    from aidp.intelligence.providers.routing import RoutingPolicy
    
    design = test_case["new_design"]
    
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
    debate_engine = ScientificDebateEngine(gateway)
    
    print("--- OLD DEBATE INPUTS ---")
    # Old Domain Expert Review (uses hypothesis["evidence"])
    old_domain = debate_engine._domain_expert_review(design, old_hypothesis)
    print(f"Domain Expert (Old): {old_domain.decision}")
    print(f"  Blocking: {old_domain.blockingIssues}")
    
    # Old Methodologist Review (uses design["protocol"])
    old_methodologist = debate_engine._methodologist_review(design)
    print(f"Methodologist (Old): {old_methodologist.decision}")
    print(f"  Blocking: {old_methodologist.blockingIssues}")
    
    print("\n--- NEW DEBATE INPUTS ---")
    # New Domain Expert Review (uses design["evidence_to_claim_mapping"])
    new_hypothesis_sim = {
        "claim": hypothesis["claim"],
        "hypothesis": hypothesis,
        "evidence": json.dumps(design.get("evidence_to_claim_mapping", [])) # SIMULATING THE FIX
    }
    new_domain = debate_engine._domain_expert_review(design, new_hypothesis_sim)
    print(f"Domain Expert (New): {new_domain.decision}")
    print(f"  Blocking: {new_domain.blockingIssues}")
    
    # New Methodologist Review (uses design["controls"], etc)
    # We will simulate the fix by modifying the private method manually, or just passing a mocked design.
    # Actually, we can monkey-patch it for this script just to see the result.
    def new_methodologist_review(self, design):
        def fallback():
            return None
        context = {
            "protocol": json.dumps({
                "controls": design.get("controls", []),
                "sampleSize": design.get("sampleSize", "Not provided"),
                "statisticalTest": design.get("statisticalTest", "Not provided")
            }),
            "experiment_flow": json.dumps(
                {
                    "independent": design.get("independentVariables", []),
                    "dependent": design.get("dependentVariables", []),
                }
            ),
            "confounders": design.get("confounders", "Not provided"),
        }
        return self._query_persona(
            "Methodologist", 
            # We must import CognitiveTaskType
            debate_engine.planner.execute_task.__globals__.get("CognitiveTaskType", None).METHODOLOGY_REVIEW, 
            context, 
            fallback
        )
    
    from aidp.intelligence.task_specification import CognitiveTaskType
    def mock_query(role, task_type, context, fallback_logic):
        return debate_engine._query_persona(role, task_type, context, fallback_logic)
        
    def new_methodologist_review_impl(design):
        context = {
            "protocol": json.dumps({
                "controls": design.get("controls", []),
                "sampleSize": design.get("sampleSize", "Not provided"),
                "statisticalTest": design.get("statisticalTest", "Not provided")
            }),
            "experiment_flow": json.dumps({
                "independent": design.get("independentVariables", []),
                "dependent": design.get("dependentVariables", []),
            }),
            "confounders": design.get("confounders", "Not provided"),
        }
        return mock_query("Methodologist", CognitiveTaskType.METHODOLOGY_REVIEW, context, lambda: None)
        
    new_methodologist = new_methodologist_review_impl(design)
    print(f"Methodologist (New): {new_methodologist.decision}")
    print(f"  Blocking: {new_methodologist.blockingIssues}")

if __name__ == "__main__":
    asyncio.run(test_domain_expert_schema())
