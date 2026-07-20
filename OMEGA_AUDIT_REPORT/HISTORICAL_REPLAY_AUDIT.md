# PHASE 4: HISTORICAL REPLAY AUDIT

## Case Review
- **Prions:** UI simulates a successful hypothesis generation and protein folding (`1QLX`). Backend is mocked.
- **H. pylori:** Framework created, no data.
- **Plate Tectonics / CRISPR:** Missing from evidence logs.

## Validity Assessment
- **Temporal cutoffs:** Not enforced in backend logic.
- **Hindsight Leakage:** Extreme risk. The LLMs have read Wikipedia; evaluating them on Prions in 2026 is inherently contaminated unless strict pre-training cutoffs are used.

## Domain Expert Verdict
A domain expert would view this as a **"Toy Simulation"** until hindsight leakage is provably mitigated through either local LMs trained on specific pre-1980 corpus data, or rigorous prompting techniques that enforce amnesia (which is notoriously unreliable).
