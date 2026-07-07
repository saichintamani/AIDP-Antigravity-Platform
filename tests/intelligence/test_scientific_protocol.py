import pytest

from aidp.intelligence.protocol import ScientificMessage


def test_scientific_message_validation() -> None:
    # Valid message
    msg = ScientificMessage(
        sender="LiteratureTeam",
        receiver="HypothesisTeam",
        goal="Extract claims",
        required_action="process",
        payload={"text": "p53 prevents cancer"},
    )
    msg.validate()

    # Missing sender
    with pytest.raises(ValueError):
        invalid_msg = ScientificMessage(
            sender="",
            receiver="HypothesisTeam",
            goal="Extract claims",
            required_action="process",
            payload={},
        )
        invalid_msg.validate()

    # Invalid confidence
    with pytest.raises(ValueError):
        invalid_msg = ScientificMessage(
            sender="Lit",
            receiver="Hyp",
            goal="Test",
            required_action="Test",
            payload={},
            confidence=1.5,
        )
        invalid_msg.validate()
