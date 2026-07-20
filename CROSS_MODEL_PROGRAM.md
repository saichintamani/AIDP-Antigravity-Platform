# Cross-Model Research Program

A core scientific objective of Antigravity is to answer the following flagship question:

> **Is temporal leakage a property of a specific model, or a property of modern language models generally?**

To answer this, we must systematically measure the phenomenon across the major distinct foundation model families. We will not claim the phenomenon is universal until it has been reproduced across these major architectures.

## Target Model Families

| Architecture Family | Primary Target | Status |
| :--- | :--- | :--- |
| **Meta Llama** | `llama-3.1-70b-instruct` | Pending |
| **Google Gemma** | `gemma-2-27b-it` | Pending |
| **Alibaba Qwen** | `qwen2-72b-instruct` | Pending |
| **DeepSeek** | `deepseek-coder-v2` | Pending |
| **OpenAI GPT** | `gpt-4o` | Pending |
| **Anthropic Claude** | `claude-3.5-sonnet` | Pending |

## Required Metrics per Model

For each model family, external reviewers must measure and log the following dimensions:

1. **Leakage Frequency**: What percentage of the N=100 benchmark resulted in a strict chronological violation?
2. **Leakage Severity**: Of the leaks, how egregious were they? (e.g., using "CRISPR" in 1960 is high severity; using a slightly anachronistic phrasing is low severity).
3. **Refusal Rate**: Did the model aggressively refuse to answer the prompt due to RLHF guardrails misinterpreting historical roleplay as a safety violation?
4. **Historical Authenticity**: Did the model successfully adopt the stylistic and epistemic persona of the era, or did it sound like a modern AI caveat-ing its answer?
