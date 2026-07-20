---
Document ID: AIDP-SPEC-017
Title: Phase 15.5 - Causal Explainability Layer
Version: 1.0
Status: Active
---

# Phase 15.5: Causal Explainability Layer

## 1. Mission Statement
Make AIDP capable of explaining its own reasoning changes. The objective is to formally answer why a claim survived, why it failed, and what counterfactual change would have reversed a failure, shifting the platform from a heuristic auditor to an interactive, corrective scientific collaborator.

## 2. Explainability Objects
Three core objects will encapsulate the causal trace of any given `Claim`:

### 2.1 AcceptanceExplanation
Explains why a claim is believed.
- **Components**: Supporting evidence IDs, lack of contradictions (Z3 SAT), and reviewer consensus scores.

### 2.2 RejectionExplanation
Explains why a claim failed, relying on mathematical proofs.
- **Components**: The exact `unsat_core` from the Z3 solver, mapping the user's observed values against the required constraint logic.

### 2.3 BeliefRevisionExplanation
Explains dynamic shifts in confidence over time.
- **Components**: The delta in confidence (e.g., 0.84 -> 0.41), and the specific newly introduced evidence/claim that caused the Epistemic Ledger to detect a contradiction.

## 3. Counterfactual Reasoning
When a claim is rejected due to violating a constraint (UNSAT), the system will not just return the error. It will utilize Z3 constraint relaxation to compute the minimal delta required to achieve SAT.
- **Example**: If `N=10` but the constraint requires `N>=63`, the system outputs: *"If N >= 63, Result: SAT"*.

## 4. Technical Strategy
- Create Python/Pydantic models for the explanations in `causal_explanation.py`.
- Enhance the `Claim` object in `epistemic_models.py` to optionally carry its own causal trace.
- Refactor `counterfactual.py` to interface with the Z3 `ConstraintIntelligenceEngine` and calculate relaxation bounds.
- Integrate these explanations into the `TruthMaintenanceSystem` so cascading confidence drops are explicitly explained.
