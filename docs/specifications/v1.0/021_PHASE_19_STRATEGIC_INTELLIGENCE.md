---
Document ID: AIDP-SPEC-021
Title: Phase 19 - Strategic Intelligence Layer (SIL)
Version: 1.0
Status: Active
---

# Phase 19: Strategic Intelligence Layer

## 1. Mission Statement
Transform AIDP into a true Uncertainty Reduction Engine. The Strategic Intelligence Layer acts as the executive brain sitting above all other phases (Knowledge, Verification, Explainability, Introspection, Adaptation, Memory). Its sole purpose is to determine where uncertainty exists, how valuable that uncertainty is, and what action would reduce it most efficiently.

## 2. Core Primitives

### 2.1 ResearchOpportunity
The platform shifts from being Claim-centric to Opportunity-centric. A `ResearchOpportunity` represents a gap in knowledge that can be investigated.
It contains:
- Current Uncertainty
- Potential Downstream Impact
- Estimated Investigation Cost
- Expected Information Gain (EIG)
- Priority Score

### 2.2 Expected Information Gain (EIG)
The flagship metric of the Strategic Intelligence Layer. It answers: *"If I perform this investigation, how much uncertainty mathematically disappears?"*
EIG is calculated using Shannon Entropy over the platform's Subjective Logic models.

## 3. Decision Framework
The SIL continuously evaluates unresolved claims and answers three strategic questions:
1. **Where is uncertainty highest?** (High entropy)
2. **Which uncertainty is most important?** (High impact mapping)
3. **What investigation would reduce it most efficiently?** (High EIG / Low Cost)

## 4. Architecture
- **StrategicModels**: Defines `ResearchOpportunity`.
- **InformationTheory**: Computes entropy and EIG from existing epistemic states.
- **StrategicIntelligenceEngine**: Scans the knowledge boundary, scores all potential investigations, and outputs a mathematically prioritized roadmap.
