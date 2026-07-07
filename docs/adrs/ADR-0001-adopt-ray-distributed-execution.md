# ADR 0001: Adopt Ray for Distributed Execution

## Context
AIDP requires a zero-trust, ephemeral execution environment that can dynamically scale Python workloads, manage stateful agents, and orchestrate ML inference across massive multi-node clusters.

## Decision
We will adopt **Ray** (and specifically **KubeRay**) as the foundational distributed execution framework for the platform.

## Status
Approved

## Consequences
*   **Positive:** Ray provides native Actor abstractions perfectly mapped to our Cognitive Agents. It handles distributed object storage natively.
*   **Negative:** Ray introduces significant operational overhead compared to a single-node script. It requires strict node-pool isolation to prevent CUDA OOM issues (e.g., vLLM colliding with PyG).

## Alternatives Considered
*   **Kubernetes Native Pods (without Ray):** Rejected. Lacks the micro-second object store and stateful actor recovery required by our fast-loop agents.
*   **Apache Spark:** Rejected. Spark is optimized for bulk data processing (ETL), not real-time reinforcement learning and asynchronous actor execution.
