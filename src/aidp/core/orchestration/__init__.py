import importlib.util


def has_ray() -> bool:
    """Checks if ray is installed."""
    return importlib.util.find_spec("ray") is not None


if has_ray():
    import ray
    from ray.util.actor_pool import ActorPool  # type: ignore
else:
    # Dummy mock for type checking on environments without ray
    ray = None
    ActorPool = None


from typing import cast
from unittest.mock import MagicMock

from aidp.intelligence.agent import BaseAgent  # noqa: E402
from aidp.intelligence.providers.base import BaseProvider


class DummyRayAgent(BaseAgent):
    """
    A simple concrete agent for the orchestrator to instantiate inside Ray workers.
    """
    def __init__(self) -> None:
        dummy_provider = cast(BaseProvider, MagicMock())
        super().__init__("Dummy", "Simulates agent for orchestration tests", dummy_provider)

    def perceive(self, payload: str) -> str:
        return f"Ray Orchestrated payload: {payload}"


if has_ray():

    @ray.remote
    class AIDPActor:
        """
        A Ray Actor wrapping our Agent.
        This provides stateful, parallelized execution of the agent metacognition loop.
        """

        def __init__(self) -> None:
            self.agent = DummyRayAgent()

        def process_payload(self, payload: str) -> bytes:
            """
            Receives a string, passes it through the agent's execute_cycle,
            and returns the resulting CognitiveObject bytes.
            """
            return self.agent.execute_cycle(payload)
else:

    class AIDPActor:  # type: ignore
        pass


class AgentOrchestrator:
    """
    Orchestrates a pool of Ray actors to parallelize agent execution.
    """

    def __init__(self, num_workers: int = 2) -> None:
        if not has_ray():
            raise RuntimeError("Ray is not installed in this environment.")

        if not ray.is_initialized():
            ray.init(ignore_reinit_error=True)

        # Initialize a pool of independent AIDP Actors
        self.actors = [AIDPActor.remote() for _ in range(num_workers)]  # type: ignore[attr-defined]
        self.pool = ActorPool(self.actors)

    def map_payloads(self, payloads: list[str]) -> list[bytes]:
        """
        Takes a list of payloads, distributes them across the actor pool,
        and returns the resulting CognitiveObjects (in bytes).
        """
        results: list[bytes] = list(
            self.pool.map(lambda actor, v: actor.process_payload.remote(v), payloads)
        )
        return results
