# Antigravity: V1 Release Notes
**Date**: July 20, 2026

## What is Antigravity?
Antigravity is a cryptographically verifiable framework for auditing whether Large Language Models (LLMs) obey historical epistemic constraints during scientific reasoning tasks.

## 🚀 V1 Features
- **ConstraintBench (N=100)**: A procedural benchmark of 100 historical scientific paradigm shifts with strict temporal cutoff dates.
- **AlignEval**: An automated evaluation system for detecting temporal leakage and hindsight bias.
- **Track E (Human Evaluation Portal)**: A locally-hosted React/FastAPI portal for blinding LLM outputs and soliciting domain-expert human evaluations.
- **Statistical Pipeline**: Automated calculation of Cohen's Kappa (Inter-Rater Reliability), False Positive Rates, and 95% Confidence Intervals for benchmark baselines.
- **Zero-Dependency Core**: The entire evaluation and validation suite runs locally using Python 3.10 and Ollama, without requiring API keys or C++/Rust compilation.

## 🔬 Call for Independent Replication
This repository is officially ready for **Hostile Scientific Review**. We are calling on independent researchers and subject-matter experts to:
1. Clone the repository.
2. Run the N=100 ConstraintBench locally on your hardware.
3. Access the `Track E` UI to blind-rank the outputs.
4. Compare your generated leakage statistics and inter-rater reliability scores with our published baselines.

See [REPRODUCTION.md](REPRODUCTION.md) for full instructions on how to replicate the pipeline from zero.

## ⚠️ Known Limitations
- The baseline data currently provided in the repository (`data/ANTIGRAVITY_EVIDENCE_V1/baselines`) serves as structural telemetry while we await wide-scale independent execution.
- We restrict evaluation to locally-executed models to prevent the `ConstraintBench` JSON from being scraped by API endpoints and contaminating future LLM training data.

We welcome PRs, independent reproduction reports, and aggressive scrutiny of the methodology.
