# AlignEval: Blinded Human-AI Alignment Workflow

AlignEval is a zero-dependency, standalone CLI tool extracted from the AIDP research program. It solves a critical operational bottleneck in modern AI research: gathering unbiased, blinded evaluations from domain experts without introducing hindsight bias or candidate ordering bias.

## The Problem
When evaluating foundation models or complex reasoning engines against historical baselines or human benchmarks, researchers often struggle to create standardized surveys. Manually randomizing options across dozens of surveys, stripping out future context, and standardizing formatting is incredibly error-prone and leads to compromised data.

## The Solution
AlignEval takes a simple, structured JSON file containing historical evidence, constraints, and candidate hypotheses. It uses the specific `case_id` to cryptographically seed the randomizer, perfectly shuffling the candidate options (preventing ordering bias like "Option C is always the historical winner") while maintaining perfect reproducibility for your audit trail.

## Usage

**1. Create your case data**
Create a `.json` file following the schema in `sample_case.json`.

**2. Generate the Survey**
```bash
python align_eval.py sample_case.json --output_dir surveys/
```

**3. Output**
The tool will generate a perfectly formatted `survey_demo_case_01.md` containing the blinded candidate options, ready to be sent to human evaluators.

## Extracted from AIDP
This tool was built to administer the N=10 historical replay baseline for the Artificial Intelligence Discovery Platform (AIDP). It is provided here as a standalone utility for the broader ML evaluation community.
