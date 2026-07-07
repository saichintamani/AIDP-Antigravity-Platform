---
Document ID: AIDP-SPEC-015
Title: Engineering Decision Framework
Version: 1.0
Status: Approved
---

# Detailed Architecture: Engineering Decision Framework

## Introduction
Architecture is not the survey of GitHub repositories; it is the formal process of making irreversible engineering decisions. The AIDP Engineering Decision Framework replaces subjective framework preferences with a reproducible, 15-point evaluation rubric. This specification captures the foundational commitments that bridge the Computational Algorithms (`014`) to physical execution.

---

## 1. The 15-Point Evaluation Rubric
Every technology adopted by AIDP must be evaluated against:
1.  **Technology:** Name and ecosystem.
2.  **Problem it solves:** The exact pain point addressed.
3.  **Architecture:** Underlying design paradigm.
4.  **Complexity:** Operational and cognitive load.
5.  **Scalability:** Multi-node limits.
6.  **Hardware utilization:** EFA/NVLink/SRAM awareness.
7.  **Cloud compatibility:** AWS native vs agnostic.
8.  **Failure modes:** What happens when it crashes?
9.  **Security implications:** Isolation and zero-trust bounds.
10. **Licensing:** Apache 2.0 / MIT vs restrictive.
11. **Community maturity:** Maintainer health and momentum.
12. **Maintenance burden:** Upgrade paths and API stability.
13. **Benchmark evidence:** Empirical latency/throughput.
14. **Alternatives:** Competitors considered.
15. **Decision:** The formal outcome and future re-evaluation criteria.

---

## 2. Core Technologies (Foundational)

### 2.1 Distributed Orchestration
*   **Technology:** KubeRay (Ray on Kubernetes).
*   **Problem:** MCTS and VMP require stateful, sub-millisecond RPC between thousands of ephemeral agents.
*   **Architecture:** Hierarchical Actor model on a decentralized object store, managed via Kubernetes CRDs.
*   **Failure Modes:** Ray head-node SPOF (Single Point of Failure); requires High Availability (HA) configuration.
*   **Security:** Multi-tenant namespace isolation via Kubernetes taints/tolerations.
*   **Alternatives:** Raw Kubernetes Pods (lacks RPC performance), Apache Spark (lacks Actor state).
*   **Decision:** **Adopt.** *See ADR-0001.*

### 2.2 Deep Learning Primitives
*   **Technology:** PyTorch (with FSDP & SDPA).
*   **Problem:** Building custom, dual-process (Autoregressive LLM + Distilled MLPs) computational graphs.
*   **Scalability:** FSDP scales to massive clusters; FlashAttention (SDPA) mitigates $O(N^2)$ memory limits.
*   **Hardware:** Native EFA and NVLink utilization via NCCL.
*   **Alternatives:** JAX (steep learning curve for dynamic control flow), DeepSpeed (intrusive API).
*   **Decision:** **Adopt.**

---

## 3. Candidate Technologies (Replaceable)

### 3.1 Inference Engine
*   **Technology:** vLLM.
*   **Problem:** Standard LLM inference suffers from KV-cache fragmentation, destroying MCTS dynamic batching throughput.
*   **Architecture:** PagedAttention (KV-cache virtualization).
*   **Failure Modes:** Aggressive VRAM pre-allocation causes OS-level OOMs if co-located with PyG.
*   **Decision:** **Adopt, strictly isolated to $p5 node pools.** 
*   **Future Re-evaluation:** Re-assess TensorRT-LLM if Nvidia's AOT compilation pipeline becomes less brittle.

### 3.2 Architectural Pattern: Durable Execution
*   **Technology:** Temporal.io
*   **Problem:** The 7-step Cognitive Pipeline (`012`) must survive node preemptions (AWS Spot Instances) without losing the Evidence DAG.
*   **Architecture:** Event sourcing via append-only execution histories.
*   **Decision:** **Adopt.** Integrating Temporal with KubeRay guarantees that if a Spot Instance terminates during a 4-hour mathematical proof, the Agent instantly resumes on a new node precisely where it left off.

---

## 4. Rejected Technologies (Institutional Memory)

### 4.1 Loopy Belief Propagation (LBP)
*   **Reason Rejected:** Mathematically incapable of guaranteeing convergence on dense cyclic biological graphs.
*   **Reconsideration Criteria:** If the underlying topology is proven to be strictly a Directed Acyclic Graph (DAG), LBP may be reconsidered for speed. *See ADR-0002.*

### 4.2 Apache Arrow (for In-Memory Active Objects)
*   **Reason Rejected:** Immutable OLAP structures incur massive serialization overhead for dynamic MCTS hypothesis trees. 
*   **Reconsideration Criteria:** None. Active memory must remain zero-copy (Cap'n Proto). Arrow remains strictly for vector databases. *See ADR-0003.*

---

## 5. Decision Register
*   **KubeRay:** Adopted as Core.
*   **PyTorch (FSDP + SDPA):** Adopted as Core.
*   **vLLM:** Adopted as Candidate.
*   **Temporal:** Adopted as Core (Durable Execution Pattern).
*   **DeepSpeed & JAX:** Rejected (for this specific dual-process architecture).
