---
Document ID: AIDP-SPEC-007
Title: EXECUTION ORCHESTRATION CORE
Version: 1.0
Status: Approved
---
# Detailed Architecture: Execution & Orchestration Core

## Introduction
The Execution & Orchestration Core is the foundational infrastructure layer of the Artificial Intelligence Discovery Platform (AIDP). Operating at the lowest level of our dependency stack, this subsystem is responsible for scheduling compute, managing distributed state, handling hardware affinity, and providing a unified API for higher-level domains (such as the Cognitive Agents and the Knowledge Substrate). 

As justified in `EDR-002`, this architecture relies on a synergy between **Kubernetes (Amazon EKS)** for physical infrastructure orchestration and **Ray** for distributed application execution.

---

## 1. Physical Layer: Hybrid Compute Topology
AIDP explicitly rejects a monolithic infrastructure paradigm. We distinguish strictly between Heavy Compute (requiring Zero-Copy memory and GPUs) and Light Compute (stateless, ephemeral).

### 1.1 Light Compute: Serverless (AWS ECS Fargate & Lambda)
*   **Use Case:** Stateless ingestion cron jobs (e.g., polling arXiv daily), API Gateway routing, and simple data validation.
*   **Justification:** Spinning up Ray workers and locking EKS nodes for a 5-second API call is a severe waste of resources. ECS Fargate provides scale-to-zero, event-driven compute at a fraction of the cost without the overhead of Ray's Global Control Store.

### 1.2 Heavy Compute: Kubernetes (Amazon EKS)
For stateful, ML-heavy workloads, EKS is mandatory. We define strict node pools managed by Karpenter:
*   **Control Plane Node Pool:** Small, high-availability `m6i` instances. Runs the Ray Head Node and Istio ingress.
*   **Memory-Optimized Pool:** `r7g` instances. Targeted for heavy Graph Laplacian approximations.
*   **GPU Inference Pool (EFA Enabled):** `p4d` instances. Dedicated exclusively to vLLM pods. Must be launched in an Elastic Fabric Adapter (EFA) placement group to bypass standard VPC networking limits, enabling 400 Gbps cross-node throughput.
*   **Spot Instance Pool:** Non-critical background tasks are routed here for an 80% cost reduction.

### 1.3 Service Mesh & Identity (Istio + SPIRE)
All intra-cluster communication routes through Istio Envoy sidecars.
*   **Identity Propagation:** We rely on **SPIFFE/SPIRE** for cryptographic identity issuance. Short-lived JWTs are injected into gRPC headers. When the Agent Core queries the Knowledge Substrate, the substrate mathematically verifies the Agent's SPIFFE ID rather than merely trusting the mTLS pipe.
*   **Rate Limiting:** Circuit breakers prevent a runaway AI Agent from DDOS'ing the Vector Database.
*   **gRPC Load Balancing:** Critical for routing traffic to long-running Ray actors.

---

## 2. Distributed Execution Layer: Ray

### 2.1 The Ray Cluster Architecture (KubeRay)
We utilize the `KubeRay` operator to manage Ray clusters natively within EKS.
*   **Ray Head Node:** Manages the Global Control Store (GCS). It maintains the global metadata of which worker nodes are alive and where specific Python objects reside in memory.
*   **Ray Worker Nodes:** Execute the actual logic. These are spawned dynamically by KubeRay based on queue depth.

### 2.2 Global Object Store (Plasma)
*   **Mechanism:** Ray uses an Apache Arrow-based shared-memory object store. 
*   **Mathematical Justification:** When an Agent generates a massive 10GB tensor of hypotheses, passing this to the Evaluator Agent via gRPC/network serialization would incur an $O(S)$ serialization penalty (where $S$ is size). With Plasma, the Evaluator Agent receives a pointer and reads the tensor from shared memory (Zero-Copy), reducing transfer latency to $O(1)$.

### 2.3 Abstraction Layer (AgentRuntime Interface)
To prevent the platform business logic from being tightly coupled to Ray's specific APIs (as critiqued in `007A`), all agent logic must inherit from an `AgentRuntime` interface. This allows us to transparently swap the backend executor (e.g., from Ray to a local thread pool for testing) without rewriting the agent's core Markov transitions.

### 2.4 Stateful Actors vs. Stateless Tasks
AIDP enforces a strict dichotomy in execution patterns:
*   **Stateless Tasks (`@ray.remote`):** Used for pure mathematical functions. E.g., computing a Cosine similarity matrix. They are idempotent and can be retried infinitely upon node failure.
*   **Stateful Actors (`@ray.remote(num_cpus=1)`):** Used for Research Agents. An Agent maintains a continuous context window (state). If an Actor node crashes, Ray automatically restarts the Actor on a healthy node, and the Actor restores its context from the Ephemeral State store (Redis) as mandated by the `006_PLATFORM_META_ARCHITECTURE.md` lifecycle.

---

## 3. Subsystem Integration Contracts

### 3.1 Gating Code Execution (Sandboxing)
*   **The Firecracker Boundary:** If a Ray Actor (Agent) decides it needs to execute a generated Python script to analyze a dataset, it CANNOT execute it locally via `eval()`. 
*   **Execution Flow:** 
    1. The Actor serializes the code.
    2. Sends a gRPC request to the `Sandbox Orchestrator`.
    3. The Sandbox Orchestrator boots a Firecracker microVM (`REQ-SEC-005`), injects the code, runs it in complete isolation (no network access), and returns the `stdout`/`stderr`.
    4. The microVM is immediately destroyed.

### 3.2 Context Propagation (Observability)
Distributed tracing in asynchronous Python (especially across Ray workers) is notoriously difficult because standard thread-local context variables are lost during serialization.
*   **Implementation:** AIDP implements a custom Ray middleware interceptor. When a task is submitted, the current OpenTelemetry `Trace-ID` and `Span-ID` are explicitly injected into the Ray task arguments. The receiving worker extracts these IDs and continues the span. This ensures that a single trace completely covers the journey from User Prompt -> Ray Agent -> Firecracker Sandbox -> Graph Database.

---

## 4. Failure Modes & Recovery

*   **Head Node Crash:** If the Ray Head Node crashes, KubeRay restarts it. However, in-flight task metadata is lost. To mitigate this, High Availability (HA) is enabled, backing the GCS to a persistent external Redis cluster.
*   **OOM (Out of Memory):** Ray workers aggressively spill the Plasma object store to local NVMe SSDs before crashing. If the SSD fills, the task fails and is routed to the Dead Letter Queue (DLQ).
*   **Poison Pill Tasks:** If a specific mathematical computation causes a segfault (e.g., a C++ extension failure), Ray will retry it. If it fails 3 times, the orchestration core flags the input as a "Poison Pill" to prevent infinite crash loops.

---

## 5. Cost Engineering & Hardware Profiles
AIDP treats cost as a primary architectural constraint.

### 5.1 Monthly Cost Estimation Baseline
To run the core orchestration plane at minimal production scale:
*   **EKS Control Plane:** ~$73/month.
*   **Ray Head Nodes (m6i.xlarge x2):** ~$280/month.
*   **Ingestion (ECS Fargate / Lambda):** Scale-to-zero. Estimated < $100/month for millions of invocations.
*   **GPU Inference (p4d.24xlarge):** ~$32.77/hour. This is the primary cost driver. 

### 5.2 Optimization Strategies
1.  **Scale-to-Zero GPU:** Karpenter is configured to aggressively terminate GPU nodes if the Ray queue is empty for > 5 minutes.
2.  **Spot Market Priority:** 80% of embedding generation (which is delay-tolerant) is forced onto Spot instances. If AWS reclaims the instance, Ray's idempotency ensures the task simply resumes later.
3.  **Network Egress Avoidance:** Because Ray Plasma keeps data in memory across nodes in the same Availability Zone (AZ), we avoid massive cross-AZ data transfer fees which would otherwise cripple a distributed ML workload.

---

## 5. Traceability
*   **SRS Requirements Satisfied:** `REQ-ML-002`, `REQ-CM-002`, `REQ-RA-004`, `REQ-SEC-005`
*   **Meta-Architecture Invariants Maintained:** OTel Trace Propagation, Strict IPC (gRPC), Ephemeral State recovery.
