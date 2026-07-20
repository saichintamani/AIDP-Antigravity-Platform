"""
Failure Genomics Dashboard (R3 Compartment 4)
=============================================
Systematically catalogs WHY the engine fails, bucketing failures into a taxonomy.
"""
from collections import Counter
from typing import Dict, List, Any


class FailureGenomics:
    """Taxonomy catalog for hypothesis failures."""

    def analyze(self, scaled_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregates failure modes from the scaled results."""
        taxonomy_counts = Counter({
            "CONSTRAINT_VIOLATION": 0,
            "TEMPORAL_LEAK": 0,
            "MECHANISM_MISS": 0,
            "HALLUCINATION": 0,
            "ADVERSARY_REJECTION": 0,
            "JSON_PARSE_FAILURE": 0,
            "TIMEOUT": 0,
            "UNKNOWN": 0
        })

        failed_cases = []

        for res in scaled_results:
            if res.get("status") != "success":
                taxonomy_counts["TIMEOUT"] += 1
                failed_cases.append(res.get("case_id"))
                continue
                
            verdict = res.get("judge_verdict", {})
            if not verdict.get("is_match", False):
                fm = verdict.get("failure_mode")
                if fm in taxonomy_counts:
                    taxonomy_counts[fm] += 1
                else:
                    taxonomy_counts["UNKNOWN"] += 1
                failed_cases.append(res.get("case_id"))

        total_failures = len(failed_cases)
        distribution = {
            k: (v / total_failures * 100 if total_failures > 0 else 0.0)
            for k, v in taxonomy_counts.items()
        }

        return {
            "total_failures": total_failures,
            "taxonomy_counts": dict(taxonomy_counts),
            "distribution_pct": distribution,
            "most_common_failure": taxonomy_counts.most_common(1)[0][0] if total_failures > 0 else "None",
            "failed_cases": failed_cases
        }
