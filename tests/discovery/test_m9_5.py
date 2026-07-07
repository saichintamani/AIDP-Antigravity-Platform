import json

from aidp.discovery.debate import ScientificDebateEngine
from aidp.intelligence.providers.capabilities import GEMINI_1_5_PRO_CAPABILITIES
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.routing import RoutingPolicy
from typing import Optional


class SmartMockProvider:
    def query(self, prompt: str, schema_hint: Optional[dict] = None) -> str:
        role = "Reviewer"
        if "Statistician" in prompt:
            role = "Statistician"
        elif "Domain Expert" in prompt:
            role = "Domain Expert"
        elif "Methodologist" in prompt:
            role = "Methodologist"
        elif "Ethicist" in prompt:
            role = "Ethicist"
        elif "Engineer" in prompt:
            role = "Engineer"

        # Check for bad designs
        is_bad_controls = "Controls: []" in prompt
        is_bad_criteria = "will see if there is an effect" in prompt

        if role == "Statistician" and is_bad_controls:
            payload = {
                "reviewerName": f"AI {role}",
                "role": role,
                "confidence": 0.9,
                "blockingIssues": ["Missing controls!"],
                "suggestions": ["Add controls"],
                "evidence": "",
                "riskScore": 0.9,
                "decision": "reject",
            }
        elif role == "Statistician" and is_bad_criteria:
            payload = {
                "reviewerName": f"AI {role}",
                "role": role,
                "confidence": 0.9,
                "blockingIssues": ["Weak falsifiability criteria."],
                "suggestions": ["Make criteria strict"],
                "evidence": "",
                "riskScore": 0.9,
                "decision": "reject",
            }
        else:
            payload = {
                "reviewerName": f"AI {role}",
                "role": role,
                "confidence": 0.9,
                "blockingIssues": [],
                "suggestions": ["Looks good"],
                "evidence": "",
                "riskScore": 0.1,
                "decision": "approve",
            }

        return f"```json\n{json.dumps(payload)}\n```"


def get_engine():
    provider = SmartMockProvider()
    routing = RoutingPolicy()
    routing.register_provider("mock", provider, GEMINI_1_5_PRO_CAPABILITIES)
    gateway = IntelligenceGateway(routing_policy=routing)
    return ScientificDebateEngine(gateway=gateway)


def test_debate_consensus_approved() -> None:
    """Validates that a rigorous experimental design passes peer review."""
    engine = get_engine()

    good_design = {
        "id": "exp1",
        "independentVariables": ["GeneX"],
        "dependentVariables": ["DiseaseY"],
        "controls": ["WildType", "Placebo"],
        "failureCriteria": "If manipulation of GeneX yields no change in DiseaseY, hypothesis is falsified.",
    }

    hypothesis = {"id": "h1", "claim": "GeneX causally induces DiseaseY"}

    record = engine.evaluate_design(good_design, hypothesis)

    assert record["consensusReached"] is True
    assert record["finalDecision"] == "approved"
    # Ensure no blocking critiques
    for critique in record["critiques"]:
        assert len(critique["blockingIssues"]) == 0


def test_debate_consensus_rejected_missing_controls() -> None:
    """Validates that a Statistician rejects a design missing controls."""
    engine = get_engine()

    bad_design = {
        "id": "exp2",
        "independentVariables": ["GeneX"],
        "dependentVariables": ["DiseaseY"],
        "controls": [],  # Missing controls!
        "failureCriteria": "If manipulation of GeneX yields no change in DiseaseY, hypothesis is falsified.",
    }

    hypothesis = {"id": "h1", "claim": "GeneX causally induces DiseaseY"}

    record = engine.evaluate_design(bad_design, hypothesis)

    assert record["consensusReached"] is False
    assert record["finalDecision"] == "rejected"

    # Verify Statistician blocked it
    statistician_critiques = [
        c
        for c in record["critiques"]
        if c["role"] == "Statistician" and len(c["blockingIssues"]) > 0
    ]
    assert len(statistician_critiques) > 0


def test_debate_consensus_rejected_weak_falsifiability() -> None:
    """Validates that a Statistician rejects a design with weak falsifiability criteria."""
    engine = get_engine()

    bad_design = {
        "id": "exp3",
        "independentVariables": ["GeneX"],
        "dependentVariables": ["DiseaseY"],
        "controls": ["WildType"],
        "failureCriteria": "We will see if there is an effect.",  # Not strictly falsifiable
    }

    hypothesis = {"id": "h1", "claim": "GeneX causally induces DiseaseY"}

    record = engine.evaluate_design(bad_design, hypothesis)

    assert record["consensusReached"] is False
    assert record["finalDecision"] == "rejected"
