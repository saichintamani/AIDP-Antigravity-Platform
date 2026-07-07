# DiscoveryBench Validation Report

**Phase:** E1 — Benchmark Harness Hardening
**Objective:** Audit DiscoveryBench to ensure deterministic and valid execution.

## 1. Benchmark Case Loading
- **Dataset Path:** `src/aidp/evaluation/data/discovery_bench_v1.json`
- **Validation Execution:** `dataset_validator.py` was executed.
- **Result:** All checks passed. The dataset properly loads **20 cases**.
- **Schema Conformity:** All cases match the `BenchmarkCase` schema with `id`, `domain`, `query`, `historical_cutoff_date`, `expected_findings`, and `required_evidence_sources`.

## 2. Cutoff Dates & Provenance
- Cutoff dates are validated to be strictly between 1950 and 2025. Format checks passed.
- Provenance references are strictly enforced to begin with valid scientific literature prefixes (`PMID:` or `DOI:`).

## 3. Scoring Function Determinism
- **Audit Findings:** The `metrics.py` scoring file was originally injecting artificial performance scores based entirely on the name of the `baseline` string (e.g. `SingleLLM` vs `AIDP`).
- **Remediation:** Removed mock logic and implemented strictly deterministic metric functions.
- **Current State:**
  - **Scientific Correctness:** Case-insensitive exact substring matching of expected findings within the output.
  - **Evidence Quality:** Checks if the provided evidence citations contain the required substrings.
  - **Hallucination Rate:** Scans the output deterministically for known contradictory claims.
  - **Calibration:** Measured via distance of reported confidence to perfect confidence (simplistic but deterministic).

## 4. Reproducibility
- The harness ensures that `BenchmarkCase` instances are immutable during evaluation.
- `metrics.py` calculates scores purely based on the explicit content of the `result` dictionary and the `BenchmarkCase` definition.

## Conclusion
The DiscoveryBench harness is structurally sound, deterministic, and ready for Live Baseline Execution (Phase E2).
