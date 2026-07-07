# Credential Readiness Report

## Objective
Verify the credential injection pathway and validation behavior required for live LLM inference.

## Required Variables
| Variable | Description | Target Provider |
|----------|-------------|-----------------|
| `OPENAI_API_KEY` | Core inference driver for Baseline A and B, reasoning loops for Baseline C. | OpenAI |
| `ANTHROPIC_API_KEY` | Secondary driver for Baseline C Debate architecture. | Anthropic |

## Loading Mechanism
- **Framework:** `litellm` (LiteLLM routing library).
- **Injection:** Read securely from standard `os.environ`.
- **Location:** Validated during `scripts/verify_connectivity.py` and strictly enforced within `scripts/run_live_discoverybench.py`.

## Validation Behavior
The `ExecutionSafetyController` natively intercepts any `litellm.InternalServerError` or `litellm.exceptions.AuthenticationError`.

## Failure Modes
1. **Missing Variables:** If keys are completely absent from the environment, `run_live_discoverybench.py` catches the initialization trace and assigns a `FAILED` status to the benchmark provenance record.
2. **Invalid Keys:** If keys are malformed or revoked, the physical network request returns an HTTP 401/403, which is trapped identically, recording the provider response inside `LIVE_RAW_OUTPUTS.json`.
3. **Budget Exhaustion (Rate Limit/Quota):** If the account budget limit is breached, the provider HTTP 429 is trapped, ending execution without fabricating output.

## Readiness Status
**READY.** The credential tracking system successfully differentiates physical failures from logic errors, preventing benchmark fabrication.
