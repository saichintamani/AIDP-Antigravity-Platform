---
Document ID: AIDP-SPEC-020
Title: Phase 18 - Scientific Memory System
Version: 1.0
Status: Active
---

# Phase 18: Scientific Memory System

## 1. Mission Statement
Preserve what the system has learned, why it learned it, and what evidence justified the learning. Transform AIDP from a system that learns per-run into one with true institutional memory. Exclude raw conversational logs to prevent noise; focus purely on epistemically rigorous metadata.

## 2. Core Deliverables

### 2.1 Adaptation Memory
Persistent storage of `AdaptationRecord` objects. Future audits can query this layer to answer: *"Why does the system behave this way today?"*

### 2.2 Failure Memory
Longitudinal tracking of recurring failure modes (e.g., Z3 constraint violations). Tracks occurrences, first_seen, and last_seen timestamps to monitor if failures are increasing or decreasing over time.

### 2.3 Assumption Memory
Longitudinal tracking of biological and structural assumptions. Assumptions remain revisable; nothing becomes permanent truth. Records support vs. contradiction ratios across all runs.

### 2.4 Reviewer Memory
Tracks reviewer performance across time windows (e.g., runs or months) to establish evidence-driven reviewer reliability.

### 2.5 Strategy Memory
Captures the feedback loop of Question -> Intervention -> Outcome -> Lesson. This provides reusable organizational intelligence.

## 3. Architecture
- **InstitutionalModels**: Longitudinal schemas (e.g., `LongitudinalReviewerStats`).
- **MemoryRepository**: A decoupled storage abstraction (e.g., `JsonMemoryRepository`) ensuring the memory layer can scale to databases later without logic changes.
- **ScientificMemorySystem**: The orchestrator that bridges Introspection/Adaptation outputs and the persistent storage backend.
