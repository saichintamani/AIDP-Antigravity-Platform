from typing import Any


class EvidenceScorer:
    """
    Evaluates the quality of evidence extracted from a scientific paper.
    Produces scores that feed into the Subjective Logic `base_rate` and `uncertainty`.
    """

    def __init__(self) -> None:
        pass

    def _score_methodology(self, methods: list[str]) -> float:
        # Check for randomized controlled trials, large-scale sequencing, etc.
        # Mock logic
        if "CRISPR" in str(methods):
            return 0.8
        return 0.5

    def _score_reproducibility(self, text: str) -> float:
        # Check for open data, code availability
        if "data availability" in text.lower():
            return 0.9
        return 0.4

    def _score_statistical_strength(self, results: list[str]) -> float:
        # Check for p-values, confidence intervals
        if "p < 0.05" in str(results) or "p<0.05" in str(results):
            return 0.8
        return 0.5

    def _score_venue(self, doi: str) -> float:
        # In a real system, look up journal impact factor via Crossref
        return 0.7

    def score_paper(self, parsed_paper: dict[str, Any], raw_text: str = "") -> dict[str, float]:
        """
        Calculates quality metrics for a paper.
        """
        methodology = self._score_methodology(parsed_paper.get("methods", []))
        reproducibility = self._score_reproducibility(raw_text)
        stats = self._score_statistical_strength(parsed_paper.get("results", []))

        # Aggregate to a base rate for subjective logic
        base_confidence = (methodology * 0.4) + (stats * 0.4) + (reproducibility * 0.2)

        return {
            "methodology_quality": methodology,
            "reproducibility": reproducibility,
            "statistical_strength": stats,
            "base_confidence": base_confidence,
        }
