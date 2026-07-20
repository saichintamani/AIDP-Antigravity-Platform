import shutil
import tempfile

from aidp.introspection.engine import ScientificIntrospectionEngine
from aidp.introspection.observatory_models import AssumptionTracker, FailureMode, ReviewerPrecision
from aidp.memory.institutional_engine import ScientificMemorySystem
from aidp.memory.repository import JsonMemoryRepository
from aidp.meta_learning.adaptation_models import AdaptationRecord


def test_institutional_memory():
    # Setup temporary directory for JSON files
    temp_dir = tempfile.mkdtemp()
    
    try:
        repo = JsonMemoryRepository(base_dir=temp_dir)
        engine = ScientificMemorySystem(repository=repo)
        
        # --- Simulate Run 1 ---
        intro1 = ScientificIntrospectionEngine()
        intro1.failure_genome["rule_X"] = FailureMode(constraint_key="rule_X", frequency=10)
        intro1.reviewer_analytics["Statistician"] = ReviewerPrecision(persona="Statistician", precision=0.8)
        intro1.assumption_observatory["Assumption A"] = AssumptionTracker(assumption="Assumption A", total_claims=10, supported=5, contradicted=5)
        
        adapt1 = AdaptationRecord(
            source_signal="Test", target_component="Test", target_key="Test",
            adaptation_type="Test", previous_state=1, new_state=2
        )
        
        engine.archive_run(introspection=intro1, adaptations=[adapt1])
        
        # Verify persistence after Run 1
        fm = repo.get_failure_mode("rule_X")
        assert fm.total_occurrences == 10
        
        rev = repo.get_reviewer_stats("Statistician")
        assert len(rev.history) == 1
        assert rev.history[0].precision == 0.8
        
        assump = repo.get_assumption("Assumption A")
        assert assump.total_claims == 10
        
        # --- Simulate Run 2 ---
        intro2 = ScientificIntrospectionEngine()
        intro2.failure_genome["rule_X"] = FailureMode(constraint_key="rule_X", frequency=5)
        intro2.reviewer_analytics["Statistician"] = ReviewerPrecision(persona="Statistician", precision=0.9)
        intro2.assumption_observatory["Assumption A"] = AssumptionTracker(assumption="Assumption A", total_claims=5, supported=5, contradicted=0)
        
        engine.archive_run(introspection=intro2, adaptations=[])
        
        # Verify longitudinal aggregation after Run 2
        fm2 = repo.get_failure_mode("rule_X")
        assert fm2.total_occurrences == 15 # 10 from Run 1 + 5 from Run 2
        
        rev2 = repo.get_reviewer_stats("Statistician")
        assert len(rev2.history) == 2
        assert rev2.history[1].precision == 0.9
        
        assump2 = repo.get_assumption("Assumption A")
        assert assump2.total_claims == 15
        assert assump2.supported == 10
        assert assump2.support_rate == (10 / 15)
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
