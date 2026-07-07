---
Document ID: AIDP-SPEC-012
Title: Canonical Knowledge and Reasoning Model
Version: 1.0
Status: Approved
---

# Detailed Architecture: Canonical Knowledge & Reasoning Model

## Introduction
The most insidious technical debt in distributed AI systems is **semantic fragmentation**. When the Agent Core, the Mathematical Engine, and the Knowledge Substrate exchange information via arbitrary `JSON` dicts, custom Protobufs, or untyped Python strings, the platform degrades into a brittle web of translation layers. 

To achieve a research-grade operating platform, AIDP mandates a **Canonical Cognitive Object**. Every subsystem in AIDP must speak this exact semantic language.

---

## 1. The Canonical Cognitive Object
Rather than passing raw "prompts" or "answers", the platform exclusively reasons over a highly typed data structure. Active in-memory cognitive objects are serialized via **Cap'n Proto** (enabling zero-copy serialization for deeply nested dynamic trees), while bulk vector knowledge is serialized in Apache Arrow. The semantic flow is strictly modeled as:

`Observation` $\rightarrow$ `Evidence Bundle` $\rightarrow$ `Verified Claim` $\rightarrow$ `Hypothesis` $\rightarrow$ `Probability Distribution` $\rightarrow$ `Decision` $\rightarrow$ `Action` $\rightarrow$ `Reflection` $\rightarrow$ `Learning Record`

*   **Universal Schema:** Every object in this pipeline inherits from a universal `CognitiveBase` schema containing standardized headers for `provenance_hash`, `joint_confidence`, `timestamp`, `source`, `uncertainty_profile`, `evidence_links`, and `mathematical_annotations`.

---

## 2. Immutable Provenance Lineage
Inspired by W3C PROV and OpenLineage, every Cognitive Object tracks its complete genealogical history without succumbing to $O(N)$ memory bloat.
*   **Merkle Tree Provenance:** Active objects do *not* hold their entire history array. They hold a cryptographic `parent_hash` (similar to a Git commit). The actual topological history DAG is offloaded asynchronously to the Neptune Substrate.
If an Agent generates a `Hypothesis`, its hash strictly links to:
*   **Which retrieval produced it?** (Direct links to the Qdrant vector UUIDs).
*   **Which model transformed it?** (MLflow Hash of the specific Llama-3-70B weight).
*   **Which mathematical process updated it?** (Reference to the MPNN execution run).
*   **Which agent approved it?** (ID of the Critic Agent).
*   **Which Knowledge Base version was used?** (Timestamped snapshot ID).

---

## 3. Strict Reasoning Contracts
To prevent hallucinations from propagating, the system enforces strict structural contracts at the schema level.
*   **Evidence Contract:** A `Hypothesis` object is structurally invalid and will be dropped by the network unless it holds a populated array of `Evidence Bundle` references OR a formal `Axiomatic Proof Trace` (for deductive logic without empirical evidence).
*   **Uncertainty Contract:** A `Belief` object cannot be serialized to the Knowledge Substrate unless it contains a calibrated `Probability Distribution`.
*   **Utility Contract:** A `Decision` object must explicitly record its expected utility estimate (Information Gain vs. Compute Cost).
*   **Reflection Contract:** A `Reflection` object must explicitly point to the prior `Assumptions` that were falsified by the reflection.

---

## 4. The 6-Dimensional Uncertainty Taxonomy
Confidence is not a single floating-point number (e.g., `confidence: 0.8`). AIDP requires agents and mathematical engines to isolate the exact source of uncertainty:
1.  **Epistemic Uncertainty:** "I don't know the answer because my model hasn't learned this scientific domain."
2.  **Aleatoric (Data) Uncertainty:** "The underlying dataset contains contradictory claims."
3.  **Retrieval Uncertainty:** "I found documents, but their cosine similarity to the query is dangerously low."
4.  **Model Uncertainty:** "My token semantic entropy is extremely high on this specific reasoning step."
5.  **Planning Uncertainty:** "I have a subgoal, but the constraint solver indicates a 40% chance of failure."
6.  **Tool Uncertainty:** "I am calling a biological API that has historically returned HTTP 500s 20% of the time."

To prevent catastrophic failure from naive averaging, the Mathematical Engine uses **Dempster-Shafer Theory (Theory of Belief Functions)** to fuse these 6 conflicting dimensions into a single mathematically sound joint belief mass (`joint_confidence`).

---

## 5. Cognitive Object Lifecycle
Every object follows a deterministic finite state machine (FSM):
1.  **Creation:** Instantiated by an Agent, Sensor, or Math Engine.
2.  **Validation:** Type-checked against the Reasoning Contracts.
3.  **Reasoning/Transformation:** Mutated by an LLM or Graph Network to produce a child object.
4.  **Evaluation:** Scored by the Critic network.
5.  **Storage:** Checkpointed to the Redis Ephemeral Store or Neptune Substrate.
6.  **Archival:** Compressed into cold storage when evicted from Working Memory.
7.  **Expiration:** Purged if proven mathematically false and deemed to hold zero procedural value.
