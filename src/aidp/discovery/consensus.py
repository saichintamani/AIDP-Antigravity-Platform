from dataclasses import dataclass
from typing import Any


@dataclass
class ReviewerResult:
    reviewerName: str
    role: str
    confidence: float
    blockingIssues: list[str]
    suggestions: list[str]
    evidence: str
    riskScore: float
    decision: str


@dataclass
class ConsensusReport:
    approved: bool
    disagreement_percentage: float
    average_confidence: float
    max_risk_score: float
    blocking_reasons: list[str]
    conflict_detected: bool
    summary: str


class ReviewerMemory:
    """
    Tracks statistics per persona over time.
    For this milestone, implemented in-memory with stubs for persistence.
    """

    def __init__(self) -> None:
        # persona -> stats
        self.stats: dict[str, dict[str, Any]] = {}

    def record_review(self, persona: str, result: ReviewerResult, final_decision: bool) -> None:
        if persona not in self.stats:
            self.stats[persona] = {
                "total_reviews": 0,
                "agreements": 0,
                "blocks": 0,
                "false_positives": 0,  # Blocked but consensus approved (conceptually)
                "false_negatives": 0,  # Approved but consensus blocked (conceptually)
            }

        s = self.stats[persona]
        s["total_reviews"] += 1

        reviewer_approved = result.decision.lower() == "approve"
        if reviewer_approved == final_decision:
            s["agreements"] += 1

        if not reviewer_approved:
            s["blocks"] += 1

        if not reviewer_approved and final_decision:
            s["false_positives"] += 1

        if reviewer_approved and not final_decision:
            s["false_negatives"] += 1

    def get_stats(self, persona: str) -> dict[str, float]:
        if persona not in self.stats:
            return {}

        s = self.stats[persona]
        total = s["total_reviews"]
        if total == 0:
            return {}

        return {
            "accuracy": s["agreements"] / total,
            "agreement_rate": s["agreements"] / total,
            "blocking_frequency": s["blocks"] / total,
            "false_positive_rate": s["false_positives"] / total,
            "false_negative_rate": s["false_negatives"] / total,
        }


class ConsensusEngine:
    """
    Aggregates reviews, computes disagreement, detects conflicts, and produces a consensus report.
    """

    def __init__(self, memory: ReviewerMemory | None = None) -> None:
        self.memory = memory or ReviewerMemory()

    def evaluate_consensus(self, reviews: list[ReviewerResult]) -> ConsensusReport:
        if not reviews:
            return ConsensusReport(False, 0.0, 0.0, 0.0, [], False, "No reviews provided.")

        total_reviews = len(reviews)
        approvals = sum(1 for r in reviews if r.decision.lower() == "approve")
        rejections = total_reviews - approvals

        disagreement_percentage = min(approvals, rejections) / total_reviews
        average_confidence = sum(r.confidence for r in reviews) / total_reviews
        max_risk_score = max(r.riskScore for r in reviews)

        blocking_reasons = []
        for r in reviews:
            if r.decision.lower() != "approve":
                blocking_reasons.extend(r.blockingIssues)

        # Simple policy: Unanimous approval required for now, or at most 1 minor rejection if we wanted.
        # But we will stick to unanimous or strict consensus rules.
        # Let's say we require 100% approval for strict experiments.
        approved = approvals == total_reviews
        conflict_detected = disagreement_percentage > 0.0

        summary = f"Consensus {'reached' if approved else 'failed'}. Approvals: {approvals}/{total_reviews}. Max Risk: {max_risk_score}."

        # Record into memory
        for r in reviews:
            self.memory.record_review(r.role, r, approved)

        return ConsensusReport(
            approved=approved,
            disagreement_percentage=disagreement_percentage,
            average_confidence=average_confidence,
            max_risk_score=max_risk_score,
            blocking_reasons=blocking_reasons,
            conflict_detected=conflict_detected,
            summary=summary,
        )
