---
Document ID: AIDP-SPEC-009
Title: MATHEMATICAL ENGINE
Version: 1.0
Status: Approved
---
# Detailed Architecture: Mathematical Engine

## Introduction
The Mathematical Engine is the intellectual core of the Artificial Intelligence Discovery Platform (AIDP). While the Agent Core performs semantic reasoning (LLM heuristics) and the Knowledge Substrate stores data, the Mathematical Engine provides absolute, statistical, and causal ground truth. It prevents the system from drowning in spurious correlations by enforcing formal mathematical rigor.

---

## 1. Architecture Quality & Modularity
**Design Pattern: The Math Services Bus**
Agents are expressly forbidden from executing heavy mathematical logic locally. 
*   **Decoupling via gRPC:** The Mathematical Engine exposes a suite of gRPC endpoints (e.g., `CalculateEigenvectorCentrality`, `RunDoCalculus`).
*   **Asynchronous Batching:** Unlike the synchronous Fusion Gateway, the Math Engine is highly asynchronous. When an Agent requests a global Graph Laplacian, the Math Engine returns a `JobID` and queues the operation via Ray.
*   **Cross-Cluster Memory Streaming:** Because Ray's Plasma Object Store is intra-cluster, passing terabytes of matrix data from the Knowledge Substrate cluster to the Math Engine cluster would normally create a severe serialization bottleneck. To bypass this, the Math Engine nodes are equipped with **AWS EFA (Elastic Fabric Adapters)**, enabling kernel-bypass RDMA (Remote Direct Memory Access) across clusters at 400 Gbps.

---

## 2. Mathematical Correctness
The Engine implements three primary pillars of mathematical analysis:
1.  **Spectral Graph Theory:** Uses the Lanczos algorithm on sparse Graph Laplacian matrices to identify hidden ontological clusters within the Knowledge Substrate (e.g., finding a structural bridge between a physics paper and a biology paper that do not share semantic keywords).
2.  **Bayesian Epistemology:** Implements Markov Chain Monte Carlo (MCMC) to update the confidence/belief scores of existing graph edges when new, contradictory evidence is ingested.
3.  **Causal Inference (Pearl's Do-Calculus):** Distinguishes correlation from causation. Because Do-Calculus mathematically requires a Directed Acyclic Graph (DAG) and knowledge graphs are highly cyclic, the Engine implements a mandatory **DAGification** preprocessing phase (removing back-edges via topological heuristics) before any Structural Causal Model (SCM) is evaluated.

---

## 3. AWS Physical Layout & Cloud Review
**Memory-Optimized Compute, Not GPUs**
*   **Compute Profile:** Sparse matrix operations (like Spectral Clustering on a 10-million node graph) require massive RAM, not necessarily massive parallel FLOPs. 
*   **Instance Types:** The Engine utilizes AWS `r7a` (up to 768 GiB RAM) or `x2gd` (up to 1,024 GiB RAM) instances. 
*   **Topology Spread Constraints:** To eliminate catastrophic AWS intra-AZ data transfer fees ($0.01/GB), strict Kubernetes scheduling constraints force Math Engine pods to deploy in the exact same Availability Zone (AZ) as the primary Neptune writer instance.
*   **Isolation:** These node pools are strictly isolated from the GPU inference pools (`p4d`) used by the LLMs to prevent resource contention.

---

## 4. MLOps & Lineage
*   **Mathematical Provenance:** If the Engine discovers a new structural cluster and promotes it to a formal "Scientific Field" node in Neptune, the exact provenance must be tracked.
*   **Immutable Logs:** The random seed, the specific MCMC chain length, the input matrix hashes, and the **exact Docker image SHA-256 digest** of the C++ execution environment are serialized into a JSON artifact and stored immutably in Amazon S3. The new Neptune node contains an `mlops_provenance_uri` pointing to this S3 object.

---

## 5. Security & Trust Boundaries
*   **Zero Internet Egress:** The Mathematical Engine has absolutely no requirement to access the public internet. Its AWS Security Group explicitly denies `0.0.0.0/0` outbound traffic.
*   **VPC Gateway Endpoints:** To allow the Math Engine to fetch models and write provenance logs to S3 without internet egress, a private AWS VPC Gateway Endpoint for S3 is explicitly provisioned.
*   **Zero-Trust Identity:** It strictly validates the SPIFFE ID of the calling service (e.g., the Agent Core or a scheduled Cron job) before accepting a computation payload.

---

## 6. Observability
*   **SLOs (Service Level Objectives):**
    *   **Real-time Inference (e.g., Do-Calculus on 3 nodes):** p99 < 500ms.
    *   **Nightly Batch (e.g., Global Spectral Clustering):** Must complete in < 6 hours.
*   **Persistent Telemetry:** Because the Ray Dashboard is ephemeral and lost on cluster shutdown, the Engine deploys the Ray Prometheus Exporter, hard-configured to remote-write all metrics to **Amazon Managed Prometheus (AMP)** for permanent retention.
*   **Metrics:** Prometheus scrapes specific mathematical health metrics, such as sparse matrix density and eigenvalue convergence rates. If the matrix becomes too dense (indicating an ontology failure), an alert is triggered.

---

## 7. Cost Engineering
*   **Spot Instance Maximization:** Nightly global graph clustering is delay-tolerant. The Ray clusters executing these algorithms are backed 100% by AWS Spot Instances.
*   **Cost Savings:** An `r7a.48xlarge` On-Demand costs ~$10.60/hr. On the Spot market, it averages ~$3.00/hr (a 70% reduction). 
*   **Fault Tolerance via Checkpointing:** If AWS reclaims the Spot node, Ray's object store (Plasma) and task idempotency ensure the computation resumes on a new node. However, to prevent a 6-hour job from restarting from scratch at hour 5, the Engine mandates **Ray Checkpointing** to S3, saving intermediate eigenvector states every 15 minutes.

---

## 8. AI Evaluation Checkpoints
The Math Engine evaluates its own statistical validity before returning results:
*   **MCMC Convergence & ESS:** For Bayesian updates, the engine calculates the **Gelman-Rubin statistic ($\hat{R}$)** across multiple MCMC chains. If $\hat{R} > 1.05$, the chains have failed to converge. Additionally, if the **Effective Sample Size (ESS)** falls below 10%, the inference is flagged as suffering from mode collapse and is statistically rejected.
*   **Graph Connectivity:** Before running Spectral Clustering, it verifies the graph is fully connected. Disconnected subgraphs are dynamically partitioned and clustered independently to avoid mathematically invalid zero-eigenvalues.
