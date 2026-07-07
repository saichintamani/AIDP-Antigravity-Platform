---
Document ID: AIDP-SPEC-011
Title: COMPUTATIONAL INTELLIGENCE ARCHITECTURE
Version: 1.0
Status: Approved
---
# Detailed Architecture: Computational Intelligence Architecture

## Introduction
AIDP is not an LLM application; it is an autonomous scientific reasoning engine. To bridge the gap between physical execution (`010`) and mathematical formalization (Phase 5), we define the **Computational Intelligence Architecture**. This subsystem specifies the exact cognitive models, memory hierarchies, and decision-theoretic frameworks that all agents must implement, abstracting away framework-specific behaviors in favor of a universal intelligence pipeline.

---

## 1. The Intelligence Pipeline
AIDP implements **Dual-Process Theory (System 1 / System 2)** to prevent astronomical latency and token overhead.

**System 2 (Slow, Rigorous Path):**
`Observation` $\rightarrow$ `Perception` $\rightarrow$ `Context Formation` $\rightarrow$ `Knowledge Activation` $\rightarrow$ `Working Memory` $\rightarrow$ `Reasoning` $\rightarrow$ `Planning` $\rightarrow$ `Decision Theory` $\rightarrow$ `Tool Selection` $\rightarrow$ `Execution` $\rightarrow$ `Reflection` $\rightarrow$ `Self Evaluation` $\rightarrow$ `Confidence Calibration` $\rightarrow$ `Learning` $\rightarrow$ `Memory Consolidation` $\rightarrow$ `Knowledge Evolution`

**System 1 (Fast Path Bypass):**
If an `Observation` structurally matches a known, high-confidence pattern in Procedural Memory, the Agent instantly executes the compiled Tool Selection (System 1). This bypasses the heavy 70B parameter LLM reasoning chain entirely, resolving the action in milliseconds.

---

## 2. The Memory Hierarchy
Agents do not rely on a monolithic "context window." AIDP implements a multi-tiered memory architecture governed by strict lifecycle and consolidation policies.

*   **Sensory Memory:** Highly volatile. Stores raw observations (e.g., the JSON output of an API call) for $< 1$ second. 
*   **Working Memory:** The active LLM context window. Bounded to task-relevant abstractions. Evicted upon task completion.
*   **Episodic Memory:** Event logs of the Agent's past trajectories ("I tried X, it failed with error Y"). Indexed temporally.
*   **Semantic Memory:** The Knowledge Substrate (`008`). Immutable, vectorized scientific facts and ontological graphs.
*   **Procedural Memory:** Compiled skills. If an Agent learns a complex data retrieval pattern, it compiles the schema into a reusable, rigid structure, bypassing the need to "re-learn" it.
*   **Collective Research Memory:** Shared hypotheses across the multi-agent swarm.

---

## 3. Planning & Constraint Satisfaction
We reject naive heuristic search (e.g., standard ReAct or Tree of Thoughts) in favor of formal **Task Graphs**.
*   **Subgoal Generation:** The global goal is decomposed into a Directed Acyclic Graph (DAG) of subgoals.
*   **Deterministic Constraint Satisfaction:** LLMs are incapable of rigorous constraint satisfaction. The Agent generates the topological DAG, but execution is handed over to an external, deterministic **Z3 Theorem Prover**, which mathematically verifies permissions, token budgets, and temporal scheduling constraints before execution is allowed.
*   **Replanning:** If execution fails, the Agent does not just "try again." It propagates the failure up the Task Graph, prunes the invalid branch, and generates a new sub-graph.

---

## 4. Formal Decision Theory
Token sampling (e.g., `temperature=0.2`) is insufficient for scientific reasoning. Action selection is governed by formal Decision Theory.
*   **Expected Utility:** Actions are chosen based on the expected reduction of uncertainty (Information Gain).
*   **Markov Blanket Sub-Sampling:** Calculating Bayesian Information Gain across a 1-Billion node graph is computationally intractable ($O(|V|^3)$). The Agent is restricted to calculating Expected Utility strictly on the **Markov Blanket** (the immediate subgraph neighborhood) of its current active context, reducing the computation to $O(k^3)$ where $k \ll |V|$.
*   **Bayesian Active Learning:** The Agent prioritizes actions within its Markov Blanket that will most significantly update its prior beliefs (via the Mathematical Engine).
*   **Cost-Aware Planning:** The utility function explicitly penalizes actions with high token/compute costs unless the expected Information Gain justifies it.

---

## 5. Learning & Skill Consolidation
Agents must evolve beyond their base weights.
*   **Pattern Discovery:** During the `Reflection` phase, if the Agent detects a recurring successful reasoning pattern, it isolates it.
*   **Secure Skill Formation:** To prevent catastrophic RCE (Remote Code Execution) vulnerabilities, Agents cannot compile skills as raw Python. The pattern is compiled into a constrained **Domain Specific Language (DSL)** (a strict JSON-based AST) that only permits whitelisted tool invocations. This DSL is pushed to **Procedural Memory**.
*   **Future Planning:** Future Task Graphs can invoke this single consolidated DSL skill (System 1 Fast Path) instead of wasting tokens reasoning from scratch.

---

## 6. The Internal World Model
AIDP maintains a mathematical representation of reality, explicitly mapping certainty.
*   **Fact vs. Hypothesis:** The Knowledge Substrate natively distinguishes between established scientific facts (Truth) and Agent-generated hypotheses (Probabilities).
*   **Structural Uncertainty:** The World Model tracks *what it does not know*, explicitly maintaining null-spaces in the graph to direct future Agent exploration.

---

## 7. Meta-Cognition (Thinking About Thinking)
Agents must possess self-awareness of their own cognitive state without doubling the primary inference cost.
*   **Shadow Models:** Meta-cognition does not run on the primary 70B/405B model. It runs asynchronously on a heavily quantized, **"shadow" 8B parameter model** deployed on cheap L4 GPUs.
*   **Source Challenging:** The shadow model constantly reads the primary agent's reasoning trace and asks, "Did I rely too heavily on a single paper from 1998?"
*   **Confidence Calibration:** If the shadow model detects severe logical inconsistencies, it acts as a circuit breaker, halting the primary agent's execution and triggering a mandatory `Self Evaluation` phase.
