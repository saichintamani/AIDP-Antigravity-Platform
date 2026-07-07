# ADR-002: In-Memory Qdrant for Rapid Validation

**Date:** 2026-07-05
**Status:** Accepted with Trade-offs

## Context
Milestone 7 requires a dense vector storage engine to test retrieval quality, indexing latency, and provenance mapping. While production will require a distributed vector database, standing up a clustered vector DB (like Milvus or distributed Qdrant) via Docker Compose slows down rapid prototyping and CI execution.

## Decision
We chose to instantiate Qdrant in "in-memory" mode directly within the Python execution context for Milestone 7 testing and validation.

## Alternatives Considered
- **Dockerized Qdrant**: High operational overhead for unit tests; introduces network variability.
- **Faiss**: Extremely fast, but lacks complex payload filtering and the schema flexibility we need for Cognitive Objects.
- **ChromaDB**: Good for local use, but Qdrant scales better to production, meaning we can use the same API locally and remotely.

## Consequences
- **Positive**: Blazing fast CI execution; zero infrastructure dependencies.
- **Negative**: Performance benchmarks generated in M7 are highly optimistic. They do not account for network jitter, payload serialization over gRPC, or true disk I/O.
- **Negative**: State is lost between test runs. (Acceptable for M7).

## Validation Evidence
- **Benchmark Gate 5 (Performance)** demonstrated storage insertion in <50ms and retrieval in <100ms.

## Related Documents
- `src/aidp/knowledge/storage.py`
- `tests/benchmarks/test_gate_5_performance.py`
