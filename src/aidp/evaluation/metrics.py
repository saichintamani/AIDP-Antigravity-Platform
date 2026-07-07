from typing import Any

from aidp.evaluation.discovery_bench import BenchmarkCase


class MetricEvaluator:
    """
    Computes scores for a given benchmark case and baseline output.
    """

    def evaluate(self, test_case: BenchmarkCase, result: dict[str, Any]) -> dict[str, float]:
        """
        Calculates all core scientific metrics.
        """
        output = result.get("output", "")
        evidence_used = result.get("evidence_used", [])

        return {
            "scientific_correctness": self._calc_correctness(test_case, result),
            "evidence_quality": self._calc_evidence_quality(test_case, evidence_used),
            "hallucination_rate": self._calc_hallucination(test_case, result),
            "calibration": self._calc_calibration(result),
            "reproducibility": self._calc_reproducibility(result),
            "runtime_sec": result.get("runtime_sec", 0.0),
            "cost_usd": result.get("cost_usd", 0.0),
            "governance_compliance": 1.0,  # Mocked
        }

    def _calc_correctness(self, case: BenchmarkCase, result: dict[str, Any]) -> float:
        # Check if expected findings are in output using deterministic string matching
        score = 0.0
        if not case.expected_findings:
            return 1.0
        
        output_lower = result.get("output", "").lower()
        matches = sum(1 for finding in case.expected_findings if finding.lower() in output_lower)
        score = matches / len(case.expected_findings)
        return score

    def _calc_evidence_quality(self, case: BenchmarkCase, evidence: list[str]) -> float:
        if not case.required_evidence_sources:
            return 1.0
        
        if not evidence:
            return 0.0
            
        evidence_lower = [e.lower() for e in evidence]
        matches = sum(1 for src in case.required_evidence_sources if any(src.lower() in e for e in evidence_lower))
        return matches / len(case.required_evidence_sources)

    def _calc_hallucination(self, case: BenchmarkCase, result: dict[str, Any]) -> float:
        # Deterministic check for known contradictions
        if not case.known_contradictions:
            return 0.0
            
        output_lower = result.get("output", "").lower()
        hallucinations = sum(1 for contra in case.known_contradictions if contra.lower() in output_lower)
        return min(1.0, hallucinations / max(1, len(case.known_contradictions)))

    def _calc_calibration(self, result: dict[str, Any]) -> float:
        # Mock calibration score. 1.0 is perfectly calibrated
        # In a real system this would compare confidence to correctness.
        # But we don't have a structured confidence output yet, so we will return 1.0 for now,
        # or calculate based on 'confidence' key if present
        confidence = result.get("confidence", 0.5)
        # Assuming we can't calculate a real calibration without correctness,
        # we'll use a simplified deterministic fallback.
        return 1.0 - abs(1.0 - confidence)

    def _calc_reproducibility(self, result: dict[str, Any]) -> float:
        # Reproducibility would normally involve multiple runs.
        # For a single run evaluation, this is a placeholder.
        return 1.0

