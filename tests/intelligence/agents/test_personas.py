from aidp.intelligence.agents.personas import MethodologistAgent, ReviewerAgent
from aidp.intelligence.providers.mock import MockProvider


def test_methodologist_persona() -> None:
    provider = MockProvider()
    agent = MethodologistAgent(provider=provider)

    prompt = agent.perceive("Experiment on p53")
    assert "Methodologist" in prompt
    assert "Experiment on p53" in prompt


def test_reviewer_persona() -> None:
    provider = MockProvider()
    agent = ReviewerAgent(provider=provider)

    prompt = agent.perceive("Results show p<0.05")
    assert "Peer Reviewer" in prompt
