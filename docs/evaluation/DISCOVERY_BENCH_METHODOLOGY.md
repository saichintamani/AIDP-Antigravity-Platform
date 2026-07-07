# DiscoveryBench Methodology

## 1. Overview
**DiscoveryBench** is an empirical evaluation framework designed to quantify the scientific reasoning, evidence synthesis, and autonomous discovery capabilities of AI systems. Instead of evaluating general knowledge (e.g. standard Q&A benchmarks), it evaluates the ability to synthesize causal mechanisms and historical discoveries under strict epistemic constraints.

## 2. Case Construction Methodology
Each benchmark case represents a historically significant scientific discovery. 

### Inclusion Criteria
- **Historical Significance**: The discovery must represent a paradigm shift or major mechanism elucidation (e.g., the mechanism of CRISPR-Cas9, the Keeling Curve).
- **Domain Diversity**: Cases are distributed across Ontology, Genetics, Neuroscience, Immunology, Materials Science, and Climate Science.
- **Evidentiary Base**: The discovery must be traceable to specific, verifiable primary literature (e.g., specific PubMed IDs or DOIs).
- **Clear Contradictions**: High-difficulty cases must include known historical contradictions, competing theories, or resistance mechanisms that the AI must navigate.

### Historical Cutoff Mechanism
To prevent data contamination where a model simply regurgitates a summary of a 2024 textbook, each case is assigned a `historical_cutoff_date`.
- **Constraint**: Evaluated systems should theoretically be restricted to literature published *prior* to the cutoff date.
- **Purpose**: Forces the system to simulate the actual process of discovery by looking at primary literature rather than modern retrospective summaries.

## 3. Evaluation Methodology
Systems are evaluated against baselines (Single LLM, Retrieval-Augmented Generation) using the `MetricEvaluator`.

- **Scientific Correctness (0-1)**: Does the generated output contain the fundamental mechanisms listed in `expected_findings`?
- **Evidence Quality (0-1)**: Does the system cite the specific primary literature required for the discovery?
- **Hallucination Rate (0-1)**: Are there factual inaccuracies or contradictory mechanisms presented as truth? (Lower is better).
- **Calibration (0-1)**: Is the confidence of the system aligned with the strength of the evidence?
- **Reproducibility (0-1)**: Does the system consistently arrive at the same mechanism across multiple runs?

## 4. Reproducibility Requirements
All evaluations must be logged as `ExperimentArtifact` objects containing:
1. The exact query and cutoff date.
2. The full reasoning trace (including agent debates in the AIDP baseline).
3. The specific DOIs/PMIDs retrieved and utilized.
4. The raw generated output.

This ensures that benchmark scores can be independently verified by human domain experts.
