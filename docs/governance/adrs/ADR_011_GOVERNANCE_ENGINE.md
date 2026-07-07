# ADR-011: Scientific Governance Engine (The Constitution of Science)

## Status
Proposed

## Context
AIDP has evolved into a massively capable autonomous laboratory (v1.0). While we have enacted an architectural feature freeze to focus on empirical validation, there is one critical gap in trust: we have no centralized "constitutional" layer that acts as an unbypassable gatekeeper for scientific claims. 

Before we run live benchmarks against ground truth, we need an absolute guarantee that no hallucinated, unsafe, or unprovenanced claim can enter the final publication.

## Decision
We will build the **Scientific Governance Engine** as the final architectural component of v1.0.

This engine sits as a constitutional wrapper around the `Predictive Scientific Reasoning Engine (PSRE)`. Every generated hypothesis or final decision MUST pass through a strict, sequential gauntlet:
1. **Evidence Check**: Does every claim map to a valid citation in the `WorldModel`?
2. **Conflict Check**: Does this violate any known physical or biological laws already established?
3. **Provenance Check**: Is the chain of custody for this idea unbroken back to the root query?
4. **Reproducibility Check**: Is the experimental design fully specified (e.g., cell lines, dosages, power)?
5. **Safety Check**: Does this violate biosafety/dual-use regulations?
6. **Confidence Calibration**: Is the subjective logic belief score > 0.85?
7. **Publication Approval**: Final sign-off.

If any check fails, the claim is rejected and kicked back to the Revisor, regardless of how well it performed in the PSRE debate.

## Consequences
- **Positive**: Makes AIDP incredibly trustworthy. Establishes a "Constitution of Science" that ensures the system cannot hallucinate an unsafe or unfounded discovery into the final output.
- **Negative**: Adds a final layer of latency and strictness that may reject otherwise highly novel but poorly cited ideas.
