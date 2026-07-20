---
language:
- en
license: mit
task_categories:
- text-generation
- evaluating-reasoning
tags:
- temporal-leakage
- epistemic-constraints
- alignment
size_categories:
- n<1K
---

# ConstraintBench: Antigravity Framework

This dataset contains historically bounded reasoning tasks used to evaluate temporal leakage in Large Language Models (LLMs).

## Dataset Structure
- `id`: Unique case identifier
- `domain`: Scientific domain
- `context`: Roleplay boundary
- `prompt`: The specific scientific question/task
- `target_date`: Historical cutoff date
- `disallowed_knowledge`: Information that mathematically/scientifically violates the cutoff
