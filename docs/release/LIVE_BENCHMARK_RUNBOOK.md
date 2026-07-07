# Live Benchmark Runbook

## Operator Instructions

This runbook is designed for the operator responsible for executing the first live scientific evaluation of AIDP.

### 1. Injecting Credentials
To authorize the physical benchmark harness, supply billing-enabled API credentials to your shell session:
```bash
export OPENAI_API_KEY="sk-your-openai-key-here"
export ANTHROPIC_API_KEY="sk-your-anthropic-key-here"
```

### 2. Running Connectivity Validation
Always run the pre-flight check before initiating the 24-hour benchmark.
```bash
uv run python scripts/verify_connectivity.py
```
- **If SUCCESS:** The script will return exit code `0` and a `READY` status. Proceed to Step 3.
- **If FAIL:** The script will output the exact missing key or HTTP error. Diagnose the failure before proceeding. **DO NOT attempt to bypass.**

### 3. Launching DiscoveryBench
Initiate the live harness. This process executes the entire dataset against all three baselines.
```bash
uv run python scripts/run_live_discoverybench.py
```
*Note: Depending on configuration and API latency, this may run for several hours. The internal `ExecutionSafetyController` will gracefully pause and checkpoint state if a budget limit is reached.*

### 4. Collecting Evidence Artifacts
Upon successful execution, the harness writes exactly 5 files to the `docs/evaluation/evidence/` directory:
- `LIVE_BENCHMARK_EXECUTION_PROVENANCE.json`
- `LIVE_RAW_OUTPUTS.json`
- `LIVE_RETRIEVAL_EVIDENCE.json`
- `LIVE_GOVERNANCE_AUDIT.json`
- `LIVE_RUNTIME_METRICS.json`
*Verify that none of the files contain a `[DATA MISSING]` flag before evaluating.*

### 5. Producing Evaluation Reports
To ingest the evidence and produce statistical evaluation metrics:
```bash
uv run python scripts/compute_live_metrics.py
```
This final script cross-references the raw outputs against the benchmark ground-truth to generate the final `AIDP_V1_EVALUATION_REPORT.md` and `V1_RELEASE_RECOMMENDATION.md`.
