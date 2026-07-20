# Investigative Playbook for Agentic Systems

This document outlines the core methodology for diagnosing and resolving failures in complex agentic workflows. 

Our fundamental axiom is: **Many apparent AI model failures are actually information-flow failures.**
Before attempting to scale a model, fine-tune weights, or add dense prompt engineering, we must first trace where context is dropped, where schema expectations mismatch, and where structural reasoning primitives are missing.

## The Core Philosophy
The goal of engineering is not to prove that we are right; it is to create conditions under which we can discover when we are wrong. Every intervention must be testable, falsifiable, and rigorously documented.

## The 8-Step Diagnostic Loop
When the system fails, execute the following loop sequentially:

1. **What would convince us we're wrong?** (Establish the falsification criteria immediately).
2. **What failed?** (Define the exact symptoms and top-level error state).
3. **Where did it fail?** (Trace the execution path through the DAG to isolate the failing node).
4. **What competing explanations exist?** (List possible root causes: Network error? Model capability? Schema mismatch? Context truncation?).
5. **What evidence would distinguish them?** (Identify the exact JSON payload, logging event, or metric that proves which explanation is correct).
6. **What intervention tests the hypothesis?** (Propose a surgical architectural change).
7. **What regression signature should we expect?** (If this intervention were removed tomorrow, exactly what behavior would break, and how would we detect it?)
8. **Did the evidence change as predicted?** (Validate the hypothesis against the new evidence trace).

## Architectural Principles
- **Treat failures as data**: Every rejection or block by a simulated reviewer is an opportunity to extract missing dependencies.
- **Separate observations from explanations**: Ensure that the claims made in post-mortems map exactly to the raw trace files (e.g., distinguishing "the model is dumb" from "the payload is missing the 'sample_size' field").
- **Design interventions that test hypotheses**: Do not introduce multiple variables simultaneously. Introduce one structural fix and measure the isolated behavioral change.
- **Preserve reproducibility**: Ensure that independent observers can run verification scripts against archived outputs without relying on generated summaries.

This playbook is designed to scale across benchmarks, new model architectures, and completely different research domains. It replaces "Optimization Thinking" (guessing and checking prompts) with "Investigation Thinking" (causal root-cause isolation).
