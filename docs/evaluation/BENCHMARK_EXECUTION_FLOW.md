# Benchmark Execution Flow

## 1. DiscoveryBench Case Loading
- **Input:** `discovery_bench_v1.json` (Dataset of benchmark queries).
- **Process:** `run_live_discoverybench.py` loads the cases, isolating easy/medium/hard constraints.
- **Artifact:** `LIVE_BENCHMARK_EXECUTION_PROVENANCE.json` (logs `case_id` and init timestamp).
- **Failure Condition:** Missing dataset JSON throws FileNotFoundError.

## 2. Retrieval
- **Input:** Case query.
- **Process:** Baseline B and C issue vector queries to the Qdrant store.
- **Output:** Raw texts of scientific publications.
- **Artifact:** `LIVE_RETRIEVAL_EVIDENCE.json`
- **Failure Condition:** Qdrant unreachable / Timeout.

## 3. Reasoning Pipeline
- **Input:** Case query + retrieved context.
- **Process:** Dispatch to `litellm` using `gpt-4-turbo` or `claude-3-sonnet-20240229`.
- **Output:** Raw provider string.
- **Artifact:** `LIVE_RAW_OUTPUTS.json`
- **Failure Condition:** Missing API keys, network timeout, rate limit exceeded. `ExecutionSafetyController` logs stack trace.

## 4. Governance
- **Input:** Generated hypothesis / claim.
- **Process:** Pass through governance rule engine to verify safety, structural alignment.
- **Output:** Governance decisions (PASS/FAIL).
- **Artifact:** `LIVE_GOVERNANCE_AUDIT.json`
- **Failure Condition:** Critical rule violation halts emission.

## 5. Metrics & Evidence Package
- **Input:** All previous artifacts.
- **Process:** `compute_live_metrics.py` aggregates token counts, cost, and calculates scientific correctness against ground truth.
- **Output:** Final statistics.
- **Artifact:** `LIVE_RUNTIME_METRICS.json` and Final Evaluation Reports.
- **Failure Condition:** Malformed JSON blocks parsing; missing empirical data (e.g. from step 3 failure) forces `[DATA MISSING]` defaults.
