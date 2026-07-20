import collections
import json
import os

RANKINGS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "tests", "evaluation", "results", "track_e_rankings.json"
)

RAW_RESULTS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "tests", "evaluation", "results", "historical_benchmarks", "latest_raw_results.json"
)

def analyze():
    if not os.path.exists(RANKINGS_FILE):
        print("No Track E rankings found.")
        return

    with open(RANKINGS_FILE) as f:
        rankings = json.load(f)

    if not rankings:
        print("Track E rankings file is empty.")
        return

    with open(RAW_RESULTS_FILE) as f:
        ai_results = {r["case_id"]: r for r in json.load(f)}

    print("=== AIDP Track E: Independent Human Evaluation Analysis ===")
    print(f"Total Submissions: {len(rankings)}")
    
    # Group by case
    case_rankings = collections.defaultdict(list)
    for r in rankings:
        case_rankings[r["case_id"]].append(r)

    print("\n--- Consensus Analysis ---")
    for case_id, subs in case_rankings.items():
        print(f"\nCase: {case_id} (Evaluators: {len(subs)})")
        
        # Calculate mean rank for each candidate
        candidate_scores = collections.defaultdict(list)
        for sub in subs:
            for idx, cand in enumerate(sub["ranked_candidates"]):
                candidate_scores[cand].append(idx + 1)
                
        mean_ranks = {cand: sum(scores)/len(scores) for cand, scores in candidate_scores.items()}
        sorted_consensus = sorted(mean_ranks.items(), key=lambda x: x[1])
        
        print("  Human Consensus Ranking:")
        for idx, (cand, score) in enumerate(sorted_consensus):
            print(f"    {idx+1}. (Mean: {score:.2f}) {cand[:80]}...")

        # Compare to AIDP
        ai_data = ai_results.get(case_id)
        if ai_data:
            # We know AIDP's top choice is typically the historical winner if it passed
            historical_winner = ai_data["historical_winner"]
            
            # Did humans put the historical winner first?
            human_top_choice = sorted_consensus[0][0]
            human_correct = (human_top_choice == historical_winner)
            
            print(f"  AIDP Rank for Winner: {ai_data['aidp_rank']}")
            print(f"  Human Rank for Winner: {mean_ranks.get(historical_winner, 'N/A')}")
            print(f"  Agreement: {'YES' if (ai_data['aidp_rank'] == 1 and human_correct) else 'NO'}")

if __name__ == "__main__":
    analyze()
