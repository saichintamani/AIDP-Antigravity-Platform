# PHASE 2: SCIENTIFIC INTEGRITY AUDIT

## Found Violations

### 1. Simulated Evidence (Critical Severity)
- **Location:** `src/aidp/frontend/src/App.jsx` and `master_orchestrator.py`
- **Issue:** The AI debate, 3D molecule folding, vector similarity scores, and hypothesis streams are entirely hardcoded or randomized via `Math.random()`. The UI implies deep computation that is not occurring.
- **Correction:** Must wire the UI to an actual LLM inference backend (e.g. Ollama/Groq) and physical protein fetching APIs.

### 2. Benchmark Contamination / Empty Metrics (High Severity)
- **Location:** `data/ANTIGRAVITY_EVIDENCE_V1/constraint_bench_raw.json`
- **Issue:** The files exist to claim the existence of a benchmark, but contain zero actual inference data. 
- **Correction:** The benchmark must be run against live instances of GPT-4, Claude 3.5, and Llama 3 to legitimately claim evaluation.

## Verdict
If submitted as a workshop paper today, reviewers would reject it immediately under grounds of **Simulated Data**. The visual claims vastly outpace the empirical data.
