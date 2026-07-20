import os
import sys

# Add src to sys.path so we can import aidp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from aidp.discovery.workflow import DiscoverySession, DiscoveryState, MemoryUpdateNode
from aidp.memory.decision_memory import DecisionMemoryManager
from aidp.memory.failure_memory import FailureMemoryManager
from aidp.memory.identity_memory import IdentityMemoryManager


def test_memory_modules():
    print("Testing Anti-Gravity Memory Modules...")
    
    # 1. Identity Memory
    imm = IdentityMemoryManager()
    identity = imm.get_identity()
    assert "core_directive" in identity
    assert identity["core_directive"] == "We are optimizing epistemic reliability."
    
    # 2. Setup mock session for success
    success_session = DiscoverySession()
    success_session.id = "test_success_123"
    success_session.hypothesis = {"claim": "DrugX cures DiseaseY."}
    success_session.consensus_report = {"summary": "All good."}
    
    # Run MemoryUpdateNode
    node = MemoryUpdateNode()
    state = node.execute(success_session)
    
    assert state == DiscoveryState.FINISHED
    
    # Verify decision logged
    dmm = DecisionMemoryManager()
    decisions = dmm.get_decisions(success_session.id)
    assert len(decisions) == 1
    assert decisions[0]["decision"] == "Consensus Approved"
    
    # 3. Setup mock session for failure
    fail_session = DiscoverySession()
    fail_session.id = "test_fail_456"
    fail_session.hypothesis = {"claim": "DrugA cures DiseaseB."}
    fail_session.experiment_design = {"variables": "mock"}
    fail_session.debate_record = {
        "consensusReached": False,
        "critiques": [
            {"role": "Statistician", "decision": "Reject", "blockingIssues": ["Missing power analysis"]}
        ]
    }
    
    # Run MemoryUpdateNode
    node.execute(fail_session)
    
    # Verify failure logged
    fmm = FailureMemoryManager()
    # Filter for our test failure
    failures = [f for f in fmm.get_failures("DEBATE_REJECTION") if f.get("session_id") == fail_session.id]
    
    assert len(failures) == 1
    assert "Missing power analysis" in failures[0]["critique"]
    
    print("Memory tests passed successfully!")
    
if __name__ == "__main__":
    test_memory_modules()
