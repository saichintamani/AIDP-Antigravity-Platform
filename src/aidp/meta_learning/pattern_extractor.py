from aidp.meta_learning.memory_system import MemorySystem


class PatternExtractor:
    """
    Scans historical failures and synthesizes them into structured, deterministic constraints
    that the Adaptive Planner can use to avoid repeating mistakes.
    """
    
    def __init__(self, memory_system: MemorySystem):
        self.memory = memory_system
        
    def extract_lessons_from_failures(self):
        """
        In a real system, this would use an LLM or clustering algorithm to detect patterns.
        For determinism in Phase 13, we map known failure types directly to strict constraints.
        """
        for failure in self.memory.failure.failures:
            # Prevent duplicate lesson extraction
            existing_lessons = self.memory.learning.get_applicable_lessons(failure.context)
            if any(L.rule == failure.details for L in existing_lessons):
                continue
                
            # Synthesize structural rules based on the error type
            if failure.error_type == "VERIFICATION_FAILURE":
                constraint_rule = f"MANDATORY CONSTRAINT: Must not violate schema rule regarding: {failure.details}"
                self.memory.learning.add_lesson(
                    context=failure.context,
                    constraint="SCHEMA_ENFORCEMENT",
                    rule=constraint_rule
                )
                print(f"[Meta-Learning] Extracted new rule for {failure.context}: {constraint_rule}")
                
            elif failure.error_type == "DEBATE_REJECTION":
                constraint_rule = f"MANDATORY CONSTRAINT: Must address reviewer criticism: {failure.details}"
                self.memory.learning.add_lesson(
                    context=failure.context,
                    constraint="DEBATE_ADAPTATION",
                    rule=constraint_rule
                )
                print(f"[Meta-Learning] Extracted new rule for {failure.context}: {constraint_rule}")
