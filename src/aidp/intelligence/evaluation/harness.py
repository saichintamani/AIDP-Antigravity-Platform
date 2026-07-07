import json
from dataclasses import dataclass
from typing import Any

from aidp.intelligence.providers.capabilities import ReasoningTier
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.routing import RoutingPolicy
from aidp.intelligence.reasoning_planner import ReasoningPlanner
from aidp.intelligence.task_specification import CognitiveTaskType, TaskSpecification


@dataclass
class EvaluationResult:
    provider_name: str
    total_calls: int
    success_rate: float
    avg_latency_ms: float
    total_cost: float
    schema_failures: int
    safety_violations: int


class EvaluationHarness:
    """
    Empirically benchmarks providers across simulated AIDP workloads.
    """

    def __init__(self, routing_policy: RoutingPolicy) -> None:
        self.routing_policy = routing_policy
        self.gateway = IntelligenceGateway(routing_policy=self.routing_policy)

    def run_benchmark(
        self, provider_name: str, test_cases: list[dict[str, Any]]
    ) -> EvaluationResult:
        """
        Runs a suite of prompts against a specific provider to calculate empirical metrics.
        We force the routing policy to only see this single provider during the test.
        """
        original_providers = self.routing_policy._providers

        if provider_name not in original_providers:
            raise ValueError(f"Provider {provider_name} not registered in RoutingPolicy.")

        # Isolate to single provider for test
        self.routing_policy._providers = {provider_name: original_providers[provider_name]}
        self.gateway.traces = []  # Clear traces

        for case in test_cases:
            try:
                self.gateway.query(
                    prompt=case["prompt"],
                    schema_hint=case.get("schema_hint"),
                    min_tier=ReasoningTier.BASIC,
                )
            except Exception:
                # Gateway will record the trace even on failure
                pass

        # Restore providers
        self.routing_policy._providers = original_providers

        # Calculate metrics from traces
        traces = self.gateway.traces
        total_calls = len(traces)
        if total_calls == 0:
            return EvaluationResult(provider_name, 0, 0.0, 0.0, 0.0, 0, 0)

        successes = len([t for t in traces if t.success])
        avg_lat = sum([t.latency_ms for t in traces]) / total_calls
        cost = sum([t.estimated_cost_usd for t in traces])
        schema_failures = sum([t.retries for t in traces])
        safety_v = sum([len(t.safety_violations) for t in traces])

        return EvaluationResult(
            provider_name=provider_name,
            total_calls=total_calls,
            success_rate=(successes / total_calls) * 100.0,
            avg_latency_ms=avg_lat,
            total_cost=cost,
            schema_failures=schema_failures,
            safety_violations=safety_v,
        )

    def run_ab_benchmark(
        self, provider_a: str, provider_b: str, dataset_path: str
    ) -> dict[str, EvaluationResult]:
        """
        Executes an A/B benchmark between two providers using a golden dataset.
        """
        test_cases = []
        with open(dataset_path) as f:
            for line in f:
                if line.strip():
                    case = json.loads(line)
                    spec = TaskSpecification(
                        task_type=CognitiveTaskType(case["task_type"]),
                        context=case["context"],
                        expected_schema=case.get("expected_schema"),
                        strict_falsifiability=True,
                    )
                    test_cases.append(spec)

        # Instead of directly using the gateway, we'll use the ReasoningPlanner
        planner = ReasoningPlanner(self.gateway)

        # Original logic in run_benchmark bypassed planner, but we can reuse the isolation logic
        def evaluate_provider(provider_name: str) -> EvaluationResult:
            original_providers = self.routing_policy._providers
            if provider_name not in original_providers:
                raise ValueError(f"Provider {provider_name} not registered in RoutingPolicy.")

            self.routing_policy._providers = {provider_name: original_providers[provider_name]}
            self.gateway.traces = []

            for spec in test_cases:
                try:
                    planner.execute_task(spec)
                except Exception:
                    pass

            self.routing_policy._providers = original_providers

            traces = self.gateway.traces
            total_calls = len(traces)
            if total_calls == 0:
                return EvaluationResult(provider_name, 0, 0.0, 0.0, 0.0, 0, 0)

            successes = len([t for t in traces if t.success])
            avg_lat = sum([t.latency_ms for t in traces]) / total_calls
            cost = sum([t.estimated_cost_usd for t in traces])
            schema_failures = sum([t.retries for t in traces])
            safety_v = sum([len(t.safety_violations) for t in traces])

            return EvaluationResult(
                provider_name=provider_name,
                total_calls=total_calls,
                success_rate=(successes / total_calls) * 100.0,
                avg_latency_ms=avg_lat,
                total_cost=cost,
                schema_failures=schema_failures,
                safety_violations=safety_v,
            )

        result_a = evaluate_provider(provider_a)
        result_b = evaluate_provider(provider_b)

        return {provider_a: result_a, provider_b: result_b}
