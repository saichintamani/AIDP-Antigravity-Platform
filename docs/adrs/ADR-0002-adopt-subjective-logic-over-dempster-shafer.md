# ADR 0002: Adopt Subjective Logic Over Dempster-Shafer

## Context
The Mathematical Engine fuses 6 dimensions of uncertainty (Epistemic, Aleatoric, Retrieval, Model, Planning, Tool) into a single joint belief mass.

## Decision
We will adopt **Subjective Logic** with strict covariance-discounting to fuse multidimensional uncertainty, explicitly replacing standard Dempster-Shafer Theory.

## Status
Approved

## Consequences
*   **Positive:** Subjective Logic naturally handles highly correlated evidence sources (e.g., Model and Planning uncertainty originating from the same LLM). This prevents the pathological overconfidence seen in standard Dempster-Shafer fusion.
*   **Negative:** Adds computational complexity. The Engine must compute the covariance matrix $\Sigma$ across dimensions in real-time before applying the consensus operator.

## Alternatives Considered
*   **Dempster-Shafer (Standard):** Rejected. Mathematically assumes all evidence sources are strictly independent, violating AIDP's correlated inference chains.
*   **Naive Averaging / Softmax:** Rejected. Averages mask fatal uncertainties (e.g., 99% Tool failure masked by 10% Data uncertainty).
