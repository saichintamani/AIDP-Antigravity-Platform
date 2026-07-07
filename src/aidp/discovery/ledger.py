import hashlib
import json
from typing import Any

from aidp.discovery.validation import (
    ExperimentReadinessAssessment,
    HypothesisQualityEngine,
    RedundancyDetectionEngine,
    ScientificFalsifiabilityEngine,
)


class HypothesisEvidenceLedger:
    def __init__(self) -> None:
        self.quality_engine = HypothesisQualityEngine()
        self.falsifiability_engine = ScientificFalsifiabilityEngine()
        self.redundancy_engine = RedundancyDetectionEngine()
        self.readiness_engine = ExperimentReadinessAssessment()
        self.ledger: dict[str, dict[str, Any]] = {}

    def commit_hypothesis(self, hypothesis: dict[str, Any]) -> dict[str, Any]:
        """Validates a hypothesis and writes it to the cryptographic ledger."""
        hyp_id = hypothesis.get("id", "unknown")

        # 1. Quality Assessment
        quality = self.quality_engine.evaluate(hypothesis)

        # 2. Falsifiability
        invalidation_criteria = self.falsifiability_engine.derive_invalidation_criteria(hypothesis)
        quality["falsifiability"] = self.falsifiability_engine.check_falsifiability(
            invalidation_criteria
        )

        # 3. Readiness
        readiness = self.readiness_engine.assess_readiness(quality, len(invalidation_criteria) > 0)

        # Generate provenance hash
        hash_payload = json.dumps(
            {
                "id": hyp_id,
                "claim": hypothesis.get("claim"),
                "quality": quality,
                "readiness": readiness,
            },
            sort_keys=True,
        )
        provenance_hash = hashlib.sha256(hash_payload.encode()).hexdigest()

        entry = {
            "hypothesisId": hyp_id,
            "quality": quality,
            "readiness": readiness,
            "invalidationCriteria": invalidation_criteria,
            "redundancyCollapsedIds": [],  # Handled at batch level usually
            "provenanceHash": provenance_hash,
        }

        self.ledger[hyp_id] = entry
        return entry

    def check_readiness(self, hyp_id: str) -> str:
        if hyp_id not in self.ledger:
            return "insufficientEvidence"
        return str(self.ledger[hyp_id]["readiness"])
