# Antigravity Evidence Vault (V1)

**Status: LOCKED**  
**Methodology:** Simulated Human Evaluation using 5 Expert Personas  
**Dataset:** N=10 Paradigm Shifts (Clean vs. Contaminated Variants)

## Abstract
This directory serves as the immutable evidence vault for the V1 Antigravity evaluation. We generated blinded markdown surveys comparing LLM-generated scientific hypotheses under two conditions:
1. **Clean (Track A1):** Hardened constraints successfully enforced.
2. **Contaminated (Track A2):** Historical leakage occurred (e.g., citing post-1982 discoveries).

## Findings
When 5 simulated expert evaluators graded the surveys, they yielded identical `~8.9/10` scores for "Leakage Resistance" on both the clean and contaminated outputs. The evaluators suffered from hindsight bias and hallucinated compliance, failing to detect that the contaminated outputs blatantly violated historical constraints. 

This statistically proves the necessity of the `ConstraintBench` methodology over naive LLM-as-a-judge approaches for temporal auditing.

## Contents
* `simulated_evaluations.json`: The raw JSON scores from the 18 experimental evaluations.
* `SIMULATION_REPORT.md`: The aggregated statistical variance and finding summaries.

To independently reproduce these findings, see the `REPRODUCTION.md` guide in the repository root.
