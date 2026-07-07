from aidp.intelligence.agent import BaseAgent
from aidp.intelligence.providers.mock import MockProvider


class DummyAgent(BaseAgent):
    def perceive(self, payload: str) -> str:
        return f"Analyze this context: {payload}"


def test_agent_reasoning_loop_e2e() -> None:
    provider = MockProvider()
    agent = DummyAgent(provider)

    # 1. Initial State should be totally uncertain
    assert agent.internal_state.uncertainty == 1.0

    # 2. Execute short cycle
    obj_bytes = agent.execute_cycle("short")
    assert isinstance(obj_bytes, bytes)
    assert len(obj_bytes) > 0

    # After first cycle, agent should be less uncertain
    assert agent.internal_state.uncertainty < 1.0

    # 3. Execute long cycle
    obj_bytes_2 = agent.execute_cycle("long payload " * 20)
    assert isinstance(obj_bytes_2, bytes)

    # Belief should increase due to the simulated LLM logic and Subjective Logic fusion
    assert agent.internal_state.belief > 0.4
