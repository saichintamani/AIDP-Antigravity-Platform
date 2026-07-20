
from aidp.intelligence.epistemic_models import Claim
from aidp.introspection.observatory_models import (
    AssumptionTracker,
    FailureMode,
    LessonLearned,
    ReviewerPrecision,
)


class ScientificIntrospectionEngine:
    """
    Aggregates atomic telemetry from Claims to generate meta-knowledge about the reasoning system.
    """
    
    def __init__(self):
        self.failure_genome: dict[str, FailureMode] = {}
        self.reviewer_analytics: dict[str, ReviewerPrecision] = {}
        self.assumption_observatory: dict[str, AssumptionTracker] = {}
        self.lessons_learned: list[LessonLearned] = []
        
    def analyze_claims(self, claims: list[Claim]):
        """Processes a corpus of claims to build the observatories."""
        for claim in claims:
            self._process_failure_genome(claim)
            self._process_reviewer_analytics(claim)
            self._process_assumption_observatory(claim)
            
        self._extract_learning_signals()
        
    def _process_failure_genome(self, claim: Claim):
        # We look for claims that were rejected with an unsat_core
        if claim.explanation and claim.explanation.rejection:
            rej = claim.explanation.rejection
            domain = "General" # Ideally extracted from claim metadata
            
            for constraint in rej.unsat_core:
                if constraint not in self.failure_genome:
                    self.failure_genome[constraint] = FailureMode(constraint_key=constraint)
                    
                self.failure_genome[constraint].frequency += 1
                self.failure_genome[constraint].domains[domain] = self.failure_genome[constraint].domains.get(domain, 0) + 1

    def _process_reviewer_analytics(self, claim: Claim):
        # We need both AcceptanceExplanation (to see who approved) and ultimate SAT/UNSAT status
        # In a real system, the AcceptanceExplanation might be generated early on, 
        # but the claim later fails formal verification. 
        # For simplicity, if the claim has individual_reviewer_scores, we check its verification_status.
        
        if claim.explanation and claim.explanation.acceptance:
            acc = claim.explanation.acceptance
            is_sat = claim.verification_status == "verified" # Assumes "verified" means SAT
            
            for persona, score in acc.individual_reviewer_scores.items():
                if persona not in self.reviewer_analytics:
                    self.reviewer_analytics[persona] = ReviewerPrecision(persona=persona)
                    
                analytics = self.reviewer_analytics[persona]
                # If score > 0.5, we consider it an "approval" by that persona
                if score >= 0.5:
                    analytics.total_reviews += 1
                    if is_sat:
                        analytics.true_positives += 1
                    else:
                        analytics.false_positives += 1
                        
                # Re-calculate precision
                if analytics.total_reviews > 0:
                    analytics.precision = analytics.true_positives / analytics.total_reviews

    def _process_assumption_observatory(self, claim: Claim):
        is_sat = claim.verification_status == "verified"
        
        for assumption in claim.assumptions:
            if assumption not in self.assumption_observatory:
                self.assumption_observatory[assumption] = AssumptionTracker(assumption=assumption)
                
            tracker = self.assumption_observatory[assumption]
            tracker.total_claims += 1
            if is_sat:
                tracker.supported += 1
            else:
                tracker.contradicted += 1
                
            tracker.support_rate = tracker.supported / tracker.total_claims

    def _extract_learning_signals(self):
        """Heuristics to generate Lessons Learned from the Observatories."""
        # Check Failure Genome for frequent constraints
        for constraint, fm in self.failure_genome.items():
            if fm.frequency >= 10:
                self.lessons_learned.append(LessonLearned(
                    lesson=f"Constraints related to '{constraint}' frequently fail validation.",
                    confidence=min(0.99, fm.frequency / 100.0), # Heuristic
                    evidence_count=fm.frequency,
                    related_constraints=[constraint]
                ))
                
        # Check Reviewer Precision
        for persona, analytics in self.reviewer_analytics.items():
            if analytics.total_reviews >= 10 and analytics.precision < 0.6:
                self.lessons_learned.append(LessonLearned(
                    lesson=f"Reviewer persona '{persona}' shows low precision ({analytics.precision:.2f}), frequently approving claims that later fail Z3 validation.",
                    confidence=1.0 - analytics.precision,
                    evidence_count=analytics.false_positives,
                    related_constraints=[]
                ))
                
        # Check Assumptions
        for assumption, tracker in self.assumption_observatory.items():
            if tracker.total_claims >= 10 and tracker.support_rate < 0.5:
                self.lessons_learned.append(LessonLearned(
                    lesson=f"The assumption '{assumption}' is highly risky and frequently contradicted.",
                    confidence=1.0 - tracker.support_rate,
                    evidence_count=tracker.contradicted,
                    related_constraints=[]
                ))
