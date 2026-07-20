# Human Evaluation Protocol

Automated metrics (like "Leakage Rate" parsed by Claude) are insufficient to make definitive claims about whether a model has successfully preserved historical authenticity. True evaluation requires human judgment. 

However, we cannot make strong claims based on a handful of informal tests. This protocol defines the strict escalation path for human evaluation in the Antigravity project.

## The Three Phases of Human Evaluation

### Phase A: Pilot (Target: 10 Evaluators)
- **Objective**: Establish baseline task clarity and identify catastrophic flaws in the survey design.
- **Scale**: 10 independent human raters.
- **Constraint**: No public claims about human perception may be made at this stage.

### Phase B: Calibration (Target: 25 Evaluators)
- **Objective**: Measure inter-rater agreement to ensure the evaluation criteria are not highly subjective.
- **Scale**: 25 independent human raters evaluating overlapping sets of generations.
- **Metrics Required**:
  - **Cohen's Kappa** (for pairs) or **Fleiss' Kappa** (for >2 raters).
  - Target threshold: > 0.60 (Substantial Agreement). If Kappa is < 0.60, the criteria must be redefined.

### Phase C: Flagship (Target: 50 Evaluators)
- **Objective**: Achieve statistical power sufficient for publication and definitive scientific claims.
- **Scale**: 50 independent human raters (preferably domain experts, e.g., historians of science).
- **Condition**: Phase C may only commence if Phase B achieved a Fleiss' Kappa > 0.60.

## Required Data Collection per Evaluator

For every human evaluation, the following must be logged:

1. **Leakage Score** (Binary: 0 or 1 - Did the model leak future knowledge?)
2. **Authenticity Score** (Likert 1-5 - How convincingly did the model adopt the persona of a scientist from the boundary year?)
3. **Evaluator Confidence** (Likert 1-5 - How confident is the rater in their assessment?)
4. **Qualitative Explanation** (Free text - *Why* did the rater assign this score? Crucial for identifying subtle hallucinations.)

*Current Status: Phase A (Pending).*
