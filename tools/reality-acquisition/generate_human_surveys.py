import os

SURVEY_TEMPLATE = """# Expert Evaluation Survey: {case_name}

**Instructions:**
You have been provided with two hypotheses representing alternative explanations for historical scientific data. Please read the provided context (attached separately) and answer the following questions.

### 1. Choice
Based *only* on the evidence provided in the dossier, which hypothesis represents a more scientifically robust direction?
- [ ] Hypothesis A
- [ ] Hypothesis B

### 2. Confidence
On a scale of 1 to 10, how confident are you in this choice? (1 = Random Guess, 10 = Absolute Certainty)
**Score:** ____

### 3. Rationale
Please provide a brief written rationale explaining *why* you chose this hypothesis over the alternative, specifically referencing any constraints or logical dependencies that influenced your decision.

**Rationale:**
(Write your explanation here)
"""

CASES = ["Prions", "Plate Tectonics", "CRISPR"]

def generate_surveys():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "ANTIGRAVITY_EVIDENCE_V1", "human_surveys")
    os.makedirs(output_dir, exist_ok=True)
    
    for case in CASES:
        filename = case.lower().replace(" ", "_") + "_survey.md"
        filepath = os.path.join(output_dir, filename)
        
        content = SURVEY_TEMPLATE.format(case_name=case)
        
        with open(filepath, "w") as f:
            f.write(content)
            
        print(f"Generated survey for {case} at {filepath}")

if __name__ == "__main__":
    generate_surveys()
    print("\n[SUCCESS] Track A survey generation complete.")
    print("Please distribute these to 5 domain experts and record the results.")
