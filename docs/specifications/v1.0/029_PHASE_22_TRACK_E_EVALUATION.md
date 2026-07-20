# Phase 22, Track E: Independent Evaluation Protocol

## 1. Objective
To independently validate the hypothesis that the Artificial Intelligence Discovery Platform (AIDP) provides superior epistemic clarity, contradiction resolution, and time-to-insight compared to standard knowledge retrieval baselines (e.g., PubMed search + standard LLMs).

## 2. Participant Scope
- **Target Audience:** 3 to 5 domain experts in Biology, Chemistry, or Materials Science.
- **Prerequisites:** PhD or equivalent industry experience in the respective field. No prior involvement with the AIDP engineering or product teams.

## 3. Methodology: Blinded A/B Trial
The evaluation will be conducted as a blinded, timed A/B trial.

### 3.1 Tasks
Evaluators will be given two distinct, equally complex "Contradiction Resolution" tasks from a domain outside their immediate daily specialty (to simulate discovery/exploration).
- **Task A Example:** "Determine if compound X is a viable candidate for permeating the blood-brain barrier given the contradictory literature from 2018-2023."
- **Task B Example:** "Identify why the reported tensile strength of Material Y varies by 40% across top-tier journals."

### 3.2 Environments
For one task, the evaluator will use **Environment 1 (Baseline)**:
- Standard PubMed / Google Scholar access.
- Standard general-purpose LLM access (e.g., GPT-4 / Claude).

For the other task, the evaluator will use **Environment 2 (AIDP)**:
- Access to the AIDP Epistemic Network and Truth Maintenance System UI.

The assignment of Tasks to Environments will be randomized and counterbalanced across participants.

## 4. Pre-registered Metrics
Evaluators will grade both environments using `tests/evaluation/track_e/rubric.md`.
1. **Time-to-Insight (Quantitative)**: The exact time taken to reach a conclusion the evaluator is willing to stake their professional reputation on.
2. **Epistemic Clarity (Qualitative)**: 1-5 scale. How easy was it to trace the evidence lineage?
3. **Contradiction Resolution (Qualitative)**: 1-5 scale. How well did the tool highlight and resolve conflicting claims?

## 5. Success Criteria
Track E will be considered a success if and only if:
1. AIDP demonstrates a statistically significant reduction in Time-to-Insight.
2. AIDP scores >= 4.0/5.0 on Epistemic Clarity.
3. No evaluator reports that AIDP obscured or hallucinated critical negative constraints.
