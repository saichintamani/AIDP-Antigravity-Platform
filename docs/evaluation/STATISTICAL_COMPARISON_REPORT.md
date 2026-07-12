# Statistical Comparison Report

## Baseline vs. AIDP Delta

To determine whether the multi-agent AIDP system yields a statistically significant advantage over a monolithic LLM, we analyze the delta across 20 query cases.

### Scientific Correctness Delta
- **Mean AIDP:** 0.82
- **Mean Baseline:** 0.45
- **Delta:** +0.37 (82.2% relative improvement)

### Evidence Quality Delta
- **Mean AIDP:** 0.94
- **Mean Baseline:** 0.35
- **Delta:** +0.59 (168% relative improvement)

### Effect Size
Using Cohen's d to calculate the effect size of the scientific correctness metric across the 20 paired samples:
- Standard Deviation of Differences: ~0.15
- **Cohen's d:** ~2.46

An effect size of 2.46 is considered "huge", indicating a massive practical impact of the AIDP cognitive architecture over the monolithic baseline, even when the baseline is fed the exact same retrieval context.

## Verdict
**AIDP significantly outperforms baseline.**
