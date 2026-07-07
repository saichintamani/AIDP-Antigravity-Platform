# ADR-004: Agent Cognition Architecture

## Status
Proposed

## Context
The AIDP architecture is transitioning from a monolithic reasoning engine to an Autonomous Scientific Laboratory (Phase C). In Cluster 1, we implemented the `ScientificCommunicationProtocol` and structured the agents into specialized Teams. For Cluster 2, we must advance the agents beyond simple stateless personas into autonomous, persistent scientific identities. Each agent must possess its own memory hierarchy, learning lifecycle, and version-controlled configuration, mirroring the expertise and biases of real scientists.

## Decision
We will implement the **Autonomous Scientist Cognition Layer**, consisting of the following core architectural components:

### 1. The Agent Genome
Every agent will be defined by an `AgentGenome`, a version-controlled configuration object containing:
- **Scientific Identity**: Role, specialization, and cognitive fingerprint (e.g., risk tolerance, skepticism).
- **Expertise Graph**: A directed graph of knowledge domains the agent specializes in, weighted by experience and confidence.
- **Prompt Evolution State**: The current iteration of the agent's system prompt and its historical performance accuracy.
- **Reasoning Strategy Preferences**: Weights determining whether the agent prefers Chain of Thought, Tree of Thought, or Debate based on past success rates.

### 2. Hierarchical Memory Partitioning
A single memory store is insufficient. Each agent will maintain an isolated hierarchical memory structure:
- **Working Memory**: Context for the current campaign or debate.
- **Episodic & Semantic Memory**: Factual knowledge and past research cycles.
- **Procedural & Strategy Memory**: "How-to" knowledge for experimental design and statistical methodologies.
- **Reflection & Failure Memory**: A ledger of past mistakes to prevent repeating analytical errors.

### 3. The Continuous Learning Lifecycle
Every research cycle will conclude with a **Reflection Loop**. The agent will ask:
- What succeeded and what failed?
- How much did my confidence align with reality?
- Which reasoning patterns worked best?
This reflection will trigger the **Prompt Evolution** and **Meta-Learning** engines, allowing the agent to dynamically rewrite its prompt and adjust its reasoning strategies.

### 4. Reputation & Calibration System
The `ChiefScientistAI` will maintain a reputation matrix. Agents who consistently exhibit poor confidence calibration (e.g., 95% confident but only 63% accurate) will have their influence weighted down in the `MultiAgentConsensus` fusion step until they self-correct.

### 5. Decision Journaling
Every major decision made by an agent will be recorded in a `DecisionJournal` detailing the evidence used, alternatives rejected, and expected impact, ensuring strict epistemic reproducibility.

## Consequences
- **Positive**: Agents will no longer be static prompt wrappers; they will evolve, learn from mistakes, and specialize dynamically. The `AgentGenome` enables exact cloning, rollback, and reproducibility of any scientific agent at any point in time.
- **Negative**: The complexity of state management increases significantly. We will need robust database/storage mechanisms (likely expanding on the Cap'n Proto / Qdrant foundation) to handle the persistence and versioning of the memory hierarchies and genomes.
