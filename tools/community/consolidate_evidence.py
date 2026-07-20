#!/usr/bin/env python3
import json
import os
from collections import defaultdict
import datetime

def consolidate_evidence(evidence_path, output_leaderboard):
    print("==================================================")
    print(" ANTIGRAVITY EVIDENCE CONSOLIDATION")
    print("==================================================\n")
    
    if not os.path.exists(evidence_path):
        print(f"[ERROR] Evidence database not found: {evidence_path}")
        return
        
    with open(evidence_path, 'r', encoding='utf-8') as f:
        reproductions = json.load(f)
        
    if not reproductions:
        print("[WARN] No valid reproductions found in database.")
        return

    # Aggregate by Model Version
    model_stats = defaultdict(lambda: {"total_evals": 0, "sum_leakage": 0.0, "successful_replications": 0})
    
    for rep in reproductions:
        model = rep.get('model', 'Unknown')
        leakage = rep.get('leakage_rate')
        outcome = rep.get('outcome', '')
        
        if leakage is not None:
            model_stats[model]["total_evals"] += 1
            model_stats[model]["sum_leakage"] += leakage
            
            if outcome in ["Full replication", "Phenomenon replication"]:
                model_stats[model]["successful_replications"] += 1
                
    # Generate Leaderboard Markdown
    markdown = f"# Antigravity Leaderboard\n\n"
    markdown += f"*Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    markdown += "This leaderboard aggregates external, independent reproductions of the ConstraintBench-100 dataset.\n\n"
    markdown += "| Model Version | Total External Evals | Avg Leakage Rate | Successful Replications (Confirmed Phenomenon) |\n"
    markdown += "| --- | --- | --- | --- |\n"
    
    for model, stats in sorted(model_stats.items(), key=lambda x: (x[1]["sum_leakage"]/x[1]["total_evals"] if x[1]["total_evals"] > 0 else 0), reverse=True):
        avg_leakage = stats["sum_leakage"] / stats["total_evals"] if stats["total_evals"] > 0 else 0.0
        markdown += f"| {model} | {stats['total_evals']} | {avg_leakage:.1f}% | {stats['successful_replications']}/{stats['total_evals']} |\n"
        
    with open(output_leaderboard, 'w', encoding='utf-8') as f:
        f.write(markdown)
        
    print(f"Consolidated data for {len(model_stats)} unique models.")
    print(f"Leaderboard written to: {output_leaderboard}")

if __name__ == "__main__":
    db = "data/ANTIGRAVITY_EVIDENCE_V1/community_evidence.json"
    leaderboard = "LEADERBOARD.md"
    consolidate_evidence(db, leaderboard)
