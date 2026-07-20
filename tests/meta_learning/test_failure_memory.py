import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from aidp.cognitive_core.adaptive_planner import AdaptivePlanner
from aidp.meta_learning.memory_system import MemorySystem
from aidp.meta_learning.pattern_extractor import PatternExtractor


def test_epistemic_evolution_loop():
    """
    Verifies that the system can:
    1. Record a failure.
    2. Extract a lesson from that failure.
    3. Inject that lesson as a constraint into future plans.
    """
    # 1. Initialize the Memory System
    memory = MemorySystem()
    extractor = PatternExtractor(memory)
    planner = AdaptivePlanner(memory)
    
    context = "CRISPR off-target clinical trial"
    
    # 2. First Attempt (No Memory)
    hypotheses = [{"id": "h1"}]
    initial_plan = planner.generate_plan(context, hypotheses)
    assert len(initial_plan["injected_constraints"]) == 0
    
    # 3. Simulate a Verification Failure on that plan
    memory.failure.record_failure(
        context=context,
        error_type="VERIFICATION_FAILURE",
        details="Missing IRB ethics board approval field in schema."
    )
    
    # 4. Extract Pattern (Epistemic Evolution)
    extractor.extract_lessons_from_failures()
    
    # Verify the lesson was stored
    lessons = memory.learning.get_applicable_lessons(context)
    assert len(lessons) == 1
    assert "MANDATORY CONSTRAINT" in lessons[0].rule
    
    # 5. Second Attempt (With Memory)
    adapted_plan = planner.generate_plan(context, hypotheses)
    
    # Verify the Adaptive Planner successfully retrieved and injected the constraint
    assert len(adapted_plan["injected_constraints"]) == 1
    assert "Missing IRB ethics board approval field" in adapted_plan["injected_constraints"][0]
