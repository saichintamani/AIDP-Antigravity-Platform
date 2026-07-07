# ADR-007: Cloud-Native Autonomous Research Platform (Phase D)

## Status
Proposed

## Context
AIDP has evolved from a monolithic Python prototype into an Autonomous Scientific Laboratory consisting of multiple subsystems (Cognitive Core, ResearchOps, Predictive Scientific Reasoning Engine). Currently, it runs as a local process. To function as a true "Operating System for Science", AIDP must scale horizontally. It needs a distributed compute backbone, a robust API, and a unified laboratory dashboard to visualize campaigns, budgets, and debate graphs.

## Decision
We will execute Phase D to transition AIDP into a Cloud-Native platform.

### 1. Distributed Compute Orchestration
- We will integrate **Ray** (or simulate its integration for now) to distribute `ResearchOps` tasks across a cluster. The `CampaignManager` will dispatch jobs to a Ray task queue, allowing hundreds of `DigitalTwin` simulations and `DebateGraphs` to resolve in parallel.

### 2. Platform API Gateway
- We will build a **FastAPI** service (`src/aidp/platform/api/`) acting as the primary entry point for human scientists. It will expose endpoints for:
  - `POST /campaigns`: Submit a new research goal.
  - `GET /campaigns/{id}`: View campaign status and spawned tasks.
  - `GET /metrics`: View `KPIDashboard` stats (cost per discovery, token burn).

### 3. Laboratory Web Dashboard
- We will build a **Streamlit** dashboard (`src/aidp/platform/dashboard/app.py`) to provide a visual interface for the laboratory. 
- It will visualize:
  - Real-time KPI metrics.
  - The live `Scheduler` queue (tasks waiting for execution).
  - High-level summaries of `DebateGraph` consensus.

## Consequences
- **Positive**: AIDP becomes a deployable enterprise system. Campaigns can scale beyond a single machine's compute constraints.
- **Negative**: Introducing Ray and FastAPI increases infrastructural complexity. We must ensure our previous deterministic test harnesses continue to work by mocking the distributed layer in CI.
