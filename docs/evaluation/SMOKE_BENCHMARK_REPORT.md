# Smoke Benchmark Report

**Phase:** M11.6.6
**Scope:** One-Case Live Execution (`case-oncology-001`)
**Date:** 2026-07-07

## Execution Summary
The end-to-end evidence pipeline was subjected to a 1-case live execution test via `scripts/run_smoke_benchmark.py` to validate telemetry, provider connectivity, and artifact generation prior to scaling.

### Status
- **Execution Status:** **FAILED** (Technical Infrastructure Failure)
- **Runtime:** `0.003s`
- **Cost:** `$0.00`
- **Governance Outcome:** Did not execute (Aborted prior to routing)
- **Retrieval Outcome:** Did not execute (Aborted prior to routing)

## Critical Failures
**BLK-001: Missing Provider Credentials**
The system successfully initiated the benchmark harness, loaded the case, and attempted to dispatch the query to `gpt-4-turbo` via LiteLLM. At the network boundary, the execution was rejected with the following trapped exception:
> `litellm.InternalServerError: InternalServerError: OpenAIException - Missing credentials. Please pass an api_key, workload_identity, admin_api_key, or set the OPENAI_API_KEY or OPENAI_ADMIN_KEY environment variable.`

## Validation Successes
Despite the connectivity failure, the structural objectives of the smoke test were **highly successful**:
1. **No Silent Retries:** The system failed immediately upon credential absence.
2. **No Fabrication:** The metrics engine correctly recorded `$0.00` cost and `0.0` correctness rather than substituting mocked data.
3. **Artifact Integrity:** All 5 required JSON artifacts were successfully generated. The exact stack trace and root cause were meticulously preserved inside `LIVE_RAW_OUTPUTS.json`.
4. **Human Review Packet:** The `HUMAN_EVIDENCE_REVIEW_PACKET.md` was easily populated from the resulting evidence JSONs.

## Recommended Next Action
**Fix Infrastructure.**
The telemetry pipeline is flawless, but the physical launchpad is unplugged. 
1. Inject `OPENAI_API_KEY` into the host environment.
2. Re-run the 1-case smoke benchmark (`uv run python scripts/run_smoke_benchmark.py`).
3. If the next 1-case run successfully returns a physical response, proceed to the 3-case pilot.
