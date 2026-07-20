import time
from typing import Any


class IdentityMemory:
    def __init__(self):
        self.capabilities = [
            "Clinical Trial Design",
            "Molecular Target Identification",
            "Epistemic Verification"
        ]
        self.limits = [
            "Cannot conduct physical wet-lab experiments",
            "Requires human-in-the-loop for ethics board approvals"
        ]

class FailureEvent:
    def __init__(self, context: str, error_type: str, details: str):
        self.context = context
        self.error_type = error_type
        self.details = details
        self.timestamp = time.time()

class FailureMemory:
    def __init__(self):
        self.failures: list[FailureEvent] = []
        
    def record_failure(self, context: str, error_type: str, details: str):
        self.failures.append(FailureEvent(context, error_type, details))
        
    def query_failures(self, context: str) -> list[FailureEvent]:
        # Simple exact match for now; would use vector similarity in full prod
        return [f for f in self.failures if f.context == context]

class DecisionMemory:
    def __init__(self):
        self.decisions: list[dict[str, Any]] = []
        
    def record_decision(self, choice: str, alternatives_rejected: list[str], reason: str):
        self.decisions.append({
            "choice": choice,
            "alternatives_rejected": alternatives_rejected,
            "reason": reason,
            "timestamp": time.time()
        })

class LearnedLesson:
    def __init__(self, context: str, constraint: str, rule: str):
        self.context = context
        self.constraint = constraint
        self.rule = rule

class LearningMemory:
    def __init__(self):
        self.lessons: list[LearnedLesson] = []
        
    def add_lesson(self, context: str, constraint: str, rule: str):
        self.lessons.append(LearnedLesson(context, constraint, rule))
        
    def get_applicable_lessons(self, context: str) -> list[LearnedLesson]:
        # Simple exact match for now
        return [L for L in self.lessons if L.context == context]

class MemorySystem:
    """
    Central hub for the Four Memory Systems.
    """
    def __init__(self):
        self.identity = IdentityMemory()
        self.failure = FailureMemory()
        self.decision = DecisionMemory()
        self.learning = LearningMemory()
        
    def synthesize_state(self) -> dict[str, int]:
        return {
            "total_failures": len(self.failure.failures),
            "total_decisions": len(self.decision.decisions),
            "total_lessons": len(self.learning.lessons)
        }
