from aidp.discovery.competition import EvidenceCompetitionEngine
from aidp.discovery.hypothesis import HypothesisGenerator


def test_hypothesis_generation() -> None:
    """Validates that mutually exclusive hypotheses are generated from a single gap."""
    generator = HypothesisGenerator()

    mock_gap = {"conceptA": "Drug X", "conceptB": "Pathway Y", "estimatedEntropy": 0.9}

    hypotheses = generator.generate_from_gap(mock_gap)

    assert len(hypotheses) >= 2
    assert "causally induces" in hypotheses[0]["claim"]
    assert "no direct causal link" in hypotheses[1]["claim"]
    assert hypotheses[0]["expectedInformationGain"] > 0.0


def test_evidence_competition() -> None:
    """Validates that opposing evidence appropriately degrades a hypothesis's confidence score."""
    engine = EvidenceCompetitionEngine()

    hypotheses = [
        {
            "id": "h1",
            "claim": "A causes B",
            "confidence": 0.8,
            "supportingEvidenceIds": [],
            "opposingEvidenceIds": [],
        },
        {
            "id": "h2",
            "claim": "A does not cause B",
            "confidence": 0.2,
            "supportingEvidenceIds": [],
            "opposingEvidenceIds": [],
        },
    ]

    # Introduce evidence that explicitly opposes h1
    new_evidence = {"id": "ev_001", "opposes_target_id": "h1"}

    result = engine.evaluate_competition(hypotheses, new_evidence)
    ranked_hypotheses = result["hypotheses"]

    # Find h1 in the updated list
    h1_updated = next(h for h in ranked_hypotheses if h["id"] == "h1")

    assert h1_updated["confidence"] < 0.8  # Confidence should degrade
    assert "ev_001" in h1_updated["opposingEvidenceIds"]
