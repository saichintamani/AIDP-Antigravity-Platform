import os
import shutil

from aidp.discovery.workflow import (
    AutonomousDiscoveryOrchestrator,
    DiscoverySession,
    DiscoveryState,
    WorkflowNode,
)


class MockGateway:
    def __init__(self):
        pass

# We will override the nodes temporarily to bypass the actual LLM generation
class MockRetrievalNode(WorkflowNode):
    def __init__(self):
        super().__init__("KnowledgeRetrieval")
    def execute(self, session: DiscoverySession) -> DiscoveryState:
        return DiscoveryState.GAP_ANALYSIS

class MockGapNode(WorkflowNode):
    def __init__(self):
        super().__init__("GapAnalysis")
    def execute(self, session: DiscoverySession) -> DiscoveryState:
        return DiscoveryState.HYPOTHESIS

class MockHypothesisNode(WorkflowNode):
    def __init__(self):
        super().__init__("HypothesisGeneration")
    def execute(self, session: DiscoverySession) -> DiscoveryState:
        session.hypothesis = {"claim": "Mock claim"}
        return DiscoveryState.PLANNING

class MockPlanningNode(WorkflowNode):
    def __init__(self):
        super().__init__("ExperimentPlanning")
    def execute(self, session: DiscoverySession) -> DiscoveryState:
        session.experiment_design = {"mock": "design"}
        return DiscoveryState.FORMAL_VERIFICATION

class MockVerificationNode(WorkflowNode):
    def __init__(self):
        super().__init__("FormalVerification")
    def execute(self, session: DiscoverySession) -> DiscoveryState:
        session.telemetry["verification_report"] = {"status": "PASS"}
        return DiscoveryState.REVIEW

def test_event_driven():
    print("Testing Event-Driven Orchestration...")
    test_storage = ".test_checkpoints"
    if os.path.exists(test_storage):
        shutil.rmtree(test_storage)
    os.makedirs(test_storage)
    
    # Initialize real orchestrator but with human approval flag
    orchestrator = AutonomousDiscoveryOrchestrator(gateway=MockGateway(), requires_human_approval=True)
    
    # Replace nodes with mocks up to REVIEW
    orchestrator.dag.nodes[DiscoveryState.RETRIEVAL] = MockRetrievalNode()
    orchestrator.dag.nodes[DiscoveryState.GAP_ANALYSIS] = MockGapNode()
    orchestrator.dag.nodes[DiscoveryState.HYPOTHESIS] = MockHypothesisNode()
    orchestrator.dag.nodes[DiscoveryState.PLANNING] = MockPlanningNode()
    orchestrator.dag.nodes[DiscoveryState.FORMAL_VERIFICATION] = MockVerificationNode()
    
    # Mock the DebateEngine inside ReviewNode to avoid actual LLM calls
    class MockDebateEngine:
        def evaluate_design(self, *args, **kwargs):
            return {"consensusReached": False, "critiques": []}
    orchestrator.dag.nodes[DiscoveryState.REVIEW].debate_engine = MockDebateEngine()
    
    # Monkeypatch session.save_checkpoint directory
    original_save = DiscoverySession.save_checkpoint
    def mock_save(self, directory=test_storage):
        original_save(self, directory=directory)
    DiscoverySession.save_checkpoint = mock_save
    
    try:
        print("Starting workflow...")
        # Run workflow
        session = orchestrator.run_discovery_cycle("test")
        
        # It should pause at REVIEW
        assert session.state == DiscoveryState.PAUSED, f"Expected PAUSED, got {session.state}"
        assert session.paused_at_state == DiscoveryState.REVIEW.value, f"Expected paused_at_state to be REVIEW, got {session.paused_at_state}"
        print("Workflow correctly paused.")
        
        checkpoint_file = os.path.join(test_storage, f"{session.id}.json")
        assert os.path.exists(checkpoint_file), "Checkpoint was not saved."
        
        # Simulate firing an event
        event_data = {
            "type": "HUMAN_REVIEW_EVENT",
            "decision": "Approve",
            "feedback": "Looks good to me."
        }
        
        print("Resuming workflow from event...")
        resumed_session = orchestrator.resume_from_event(checkpoint_file, event_data)
        
        assert resumed_session.state == DiscoveryState.FINISHED, f"Expected FINISHED, got {resumed_session.state}"
        
        assert resumed_session.debate_record["consensusReached"]
        assert len(resumed_session.debate_record["critiques"]) == 1
        assert resumed_session.debate_record["critiques"][0]["role"] == "Human PI"
        
        print("Success! Event-Driven Orchestration works.")
    finally:
        DiscoverySession.save_checkpoint = original_save
        if os.path.exists(test_storage):
            shutil.rmtree(test_storage)


if __name__ == "__main__":
    test_event_driven()
