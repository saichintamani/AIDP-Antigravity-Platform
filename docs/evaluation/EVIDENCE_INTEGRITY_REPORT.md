# Evidence Integrity Report

## Objective
Audit the 5 core JSON artifacts to ensure they contain sufficient fields to flawlessly reproduce a benchmark run and support statistical analysis.

## Artifact Field Audit

### 1. LIVE_BENCHMARK_EXECUTION_PROVENANCE.json
**Included Fields:** `case_id`, `timestamp`, `provider`, `model`, `runtime`, `token_usage` (input/output), `cost`, `run_identifier`.
**Integrity:** Sufficient. Uniquely IDs runs against exact timestamps to prevent confusing successive iterations.

### 2. LIVE_RAW_OUTPUTS.json
**Included Fields:** `case_id`, `baseline_output`, `rag_output`, `aidp_output`, `failure_details` (root cause, stack trace).
**Integrity:** Sufficient. Preserves the untouched, verbatim string emitted by the LLM. 
**Missing/Recommended Field:** Suggest adding a `prompt_hash` or `system_prompt` field in the future if prompt versions change, but current architecture relies on Git SHA for prompt versioning.

### 3. LIVE_RETRIEVAL_EVIDENCE.json
**Included Fields:** `case_id`, `papers_retrieved`, `evidence_quality_scores`.
**Integrity:** Sufficient for assessing vector-search relevance. 

### 4. LIVE_GOVERNANCE_AUDIT.json
**Included Fields:** `case_id`, `governance_checks_executed`, `decisions`.
**Integrity:** Sufficient.

### 5. LIVE_RUNTIME_METRICS.json
**Included Fields:** `case_id`, `scientific_correctness`, `evidence_quality`, `hallucination_rate`, `calibration`, `runtime`, `token_usage`, `cost`.
**Integrity:** Sufficient. All high-level statistics can be derived directly from these keys.

## Conclusion
The data schema defined in the JSON artifacts perfectly encapsulates an entire end-to-end execution. No critical fields are missing. The evidence package is structurally sound and reproducible.
