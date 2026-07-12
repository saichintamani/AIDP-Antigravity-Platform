# Benchmark Resume Protocol

**Objective:** Define the procedure and technical mechanism for resuming an interrupted 20-case benchmark execution without data loss or duplicate execution.

## Mechanism

1. **Incremental Persistence:** 
   The execution script (`scripts/run_live_discoverybench.py`) has been refactored to write to disk *immediately* after every individual case completes, rather than waiting for the entire 20-case loop to finish. The following artifacts are updated sequentially:
   - `LIVE_BENCHMARK_EXECUTION_PROVENANCE.json`
   - `LIVE_RAW_OUTPUTS.json`
   - `LIVE_RETRIEVAL_EVIDENCE.json`
   - `LIVE_GOVERNANCE_AUDIT.json`
   - `LIVE_RUNTIME_METRICS.json`

2. **State Recovery:** 
   Upon startup, the script parses the existing `LIVE_RAW_OUTPUTS.json` (if present) to build a set of `completed_cases`. 

3. **Skipping Logic:** 
   During the iteration over `discovery_bench_v1.json`, if a `case_id` is found in the `completed_cases` set, the script emits `--- Skipping case: {case_id} (already completed) ---` and moves to the next case.

## Resuming an Interrupted Run

If the benchmark crashes (e.g., due to an API timeout, power failure, or out-of-memory error):

1. **Do not delete any artifacts** in `docs/evaluation/evidence/`.
2. Simply **re-run the standard execution command**:
   ```powershell
   $env:PYTHONPATH="src"
   python scripts/run_live_discoverybench.py
   ```
3. The script will automatically detect the completed cases, skip them, and resume execution precisely where the crash occurred.
