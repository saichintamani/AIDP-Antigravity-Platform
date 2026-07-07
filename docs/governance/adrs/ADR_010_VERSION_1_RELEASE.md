# ADR-010: Version 1.0 - Scientific Validation Release & Feature Freeze

## Status
Proposed

## Context
AIDP has completed Phases A through E, establishing a massive cognitive and operational architecture (Provenance, PSRE, ResearchOps, Meta-Learning). To transition the project from an experimental architecture to a credible scientific tool, we must prioritize validation over adding new features. The next milestone must demonstrate—with measurable evidence—that AIDP performs useful autonomous scientific reasoning.

## Decision
We enact an immediate **Feature Freeze** on the core intelligence architecture. All future engineering effort will be directed toward the **Version 1.0 Scientific Validation Release**, containing 8 pillars:

1. **V1 - Scientific Evaluation Framework**: A comprehensive report card generator for every campaign (correctness, EIG, hallucination rate, cost, etc.).
2. **V2 - Gold-Standard Benchmarks**: Testing against historical breakthroughs (e.g., COVID-19, CRISPR) with future-data masking.
3. **V3 - Domain Demonstrations**: End-to-end runs in Oncology, Drug Discovery, and Climate Science.
4. **V4 - Explainability Dashboard**: A UI tracing Evidence -> Confidence -> Debate -> Rejected Hypotheses -> Decision.
5. **V5 - Scientific Whitepaper**: A technical paper detailing architecture and results.
6. **V6 - Public Benchmark**: Releasing "DiscoveryBench" to the public.
7. **V7 - Open Source Readiness**: Polish documentation, API specs, and contribution guidelines.
8. **V8 - Production Demonstration**: A single, flawless end-to-end presentation of the platform solving a complex user query.

## Consequences
- **Positive**: Forces the project to prove its claims. Provides the necessary evidence for stakeholders, academics, and employers that the architecture translates into real-world scientific utility.
- **Negative**: No new intelligent components (e.g., new types of agents or memory structures) will be added until Version 1.0 is shipped, which may limit scope if a fundamental flaw is discovered during validation. However, the freeze ensures focus.
