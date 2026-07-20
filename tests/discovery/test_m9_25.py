import pytest

from aidp.discovery.causal import CausalDiscoveryEngine
from aidp.discovery.ledger import HypothesisEvidenceLedger
from aidp.discovery.scientific_planning import WetLabPlanner
from aidp.discovery.validation import RedundancyDetectionEngine


def test_m9_25_redundancy() -> None:
    """Validates that redundant hypotheses are collapsed."""
    engine = RedundancyDetectionEngine()
    hypotheses = [
        {"id": "h1", "claim": "GeneA causally induces DiseaseB."},
        {"id": "h2", "claim": " GeneA causally induces DiseaseB. "},  # Semantically identical
    ]

    unique = engine.collapse_redundant(hypotheses)
    assert len(unique) == 1
    assert unique[0]["id"] == "h1"


def test_m9_25_falsifiability_and_ledger() -> None:
    """Validates that unfalsifiable hypotheses are rejected by the ledger."""
    ledger = HypothesisEvidenceLedger()

    # Valid causal claim
    valid_hyp = {"id": "h1", "claim": "GeneA causally induces DiseaseB.", "confidence": 0.8}
    entry1 = ledger.commit_hypothesis(valid_hyp)
    assert entry1["readiness"] == "readyForCausal"
    assert entry1["quality"]["falsifiability"] > 0.8
    assert "provenanceHash" in entry1

    # Unfalsifiable claim
    invalid_hyp = {"id": "h2", "claim": "God is real.", "confidence": 0.9}
    entry2 = ledger.commit_hypothesis(invalid_hyp)
    assert entry2["readiness"] == "needsContradictionResolution"
    assert entry2["quality"]["falsifiability"] < 0.5


def test_m9_25_causal_gate() -> None:
    """Validates that CausalDiscoveryEngine respects the ledger gate."""
    ledger = HypothesisEvidenceLedger()
    invalid_hyp = {"id": "h2", "claim": "God is real.", "confidence": 0.9}
    entry = ledger.commit_hypothesis(invalid_hyp)

    causal_engine = CausalDiscoveryEngine()
    with pytest.raises(ValueError, match="failed M9.25 governance gate"):
        causal_engine.simulate_intervention(invalid_hyp, {}, entry)


def test_m9_25_experiment_gate() -> None:
    """Validates that WetLabPlanner respects the ledger gate."""
    ledger = HypothesisEvidenceLedger()
    invalid_hyp = {"id": "h2", "claim": "God is real.", "confidence": 0.9}
    entry = ledger.commit_hypothesis(invalid_hyp)

    planner = WetLabPlanner()
    with pytest.raises(ValueError, match="failed M9.25 governance gate"):
        planner.design_experiment(invalid_hyp, entry, {})
