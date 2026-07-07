from collections.abc import Callable
from typing import Any

from aidp.intelligence.providers.middleware import GatewayTrace


class ReasoningReplayEngine:
    """
    Ingests a historical trace and re-executes the context to verify determinism.
    """

    def __init__(self, reasoning_engine_fn: Callable[[str], dict[str, Any]]) -> None:
        self.reasoning_engine_fn = reasoning_engine_fn

    def replay_and_compare(self, historical_trace: dict[str, Any]) -> float:
        """
        Re-executes the query and computes a determinism score [0.0 - 1.0].
        A score of 1.0 means the reasoner followed the exact same path.
        Can also optionally extract forensics from traces if passed into the trace objects.
        """
        query = historical_trace.get("query")
        if not query:
            return 0.0

        traces = historical_trace.get("gateway_traces", [])
        if traces:
            self.validate_forensics(traces)

        new_trace = self.reasoning_engine_fn(query)

        return self._compute_diff_score(historical_trace, new_trace)

    def _compute_diff_score(self, trace_a: dict[str, Any], trace_b: dict[str, Any]) -> float:
        """
        Compares two traces. In a real implementation this would perform graph
        edit distance. Here we do a simplified matching on final decision.
        """
        if trace_a.get("finalDecision") == trace_b.get("finalDecision"):
            return 1.0
        return 0.0

    def extract_forensics(self, traces: list[GatewayTrace]) -> dict[str, Any]:
        """
        Extracts forensics from a list of GatewayTraces.
        """
        if not traces:
            return {}

        forensics: dict[str, Any] = {
            "total_queries": len(traces),
            "prompt_hashes": set(),
            "model_identifiers": set(),
            "routing_decisions": set(),
            "avg_latency": sum(t.latency_ms for t in traces) / len(traces),
            "total_cost": sum(t.estimated_cost_usd for t in traces),
        }

        for t in traces:
            forensics["prompt_hashes"].add(t.prompt_version)
            if t.model_identifier:
                forensics["model_identifiers"].add(t.model_identifier)
            if t.routing_decision:
                forensics["routing_decisions"].add(t.routing_decision)

        # Convert sets back to lists for JSON serialization downstream
        forensics["prompt_hashes"] = list(forensics["prompt_hashes"])
        forensics["model_identifiers"] = list(forensics["model_identifiers"])
        forensics["routing_decisions"] = list(forensics["routing_decisions"])

        return forensics

    def validate_forensics(self, traces: list[GatewayTrace]) -> None:
        """
        Gate 2 Validation: Ensures that traces contain all required fields
        to enable reproducibility. Fails fast if incomplete.
        """
        for t in traces:
            missing = []
            if not getattr(t, "request_id", None):
                missing.append("request_id")
            if not getattr(t, "prompt_version", None):
                missing.append("prompt_version")
            if not getattr(t, "provider_name", None):
                missing.append("provider_name")
            if not getattr(t, "routing_decision", None):
                missing.append("routing_decision")

            if missing:
                raise ValueError(
                    f"Trace {getattr(t, 'request_id', 'unknown')} missing required forensic metadata: {missing}"
                )
