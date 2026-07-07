import json
from typing import Optional, Any

from aidp.discovery.debate import ScientificDebateEngine
from aidp.discovery.experimental_design import ExperimentPlanner
from aidp.intelligence.providers.capabilities import GEMINI_1_5_PRO_CAPABILITIES
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.routing import RoutingPolicy


class MockLLMProviderForPipeline:
    """Mocks the raw string output of an LLM responding to pipeline prompts."""

    def query(self, prompt: str, schema_hint: Optional[dict[str, Any]] = None) -> Any:
        if "Scientific Methodologist" in prompt:
            # Responding to ExperimentPlanner
            payload = {
                "independentVariables": ["Variable X"],
                "dependentVariables": ["Variable Y"],
                "controls": ["Control Group 1"],
                "failureCriteria": "If X does not change Y, it is falsified.",
                "resourceEstimation": "Standard compute",
                "costPrediction": "Low",
                "failurePrediction": "Convergence failure",
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

    planner = ExperimentPlanner(gateway=gateway)
    debate_engine = ScientificDebateEngine(gateway=gateway)

    hypothesis = {"id": "h_1", "claim": "X causes Y"}
    ledger_entry = {"id": "l_1", "readiness": "readyForExperiment"}

    # 1. Plan Experiment via LLM
    design = planner.design_experiment(hypothesis, ledger_entry)

    assert "Variable X" in design["independentVariables"]
    assert "Variable Y" in design["dependentVariables"]
    assert design["failureCriteria"] != ""

    # 2. Debate Experiment via LLM
    debate_record = debate_engine.evaluate_design(design, hypothesis)
    print(f"DEBATE RECORD: {debate_record}")

    assert debate_record["consensusReached"] is True
    assert debate_record["finalDecision"] == "approved"
    assert len(debate_record["critiques"]) == 5
    for critique in debate_record["critiques"]:
        assert critique["decision"] == "approve"
        assert len(critique["blockingIssues"]) == 0

    # Check Telemetry to ensure the Gateway actually processed all 6 calls
    # (1 for planner, 5 for debate)
    assert len(gateway.traces) == 6
