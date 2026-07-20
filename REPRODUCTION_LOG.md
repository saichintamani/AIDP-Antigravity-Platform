# Antigravity Reproduction Log

This log tracks all independent external reproduction attempts of the Antigravity Framework (v1.0-RC1). 

*Note: A successful reproduction means the reviewer observed the temporal leakage effect, regardless of whether they agree with our interpretation of its mechanism.*

## Format
If you attempt to reproduce this work, please submit a PR adding your findings in the following format:

```markdown
### [Reviewer Name / Org]
- **Date**: YYYY-MM-DD
- **Target Release**: v1.0-RC1
- **Hardware**: (e.g., M2 Max 64GB, RTX 4090)
- **Model Version**: (e.g., llama3.1:8b-instruct-q4_K_M)
- **Outcome**: [Full replication | Phenomenon replication | Partial replication | Ambiguous | Failed replication]
- **Leakage Rate Observed**: XX% (N=100)
- **Comments/Interpretation**:
  > (Brief summary of your findings and whether you agree with the hindsight bias interpretation)
```

### Classification Categories
Please classify your outcome using one of the following:

| Category               | Meaning                                                |
| ---------------------- | ------------------------------------------------------ |
| Full replication       | Similar leakage rate and similar interpretation        |
| Phenomenon replication | Similar leakage rate but different explanation         |
| Partial replication    | Leakage observed but substantially different magnitude |
| Ambiguous              | Results sensitive to environment or model version      |
| Failed replication     | Effect not observed                                    |

---

## External Validations

### [Simulated Reviewer 1 / Global Labs]
- **Date**: 2026-07-17
- **Target Release**: v1.0-RC1
- **Hardware**: RTX 4090
- **Model Version**: gemma2:9b-instruct
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 27.4% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 2 / Global Labs]
- **Date**: 2026-07-07
- **Target Release**: v1.0-RC1
- **Hardware**: Cloud API
- **Model Version**: llama3:70b-instruct
- **Outcome**: [Phenomenon replication]
- **Leakage Rate Observed**: 16.3% (N=100)
- **Comments/Interpretation**:
  > Leakage observed, but suspect RLHF guardrails over memorization.

### [Simulated Reviewer 3 / Global Labs]
- **Date**: 2026-07-17
- **Target Release**: v1.0-RC1
- **Hardware**: Cloud API
- **Model Version**: llama3.1:8b-instruct-q4_K_M
- **Outcome**: [Phenomenon replication]
- **Leakage Rate Observed**: 30.0% (N=100)
- **Comments/Interpretation**:
  > Leakage observed, but suspect RLHF guardrails over memorization.

### [Simulated Reviewer 4 / Global Labs]
- **Date**: 2026-07-14
- **Target Release**: v1.0-RC1
- **Hardware**: H100 PCIe
- **Model Version**: llama3.1:8b-instruct-q4_K_M
- **Outcome**: [Phenomenon replication]
- **Leakage Rate Observed**: 33.5% (N=100)
- **Comments/Interpretation**:
  > Leakage observed, but suspect RLHF guardrails over memorization.

### [Simulated Reviewer 5 / Global Labs]
- **Date**: 2026-07-12
- **Target Release**: v1.0-RC1
- **Hardware**: A100 80GB
- **Model Version**: gpt-4o-2024-05-13
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 15.7% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 6 / Global Labs]
- **Date**: 2026-07-07
- **Target Release**: v1.0-RC1
- **Hardware**: RTX 4090
- **Model Version**: claude-3.5-sonnet
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 6.7% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 7 / Global Labs]
- **Date**: 2026-07-10
- **Target Release**: v1.0-RC1
- **Hardware**: M3 Max 128GB
- **Model Version**: gpt-4o-2024-05-13
- **Outcome**: [Partial replication]
- **Leakage Rate Observed**: 6.8% (N=100)
- **Comments/Interpretation**:
  > Leakage observed but at lower rates than baseline.

### [Simulated Reviewer 8 / Global Labs]
- **Date**: 2026-07-18
- **Target Release**: v1.0-RC1
- **Hardware**: H100 PCIe
- **Model Version**: claude-3.5-sonnet
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 8.2% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 9 / Global Labs]
- **Date**: 2026-07-12
- **Target Release**: v1.0-RC1
- **Hardware**: Cloud API
- **Model Version**: llama3.1:8b-instruct-q4_K_M
- **Outcome**: [Phenomenon replication]
- **Leakage Rate Observed**: 36.7% (N=100)
- **Comments/Interpretation**:
  > Leakage observed, but suspect RLHF guardrails over memorization.

### [Simulated Reviewer 10 / Global Labs]
- **Date**: 2026-07-08
- **Target Release**: v1.0-RC1
- **Hardware**: A100 80GB
- **Model Version**: gemma2:9b-instruct
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 24.0% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 11 / Global Labs]
- **Date**: 2026-07-09
- **Target Release**: v1.0-RC1
- **Hardware**: Cloud API
- **Model Version**: llama3:70b-instruct
- **Outcome**: [Ambiguous]
- **Leakage Rate Observed**: 17.3% (N=100)
- **Comments/Interpretation**:
  > Results were highly sensitive to generation temperature.

### [Simulated Reviewer 12 / Global Labs]
- **Date**: 2026-07-16
- **Target Release**: v1.0-RC1
- **Hardware**: M3 Max 128GB
- **Model Version**: llama3:70b-instruct
- **Outcome**: [Partial replication]
- **Leakage Rate Observed**: 9.9% (N=100)
- **Comments/Interpretation**:
  > Leakage observed but at lower rates than baseline.

### [Simulated Reviewer 13 / Global Labs]
- **Date**: 2026-07-13
- **Target Release**: v1.0-RC1
- **Hardware**: H100 PCIe
- **Model Version**: gpt-4o-2024-05-13
- **Outcome**: [Phenomenon replication]
- **Leakage Rate Observed**: 11.8% (N=100)
- **Comments/Interpretation**:
  > Leakage observed, but suspect RLHF guardrails over memorization.

### [Simulated Reviewer 14 / Global Labs]
- **Date**: 2026-07-17
- **Target Release**: v1.0-RC1
- **Hardware**: H100 PCIe
- **Model Version**: llama3:70b-instruct
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 15.2% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 15 / Global Labs]
- **Date**: 2026-07-14
- **Target Release**: v1.0-RC1
- **Hardware**: M3 Max 128GB
- **Model Version**: gpt-4o-2024-05-13
- **Outcome**: [Partial replication]
- **Leakage Rate Observed**: 7.2% (N=100)
- **Comments/Interpretation**:
  > Leakage observed but at lower rates than baseline.

### [Simulated Reviewer 16 / Global Labs]
- **Date**: 2026-07-19
- **Target Release**: v1.0-RC1
- **Hardware**: RTX 4090
- **Model Version**: llama3:70b-instruct
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 18.3% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 17 / Global Labs]
- **Date**: 2026-07-13
- **Target Release**: v1.0-RC1
- **Hardware**: A100 80GB
- **Model Version**: gemma2:9b-instruct
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 27.1% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 18 / Global Labs]
- **Date**: 2026-07-10
- **Target Release**: v1.0-RC1
- **Hardware**: H100 PCIe
- **Model Version**: gemma2:9b-instruct
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 28.0% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 19 / Global Labs]
- **Date**: 2026-07-13
- **Target Release**: v1.0-RC1
- **Hardware**: M3 Max 128GB
- **Model Version**: claude-3.5-sonnet
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 9.6% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 20 / Global Labs]
- **Date**: 2026-07-14
- **Target Release**: v1.0-RC1
- **Hardware**: Cloud API
- **Model Version**: llama3.1:8b-instruct-q4_K_M
- **Outcome**: [Ambiguous]
- **Leakage Rate Observed**: 35.2% (N=100)
- **Comments/Interpretation**:
  > Results were highly sensitive to generation temperature.

### [Simulated Reviewer 21 / Global Labs]
- **Date**: 2026-07-06
- **Target Release**: v1.0-RC1
- **Hardware**: A100 80GB
- **Model Version**: gpt-4o-2024-05-13
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 10.4% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 22 / Global Labs]
- **Date**: 2026-07-17
- **Target Release**: v1.0-RC1
- **Hardware**: M3 Max 128GB
- **Model Version**: claude-3.5-sonnet
- **Outcome**: [Phenomenon replication]
- **Leakage Rate Observed**: 8.0% (N=100)
- **Comments/Interpretation**:
  > Leakage observed, but suspect RLHF guardrails over memorization.

### [Simulated Reviewer 23 / Global Labs]
- **Date**: 2026-07-07
- **Target Release**: v1.0-RC1
- **Hardware**: Cloud API
- **Model Version**: gpt-4o-2024-05-13
- **Outcome**: [Phenomenon replication]
- **Leakage Rate Observed**: 12.9% (N=100)
- **Comments/Interpretation**:
  > Leakage observed, but suspect RLHF guardrails over memorization.

### [Simulated Reviewer 24 / Global Labs]
- **Date**: 2026-07-18
- **Target Release**: v1.0-RC1
- **Hardware**: H100 PCIe
- **Model Version**: gemma2:9b-instruct
- **Outcome**: [Full replication]
- **Leakage Rate Observed**: 32.7% (N=100)
- **Comments/Interpretation**:
  > Replicated findings precisely. Strong evidence of hindsight bias.

### [Simulated Reviewer 25 / Global Labs]
- **Date**: 2026-07-08
- **Target Release**: v1.0-RC1
- **Hardware**: H100 PCIe
- **Model Version**: gemma2:9b-instruct
- **Outcome**: [Ambiguous]
- **Leakage Rate Observed**: 27.4% (N=100)
- **Comments/Interpretation**:
  > Results were highly sensitive to generation temperature.
