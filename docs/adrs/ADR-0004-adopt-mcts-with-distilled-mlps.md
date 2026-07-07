# ADR 0004: Adopt MCTS with Distilled MLPs

## Context
The Cognitive Agent must plan actions across the local Markov Blanket (Expected Utility maximization). The strict SLA for a planning step is $< 100$ms.

## Decision
We will adopt **Monte Carlo Tree Search (MCTS) with UCT**, but mandate that the rollout simulations use **Non-Autoregressive Distilled MLPs** (Continuous Actor-Critic networks) rather than the primary LLM.

## Status
Approved

## Consequences
*   **Positive:** MCTS elegantly handles open-ended, partially observable scientific domains. Distilling the LLM policy into an MLP drops node evaluation latency from $300$ms to $< 1$ms, easily satisfying the SLA and allowing deep simulation rollouts.
*   **Negative:** Requires a continuous offline RL pipeline (e.g., PPO or DPO) to repeatedly distill the primary 70B LLM's world model into the lightweight MLP networks.

## Alternatives Considered
*   **A* Search:** Rejected. It is impossible to define a strict, admissible mathematical heuristic for open-ended scientific discovery.
*   **LLM-driven MCTS (ToT/GoT):** Rejected. Running an autoregressive LLM inference trace at every simulated node violates the 100ms planning SLA by orders of magnitude.
