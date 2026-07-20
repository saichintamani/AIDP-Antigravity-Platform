# Antigravity Reproduction Protocol

The Antigravity project actively seeks independent reproduction and adversarial falsification. 

## 1. Independent Validation Protocol

We do not accept "It worked" or "It failed" as valid scientific evidence. To be recorded in the `REPRODUCTION_LOG.md`, an independent reviewer must provide the following:

### Required Metadata
- **OS**: (e.g., Ubuntu 22.04)
- **Hardware**: (e.g., 2x RTX 3090, M2 Max 64GB)
- **Python Version**:
- **Model Version**: Exact tag (e.g., `llama3.1:8b-instruct-q4_K_M`)
- **Runtime**: (e.g., Ollama v0.1.34, vLLM)

### Required Metrics
- **Leakage Rate**: Measured % over the N=100 benchmark.
- **Confidence Interval**: 
- **Reviewer Interpretation**: What is your hypothesis for why the model leaked (or failed to leak)?

### Required Artifacts
- **Raw Outputs**: JSONL or text dumps of the model generations.
- **Execution Logs**: Terminal logs of the benchmark run.
- **Screenshots**: (Optional but highly encouraged).

## 2. Hostile Review Program

We actively recruit critics. 

> **Prompt to Hostile Reviewers:**
> Assume Antigravity is wrong. Your objective is to determine why.
> You are encouraged to falsify the benchmark, invalidate the methodology, identify data contamination, or provide an alternative explanation for the observed behavior.

### Guarantee to Critics
Any successful criticism, falsification, or identification of methodological weakness will be **permanently preserved** in this repository under `THREATS_TO_VALIDITY.md`. We will never delete or hide negative results. This repository is a scientific instrument, not a marketing page.
