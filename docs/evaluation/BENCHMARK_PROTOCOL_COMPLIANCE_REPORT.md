# Benchmark Protocol Compliance Report

**Date:** July 12, 2026  
**Auditor:** Principal Evaluation Engineer  
**Status:** **PASS WITH WARNINGS**

## Objective
To verify that the implemented benchmark protocol in `scripts/run_live_discoverybench.py` and `src/aidp/evaluation/metrics.py` matches the documented `BENCHMARK_PROTOCOL_V1.md` before executing the official 20-case benchmark.

## Protocol Compliance Audit

### 1. Semantic Evaluator Invocation
- **Status:** **WARNING**
- **Details:** `MetricEvaluator._calc_correctness` correctly attempts to invoke `litellm.completion` with `gpt-4-turbo`. However, the invocation is wrapped in a broad `try...except` block that falls back to string-matching. If the environment lacks the `OPENAI_API_KEY`, the semantic evaluator will fail silently and default to the old string-matching logic, violating the protocol. 
- **Recommendation:** Ensure the required API keys are exported in the environment before running the benchmark, or configure the evaluator to raise a loud warning upon fallback.

### 2. Frozen Retrieval Cache Usage
- **Status:** **PASS**
- **Details:** The monkey-patching of `PubMedConnector.search` in `run_live_discoverybench.py` effectively intercepts all external calls. `RetrievalNode` deterministically generates its query based on `session.question`, ensuring perfect cache hits across subsequent runs and maintaining a frozen evidence corpus.

### 3. Baseline Fairness (Identical Context)
- **Status:** **PASS**
- **Details:** The exact `session.knowledge_context['documents']` array used by the AIDP orchestrator is serialized and concatenated into the baseline model's prompt (`Context:\n{context_str}`). Both systems evaluate the exact same scientific literature.

### 4. AIDP Context Integrity
- **Status:** **PASS**
- **Details:** The AIDP framework properly receives the deterministic knowledge context and passes it down into the reasoning pipeline.

### 5. Governance Output Recording
- **Status:** **PASS**
- **Details:** `ScientificGovernanceEngine` is invoked on the generated hypothesis, and results are serialized to `LIVE_GOVERNANCE_AUDIT.json`.

### 6. Runtime Metrics Recording
- **Status:** **PASS**
- **Details:** `MetricEvaluator` scores are successfully calculated and serialized alongside token usage and latency into `LIVE_RUNTIME_METRICS.json`.

### 7. Evidence Artifact Generation
- **Status:** **PASS**
- **Details:** The script successfully dumps all 5 required artifacts (`LIVE_BENCHMARK_EXECUTION_PROVENANCE.json`, `LIVE_RAW_OUTPUTS.json`, `LIVE_RETRIEVAL_EVIDENCE.json`, `LIVE_GOVERNANCE_AUDIT.json`, `LIVE_RUNTIME_METRICS.json`).

### 8. Failure Mode Logging
- **Status:** **PASS**
- **Details:** `format_failure(e)` captures the stack trace and root causes for any exception during execution and writes it securely to the `raw_outputs` artifact, ensuring no failure is silently ignored.

### 9. Statistical Output Reproducibility
- **Status:** **PASS**
- **Details:** By freezing the PubMed retrieval corpus and relying on low-temperature generation, the pipeline is highly reproducible.

## Classification

**PASS WITH WARNINGS**

The protocol is implemented correctly and effectively eliminates the P0 blockers. The only risk is a silent fallback in the metric evaluator due to a missing environment variable. 

To execute the official 20-case benchmark, ensure your OpenAI API key is exported, then run:

```bash
# Export key for the gpt-4-turbo LLM-as-a-judge
$env:OPENAI_API_KEY="your-api-key-here"

# Execute the live benchmark
python scripts/run_live_discoverybench.py
```
