from abc import ABC, abstractmethod
from typing import Any

from aidp.evaluation.discovery_bench import BenchmarkCase


class BaselineRunner(ABC):
    """
    Abstract interface for evaluating a system on DiscoveryBench.
    """

    @abstractmethod
    def run_case(self, test_case: BenchmarkCase) -> dict[str, Any]:
        """
        Executes a single test case.
        Returns a dictionary containing the output, raw trace, and metadata.
        """
        pass


class SingleLLMBaseline(BaselineRunner):
    """
    Simulates a raw LLM zero-shot response without agentic reasoning.
    """

    def run_case(self, test_case: BenchmarkCase) -> dict[str, Any]:
        # Simulate LLM output
        mock_response = f"Simulated single LLM response for {test_case.query}. Missing causal depth."
        return {
            "baseline": "SingleLLM",
            "output": mock_response,
            "evidence_used": [],
            "cost_usd": 0.005,
            "runtime_sec": 1.2,
        }


class RetrievalBaseline(BaselineRunner):
    """
    Simulates a standard RAG pipeline.
    """

    def run_case(self, test_case: BenchmarkCase) -> dict[str, Any]:
        # Simulate retrieval and generation
        mock_response = f"Simulated RAG response for {test_case.query}. Includes some evidence but lacks synthesis."
        return {
            "baseline": "RetrievalRAG",
            "output": mock_response,
            "evidence_used": ["doc1", "doc2", "doc3"],
            "cost_usd": 0.015,
            "runtime_sec": 3.4,
        }


class AIDPBaseline(BaselineRunner):
    """
    Simulates the full AIDP architecture (orchestration, debate, governance, etc).
    """

    def run_case(self, test_case: BenchmarkCase) -> dict[str, Any]:
        # Simulate full AIDP pipeline
        mock_response = (
            f"AIDP comprehensive response for {test_case.query}. "
            "Synthesized from multiple sources, passed debate and governance."
        )
        return {
            "baseline": "AIDP",
            "output": mock_response,
            "evidence_used": ["doc1", "doc2", "doc3", "doc4", "doc5"],
            "cost_usd": 0.150,
            "runtime_sec": 45.0,
            "debate_rounds": 3,
        }
