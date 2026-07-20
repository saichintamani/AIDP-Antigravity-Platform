import json
import os
from datetime import datetime


def main():
    print("==================================================")
    print(" AIDP Evaluator Feedback Collection Tool ")
    print("==================================================")
    
    participant_id = input("Enter Participant ID: ")
    task_id = input("Enter Task Name/ID: ")
    environment = input("Environment (Baseline/AIDP): ")
    
    print("\n--- Section 1: Quantitative ---")
    time_minutes = input("Time to Completion (minutes): ")
    
    print("\n--- Section 2: Qualitative (1-5 Scale) ---")
    epistemic_clarity = input("2.1 Epistemic Clarity (1-5): ")
    contradiction_res = input("2.2 Contradiction Resolution (1-5): ")
    constraint_enf = input("2.3 Physical Constraint Enforcement (1-5): ")
    confidence_align = input("2.4 Confidence Alignment (1-5): ")
    
    print("\n--- Section 3: Open Feedback ---")
    limitation = input("3.1 Primary limitation: ")
    hallucination = input("3.2 Did it state false facts without context? ")
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "participant_id": participant_id,
        "task_id": task_id,
        "environment": environment,
        "metrics": {
            "time_minutes": float(time_minutes) if time_minutes else None,
            "epistemic_clarity": int(epistemic_clarity) if epistemic_clarity else None,
            "contradiction_resolution": int(contradiction_res) if contradiction_res else None,
            "constraint_enforcement": int(constraint_enf) if constraint_enf else None,
            "confidence_alignment": int(confidence_align) if confidence_align else None
        },
        "feedback": {
            "limitation": limitation,
            "hallucination": hallucination
        }
    }
    
    output_dir = os.path.join("tests", "evaluation", "results", "track_e")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"eval_{participant_id}_{environment}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    print(f"\n[SUCCESS] Feedback saved to {filepath}")

if __name__ == "__main__":
    main()
