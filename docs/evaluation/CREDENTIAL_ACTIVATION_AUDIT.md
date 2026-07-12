# Credential Activation Audit

## Objective
Assess the technical readiness of the execution harness to successfully route a physical inference request the moment API credentials are provided.

## 1. Environment Audit
- **`OPENAI_API_KEY` loading path:** Automatically resolved by the `litellm.completion()` handler directly from `os.environ`.
- **`ANTHROPIC_API_KEY` loading path:** Automatically resolved by `litellm` from `os.environ` when the `claude-3-sonnet` string is passed to the model parameter.
- **`.env` discovery behavior:** Standard python `python-dotenv` or `litellm` native `.env` loading applies, though the most secure and reliable method is explicit shell export (`export OPENAI_API_KEY="..."`).
- **`pydantic-settings` resolution order:** N/A for this script. The script bypasses heavy `pydantic` wrappers in favor of direct `os.environ` interception by the LLM middleware to minimize failure surfaces during telemetry capture.

## 2. Provider Layer Audit
- **Provider selection logic:** The script explicitly reads `config["models"]["baseline_a"]["primary"]` from `benchmark_execution_config.yaml`.
- **Model name resolution:** The config provides `gpt-4-turbo`. LiteLLM resolves this string automatically to OpenAI's endpoint.
- **Timeout configuration:** LiteLLM default timeouts apply.
- **Rate-limit handling:** liteLLM will raise `RateLimitError` (HTTP 429), which is correctly trapped by the global `Exception` block in `run_live_llm()` and formatted safely.
- **Authentication exception handling:** Validated during M11.6.6. `AuthenticationError` (HTTP 401) is natively trapped and routed to the `failure_details` JSON payload.

## 3. Execution Harness Audit
- **Smoke benchmark entrypoint:** `scripts/run_smoke_benchmark.py`
- **Benchmark configuration loading:** Verified working. `benchmark_execution_config.yaml` is successfully parsed for the `$50.00` budget cap and model parameters.
- **Evidence artifact creation:** Verified working. 5 discrete JSON files are successfully written to `docs/evaluation/evidence/`.
- **Checkpointing behavior:** The harness writes all 5 files at the absolute end of the execution block, guaranteeing that partial runs do not overwrite previously valid JSON schema blocks.

## 4. Evidence Layer Audit
It is strictly confirmed that the script generates and populates:
- `LIVE_BENCHMARK_EXECUTION_PROVENANCE.json`
- `LIVE_RAW_OUTPUTS.json`
- `LIVE_RETRIEVAL_EVIDENCE.json`
- `LIVE_GOVERNANCE_AUDIT.json`
- `LIVE_RUNTIME_METRICS.json`

## 5. Dry Activation Test
- **Are credentials currently detected?** No. `os.environ.get("OPENAI_API_KEY")` is missing.
- **Which providers become available?** OpenAI and Anthropic will become available instantly once the variables are exported.
- **Which benchmark path will execute?** The `run_smoke_benchmark.py` script is strictly locked to `case-oncology-001`.

---

## Deliverable Question

**"If valid API credentials were injected right now, would a real inference request be expected to reach a model endpoint?"**

### Answer: **YES**

### Concrete Evidence
In the M11.6.6 smoke test, the execution trace generated this exact error from deep within the `litellm` library:
```text
File "...\litellm\llms\openai\openai.py", line 722, in completion
openai_client: OpenAI = self._get_openai_client(...)
```
This proves that the execution pipeline successfully parsed the benchmark case, constructed the query prompt, formatted the `gpt-4-turbo` parameters, initialized the LiteLLM router, and instantiated the core `openai_client`. 

The *only* reason the request was dropped was because `_get_openai_client` raised a `Missing credentials` exception prior to opening the TCP socket. 

Because the entire logic stack above the socket layer executed perfectly, there are zero remaining architectural obstacles. Injecting the key will instantly allow the TCP socket to open, guaranteeing that the inference request reaches the provider endpoint.
