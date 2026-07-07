from dataclasses import dataclass
from typing import Any


@dataclass
class CognitiveTelemetryRecord:
    trace_id: str
    average_hypotheses_per_step: float
    reflection_iterations: int
    counterfactuals_explored: int
    memory_writes: int
    reasoning_latency_ms: float


class CognitiveTelemetryTracker:
    """
    Collects telemetry on the *cognitive* execution of the platform, distinct from
    infrastructure telemetry (like CPU/RAM usage).
    """

    def __init__(self) -> None:
        self.records: list[CognitiveTelemetryRecord] = []

    def record_trace_execution(self, trace_dict: dict[str, Any], latency_ms: float) -> CognitiveTelemetryRecord:
        """
        Parses a trace and extracts cognitive metrics.
        """
        # Parse steps to find hypotheses
        steps = trace_dict.get("steps", [])
        total_hyps = 0
        counterfactuals = 0
        for step in steps:
            # 1 main hypothesis + alternatives
            total_hyps += 1 + len(step.get("alternativesConsidered", []))
            if step.get("counterfactualDependency", False):
                counterfactuals += 1

        avg_hyps = total_hyps / len(steps) if steps else 0.0

        # Parse reflections/memory
        reflections = 1 if trace_dict.get("reflection") else 0
        memory_writes = len(trace_dict.get("memoryUpdates", []))

        record = CognitiveTelemetryRecord(
            trace_id=trace_dict.get("id", "unknown"),
            average_hypotheses_per_step=avg_hyps,
            reflection_iterations=reflections,
            counterfactuals_explored=counterfactuals,
            memory_writes=memory_writes,
            reasoning_latency_ms=latency_ms,
        )
        self.records.append(record)
        return record
