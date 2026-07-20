import time
from typing import Any

from aidp.evaluation.baselines import (
    AIDPBaseline,
    BaselineRunner,
    RetrievalBaseline,
    SingleLLMBaseline,
)
from aidp.evaluation.discovery_bench import DiscoveryBenchDataset
from aidp.evaluation.metrics import MetricEvaluator


class BenchmarkRunner:
    """
    Orchestrates the evaluation of multiple baselines against the DiscoveryBench dataset.
    """

    def __init__(self) -> None:
        self.dataset = DiscoveryBenchDataset()
        self.evaluator = MetricEvaluator()
        self.baselines: dict[str, BaselineRunner] = {
            "SingleLLM": SingleLLMBaseline(),
            "RetrievalRAG": RetrievalBaseline(),
            "AIDP": AIDPBaseline(),
        }

    def run_benchmark(self) -> dict[str, Any]:
        """
        Runs all configured baselines on all dataset cases.
        """
        results: dict[str, Any] = {}

        for baseline_name, runner in self.baselines.items():
            results[baseline_name] = {"cases": [], "aggregate": {}}
            print(f"Running baseline: {baseline_name}")

            for case in self.dataset.get_cases():
                # Execute run
                start_t = time.time()
                run_result = runner.run_case(case)
                end_t = time.time()
                run_result["runtime_sec"] = end_t - start_t

                # Evaluate metrics
                metrics = self.evaluator.evaluate(case, run_result)
                
                results[baseline_name]["cases"].append({
                    "case_id": case.id,
                    "metrics": metrics,
                    "output": run_result.get("output", ""),
                })
            
            # Aggregate metrics for the baseline
            results[baseline_name]["aggregate"] = self._aggregate_metrics(results[baseline_name]["cases"])
            
        return results

    def _aggregate_metrics(self, case_results: list[dict[str, Any]]) -> dict[str, float]:
        if not case_results:
            return {}
        
        aggregated: dict[str, float] = {}
        for result in case_results:
            metrics = result["metrics"]
            for k, v in metrics.items():
                aggregated[k] = aggregated.get(k, 0.0) + v
        
        for k in aggregated:
            aggregated[k] /= len(case_results)
            
        return aggregated
