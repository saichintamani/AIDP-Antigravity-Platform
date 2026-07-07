from aidp.intelligence.laboratory import LaboratoryOrchestrator
from aidp.intelligence.providers.mock import MockProvider

def test_laboratory_orchestrator() -> None:
    lab = LaboratoryOrchestrator(default_provider=MockProvider())

    # Send initial goal to start the campaign
    lab.run_campaign("Find new treatments for cancer")

    # Our mock blackboard logic posts exactly one response per rule and ends
    assert len(lab.blackboard) == 1
    assert lab.blackboard[0]["topic"] == "experiment_reviewed"
