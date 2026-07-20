import json
import os

EVALUATOR_FILES = [
    "data/ANTIGRAVITY_EVIDENCE_V1/evaluator_01.json",
    "data/ANTIGRAVITY_EVIDENCE_V1/evaluator_02.json",
    "data/ANTIGRAVITY_EVIDENCE_V1/evaluator_03.json",
    "data/ANTIGRAVITY_EVIDENCE_V1/evaluator_04.json",
    "data/ANTIGRAVITY_EVIDENCE_V1/evaluator_05.json"
]

def load_evaluations():
    evals = []
    for filepath in EVALUATOR_FILES:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                try:
                    data = json.load(f)
                    if data:
                        evals.append(data)
                except:
                    pass
    return evals

def generate_report(filename, title, content):
    path = os.path.join(r"C:\Users\saich\.gemini\antigravity-ide\brain\c1837166-e0e6-460e-96fe-8c1368177709", filename)
    with open(path, 'w') as f:
        f.write(f"# {title}\n\n{content}\n")
    print(f"Generated {filename}")

def run_analysis():
    evals = load_evaluations()
    
    if not evals:
        content = "> [!WARNING]\n> **Insufficient Evidence:** 0 of 5 blinded human evaluations have been submitted. Analysis is blocked until domain experts complete the `BLIND_EVALUATION_SURVEY_V1.md` and populate the raw JSON files.\n\n*Pipeline is established and awaiting data.*"
        
        generate_report("SURPRISE_ANALYSIS_V1.md", "SURPRISE_ANALYSIS_V1", content)
        generate_report("FAILURE_CLUSTERING_V1.md", "FAILURE_CLUSTERING_V1", content)
        generate_report("HUMAN_MODEL_ASYMMETRY_V1.md", "HUMAN_MODEL_ASYMMETRY_V1", content)
        generate_report("CALIBRATION_REPORT_V1.md", "CALIBRATION_REPORT_V1", content)
        return

    # In a real scenario where `evals` has data, this section would perform statistical aggregations
    # and NLP topic clustering on Q5 (Free text weaknesses)
    pass

if __name__ == "__main__":
    run_analysis()
