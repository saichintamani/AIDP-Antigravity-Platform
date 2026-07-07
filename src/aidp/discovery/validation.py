from typing import Any


class HypothesisQualityEngine:
    def evaluate(self, hypothesis: dict[str, Any]) -> dict[str, float]:
        """Grades hypothesis on novelty, consistency, testability, and plausibility."""
        # Mock evaluation heuristics
        confidence = hypothesis.get("confidence", 0.5)
        return {
            "novelty": 0.85 if confidence < 0.6 else 0.4,
            "logicalConsistency": 0.9,
            "testability": 0.95,
            "falsifiability": 0.0,  # Determined by ScientificFalsifiabilityEngine
            "scientificPlausibility": 0.75,
        }


class ScientificFalsifiabilityEngine:
    def derive_invalidation_criteria(self, hypothesis: dict[str, Any]) -> list[str]:
        """Automatically derives what evidence would invalidate the hypothesis."""
        claim = hypothesis.get("claim", "")
        if "causally induces" in claim:
            parts = claim.split(" causally induces ")
            return [f"Evidence showing {parts[0]} varies independently of {parts[1].strip('.')}."]
        return ["Null hypothesis cannot be rejected."]

    def check_falsifiability(self, criteria: list[str]) -> float:
        """Returns a score of how falsifiable the claim is."""
        if not criteria or criteria[0] == "Null hypothesis cannot be rejected.":
            return 0.2
        return 0.95


class RedundancyDetectionEngine:
    def collapse_redundant(self, hypotheses: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Uses semantic similarity mock to merge duplicated hypotheses."""
        unique = []
        seen_claims = set()

        for h in hypotheses:
            claim = h.get("claim", "").lower().strip()
            # Simple mock: if claim string is identical, it's redundant
            if claim not in seen_claims:
                seen_claims.add(claim)
                unique.append(h)
            else:
                # In M9+, append this to redundancyCollapsedIds
                pass
        return unique


class ExperimentReadinessAssessment:
    def assess_readiness(self, quality: dict[str, float], has_invalidation: bool) -> str:
        """Determines if a hypothesis is ready for causal analysis or experiment planning."""
        if quality["logicalConsistency"] < 0.5:
            return "insufficientEvidence"
        if not has_invalidation or quality["falsifiability"] < 0.5:
            return "needsContradictionResolution"

        # If it passes quality and falsifiability, it is ready for causal validation
        return "readyForCausal"
