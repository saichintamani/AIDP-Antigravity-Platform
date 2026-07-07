# ADR-005: Autonomous Research Operations Architecture

## Status
Proposed

## Context
With the Autonomous Scientist Cognition Layer established (ADR-004), AIDP agents now possess isolated memories, persistent identities, and the ability to self-evolve. However, these highly capable agents lack constraints. Left to their own devices, they could theoretically consume unlimited compute, API tokens, and time chasing low-value hypotheses. To transform AIDP into a mature, self-managing scientific laboratory, we need an **Autonomous Research Operations (ResearchOps) Engine**.

## Decision
We will introduce the `src/aidp/research_ops` layer to govern resource allocation, scheduling, and scientific economics. This engine will act as the operational brain of the laboratory, enforcing constraints before any cognitive or execution task occurs.

### 1. Scientific Economics Engine
Every proposed task (e.g., hypothesis generation, literature review, experiment) will be evaluated by an `EconomicsEngine` to calculate its scientific ROI. The priority score will be derived from a function of Expected Impact, Expected Information Gain (EIG), and Novelty, divided by Estimated Cost, Time, and Risk.

### 2. Intelligent Scheduler
The system will move away from FIFO execution. An `IntelligentScheduler` will maintain a dependency-aware priority queue. High-ROI tasks will pre-empt lower-priority tasks. The scheduler will support parallel execution, delayed jobs, and checkpoint resumption.

### 3. Resource & Budget Controllers
A strict `ResourceManager` and `BudgetController` will govern the laboratory's daily spend across LLM tokens, GPU cycles, and API quotas. 
- If a budget threshold (e.g., 80% of daily limit) is breached, the controller will automatically enforce policies such as downgrading to cheaper LLM models or delaying expensive reasoning cycles.
- Experiments must explicitly "reserve" resources before they can be scheduled.

### 4. Campaign Management
Isolated hypothesis testing will be superseded by the `CampaignManager`. A Research Campaign is a long-running, multi-week objective (e.g., "Identify novel inhibitors for target X") containing a hierarchy of hypotheses, experiments, peer reviews, and ultimately publications.

### 5. Portfolio Optimizer
The `PortfolioOptimizer` will distribute laboratory resources across diverse scientific domains (e.g., 35% Cancer, 25% Virology) based on uncertainty reduction and expected value, ensuring the laboratory doesn't over-invest in dead ends.

### 6. Executive Control Center
The `ChiefScientistAI` will consume a real-time `ScientificKPIDashboard` tracking metrics like Knowledge Graph Growth, Cost per Discovery, and Evidence Quality. The Executive Controller will autonomously decide to pause failing campaigns, re-allocate budgets, or request additional evidence.

## Consequences
- **Positive**: AIDP transforms from a loose collection of scripts into a financially and computationally responsible scientific organization. We gain the ability to launch multi-week campaigns without fear of runaway API costs or infinite loops.
- **Negative**: The orchestration complexity increases exponentially. We must carefully mock or abstract compute/API metrics during testing to prevent brittle test suites.
