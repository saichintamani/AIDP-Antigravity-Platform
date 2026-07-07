import ray


@ray.remote
class AIDPActor:
    """
    A foundational Ray Actor for the AIDP platform.
    This serves as the base template for distributed cognitive execution.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.invocations = 0

    def ping(self) -> str:
        self.invocations += 1
        return f"ACK from {self.name} (invocations: {self.invocations})"

    def get_invocations(self) -> int:
        return self.invocations
