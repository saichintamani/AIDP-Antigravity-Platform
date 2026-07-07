import uuid
from dataclasses import dataclass, field


@dataclass
class ResourceReservation:
    id: str = field(default_factory=lambda: f"res_{uuid.uuid4()}")
    tokens_estimated: int = 0
    gpu_hours_estimated: float = 0.0
    api_calls_estimated: int = 0


class ResourceManager:
    """
    Tracks and allocates resources for the entire laboratory.
    Experiments must reserve resources here before execution.
    """

    def __init__(self) -> None:
        self.available_gpus = 4
        self.active_reservations: dict[str, ResourceReservation] = {}

    def reserve_resources(self, req: ResourceReservation) -> bool:
        """Attempts to reserve resources. Returns True if successful."""
        # Simple mock for Phase C: Always succeeds unless explicitly blocked
        self.active_reservations[req.id] = req
        return True

    def release_resources(self, reservation_id: str) -> None:
        if reservation_id in self.active_reservations:
            del self.active_reservations[reservation_id]
