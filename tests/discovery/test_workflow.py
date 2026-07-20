import json
import os
import shutil
from typing import Any

import pytest

from aidp.discovery.workflow import (
    AutonomousDiscoveryOrchestrator,
    DiscoverySession,
    DiscoveryState,
)
from aidp.intelligence.providers.capabilities import GEMINI_1_5_PRO_CAPABILITIES
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.routing import RoutingPolicy


class MockLLMProviderForWorkflow:
    def __init__(self, fail_count=0) -> None:
        self.fail_count = fail_count
        self.current_fails = 0

    def query(self, prompt: str, schema_hint=None) -> Any:
        if self.current_fails < self.fail_count:
            self.current_fails += 1
            raise RuntimeError("Temporary Network Failure")

        schema_name = getattr(schema_hint, "__name__", "") if schema_hint else ""

        if "HypothesisPayload" in schema_name or ("Hypothesis" in prompt and "Experimental Methodology Generator" not in prompt):
            payload = {
                "claim": "X causes Y",
                "rationale": "Because of Z",
                "confidence_prior": 0.8,
            }
            return f"```json\n{json.dumps(payload)}\n```"

        if "Methodology" in schema_name or "Methodolog" in prompt:
            payload = {
                "independent_variables": ["Variable X"],
                "dependent_variables": ["Variable Y"],
                "control_groups": ["Control Group 1"],
                "blinding_strategy": "Double-blind",
                "randomization": "Randomized",
                "success_criteria": "If X does not change Y, it is falsified.",
                "independentVariables": ["Variable X"],
                "dependentVariables": ["Variable Y"],
                "controls": ["Control Group 1"],
                "failureCriteria": "If X does not change Y, it is falsified.",
                "resourceEstimation": "Standard compute",
                "costPrediction": "Low",
                "failurePrediction": "Convergence failure",
            }
            return f"```json\n{json.dumps(payload)}\n```"

        if "Reviewer" in schema_name or any(
            role in prompt
            for role in ["Statistician", "Domain Expert", "Methodologist", "Ethicist", "Engineer"]
        ):
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

        if "Cohort" in schema_name or "cohort" in prompt.lower():
            payload = {
                "size": 100,
                "inclusion_criteria": ["Healthy"],
                "exclusion_criteria": ["Sick"],
                "demographic_considerations": "Balanced",
            }
            return f"```json\n{json.dumps(payload)}\n```"

        if "SafetyEfficacy" in schema_name or "safety" in prompt.lower():
            payload = {
                "anticipated_adverse_events": ["Mild headache"],
                "safety_monitoring_plan": "Weekly checkups",
                "stopping_rules": "Stop if severe side effects occur",
                "primary_efficacy_endpoint": "Reduction in symptoms",
                "secondary_efficacy_endpoints": ["Improved sleep"],
            }
            return f"```json\n{json.dumps(payload)}\n```"

        return "{}"


@pytest.fixture
def gateway():
    provider = MockLLMProviderForWorkflow()
    routing = RoutingPolicy()
    routing.register_provider("mock", provider, GEMINI_1_5_PRO_CAPABILITIES)
    return IntelligenceGateway(routing_policy=routing)


@pytest.fixture
def clean_checkpoints():
    if os.path.exists(".checkpoints"):
        shutil.rmtree(".checkpoints")
    yield
    if os.path.exists(".checkpoints"):
        shutil.rmtree(".checkpoints")


def test_workflow_gate_1_end_to_end(gateway, clean_checkpoints) -> None:
    """Gate 1: End-to-end workflow succeeds."""
    orchestrator = AutonomousDiscoveryOrchestrator(gateway)
    session = orchestrator.run_discovery_cycle("How does X affect Y?")

    assert session.state == DiscoveryState.FINISHED
    assert session.question == "How does X affect Y?"
    assert session.hypothesis["claim"] == "X causes Y"
    assert "Variable X" in session.experiment_design["independentVariables"]
    assert session.debate_record["consensusReached"] is True

    # Gate 6: Report generation
    report = orchestrator.generate_report(session)
    assert "Discovery Report:" in report
    assert "**Consensus Reached:** True" in report


def test_workflow_gate_2_deterministic_replay(gateway, clean_checkpoints) -> None:
    """Gate 2: Replay reproduces identical state transitions (mocked)."""
    orchestrator = AutonomousDiscoveryOrchestrator(gateway)
    session1 = orchestrator.run_discovery_cycle("How does X affect Y?")

    # Run a second session
    session2 = orchestrator.run_discovery_cycle("How does X affect Y?")

    # Check that trace sequence of events is identical
    trace1_events = [t["event"] for t in session1.trace]
    trace2_events = [t["event"] for t in session2.trace]
    assert trace1_events == trace2_events


def test_workflow_gate_4_checkpoint_recovery(gateway, clean_checkpoints) -> None:
    """Gate 4: Checkpoint recovery works."""
    orchestrator = AutonomousDiscoveryOrchestrator(gateway)

    # Instead of running end-to-end, let's create an incomplete session and save it
    session = DiscoverySession(question="Test question", state=DiscoveryState.HYPOTHESIS)
    session.contradictions = [{"description": "test contradiction"}]
    session.save_checkpoint()

    # Resume from checkpoint
    path = os.path.join(".checkpoints", f"{session.id}.json")
    resumed_session = orchestrator.resume_discovery_cycle(path)

    assert resumed_session.state == DiscoveryState.FINISHED
    assert resumed_session.id == session.id
    assert resumed_session.question == "Test question"


def test_workflow_gate_5_failure_recovery(clean_checkpoints) -> None:
    """Gate 5: Provider failure recovery works (retry logic)."""
    provider = MockLLMProviderForWorkflow(fail_count=2)
    routing = RoutingPolicy()
    routing.register_provider("mock", provider, GEMINI_1_5_PRO_CAPABILITIES)
    gateway = IntelligenceGateway(routing_policy=routing)

    orchestrator = AutonomousDiscoveryOrchestrator(gateway)
    session = orchestrator.run_discovery_cycle("Fail and retry")

    # It should have failed twice on Hypothesis generation and retried, eventually succeeding
    assert session.state == DiscoveryState.FINISHED
    # Ensure retries were logged
    retry_logs = [t for t in session.trace if "Exception" in t["event"]]
    assert len(retry_logs) == 2
