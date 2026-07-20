import os
import random
import sys
import pandas as pd

# Add src and current dir to path to allow absolute imports



from tests.evaluation.datasets.historical_cases import ALL_CASES

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'results')
NUM_RATERS = 5
ACCURACY_TARGET = 0.5

def generate_mock_data():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    rows = []
    
    for case in ALL_CASES:
        candidates = case.candidate_experiments.copy()
        # Same seed as the survey generator to ensure options match
        random.seed(42) 
        random.shuffle(candidates)
        
        # Find the correct option index (A=0, B=1, C=2, D=3)
        correct_idx = candidates.index(case.historical_winner)
        options = ["Option A", "Option B", "Option C", "Option D"]
        correct_option = options[correct_idx]
        
        # Re-seed for randomness in rater generation
        random.seed(hash(case.case_id)) 
        
        for rater_id in range(1, NUM_RATERS + 1):
            if random.random() < ACCURACY_TARGET:
                rank1 = correct_option
            else:
                wrong_options = [opt for opt in options if opt != correct_option]
                rank1 = random.choice(wrong_options)
                
            # Fill the rest randomly
            remaining = [opt for opt in options if opt != rank1]
            random.shuffle(remaining)
            rank2, rank3, rank4 = remaining
            
            rows.append({
                "rater_id": f"Expert_{rater_id}",
                "case_id": case.case_id,
                "rank_1": rank1,
                "rank_2": rank2,
                "rank_3": rank3,
                "rank_4": rank4,
                "rationale": f"Mock rationale from Expert_{rater_id} for {case.case_id}. I believe {rank1} is the most viable path forward based on current evidence."
            })
            
    df = pd.DataFrame(rows)
    out_path = os.path.join(OUTPUT_DIR, "expert_scores.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated mock data for {len(ALL_CASES)} cases and {NUM_RATERS} raters.")
    print(f"Saved to {out_path}")

if __name__ == "__main__":
    generate_mock_data()
