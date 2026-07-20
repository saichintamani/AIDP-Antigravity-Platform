import pytest

from aidp.discovery.causal import CausalDiscoveryEngine
from aidp.discovery.debate import ScientificDebateEngine
from aidp.discovery.scientific_planning import WetLabPlanner


def test_architecture_no_hypothesis_without_provenance() -> None:
    """Architecture Invariant: No hypothesis can enter causal or experiment phases without a ledger provenance hash."""
    causal_engine = CausalDiscoveryEngine()
    planner = WetLabPlanner()

    mock_hyp = {"id": "h_rogue", "claim": "Rogue claim."}

    # Passing a None ledger entry should fail
    with pytest.raises(ValueError):
        causal_engine.simulate_intervention(mock_hyp, {}, None)

    with pytest.raises(ValueError):
        planner.design_experiment(mock_hyp, None, {})


def test_architecture_no_experiment_without_failure_criteria() -> None:
    """Architecture Invariant: No experiment design is valid unless it defines failure criteria."""
    debate_engine = ScientificDebateEngine()

    bad_design = {
        "id": "exp1",
        "independentVariables": ["A"],
        "dependentVariables": ["B"],
        "controls": ["C"],
        "failureCriteria": "",  # Missing
    }

    # Debate engine statistician must block it
    record = debate_engine.evaluate_design(bad_design, {})
    assert record["consensusReached"] is False
    assert record["finalDecision"] == "rejected"
