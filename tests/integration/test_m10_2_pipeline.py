import json
from typing import Any

from aidp.discovery.debate import ScientificDebateEngine
from aidp.discovery.scientific_planning import WetLabPlanner
from aidp.intelligence.providers.capabilities import GEMINI_1_5_PRO_CAPABILITIES
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.routing import RoutingPolicy


class MockLLMProviderForPipeline:
    """Mocks the raw string output of an LLM responding to pipeline prompts."""

    def query(self, prompt: str, schema_hint: dict[str, Any] | None = None) -> Any:
        print(f"MOCK RECEIVED PROMPT:\n{prompt}")
        if "Evidence Linkage Validator" in prompt:
            payload = {
                "evidence_to_claim_mapping": [{"claim_component": "X causes Y", "supporting_evidence": "Found in text."}],
                "supporting_dois": ["10.123/456"],
                "unsupported_claims": [],
                "evidence_confidence": "High"
            }
            return f"```json\n{json.dumps(payload)}\n```"

        if "Experimental Methodology Generator" in prompt:
            payload = {
                "independent_variables": ["Variable X"],
                "dependent_variables": ["Variable Y"],
                "control_groups": [{"group_name": "Control", "purpose": "Baseline"}],
                "confounders_identified": ["None"],
                "success_criteria": "If X changes Y",
            }
            return f"```json\n{json.dumps(payload)}\n```"

        if "Statistical Design Validator" in prompt:
            payload = {
                "sample_size_recommendation": {"n_per_group": 30, "justification": "Standard"},
                "statistical_test": "ANOVA",
                "power_considerations": "High power",
                "reproducibility_notes": "Replicate 3 times",
            }
            return f"```json\n{json.dumps(payload)}\n```"

        if "Control Taxonomy Generator" in prompt:
            payload = {
                "controls": [
                    {
                        "type": "Negative",
                        "group_name": "Vehicle Control",
                        "isolated_variable": "Buffer",
                        "purpose_and_justification": "To ensure buffer has no effect"
                    }
                ]
            }
            return f"```json\n{json.dumps(payload)}\n```"

        if "Engineer Feasibility Generator" in prompt:
            payload = {
                "resource_estimation": "Standard compute",
                "cost_prediction": "Low",
                "failure_prediction": "Convergence failure",
                "critical_engineering_risks": ["Risk 1"]
            }
            return f"```json\n{json.dumps(payload)}\n```"

        if (
            "Statistician" in prompt
            or "Domain Expert" in prompt
            or "Methodologist" in prompt
            or "Ethicist" in prompt
            or "Engineer" in prompt
        ):
            # Responding to Debate Engine
            payload = {
                "reviewerName": "AI Reviewer",
                "role": "Reviewer",
                "confidence": 0.9,
                "blockingIssues": [],
                "suggestions": ["Looks acceptable."],
                "evidence": "Tested before.",
                "riskScore": 0.1,
                "decision": "approve",
            }
            return f"```json\n{json.dumps(payload)}\n```"

        return "{}"


def test_m10_2_end_to_end_pipeline() -> None:
    """
    Tests that a hypothesis correctly flows through the LLM-powered ExperimentPlanner
    and the LLM-powered ScientificDebateEngine.
    """
    provider = MockLLMProviderForPipeline()
    routing = RoutingPolicy()
    routing.register_provider("mock", provider, GEMINI_1_5_PRO_CAPABILITIES)
    gateway = IntelligenceGateway(routing_policy=routing)

    planner = WetLabPlanner(gateway=gateway)
    debate_engine = ScientificDebateEngine(gateway=gateway)

    hypothesis = {"id": "h_1", "claim": "X causes Y"}
    ledger_entry = {"id": "l_1", "readiness": "readyForExperiment"}
    knowledge_context = {"documents": []}

    # 1. Plan Experiment via LLM
    design = planner.design_experiment(hypothesis, ledger_entry, knowledge_context)

    assert "Variable X" in design["independentVariables"]
    assert "Variable Y" in design["dependentVariables"]
    assert design["successCriteria"] != ""

    # 2. Debate Experiment via LLM
    debate_record = debate_engine.evaluate_design(design, hypothesis)
    print(f"DEBATE RECORD: {debate_record}")

    assert debate_record["consensusReached"] is True
    assert debate_record["finalDecision"] == "approved"
    assert len(debate_record["critiques"]) == 5
    for critique in debate_record["critiques"]:
        assert critique["decision"] == "approve"
        assert len(critique["blockingIssues"]) == 0

    # Check Telemetry to ensure the Gateway actually processed all 8 calls
    # (3 for planner, 5 for debate)
    assert len(gateway.traces) == 8
