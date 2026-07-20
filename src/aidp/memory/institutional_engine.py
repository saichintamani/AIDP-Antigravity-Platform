from datetime import UTC, datetime

from aidp.introspection.engine import ScientificIntrospectionEngine
from aidp.memory.institutional_models import (
    LongitudinalAssumption,
    LongitudinalFailureMode,
    LongitudinalReviewerStats,
    ReviewerSnapshot,
    StrategyMemoryRecord,
)
from aidp.memory.repository import InstitutionalMemoryRepository
from aidp.meta_learning.adaptation_models import AdaptationRecord


class ScientificMemorySystem:
    """
    Orchestrator that persists per-run introspection and adaptation data 
    into longitudinal institutional memory.
    """
    
    def __init__(self, repository: InstitutionalMemoryRepository):
        self.repository = repository
        
    def recall_relevant_history(self, evidence_text: str, case_time_window: str = None) -> list[str]:
        """
        Uses the Vector DB to recall previous failures semantically related to the current evidence.
        Enforces a strict chronological firewall if a case_time_window is provided.
        """
        current_year = None
        if case_time_window:
            import re
            # Extract first 4-digit number as the year (e.g. "Cutoff Date: 1982")
            match = re.search(r'\d{4}', case_time_window)
            if match:
                current_year = int(match.group())

        if hasattr(self.repository, "query_relevant_failures"):
            return self.repository.query_relevant_failures(evidence_text, current_year=current_year)
        return []
        
    def archive_failure(self, failure_text: str, domain: str = "Unknown", case_time_window: str = None):
        """
        Quickly archive a failure (e.g. from Adversarial Review) without a full introspection pass.
        """
        from datetime import datetime, UTC
        from aidp.memory.institutional_models import LongitudinalFailureMode
        now = datetime.now(UTC)
        long_fm = self.repository.get_failure_mode(failure_text)
        if not long_fm:
            long_fm = LongitudinalFailureMode(constraint_key=failure_text, first_seen=now)
            
        long_fm.total_occurrences += 1
        long_fm.last_seen = now
        
        case_year = None
        if case_time_window:
            import re
            match = re.search(r'\d{4}', case_time_window)
            if match:
                case_year = int(match.group())
                
        # Only ChromaMemoryRepository accepts case_year right now, check signature dynamically
        import inspect
        if "case_year" in inspect.signature(self.repository.save_failure_mode).parameters:
            self.repository.save_failure_mode(long_fm, case_year=case_year)
        else:
            self.repository.save_failure_mode(long_fm)
        
    def archive_run(self, introspection: ScientificIntrospectionEngine, adaptations: list[AdaptationRecord]):
        """Saves the outcomes of a single run into long-term memory."""
        now = datetime.now(UTC)
        
        # 1. Archive Adaptations
        for record in adaptations:
            self.repository.save_adaptation(record)
            
        # 2. Archive Failures
        for constraint, fm in introspection.failure_genome.items():
            long_fm = self.repository.get_failure_mode(constraint)
            if not long_fm:
                long_fm = LongitudinalFailureMode(constraint_key=constraint, first_seen=now)
                
            long_fm.total_occurrences += fm.frequency
            long_fm.last_seen = now
            self.repository.save_failure_mode(long_fm)
            
        # 3. Archive Reviewer Stats
        for persona, analytics in introspection.reviewer_analytics.items():
            long_stats = self.repository.get_reviewer_stats(persona)
            if not long_stats:
                long_stats = LongitudinalReviewerStats(persona=persona)
                
            snapshot = ReviewerSnapshot(timestamp=now, precision=analytics.precision)
            long_stats.history.append(snapshot)
            self.repository.save_reviewer_stats(long_stats)
            
        # 4. Archive Assumptions
        for assumption, tracker in introspection.assumption_observatory.items():
            long_assump = self.repository.get_assumption(assumption)
            if not long_assump:
                long_assump = LongitudinalAssumption(assumption=assumption)
                
            long_assump.total_claims += tracker.total_claims
            long_assump.supported += tracker.supported
            long_assump.contradicted += tracker.contradicted
            long_assump.unresolved += tracker.unresolved
            self.repository.save_assumption(long_assump)
            
        # 5. Archive Strategy (Mapping Lessons + Adaptations)
        # For this PoC, we map each adaptation record back to a strategy record
        for lesson in introspection.lessons_learned:
            # Find adaptations triggered by this lesson (heuristic matching)
            related_adaptations = [a for a in adaptations if lesson.lesson in a.source_signal or a.source_signal in lesson.lesson]
            
            for adaptation in related_adaptations:
                strategy = StrategyMemoryRecord(
                    question="Unknown intent (batch run)", # In a real system, this comes from the Planner
                    intervention=adaptation,
                    outcome_metrics={"confidence": lesson.confidence, "evidence_count": lesson.evidence_count},
                    lesson_learned=lesson.lesson,
                    timestamp=now
                )
                self.repository.save_strategy(strategy)
