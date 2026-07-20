from aidp.discovery.active_discovery import ActiveDiscoveryPlanner
from aidp.discovery.scientific_planning import WetLabPlanner


def test_experiment_planning() -> None:
    """Validates that a hypothesis generates an experiment with controls and falsifiable failure criteria."""
    planner = WetLabPlanner()

    mock_hypothesis = {
        "id": "h1",
        "claim": "CompoundA causally induces ProteinB",
        "confidence": 0.5,
    }

    mock_ledger_entry = {
        "hypothesisId": "h1",
        "provenanceHash": "abc123hash",
        "readiness": "readyForExperiment",
    }

    design = planner.design_experiment(mock_hypothesis, mock_ledger_entry, {})

    assert "Mock IV" in design["independentVariables"]
    assert "Mock DV" in design["dependentVariables"]
    assert "Mock" in design["failureCriteria"]
    assert len(design["controls"]) >= 1
    assert "resourceEstimation" in design
    assert "costPrediction" in design
    assert "failurePrediction" in design


def test_active_discovery_prioritization() -> None:
    """Validates that Thompson Sampling / EIG prioritizes high-variance hypotheses over high-confidence ones."""
    planner = ActiveDiscoveryPlanner()

    # h1 is an unknown/risky hypothesis (conf 0.5, high variance)
    h1 = {"id": "h1", "confidence": 0.5, "risk": 0.8, "expectedInformationGain": 1.0}
    # h2 is a 'safe', already-known hypothesis (conf 0.95, low variance)
    h2 = {"id": "h2", "confidence": 0.95, "risk": 0.1, "expectedInformationGain": 0.5}

    hypotheses = [h1, h2]
    designs = [{"id": "exp1", "hypothesisId": "h1"}, {"id": "exp2", "hypothesisId": "h2"}]

    tasks = planner.prioritize_experiments(hypotheses, designs)

    # task targeting exp1 should rank higher because of EIG
    assert tasks[0]["experimentalDesignId"] == "exp1"
    assert tasks[1]["experimentalDesignId"] == "exp2"
    assert tasks[0]["expectedInformationGain"] > tasks[1]["expectedInformationGain"]
