from aidp.intelligence.agents.teams import ChiefScientistAI
from aidp.intelligence.protocol import ScientificMessage
from aidp.intelligence.providers.mock import MockProvider


def test_chief_scientist_routing() -> None:
    provider = MockProvider()
    chief = ChiefScientistAI(provider)

    msg = ScientificMessage(
        sender="External",
        receiver="HypothesisTeam",
        goal="Generate hypothesis",
        required_action="process",
        payload={"data": "test"},
    )

    response = chief.route_message(msg)

    assert response.sender == "HypothesisTeam"
    assert response.receiver == "External"
    assert "Hypothesis Scientist" in response.payload["result"]
    assert response.confidence == 0.8
