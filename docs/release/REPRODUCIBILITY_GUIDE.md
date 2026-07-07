# AIDP Reproducibility Guide

## Environment Setup
AIDP requires a standard Python environment (`>=3.11`) configured with `uv` for dependency management. 

1. **Clone and Enter Directory:**
   ```bash
   git clone <repository_url> aidp
   cd aidp
   ```
2. **Install Dependencies:**
   ```bash
   uv pip install -e .
   ```
   *Note: Ensure `litellm` and `openai` are installed if executing live benchmarks.*

## Benchmark Execution Procedure
1. **Inject Credentials:** You must provide active billing-enabled API keys.
   ```bash
   export OPENAI_API_KEY="sk-..."
   export ANTHROPIC_API_KEY="sk-..."
   ```
2. **Verify Connectivity:**
   ```bash
   uv run python scripts/verify_connectivity.py
   ```
   *Expected output: Exit code 0 with `READY` status.*
3. **Execute Harness:**
   ```bash
   uv run python scripts/run_live_discoverybench.py
   ```

## Evidence Artifact Generation
The execution harness enforces the automatic generation of 5 strict JSON files directly to `docs/evaluation/evidence/`. No manual intervention is required.
- `LIVE_BENCHMARK_EXECUTION_PROVENANCE.json`
- `LIVE_RAW_OUTPUTS.json`
- `LIVE_RETRIEVAL_EVIDENCE.json`
- `LIVE_GOVERNANCE_AUDIT.json`
- `LIVE_RUNTIME_METRICS.json`

## Expected Outputs
- Execution generates raw output strings sourced entirely from external LLM providers.
- Total cost will strictly adhere to the `budget_cap_usd` defined in `scripts/benchmark_execution_config.yaml`.
- The metrics engine will subsequently grade scientific correctness based purely on the `LIVE_RAW_OUTPUTS.json` payload against the benchmark ground truth.
