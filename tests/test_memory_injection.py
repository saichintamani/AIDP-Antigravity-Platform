import os
import shutil
from typing import Any

from aidp.discovery.scientific_planning import ExperimentalMethodologyGenerator
from aidp.intelligence.reasoning_planner import ReasoningPlanner
from aidp.intelligence.task_specification import TaskSpecification
from aidp.memory.failure_memory import FailureMemoryManager


# Mock the planner just to capture the prompt spec
class MockPlanner(ReasoningPlanner):
    def __init__(self):
        self.captured_spec = None
        
    def execute_task(self, spec: TaskSpecification) -> Any:
        self.captured_spec = spec
        return {"mock": "result"}


def test_memory_injection():
    print("Testing Anti-Gravity Memory Modules...")
    
    # 1. Setup fresh storage
    test_storage = ".test_aidp_memory"
    if os.path.exists(test_storage):
        shutil.rmtree(test_storage)
    os.makedirs(test_storage)
    
    # Override FailureMemoryManager default storage directory dynamically for tests if needed, 
    # but the simplest way is to explicitly initialize it with the test dir.
    fm = FailureMemoryManager(storage_dir=test_storage)
    
    # 2. Simulate a failure
    fm.log_failure(
        session_id="test_sess_1",
        failure_type="VERIFICATION_REJECTION",
        domain="WetLab",
        context={"claim": "Test claim"},
        critique="Verification Failed: Cannot use Vehicle Controls."
    )
    
    # Check it logged
    failures = fm.get_failures(domain="WetLab")
    assert len(failures) == 1, "Failure was not logged correctly."
    assert "Vehicle Controls" in failures[0]["critique"]
    
    # 3. Test injection into ExperimentalMethodologyGenerator
    # In the actual code, ExperimentalMethodologyGenerator creates a new FailureMemoryManager without args,
    # so we need to mock or ensure it reads from the test storage. 
    # We will temporarily monkeypatch the storage path.
    import aidp.memory.failure_memory
    original_init = aidp.memory.failure_memory.FailureMemoryManager.__init__
    def mock_init(self, storage_dir=test_storage):
        original_init(self, storage_dir=storage_dir)
    aidp.memory.failure_memory.FailureMemoryManager.__init__ = mock_init
    
    try:
        mock_planner = MockPlanner()
        generator = ExperimentalMethodologyGenerator(planner=mock_planner)
        
        generator.generate(
            hypothesis={"claim": "New test claim"}, 
            evidence_linkage={}, 
            ablation_config=None
        )
        
        spec = mock_planner.captured_spec
        assert spec is not None
        
        context_dict = spec.context
        assert "failure_memory" in context_dict
        
        injected_memory = context_dict["failure_memory"]
        assert "AVOID PREVIOUS FAILURES" in injected_memory
        assert "Vehicle Controls" in injected_memory
        
        print("Success! Failure successfully injected into Methodology Generator prompt.")
    finally:
        # Restore original init
        aidp.memory.failure_memory.FailureMemoryManager.__init__ = original_init
        # Cleanup
        if os.path.exists(test_storage):
            shutil.rmtree(test_storage)

if __name__ == "__main__":
    test_memory_injection()
