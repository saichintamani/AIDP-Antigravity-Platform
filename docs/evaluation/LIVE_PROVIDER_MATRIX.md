# Live Provider Matrix

This document provides an inventory of API providers available for the live DiscoveryBench evaluation.

| Provider | Status | API Key Present | Connectivity Status | Rate Limits | Estimated Cost per 1M Input / Output Tokens |
|----------|--------|----------------|---------------------|-------------|-------------------------------------------|
| **OpenAI** (gpt-4o) | Active | `OPENAI_API_KEY` expected | Connected (Verified via `litellm`) | 500 RPM, 300K TPM | $5.00 / $15.00 |
| **OpenAI** (gpt-4-turbo) | Active | `OPENAI_API_KEY` expected | Connected (Verified via `litellm`) | 500 RPM, 300K TPM | $10.00 / $30.00 |
| **Anthropic** (claude-3-opus-20240229) | Ready | `ANTHROPIC_API_KEY` expected | Unverified (Pending configuration) | 50 RPM, 40K TPM | $15.00 / $75.00 |
| **Anthropic** (claude-3-sonnet-20240229) | Ready | `ANTHROPIC_API_KEY` expected | Unverified (Pending configuration) | 50 RPM, 40K TPM | $3.00 / $15.00 |

## Provider Selection Rules
- The Live Execution Harness natively supports routing via `litellm`.
- The `benchmark_execution_config.yaml` controls the primary and fallback models per baseline.
- `gpt-4o` or `gpt-4-turbo` will serve as the default driver for Baseline A (Single LLM) and Baseline B (RetrievalRAG).
- Multi-agent debate in Baseline C (AIDP) may mix `gpt-4o` and `claude-3-sonnet` if both keys are present.
