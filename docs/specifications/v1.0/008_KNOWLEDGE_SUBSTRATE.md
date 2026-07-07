---
Document ID: AIDP-SPEC-008
Title: KNOWLEDGE SUBSTRATE
Version: 1.0
Status: Approved
---
# Detailed Architecture: Knowledge Substrate

## Introduction
The Knowledge Substrate is the foundational data layer of the Artificial Intelligence Discovery Platform (AIDP). It strictly segregates semantic context (dense vectors) from logical relations (discrete graphs), yet fuses them mathematically at the query API boundary. This document governs the design of this substrate, explicitly evaluated across the 8 rigorous dimensions established in `007A`.

---

## 1. Architecture Quality & Modularity
**Design Pattern: The Fusion Gateway**
Agents do not communicate directly with databases (e.g., Qdrant or Neptune). Doing so would create severe vendor lock-in and tight coupling.
*   **Abstraction Layer:** All data reads/writes pass through a gRPC-based `Fusion Gateway`. To handle the extreme concurrency of scattering requests to Qdrant and Neptune simultaneously without GIL bottlenecks, this Gateway is implemented in **async Rust**. 
*   **Decoupling:** If we migrate from Neptune to Neo4j, the Agents remain entirely unaware. The Gateway implements a strict Protobuf contract (e.g., `GetSubgraphRequest(UUID)`).
*   **Ingestion Bottleneck Avoidance:** Analyzing monolithic pipelines like LlamaIndex, we observed severe throughput issues when ingestion and retrieval share compute. AIDP strictly separates Write Paths (Ingestion ECS Tasks) from Read Paths (Agent Query EKS Pods).

---

## 2. Mathematical Correctness
**Hybrid Graph-Vector Search & Traversal Limits**
*   **Filtering First (Qdrant Insight):** Instead of vector similarity search followed by post-filtering (which ruins recall), we adopt Qdrant's payload filtering. Vector search is mathematically restricted *only* to nodes satisfying boolean criteria.
*   **UUID Intersection Bounds:** To prevent crashing Neptune's query parser, the Fusion Gateway enforces a strict `top_k <= 500` limit on the number of UUIDs extracted from Qdrant before passing them to Neptune (`g.V(uuids)`). Intersections larger than this must be processed via asynchronous Ray batch jobs.
*   **Traversal Explosion ($O(d^k)$):** Taking principles from Apache TinkerPop, the Fusion Gateway hardcodes traversal depth limits. Unbounded BFS is mathematically forbidden. Traversals must provide a `limit(N)` or a max timeout (e.g., 200ms) to ensure query execution does not exhaust cluster memory.

---

## 3. AWS Physical Layout & Cloud Review
**Neptune vs. Self-Hosted Neo4j**
*   **Decision:** Amazon Neptune (Serverless).
*   **Justification:** While Neo4j offers richer developer ergonomics, managing a distributed, highly-available graph cluster on EKS introduces massive operational burden. Neptune offloads this entirely.
*   **Auto-scaling Constraint:** To prevent bursty queries from spiking Neptune to 128 NCUs ($17.66/hr), strict `neptune_query_timeout` parameters are enforced at the AWS cluster parameter group level, violently killing runaway queries before they trigger expensive scaling events.
**Qdrant on EKS vs. SaaS (Pinecone/Weaviate Cloud)**
*   **Decision:** Self-Hosted Qdrant on EKS.
*   **Justification:** Pushing 1+ Billion vectors (terabytes of data) across the internet to a SaaS provider incurs catastrophic AWS NAT Gateway / Egress costs. Qdrant running inside our VPC on memory-mapped EBS volumes eliminates data gravity penalties.

---

## 4. MLOps & Lineage
*   **The Lineage Invariant:** An embedding vector is useless without knowing *how* it was generated.
*   Every node written to the Knowledge Substrate must contain metadata linking to:
    1.  The MLflow Run ID of the embedding model.
    2.  The Git commit hash of the ingestion parser code.
    3.  The Delta Lake version of the original raw document.
*   **Graph Schema Lineage:** Neptune is schemaless, which risks ontology rot. AIDP mandates an explicit **Graph Ontology Registry** (using SHACL). All edge types must be versioned and validated against this registry before insertion.
*   **Rollback:** If an embedding model is found to be defective, the Fusion Gateway can instantly deprecate all vectors matching that MLflow Run ID, forcing a re-ingestion.

---

## 5. Security & Trust Boundaries
*   **SPIFFE Identity:** The Fusion Gateway does not blindly trust requests. It cryptographically verifies the SPIFFE ID of the calling Agent.
*   **Query Compilation (No Raw Gremlin):** To prevent malicious or compromised Agents from executing destructive queries (e.g., `g.V().drop()`), Agents are banned from submitting raw Gremlin strings. They submit parameterized gRPC requests, which the Rust Gateway compiles into safe, read-only graph traversals.
*   **Tenant Isolation:** If AIDP serves multiple research domains (e.g., Oncology vs. Materials Science), data is isolated logically via Qdrant Collections and Neptune Tenant IDs. An Oncology Agent's JWT token lacks the scopes to traverse Materials Science nodes.
*   **Encryption:** All volumes backing Qdrant and Neptune are encrypted at rest with AWS KMS Customer Managed Keys (CMK).

---

## 6. Observability
*   **SLOs (Service Level Objectives):**
    *   **Vector Search Latency:** 99th percentile (p99) < 40ms.
    *   **Graph Traversal (2-hop):** 99th percentile (p99) < 150ms.
    *   **Ingestion Throughput:** Minimum 10,000 documents processed per hour.
*   **Error Budgets:** A 0.1% failure rate for insertions. If exceeded, alerting triggers an immediate PagerDuty incident for the Data Platform team, and deployments are locked.
*   **Distributed Span Linking:** Because a single Agent query scatters across Qdrant and Neptune, standard Trace-IDs are insufficient. The Fusion Gateway explicitly implements OpenTelemetry **Span Linking** to correlate the parallel database operations for debugging latency spikes.

---

## 7. Cost Engineering
AIDP must maintain strict financial efficiency at the multi-terabyte scale.
*   **Baseline AWS Cost Estimation:**
    *   **Amazon Neptune Serverless:** Scales from 2.5 NCUs ($0.34/hr) to 128 NCUs ($17.66/hr) based on demand. Estimated monthly cost: ~$1,200.
    *   **Qdrant EC2 (i4i.4xlarge x 3):** ~$2,400/month. 
*   **Cost Optimization Strategy:** 
    *   **Hardware Shift:** Standard `gp3` EBS volumes (3000 IOPS) will throttle under Qdrant mmap loads. By switching to `i4i` instances with local NVMe storage, we pay slightly more for EC2 but completely avoid unpredictable EBS IOPS charges and latency penalties.
    *   **Quantization:** Qdrant's Scalar Quantization (INT8) compresses the vector footprint by 4x. This single architectural decision reduces the required RAM by 75%, allowing us to fit 1 Billion vectors on the `i4i` NVMe drives economically.

---

## 8. AI Evaluation Checkpoints
Before an Agent's generated hypothesis is committed to the Substrate as an immutable graph edge, it must pass the AI Evaluation Gateway.
*   **Hallucination Check:** The generated $(u, v)$ relationship is cross-referenced against the raw text vectors. The Cosine Similarity threshold is **not hardcoded**; it is dynamically calibrated by the Mathematical Engine based on the specific domain's latent space density (e.g., biological interactions require a higher confidence threshold than abstract physics hypotheses).
*   **Citation Validation:** The payload must contain valid UUIDs for existing literature. Dead links result in an immediate `RESOURCE_EXHAUSTED` rejection (triggering a backoff).
