# 024 Benchmark Suite Protocol

Every empirical claim made by the AIDP engineering team must be reproducible. This document dictates the required parameters for declaring a benchmark valid.

## Benchmark Template

When submitting a Benchmark Report (e.g., `docs/benchmarks/BM-001.md`), the following fields are strictly required:

```markdown
### Target Metric
- [ ] What is being measured? (e.g., Token generation latency, Sub-graph retrieval time, Hypothesis uncertainty variance).

### Environment Specification
- [ ] Hardware: (e.g., 1x A100 80GB PCIe, 32 vCPU, 128GB RAM)
- [ ] Software: (e.g., Ubuntu 22.04, Python 3.11, Ray 2.9.0, vLLM 0.3.2)
- [ ] Dependency Hash: (SHA-256 of the `uv.lock` file)

### Dataset & State
- [ ] Dataset: (Path, UUID, or URL to the exact input data)
- [ ] Random Seed: (Global RNG seed injected for determinism)

### Expected Outcomes
- [ ] Expected Value: 
- [ ] Tolerance (+/- %): 

### Pass Criteria
- [ ] What defines a successful validation of the architectural assumption?
```
