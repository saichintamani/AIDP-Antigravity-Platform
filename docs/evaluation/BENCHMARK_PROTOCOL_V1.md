# AIDP Benchmark Protocol V1

**Version:** 1.0  
**Target:** Gemma 2 2B / 9B  
**Framework:** DiscoveryBench v1

## 1. Overview
The AIDP Benchmark Protocol guarantees that evaluating AI-driven scientific discovery is reproducible, fair to baseline systems, and scientifically rigorous. This protocol specifically targets the Gemma 2 models for execution within the DiscoveryBench framework.

## 2. Reproducibility Guarantee
To prevent context drift, all benchmark executions MUST use a **Frozen Knowledge Corpus**.
- **Mechanism:** Interception of `PubMedConnector`.
- **Cache Location:** `docs/evaluation/evidence/BENCHMARK_CORPUS_CACHE.json`
- **Behavior:** The benchmark runtime will exclusively pull from this static JSON artifact. If a query is not present in the cache during the initial run, it will be fetched and permanently serialized to this file. 

## 3. Baseline Fairness Rules
A baseline LLM (e.g., standard Gemma 2 via prompt) must be evaluated on identical footing as the AIDP Orchestrator.
- **Context Injection:** The exact `papers_retrieved` array constructed by the AIDP Retrieval Node is flattened and injected into the Baseline's prompt (`Context: \n {context_str}`).
- **Purpose:** This ensures the evaluation measures the *reasoning, planning, and synthesis* delta introduced by the AIDP Cognitive Architecture, rather than just measuring RAG capabilities.

## 4. Evaluation Metrics
### 4.1. Scientific Correctness (LLM-as-a-Judge)
- **Method:** Semantic Entailment.
- **Judge Model:** `gpt-4-turbo` (or an equivalent high-capacity instruction-tuned model).
- **Criterion:** Does the generated hypothesis affirm all `expected_findings` without introducing negations or contradictions?
- **Output:** Continuous float [0.0 - 1.0].

### 4.2. Evidence Quality
- **Method:** Multi-stage citation extraction.
- **Stage 1:** Parse structured `evidence_links` emitted by the LLM.
- **Stage 2 (Fallback):** Execute a regex sweep across the raw output for standard citation markers (`10.xxxx/yyyy`, `PMID: \d+`).
- **Criterion:** Overlap between extracted citations and `required_evidence_sources`.

### 4.3. Hallucination Rate
- **Method:** Deterministic contradiction check.
- **Criterion:** Checks for the presence of specific `known_contradictions` in the generated hypothesis.

## 5. Artifact Emittance
Every benchmark run must emit the following 5 cryptographic-ready artifacts into `docs/evaluation/evidence`:
1. `LIVE_BENCHMARK_EXECUTION_PROVENANCE.json`: Token usage, runtime, execution trace.
2. `LIVE_RAW_OUTPUTS.json`: Unadulterated strings for both AIDP and Baseline.
3. `LIVE_RETRIEVAL_EVIDENCE.json`: The frozen context chunks utilized.
4. `LIVE_GOVERNANCE_AUDIT.json`: Security and dual-use policy check outcomes.
5. `LIVE_RUNTIME_METRICS.json`: The final numerical scores per query.

**Approval:** This protocol is enforced programmatically in `scripts/run_live_discoverybench.py`.
