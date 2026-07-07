# Engineering Decision Record: Distributed Execution Framework

## Status
Accepted

## Date
2026-07-05

## Context
AIDP requires a framework to distribute intensive computational tasks across clusters of machines. These tasks include generating hypotheses via LLMs (which may require dynamic batching across GPUs), computing spectral approximations of billion-node graphs (CPU/RAM intensive), and managing stateful, long-running agent workflows. The framework must efficiently serialize Python objects and orchestrate tasks without excessive network bottlenecks.
Reference: `REQ-ML-002`, `REQ-CM-002`, `REQ-RA-004`

## Options Considered
*   **Celery:** Traditional Python task queue using message brokers (RabbitMQ/Redis).
*   **Dask:** Parallel computing library for Python, optimizing NumPy/Pandas workflows.
*   **Temporal:** Highly durable microservice orchestration platform.
*   **Ray:** Unified distributed compute framework with native GPU and ML support.

## Trade-offs & Analysis
*   **Celery:** Excellent for background web tasks. Fails catastrophically for ML workloads due to high serialization overhead (Pickle/JSON) and lack of native GPU or tensor-awareness. It cannot effectively handle stateful actors.
*   **Dask:** Fantastic for parallelizing dataframe operations (ETL). However, it is fundamentally a data-parallel framework, not a general-purpose actor framework. Orchestrating complex, stateful multi-agent communication over Dask is an anti-pattern.
*   **Temporal:** Provides "invincible" durability. If a cluster dies, Temporal resumes the exact line of code when it recovers. However, it requires a massive JVM-based control plane and is not optimized for high-throughput tensor manipulation or GPU scheduling.
*   **Ray:** Designed specifically for AI/ML workloads. Ray offers a global object store (Plasma) built on Apache Arrow, allowing zero-copy reads of massive tensors across processes on the same node. It provides `Ray Core` (for stateful actors—our research agents), `Ray Train` (for distributed fine-tuning), and `Ray Serve` (for model inference). It natively understands GPU placement and affinity.

## Decision
We select **Ray** as the primary distributed execution and orchestration framework for AIDP.

## Justification
Ray is the only framework that seamlessly bridges the gap between stateful agent logic and high-performance ML tensor execution. By leveraging Ray's zero-copy shared memory, we bypass the $O(S)$ network serialization penalties that would otherwise bottleneck our LLM inference and graph updates (as detailed in `005_COMPLEXITY_ANALYSIS.md`).

## Consequences
### Positive
*   Unified framework for both logical agents (Actors) and ML training (Tasks).
*   Native Kubernetes support via KubeRay operator.
*   Near-linear scaling for compute-bound tasks.

### Negative (Risks)
*   Ray's control plane (GCS - Global Control Service) can become a single point of failure if not configured with High Availability (HA) on EKS.
*   Complex learning curve for engineers accustomed to simple stateless HTTP microservices.

## Traceability
*   **SRS Requirements Satisfied:** `REQ-ML-002`, `REQ-CM-002`, `REQ-RA-004`
*   **Architecture Documents Updated:** `002_HIGH_LEVEL_SYSTEM_ARCHITECTURE.md`
