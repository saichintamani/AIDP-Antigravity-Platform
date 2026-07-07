# ADR-009: External Validation & Demonstration

## Status
Proposed

## Context
AIDP has accumulated a vast amount of infrastructure:
- Phase A: Scientific Knowledge Core
- Phase B: Scientific Intelligence Network
- Phase C: Autonomous Scientific Laboratory
- Phase D: Autonomous Research Platform
- Phase E: Self-Improving Scientific Intelligence

Adding more architectural features (such as Phase F: Digital Research Institute) yields diminishing returns at this stage. The project must now demonstrate its value. To distinguish AIDP from theoretical prototypes, we must rigorously quantify its performance, provide compelling case studies, and document the system academically.

## Decision
We will execute an **External Validation** phase, structured into four pillars:

### 1. Scientific Evaluation Suite
- **Component**: `src/aidp/evaluation/suite.py`
- **Objective**: Automate the quantification of discovery quality, evidence quality, calibration, reproducibility, and cost efficiency across multiple simulated campaigns.

### 2. End-to-End Case Studies
- **Component**: `scripts/case_studies/`
- **Objective**: We will run AIDP through full, unmocked campaigns in domains such as Oncology (e.g., discovering novel KRAS G12C inhibitors) and Materials Science (e.g., solid-state battery electrolytes). We will record the logs, debate graphs, and final hypotheses.

### 3. Academic Research Paper
- **Component**: `docs/paper/aidp_whitepaper.tex` (or Markdown)
- **Objective**: Draft a rigorous academic paper detailing the system's architecture, the concept of the Predictive Scientific Reasoning Engine (PSRE), and the results of the evaluation suite.

### 4. Public Benchmark Release
- **Component**: `data/benchmarks/`
- **Objective**: Package the Discovery Simulator data and evaluation scripts into a release that other autonomous scientific systems can use to compare themselves against AIDP.

## Consequences
- **Positive**: Transitions AIDP from a software engineering project to a validated, credible scientific tool. It provides the necessary evidence to stakeholders or the scientific community that the architecture works.
- **Negative**: Requires substantial time generating data for the case studies and meticulously analyzing the debate graphs for the paper.
