from aidp.discovery.causal import CausalDiscoveryEngine


def test_causal_discovery_confounded() -> None:
    """Validates that a hypothesis degrades if a backdoor confounder explains the correlation."""
    engine = CausalDiscoveryEngine()

    mock_hypothesis = {
        "id": "h1",
        "claim": "GeneX causally induces DiseaseY.",
        "confidence": 0.8,
        "risk": 0.2,
    }

    mock_causal_graph = {
        "nodes": ["GeneX", "DiseaseY", "Age"],
        "directedEdges": [],
        "unobservedConfounders": ["Age->GeneX,DiseaseY"],  # Age confounds the relationship
    }

    mock_ledger_entry = {
        "hypothesisId": "h1",
        "provenanceHash": "abc123hash",
        "readiness": "readyForCausal",
    }

    validated_h = engine.simulate_intervention(
        mock_hypothesis, mock_causal_graph, mock_ledger_entry
    )

    assert validated_h["confidence"] < 0.8  # Degraded due to confounding
    assert validated_h["risk"] > 0.2
    assert validated_h.get("causal_validation_failed") is True
    assert "Age" in validated_h.get("confounders_detected", [])


def test_causal_discovery_unconfounded() -> None:
    """Validates that a hypothesis strengthens if it survives structural backdoor checks."""
    engine = CausalDiscoveryEngine()

    mock_hypothesis = {
        "id": "h2",
        "claim": "DrugA causally induces RecoveryB.",
        "confidence": 0.5,
        "risk": 0.5,
    }

    # Clean graph, no backdoors
    mock_causal_graph = {
        "nodes": ["DrugA", "RecoveryB", "Age"],
        "directedEdges": [],
        "unobservedConfounders": ["Age->RecoveryB"],  # Age affects recovery but not drug assignment
    }

    mock_ledger_entry = {
        "hypothesisId": "h2",
        "provenanceHash": "xyz789hash",
        "readiness": "readyForExperiment",
    }

    validated_h = engine.simulate_intervention(
        mock_hypothesis, mock_causal_graph, mock_ledger_entry
    )

    assert validated_h["confidence"] > 0.5  # Strengthened, survived intervention check
    assert validated_h.get("causal_validation_failed", False) is False
