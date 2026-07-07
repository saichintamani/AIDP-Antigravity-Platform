# Engineering Decision Record: Vector Database Selection

## Status
Accepted

## Date
2026-07-05

## Context
AIDP requires a highly scalable, extremely low-latency vector database to handle the semantic retrieval of hundreds of millions of chunks of scientific text, mathematical formulas, and embedding representations of graph structures. This database must support strict metadata filtering (e.g., searching within specific timeframes or domains) without catastrophic degradation of Approximate Nearest Neighbor (ANN) search speeds.
Reference: `REQ-VS-001`, `REQ-VS-005`

## Options Considered
*   **Milvus:** Highly distributed, enterprise-scale vector database.
*   **Pinecone:** Fully managed, closed-source SaaS vector database.
*   **Qdrant:** Rust-based, highly optimized vector database with custom payload indexing.
*   **pgvector:** PostgreSQL extension for vector similarity search.

## Trade-offs & Analysis
*   **pgvector:** Excellent for small-scale applications already using Postgres. However, HNSW index build times and memory overhead at 100M+ vectors become prohibitive. It lacks the distributed, high-concurrency throughput required by an autonomous agent ecosystem.
*   **Pinecone:** Exceptional ease of use. However, as a closed-source SaaS, it violates our requirement for deployment flexibility (if we need to deploy AIDP into an air-gapped AWS GovCloud for defense/healthcare clients in the future). Data gravity costs on AWS egress would also be significant.
*   **Milvus:** Built for the multi-billion vector scale. However, the architectural footprint is massive (requires Etcd, MinIO, Pulsar, and proxy nodes). The operational overhead for the current phase of AIDP is unjustified when a simpler binary can achieve similar throughput.
*   **Qdrant:** Written in Rust, offering near C++ performance with memory safety. Its defining feature is the *Payload Index*—unlike traditional vector databases that filter *after* ANN (leading to low recall) or *before* ANN (leading to slow queries), Qdrant utilizes a custom filtered-HNSW algorithm that maintains $O(\log N)$ search complexity even under heavy metadata constraints. It natively supports Product/Scalar Quantization to reduce memory footprint.

## Decision
We select **Qdrant** as the primary vector search engine for the AIDP Knowledge Substrate.

## Justification
Qdrant provides the optimal intersection of extreme performance (Rust), deployment simplicity (single binary or Kubernetes operator), and the exact filtering capabilities AIDP requires. The ability to push vector quantization to disk via mmap ensures our memory complexity does not explode ($O(N)$ RAM constraint mitigated), directly satisfying the findings in `005_COMPLEXITY_ANALYSIS.md`.

## Consequences
### Positive
*   Minimal operational overhead compared to Milvus.
*   Maintains sub-20ms latency on highly filtered scientific queries.
*   Can run fully air-gapped within our VPC.

### Negative (Risks)
*   The Rust ecosystem is younger than Java/C++ ecosystems; debugging core engine issues may require specialized Rust expertise if we encounter edge-case segfaults (unlikely due to Rust's safety, but possible in FFI layers).

## Traceability
*   **SRS Requirements Satisfied:** `REQ-VS-001`, `REQ-VS-004`, `REQ-VS-005`
*   **Architecture Documents Updated:** `002_HIGH_LEVEL_SYSTEM_ARCHITECTURE.md`
