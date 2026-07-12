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
            "evidence_quality": self._calc_evidence_quality(test_case, result, evidence_used),
            "hallucination_rate": self._calc_hallucination(test_case, result),
            "calibration": self._calc_calibration(result),
            "reproducibility": self._calc_reproducibility(result),
            "runtime_sec": result.get("runtime_sec", 0.0),
            "cost_usd": result.get("cost_usd", 0.0),
            "governance_compliance": 1.0,  # Mocked
        }

    def _calc_correctness(self, case: BenchmarkCase, result: dict[str, Any]) -> float:
        # P0-1: LLM-as-a-judge for semantic correctness to handle negation and paraphrasing
        if not case.expected_findings:
            return 1.0
        
        output = result.get("output", "")
        if not output:
            return 0.0

        try:
            import litellm
            import re
            prompt = (
                "Evaluate if the following generated scientific hypothesis correctly entails the expected findings.\n"
                f"Hypothesis:\n{output}\n\n"
                f"Expected Findings:\n- " + "\n- ".join(case.expected_findings) + "\n\n"
                "Does the hypothesis affirm all expected findings without negating them? "
                "Reply with a number from 0.0 to 1.0 representing the correctness score. Only output the number."
            )
            response = litellm.completion(
                model="ollama/llama3.2:3b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                num_ctx=4096
            )
            score_str = response.choices[0].message.content.strip()
            match = re.search(r"[-+]?\d*\.\d+|\d+", score_str)
            if match:
                return float(match.group())
            return 0.0
        except Exception as e:
            # P0-1 Hard Fail: Do not silently fallback to string-matching.
            raise RuntimeError(f"Semantic judge unavailable or failed. Aborting benchmark execution to preserve integrity. Details: {str(e)}")

    def _extract_concepts(self, sentence: str) -> set[str]:
        # Simple stop word list to isolate significant scientific nouns/adjectives
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
            "of", "with", "by", "as", "is", "are", "was", "were", "be", "been", 
            "being", "it", "its", "that", "this", "these", "those", "from", "their", 
            "they", "we", "our", "you", "your", "he", "his", "she", "her", "has", 
            "have", "had", "do", "does", "did", "can", "could", "will", "would"
        }
        # Replace punctuation with spaces
        for p in ".,;:'\"()[]{}!?":
            sentence = sentence.replace(p, " ")
        words = sentence.lower().split()
        return {w for w in words if w not in stop_words and len(w) > 2}

    def _calc_evidence_quality(self, case: BenchmarkCase, result: dict[str, Any], evidence: list[str]) -> float:
        import re
        if not case.required_evidence_sources:
            return 1.0
        
        # P0-2: Fallback to regex extraction from output if evidence array is empty
        if not evidence:
            output_text = result.get("output", "")
            # Extract basic DOI format or PMID format
            extracted = set(re.findall(r"(10\.\d{4,9}/[-._;()/:A-Z0-9]+|PMID:\s*\d+)", output_text, re.IGNORECASE))
            evidence = list(extracted)
            
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

