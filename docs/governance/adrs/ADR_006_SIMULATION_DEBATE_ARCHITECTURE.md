# ADR-006: Predictive Scientific Reasoning Architecture

## Status
Proposed

## Context
With ResearchOps (ADR-005) managing resources and the Cognitive Core (ADR-004) managing agent evolution, the AIDP lacks a vital capability: **Reasoning before Executing**. A real scientist mentally simulates experiments, anticipates failure modes, undergoes rigorous debate, and revises methodologies *before* committing laboratory resources. AIDP must evolve its Cluster 4 from simple "Distributed Debate" into a full **Predictive Scientific Reasoning Engine (PSRE)** to maximize Expected Information Gain (EIG) and publication probability.

## Decision
We will implement the PSRE within a new `src/aidp/reasoning_engine/` module, acting as the laboratory's "imagination" and rigorous vetting ground.

### 1. Digital Twin & Simulation Engine
Before an experiment enters the `ResearchOps` queue, it is modeled in a `DigitalTwin` laboratory. The `SimulationEngine` runs (currently deterministic/lightweight stochastic) models to predict outcomes, calculating prior probabilities and EIG.

### 2. Recursive Debate & Reviewer Tournaments
Peer review will transition into a `DebateGraph` (a DAG). Furthermore, instead of single reviewers, the system will use a `ReviewerTournament` where random pools of agents independently review, rank, and form consensus, dramatically filtering out hallucinations. If consensus is low, the system will self-correct by recruiting new reviewers to expand the graph.

### 3. The Adversarial Scientist
A dedicated "Devil's Advocate" agent will systematically attack conclusions, search for hidden assumptions, and generate counter-hypotheses. This breaks confirmation bias prior to execution.

### 4. Counterfactual & Causal Sandbox
The `CounterfactualEngine` will generate "What if?" alternate worlds. The `CausalSandbox` allows agents to test interventions (e.g., "Decrease Protein X") logically to observe predicted outcomes, grounding the reasoning in causality rather than correlation.

### 5. Risk & Discovery Value Engines
The `RiskEngine` scores experiments across Scientific, Economic, Ethical, Execution, and Reproducibility risk axes. The `DiscoveryValueEngine` calculates the master objective function: `Novelty × Scientific Impact × Expected Information Gain × Publication Probability`. 

### 6. Autonomous Experiment Revision
If an experiment's Discovery Value is too low or Risk is too high, it is not simply rejected. The `ExperimentReviser` autonomously modifies weak variables, recalculates metrics, and simulates again until approval criteria are met.

## Consequences
- **Positive**: AIDP transforms into a system that predicts, critiques, revises, and optimizes scientific work autonomously. Experimental failure rates in physical/API space should plummet.
- **Negative**: The complexity of the reasoning graph and tournament logic will drastically increase token latency during the planning phase. We will follow the recommendation to keep Monte Carlo simulations lightweight/deterministic initially to prevent unmanageable state explosions.
