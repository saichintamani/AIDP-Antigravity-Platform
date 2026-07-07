---
Document ID: AIDP-SPEC-010
Title: COGNITIVE AGENT CORE
Version: 1.0
Status: Approved
---
# Detailed Architecture: Cognitive Agent Core

## Introduction
The Cognitive Agent Core sits at the top of the AIDP dependency stack. This is the domain of large language models, autonomous exploration, and hypothesis generation. To prevent this layer from degrading into an uncontrollable, expensive wrapper around LLM APIs, AIDP strictly mandates self-hosted, open-weight models bounded by formal Markov logic and zero-trust orchestration.

---

## 1. Architecture Quality & Modularity
**Design Pattern: Stateful Ray Actors**
Agents are long-running state machines, not synchronous scripts.
*   **Implementation:** Every Agent is deployed as a `@ray.remote(num_cpus=1)` Actor. 
*   **Event Log Rehydration:** The internal "context window" and current exploration path are not held purely in Python memory. To avoid the massive network bottleneck of serializing a 128k token context window to Redis every step, Agents continuously push a highly compressed **Event Log** (a ledger of tool calls and results) to the Ephemeral State Store (Redis) defined in `006`. If the underlying EKS node crashes, Ray spins up the Agent on a healthy node, which immediately rebuilds its context by re-hydrating from the Event Log.

---

## 2. Mathematical Correctness
**Bounding the Markov Decision Process (MDP)**
Unconstrained LLM agents fall into infinite loops (e.g., endlessly querying the same database record).
*   **Formal Bounds:** The agent's exploration of the Knowledge Substrate is strictly modeled as an MDP. 
*   **Intrinsic Reward Function $R(s,a)$:** An MDP requires a reward. The agent calculates its expected reward by calling the Mathematical Engine (`009`) to compute the **Information Gain** (Kullback-Leibler divergence) achieved by a proposed hypothesis. The agent is mathematically compelled to maximize Information Gain.
*   **Discount Factor ($\gamma$):** The agent applies a temporal discount factor to expected Information Gain, penalizing long, wandering reasoning chains.
*   **Epsilon-Greedy Exploration:** The agent's action selection enforces an exploration rate ($\epsilon$) that decays over time, forcing the agent to eventually converge on a hypothesis rather than exploring forever.

---

## 3. AWS Physical Layout & Cloud Review
**Self-Hosted GPU Inference Tier**
Relying on external APIs (OpenAI/Anthropic) introduces unacceptable IP leakage risks for scientific discovery and subjects the platform to external rate limits.
*   **Inference Engine:** The Core utilizes `vLLM`, an ultra-fast, PagedAttention-enabled inference server.
*   **Hardware:** Deployed on Amazon EKS `p4d.24xlarge` (A100) or `p5.48xlarge` (H100) instances.
*   **KV-Cache Aware Routing:** Standard Kubernetes Layer 4 (TCP) load balancing destroys the LLM KV Cache by scattering multi-turn agent sessions across random GPU pods. AIDP deploys a custom **Prefix-Caching LLM Gateway** (using Ray Serve) that guarantees session stickiness, routing an Agent's subsequent turns directly to the specific GPU pod holding its KV Cache.
*   **Tensor Parallelism:** Cross-node model sharding is supported via Elastic Fabric Adapters (EFA) to serve massive multi-modal models with ultra-low latency.

---

## 4. MLOps & Lineage
*   **Prompt Lineage as Code:** The exact system instructions, few-shot prompt examples, and the specific SHA-256 hash of the LLM weights used for a session are tracked in MLflow.
*   **RAG Provenance:** Because agents dynamically pull context, static prompt lineage is insufficient. The exact JSON payload of chunks retrieved from Qdrant must be cryptographically hashed and appended to the MLflow run.
*   **Invalidation:** If an agent discovers a groundbreaking hypothesis, but the prompt lineage cannot be retrieved from MLflow, the hypothesis is mathematically voided. We must know *exactly* what cognitive parameters produced the insight.

---

## 5. Security & Trust Boundaries
*   **Zero-Trust Execution (Firecracker):** Inevitably, agents will generate Python scripts or SQL queries to analyze data they find. They are absolutely forbidden from executing this code locally within the Ray worker. All generated code is dispatched to the `Sandbox Orchestrator` (`007`), executing in network-isolated AWS Firecracker microVMs.
*   **Strict Egress Proxy:** GPU pods cannot access the internet directly, preventing exfiltration of IP. However, they can submit Tool Calls to an internal **Egress Gateway**, which strictly whitelists permitted scientific domains (e.g., `*.arxiv.org`, `eutils.ncbi.nlm.nih.gov`) allowing agents to fetch real-time papers without compromising the VPC.

---

## 6. Observability
*   **Inference SLIs (Service Level Indicators):**
    *   **Time To First Token (TTFT):** p99 < 200ms.
    *   **Inter-Token Latency (ITL):** p99 < 50ms.
*   **Agentic SLIs:** Hardware metrics do not prove cognitive progress. AIDP introduces two custom SLIs:
    *   **Time To Action (TTA):** The latency before an agent successfully invokes a valid tool call.
    *   **Tokens Per Action (TPA):** The compute cost burned to reach a decision state. High TPA indicates agent confusion and prompts an alert.
*   **Token Economics Tracking:** Every Ray Actor emits custom Prometheus metrics tracking `tokens_consumed` and `tokens_generated`, tagged by Agent ID and Research Domain, enabling exact cost-per-discovery calculations.

---

## 7. Cost Engineering
**Dynamic LLM Routing**
Running all agent cognition on `p5.48xlarge` ($98/hr) is financially ruinous.
*   **Heuristic Router:** To avoid the latency penalty of running a BERT-based semantic router, AIDP uses a lightweight depth-heuristic router.
*   **Tier 1 (Cheap):** Initial tool formulation and simple JSON formatting tasks are routed to an 8B parameter model (e.g., Llama-3-8B) running on cheap `g5` (L4 GPU) instances.
*   **Tier 2 (Expensive):** Deep reasoning, final hypothesis generation, and causal structuring are routed to the 70B+ parameter models on H100s.

---

## 8. AI Evaluation Checkpoints
**Confidence-Based Critic Sampling**
Before an Agent submits a hypothesis to the Mathematical Engine (`009`) or the Knowledge Substrate (`008`), it must pass a localized adversarial evaluation.
*   **Self-Evaluation Trigger:** Running a secondary Critic agent on every step doubles inference costs. Instead, the primary agent evaluates its own token softmax log-probabilities. It only invokes the heavy Critic Agent if its mathematical confidence drops below a threshold (e.g., 85%).
*   **Model Diversity:** To prevent shared blind spots, the Critic Agent is intentionally instantiated with a *different* foundational model weight (e.g., Mistral instead of Llama).
*   **Rejection:** If the Critic detects a logical fallacy or hallucination, it rejects the state transition, forcing the primary agent to backtrack in its MDP.
