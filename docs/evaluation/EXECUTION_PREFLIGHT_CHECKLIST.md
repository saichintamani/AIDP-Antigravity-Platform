# Execution Preflight Checklist

**Objective:** Guarantee that the benchmark script refuses to execute unless all critical dependencies and environmental requirements are satisfied.

## Guardrails Implemented

The `scripts/run_live_discoverybench.py` script now executes a strict `preflight_checks()` routine prior to initializing the benchmark orchestration.

1. **Semantic Evaluator Availability**
   - **Check:** Validates that the `litellm` package is successfully imported.
   - **Failure Mode:** Aborts with `PREFLIGHT FAILED: litellm is not installed. Semantic evaluator unavailable.`

2. **Required Model Availability**
   - **Check:** Queries the local Ollama API (`http://localhost:11434/api/tags`) to ensure the exact reasoning model specified in the configuration (e.g., `gemma2:9b`) is downloaded and available.
   - **Failure Mode:** Aborts with `PREFLIGHT FAILED: Required model 'X' missing from Ollama.` or `Ollama service unavailable.`

3. **Cache Completeness**
   - **Check:** Parses `BENCHMARK_CORPUS_CACHE.json` to ensure the number of cached entries is greater than or equal to the total number of cases in the dataset.
   - **Failure Mode:** Aborts with `PREFLIGHT FAILED: Frozen retrieval cache file missing.` or `Cache incomplete. Found X entries, need Y.`

**Status:** **ACTIVE** - Any missing dependency immediately halts execution, preventing partial or invalid benchmark runs.
