# Human Evidence Review Packet

*This document is a template. It should be duplicated and completed by a human evaluator immediately following a live benchmark execution.*

## 1. Run Metadata
- **Run ID:** `[e.g., run_case-oncology-001_1718000000]`
- **Date/Time:** `[YYYY-MM-DD HH:MM UTC]`
- **Model(s):** `[e.g., gpt-4-turbo, claude-3-sonnet]`
- **Provider(s):** `[e.g., OpenAI, Anthropic]`
- **Benchmark Cases Executed:** `[List of case IDs, e.g., 3-case pilot]`
- **Total Cost:** `[$0.00]`
- **Total Runtime:** `[0.0s]`

## 2. Connectivity Validation
- **Provider Authentication Results:** `[PASS / FAIL]`
- **Any Failures:** `[List any network/API errors encountered during pre-flight]`

## 3. Case-by-Case Review

### Case ID: `[Insert Case ID]`
- **DiscoveryBench Query:** `[The scientific question]`
- **Ground-Truth Discovery:** `[The expected conclusion]`
- **AIDP Output (Baseline C):** `[The actual hypothesis/claim emitted]`
- **Retrieval Evidence Used:** `[List of PMIDs/DOIs utilized by the model]`
- **Governance Outcome:** `[PASS / FAIL and why]`
- **Human Assessment Notes:** `[Subjective review of reasoning quality, leaps of logic, or missing steps]`

*(Duplicate Section 3 for each case evaluated)*

## 4. Metrics Summary
*(Extracted from `LIVE_RUNTIME_METRICS.json`)*
| Metric | Value | Target |
|--------|-------|--------|
| **Scientific Correctness** | `%` | `> 85%` |
| **Evidence Quality** | `0.0` | `> 0.8` |
| **Hallucination Rate** | `%` | `< 5%` |
| **Calibration (Brier Score)** | `0.0` | `< 0.2` |
| **Average Runtime** | `s` | `< 120s` |
| **Average Cost / Case** | `$` | `< $5.00` |

## 5. Baseline Comparison
| Baseline | Correctness | Hallucination Rate | Cost | Human Verdict |
|----------|-------------|--------------------|------|---------------|
| **Baseline A (Single LLM)** | `%` | `%` | `$` | `[Notes]` |
| **Baseline B (Retrieval)** | `%` | `%` | `$` | `[Notes]` |
| **Baseline C (AIDP)** | `%` | `%` | `$` | `[Notes]` |

## 6. Failure Analysis
- **Retrieval Failures:** `[Did the vector store surface irrelevant papers?]`
- **Reasoning Failures:** `[Did the LLM misinterpret the evidence?]`
- **Governance Rejections:** `[Were valid hypotheses blocked by overly strict rules?]`
- **Provider/API Failures:** `[Rate limits, timeouts, token limit breaches?]`

## 7. Key Findings
- **What Worked:** `[e.g., Governance successfully blocked ungrounded claims]`
- **What Failed:** `[e.g., Multi-agent debate cost $10/case without improving accuracy]`
- **What Surprised Us:** `[e.g., Baseline B outperformed AIDP on simple queries]`

## 8. Final Recommendation
*Check one based purely on empirical evidence:*
- [ ] **Continue Benchmark Expansion** (Proceed to full 1000-case DiscoveryBench)
- [ ] **Tune Governance** (Rules are too strict/loose)
- [ ] **Tune Retrieval** (Embeddings are failing to fetch relevant domain context)
- [ ] **Revisit Architecture** (The fundamental cognitive approach requires redesign)
- [ ] **Stop Project** (Baselines definitively outperform the complex architecture)
