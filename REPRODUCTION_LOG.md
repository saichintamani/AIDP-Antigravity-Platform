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

*(Awaiting independent reproductions...)*
