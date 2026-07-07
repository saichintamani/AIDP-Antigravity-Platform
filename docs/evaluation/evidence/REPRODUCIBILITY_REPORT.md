# Reproducibility Report

**Status:** SIMULATED_ONLY

## Objective
Measure the variance in score, confidence, and retrieval across 3 independent runs of the DiscoveryBench cases.

## Methodology
In a real execution environment, this involves executing the live LLM calls and live retrieval across multiple identical queries to measure non-determinism introduced by LLM temperature or retrieval drift. 

During the M11.6 simulation execution, `simulate_benchmark_run.py` was used, which utilizes `random.uniform()` to artificially generate metrics. Therefore, running the simulation three times simply generates three distinct sets of stochastic values bounds. 

## Variance Analysis (Simulated)
Because the data was generated via randomized Python functions:
- **Score Variance:** High variance is artificially present due to random sampling bounds for `SingleLLM` and `RetrievalRAG`.
- **Confidence Variance:** High variance artificially present due to random sampling.
- **Retrieval Variance:** No actual papers were retrieved; therefore, variance in paper identity is undefined. Evidence quality was randomly sampled.

## Conclusion
True reproducibility cannot be evaluated until a live benchmark is executed against real model endpoints. This report acts as a placeholder schema for the eventual live evaluation.
