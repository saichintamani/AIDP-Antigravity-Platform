# Golden Dataset Governance

This directory contains datasets used for evaluating the Cognitive Pipeline via the `EvaluationHarness`.

Because we are incrementally replacing mock providers with live models, dataset inputs must be strictly categorized to ensure evaluation metrics reflect reality rather than overfitting to test cases.

## Dataset Categories

### 1. Canonical Tasks (`canonical/`)
- **Definition**: Hand-written, scientifically rigorous reference examples curated by human experts.
- **Purpose**: Defines the "gold standard" for cognitive output. These are the primary artifacts used to score provider capabilities during gate reviews.
- **Example**: A well-documented biological contradiction with an expected, validated hypothesis schema.

### 2. Regression Tasks (`regression/`)
- **Definition**: Previously discovered bugs, edge cases, or LLM hallucinations that have been fixed.
- **Purpose**: Ensures that once a failure mode is addressed (e.g., via a prompt update or safety validator), it never reappears in production.
- **Example**: A prompt that previously caused an LLM to violate the structured output schema.

### 3. Synthetic Tasks (`synthetic/`)
- **Definition**: Auto-generated examples used for load testing, fuzzy matching, and edge-case boundary testing.
- **Purpose**: High-volume testing for latency, cost estimation, and stability. 
- **Constraint**: Synthetic tasks are **never** to be presented as representative of production quality or used for core capability gate reviews.

## Usage Guidelines

- Any benchmark run for a Gate Review must clearly label which dataset categories were included.
- Never mix Canonical and Synthetic metrics in executive summaries.
