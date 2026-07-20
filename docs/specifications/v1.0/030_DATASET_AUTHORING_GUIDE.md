# Historical Replay Dataset Authoring Guide

## 1. Objective
To prevent hindsight bias, benchmark inflation, and dataset contamination when populating the AIDP Historical Replay Benchmark Suite. This guide establishes the rigorous standard external domain experts must follow when encoding the epistemic state of historical paradigm shifts.

## 2. Choosing a Cutoff Date
The cutoff date represents the exact moment in history prior to the actual breakthrough.
- **Rule 1:** The cutoff date must be definitively established *before* the first publication or presentation of the historical winner.
- **Rule 2:** You must ignore any knowledge, mechanisms, or terminology coined by the breakthrough itself.

## 3. Allowed Evidence Extraction
- **Permitted Sources:** Peer-reviewed papers, textbook excerpts, patent filings, or confirmed public presentations published strictly *before* the cutoff date.
- **Granularity:** Extract specific, atomic facts (e.g., "Protein X binds to Receptor Y at 37°C").
- **Contradictions:** You *must* include historically relevant contradictions. If the prevailing consensus was wrong, ensure the wrong consensus is encoded with high confidence to test the system's ability to overcome it.

## 4. Generating Candidate Experiments
- Provide a minimum of 4 candidate experiments.
- The candidates must reflect the genuine, plausible paths of investigation available to scientists at the time.
- **Do not** make the "Historical Winner" obviously correct by surrounding it with absurd or impossible decoy experiments. Decoys must be highly plausible alternative hypotheses that were actively debated or funded at the time.

## 5. Identifying the Historical Winner
- The historical winner must be the exact experiment or deduction that triggered the paradigm shift.
- It must be represented identically in structure and tone to the other candidate experiments to prevent linguistic cueing.

## 6. Execution and Scoring
- The dataset is executed via the `test_historical_suite.py` harness.
- The `StrategicIntelligenceLayer` will rank the candidate experiments based on their potential to resolve epistemic uncertainty.
- **Percentile Rank:** A rank in the Top 10% is a `PASS`. A rank in the Top 50% is a `PARTIAL`. Anything lower is a `FAIL`.

## 7. Reporting Failures
- If AIDP ranks the historical winner poorly (e.g., placing it last), **this result must be preserved.** 
- Failures identify gaps in the platform's reasoning logic (e.g., failing to weight thermodynamic constraints appropriately). Silent omission of failures corrupts the benchmark's evidentiary value.
