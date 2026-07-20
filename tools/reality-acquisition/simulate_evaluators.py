import os
import json
import urllib.request
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SURVEYS_DIR = Path("surveys")
OUTPUT_FILE = Path("data/human_pilot_surveys/simulated_evaluations.json")
LOCK = threading.Lock()

PERSONAS = {
    "Dr. Silva (Biology/Life Science)": "You are Dr. Silva, a rigorous molecular biologist and geneticist. You prioritize molecular accuracy, protein mechanics, and feasibility in living systems.",
    "Dr. Chen (Physics/Materials)": "You are Dr. Chen, a strict condensed matter physicist. You prioritize thermodynamics, crystallography, atomic structure, and mathematical consistency.",
    "Dr. Vance (Engineering)": "You are Dr. Vance, a practical systems engineer. You prioritize experimental feasibility, design mechanics, scaleability, and concrete applications.",
    "Dr. Reyes (General Reviewer 1)": "You are Dr. Reyes, a multidisciplinary scientific reviewer. You focus on logical consistency, depth of reasoning, and clarity of the hypothesis.",
    "Dr. Patel (General Reviewer 2)": "You are Dr. Patel, a strict methodologist. You focus heavily on epistemological bounds, strength of evidence, and adherence to scientific methodology."
}

def load_surveys():
    surveys = []
    
    TARGETS = {
        "Track_A2": ["survey_plate tectonics.md", "survey_prions.md"]
    }
    
    for track, files in TARGETS.items():
        track_dir = SURVEYS_DIR / track
        if not track_dir.exists():
            continue
        for filename in files:
            file = track_dir / filename
            if file.exists():
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                surveys.append({
                    "track": track,
                    "case": file.stem.replace("survey_", ""),
                    "content": content
                })
    return surveys

def evaluate_survey(persona_name, persona_desc, survey_content):
    prompt = f"""
{persona_desc}

You are participating in a blind scientific evaluation. You must read the survey provided below and evaluate the candidate experiment.
Score the experiment on the following 4 dimensions using a 1 to 10 scale (where 10 is the best).

1. Leakage Resistance: Did the proposal import post-cutoff knowledge or rely on hindsight? (10 = perfectly bounded and innocent, 1 = blatant cheating/hindsight).
2. Reasoning Depth: Did it actually reason step-by-step, or just become vague? (10 = profound multi-step logic, 1 = superficial/vague).
3. Constraint Compliance: Did it obey the instruction constraints? (10 = strict compliance, 1 = ignored instructions).
4. Scientific Usefulness: Would a domain expert consider this worth reviewing? (10 = paradigm-shifting insight, 1 = useless hallucination).

Provide your evaluation as a valid JSON object with EXACTLY these keys:
"leakage_resistance" (int), "reasoning_depth" (int), "constraint_compliance" (int), "scientific_usefulness" (int), "rationale" (string).

Survey Content:
-------------------
{survey_content}
-------------------

OUTPUT ONLY VALID JSON. Do not include markdown formatting like ```json or any conversational text.
"""
    
    url = "http://localhost:11434/api/chat"
    data = {
        "model": "llama3.1:8b",
        "messages": [{"role": "user", "content": prompt}],
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.7}
    }
    
    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), {'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            content = result["message"]["content"]
            return json.loads(content)
    except Exception as e:
        print(f"Error evaluating: {e}")
        return None

def process_evaluation(survey, persona_name, persona_desc):
    print(f"Starting {survey['track']} - {survey['case']} by {persona_name}...")
    eval_data = evaluate_survey(persona_name, persona_desc, survey["content"])
    return {
        "track": survey["track"],
        "case": survey["case"],
        "persona": persona_name,
        "scores": eval_data
    }

def main():
    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    surveys = load_surveys()
    results = []

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                results = json.load(f)
            except:
                results = []
            
    processed_keys = set(f"{r['track']}_{r['case']}_{r['persona']}" for r in results)

    tasks = []
    for survey in surveys:
        for persona_name, persona_desc in PERSONAS.items():
            key = f"{survey['track']}_{survey['case']}_{persona_name}"
            if key in processed_keys:
                continue
            tasks.append((survey, persona_name, persona_desc))

    print(f"Found {len(tasks)} evaluations to run.")

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = {executor.submit(process_evaluation, t[0], t[1], t[2]): t for t in tasks}
        for future in as_completed(futures):
            res = future.result()
            if res["scores"]:
                with LOCK:
                    results.append(res)
                    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                        json.dump(results, f, indent=2)
                print(f"Finished {res['track']} - {res['case']} by {res['persona']}")
            else:
                print(f"Failed {res['track']} - {res['case']} by {res['persona']}")

    print("Evaluation complete.")

if __name__ == "__main__":
    main()
