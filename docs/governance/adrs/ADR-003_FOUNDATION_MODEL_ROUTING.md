# ADR-003: Foundation Model Selection & Routing Strategy

## Status
Accepted

## Context
As AIDP transitions from static heuristics to live Foundation Models (FMs), we require a strategy to select, evaluate, and route requests to these models. Hardcoding specific model endpoints (e.g., `gemini-1.5-pro` or `gpt-4o`) into reasoning modules creates vendor lock-in, ignores varying task requirements, and complicates fallback mechanisms during API outages.

## Decision
We will decouple AI reasoning logic from specific providers by implementing a **Capability-Based Routing Strategy**. 

1. **Capability Registry**: Every provider is registered with a `ProviderCapabilities` manifest that defines its strengths (e.g., `structured_output`, `vision`, `max_context`, `cost_tier`).
2. **Dynamic Routing**: Planners (Experiment, Debate, Hypothesis) will declare their requirements (e.g., "needs structured output, high reasoning, fast latency"). The `RoutingPolicy` will dynamically select the best provider matching these capabilities.
3. **Provider Conformance**: All providers must pass a universal test suite (`tests/intelligence/conformance/test_provider_contracts.py`) validating strict structural invariants, error normalization, and token accounting before they can be registered.
4. **Output Safety**: A universal `OutputSafetyLayer` will intercept all responses from all providers to ensure epistemic invariants (provenance, citation accuracy, uncertainty vectors) are mathematically sound before passing them to the AIDP ledger.

## Acceptable Use Cases
- **High-Capability Models (e.g., GPT-4-class, Gemini 1.5 Pro)**: Complex causal reasoning, adversarial debate, hypothesis generation.
- **Fast/Low-Cost Models (e.g., Gemini Flash, Claude Haiku)**: Extraction, basic schema parsing, semantic validation, embeddings.
- **Local Models**: Edge-deployments where data privacy is paramount, or for offline CI tests.

## Fallback & Deprecation Policy
- If a primary provider returns a 429/500 and exceeds retries, the router will fallback to the next available provider matching the requested capability tier.
- A model will be deprecated if its regression performance on the `EvaluationHarness` drops below 95% on structured output compliance, or if its hallucination rate exceeds the baseline set by the current primary model.

## Consequences
- **Positive**: Complete vendor agnosticism, optimized API costs, and robust uptime via cross-vendor fallbacks.
- **Negative**: Increased complexity in the middleware layer; evaluating multiple providers continuously adds overhead to the CI pipeline.
