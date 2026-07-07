from aidp.reasoning_engine.experiment_reviser import ExperimentReviser


def test_autonomous_revision() -> None:
    reviser = ExperimentReviser()

    weak_design = {"power": 0.5, "setup": "in-vitro"}
    feedback = "Power too low for confidence."

    revised = reviser.revise(weak_design, feedback)

    assert revised["power"] == 0.9
    assert "revision_notes" in revised
