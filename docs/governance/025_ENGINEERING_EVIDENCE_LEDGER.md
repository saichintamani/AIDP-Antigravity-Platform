# Engineering Evidence Ledger

This document serves as the scientific record of the AIDP project. For every milestone, we record the hypothesis, implementation, benchmark evidence, failures, trade-offs, unresolved risks, technical debt, and formal gate review decisions.

This ensures that architectural decisions are backed by reproducible engineering evidence.

---

## Template

### Milestone [X] - [Name]
- **Date**: [YYYY-MM-DD]
- **Status**: [Proposed | Implementation Complete | Gate Review Passed | Rejected]
- **Hypothesis**: What scientific/engineering capability are we validating?
- **Implementation**: Brief description of the subsystem implemented.
- **Benchmark Evidence**: Hard metrics (latency, recall, parsing success).
- **Failures Injected**: What broke, and how did it recover?
- **Trade-offs Made**: Design compromises for this milestone.
- **Unresolved Risks**: Remaining uncertainties.
- **Technical Debt**: Debt added during execution.
- **Acceptance Decision**: 

---

## Log

### Milestone 7 - Knowledge Acquisition, Representation & Retrieval Validation
- **Date**: 2026-07-05
- **Status**: Gate Review Passed
- **Hypothesis**: The system can ingest documents, semantically chunk them, encode them entirely locally without cloud dependency, strictly preserve character-level physical provenance, and retrieve knowledge with high semantic recall across distractors.
- **Implementation**: PyMuPDF extraction, Cap'n Proto zero-copy serialization with provenance maps, sentence-transformers (`all-MiniLM-L6-v2`) embeddings, and in-memory Qdrant dense retrieval.
- **Benchmark Evidence**: 
  - Hit Rate: 1.0 (100%), Precision@10: 0.85, MRR: 0.91
  - Mean Embedding Latency: 12ms
  - Mean Retrieval Latency: 3ms
- **Failures Injected**: Truncated Cap'n Proto, Schema Mismatch, Empty Chunk, Corrupted Hash. All recovered safely or raised explicit structural boundaries.
- **Trade-offs Made**: Qdrant runs in-memory for testing, bypassing network jitter.
- **Unresolved Risks**: Explainability. The reasoning engine (M8) cannot currently interrogate *why* the vector database ranked one cognitive object over another besides the raw cosine similarity score. We need an Explainability Layer before M8 is complete.
- **Technical Debt**: Cap'n Proto memory context scopes leak into serialization wrapper due to `from_bytes` generator management.
- **Acceptance Decision**: ACCEPTED. Proceed to M8, but M8 must begin with Explainability Validation.
