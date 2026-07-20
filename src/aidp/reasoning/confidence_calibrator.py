from enum import StrEnum
from typing import Any

from aidp.intelligence.epistemic_models import (
    ConfidenceLineageEvent,
    ConfidenceOntology,
    EpistemicClaim,
)


class ConfidenceLevel(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    REJECTED = "REJECTED"

class ConfidenceCalibrator:
    """
    Calculates the 6 dimensions of the Confidence Ontology based on available evidence, reviews, and verification checks.
    """

    def __init__(self):
        pass

    def calibrate(self, claim: EpistemicClaim, debate_record: dict[str, Any], verification_report: dict[str, Any]) -> ConfidenceOntology:
        """
        Calculates the calibrated ConfidenceOntology.
        """
        
        # 1. Verification Confidence
        verification_status_str = verification_report.get("status", "FAILED")
        ver_score = 1.0 if verification_status_str == "PASS" else 0.0

        # 2. Consensus Confidence
        rev_score = self._calculate_review_score(debate_record)

        # 3. Knowledge Confidence
        kg_score = self._calculate_kg_score(claim, verification_report)

        # 4. Evidence Confidence
        ev_score = self._calculate_evidence_score(claim)
        
        # 5. Assumption Confidence
        assump_score = self._calculate_assumption_score(claim)
        
        # 6. Reproducibility Confidence
        # Placeholder: If verification passed and evidence is high, reproducibility is assumed higher.
        repro_score = 0.8 if (ver_score > 0 and ev_score > 0.5) else 0.4

        # Final Overall Score (simple average of the 5 dimensions, gated by verification)
        if ver_score == 0.0:
            overall = 0.0
        else:
            overall = (rev_score + kg_score + ev_score + assump_score + repro_score) / 5.0

        return ConfidenceOntology(
            evidence_confidence=ev_score,
            verification_confidence=ver_score,
            assumption_confidence=assump_score,
            consensus_confidence=rev_score,
            knowledge_confidence=kg_score,
            reproducibility_confidence=repro_score,
            overall_confidence=overall
        )

    def _calculate_assumption_score(self, claim: EpistemicClaim) -> float:
        num_assumptions = len(claim.assumptions)
        if num_assumptions == 0:
            return 1.0
        # More assumptions = less confidence
        return max(0.0, 1.0 - (0.1 * num_assumptions))
    def _calculate_review_score(self, debate_record: dict[str, Any]) -> float:
        critiques = debate_record.get("critiques", [])
        if not critiques:
            return 0.5 # Neutral if no reviews
            
        approve_count = 0
        total_count = len(critiques)
        for critique in critiques:
            if critique.get("decision", "Abstain").lower() == "approve":
                approve_count += 1
                
        return approve_count / total_count if total_count > 0 else 0.0

    def _calculate_kg_score(self, claim: EpistemicClaim, verification_report: dict[str, Any]) -> float:
        # In Phase 8.2, AssumptionSolver (Level 4) verifies assumptions against the KG.
        # We can extract the assumption verification results if available.
        # For simplicity, we look at the level_4_assumption report.
        
        l4_report = verification_report.get("levels", {}).get("level_4_assumption", {})
        if l4_report.get("status") == "FAILED":
            return 0.0 # Contradicted
            
        assumptions = claim.assumptions
        if not assumptions:
            return 1.0 # No assumptions to be contradicted, entirely grounded in evidence
            
        # If it passed and has assumptions, we give it a 0.8 as it wasn't contradicted,
        # but might just be UNKNOWN.
        # In a fully connected KG, we would score the ratio of SUPPORTED vs UNKNOWN.
        return 0.8

    def _calculate_evidence_score(self, claim: EpistemicClaim) -> float:
        evidence_list = claim.evidence
        if not evidence_list:
            return 0.5 # Neutral
            
        total_rel = 0.0
        for ev in evidence_list:
            total_rel += ev.relevance_score
            
        return total_rel / len(evidence_list)

    def _determine_level(self, final_score: float, ver_score: float) -> ConfidenceLevel:
        if ver_score == 0.0:
            return ConfidenceLevel.REJECTED
        if final_score >= 0.8:
            return ConfidenceLevel.HIGH
        elif final_score >= 0.5:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

class LineageEngine:
    """
    Diffs two ConfidenceOntology objects to explain exactly why confidence changed over time.
    """
    def __init__(self):
        self.threshold = 0.01  # only log meaningful changes

    def generate_lineage(self, old_ont: ConfidenceOntology | None, new_ont: ConfidenceOntology) -> list[ConfidenceLineageEvent]:
        events = []
        if not old_ont:
            # Baseline establishment
            events.append(ConfidenceLineageEvent(
                dimension="overall_confidence",
                delta=new_ont.overall_confidence,
                reason="Baseline confidence established."
            ))
            return events

        # Compare dimensions
        dimensions = [
            ("evidence_confidence", "Evidence support"),
            ("verification_confidence", "Formal verification"),
            ("assumption_confidence", "Assumption validation"),
            ("consensus_confidence", "Reviewer consensus"),
            ("knowledge_confidence", "Knowledge Graph support"),
            ("reproducibility_confidence", "Reproducibility assessment"),
            ("overall_confidence", "Overall confidence")
        ]

        for dim, name in dimensions:
            old_val = getattr(old_ont, dim)
            new_val = getattr(new_ont, dim)
            delta = new_val - old_val

            if abs(delta) >= self.threshold:
                reason = f"{name} improved." if delta > 0 else f"{name} decreased."
                
                # Special cases for clearer MVP explanations
                if dim == "verification_confidence":
                    reason = "Verification passed." if delta > 0 else "Verification failed."
                elif dim == "knowledge_confidence":
                    if delta < 0: reason = "Contradictory graph evidence discovered."
                
                events.append(ConfidenceLineageEvent(
                    dimension=dim,
                    delta=round(delta, 3),
                    reason=reason
                ))

        return events
