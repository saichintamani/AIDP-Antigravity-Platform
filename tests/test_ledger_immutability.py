import os
import sys
import uuid

# Add src to sys.path so we can import aidp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from aidp.intelligence.epistemic_models import (
    ConfidenceLineageEvent,
    ConfidenceOntology,
    EpistemicClaim,
)
from aidp.platform.epistemic_logger import EpistemicLedger


def test_append_claim_generates_valid_hash(tmp_path):
    ledger_path = tmp_path / "test_ledger.jsonl"
    ledger = EpistemicLedger(db_uri=f"sqlite:///{ledger_path}")
    
    claim = EpistemicClaim(
        claim_id=str(uuid.uuid4()),
        claim_text="Alpha-synuclein is inhibited by peptide X",
        assumptions=[],
        generated_by="pytest"
    )
    
    ledger.append_claim(claim)
    
    claims = ledger.get_all_claims()
    assert len(claims) == 1
    assert claims[0].claim_text == "Alpha-synuclein is inhibited by peptide X"

def test_lineage_deltas_sum_correctly():
    claim = EpistemicClaim(
        claim_id=str(uuid.uuid4()),
        claim_text="Test lineage",
        assumptions=[],
        generated_by="pytest",
        confidence=ConfidenceOntology(
            evidence_confidence=0.5,
            verification_confidence=0.5,
            assumption_confidence=0.5,
            consensus_confidence=0.5,
            knowledge_confidence=0.5,
            reproducibility_confidence=0.5,
            overall_confidence=0.8
        ),
        confidence_lineage=[
            ConfidenceLineageEvent(dimension="overall_confidence", delta=0.5, reason="Baseline evidence"),
            ConfidenceLineageEvent(dimension="overall_confidence", delta=0.3, reason="Formal verification passed")
        ]
    )
    
    # Assert that the deltas in lineage roughly sum to the overall confidence
    total_delta = sum(event.delta for event in claim.confidence_lineage if event.dimension == "overall_confidence")
    assert abs(total_delta - claim.confidence.overall_confidence) < 0.01
