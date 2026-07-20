import json
import os
from datetime import datetime

RESULTS_PATH = "tests/evaluation/results/historical_benchmarks/latest_raw_results.json"
DASHBOARD_PATH = "docs/PUBLIC_DASHBOARD.md"

def generate_dashboard():
    if not os.path.exists(RESULTS_PATH):
        print(f"Error: {RESULTS_PATH} not found. Run the test suite first.")
        return
        
    with open(RESULTS_PATH) as f:
        results = json.load(f)
        
    md = [
        "# AIDP Public Benchmark Dashboard",
        f"*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "This dashboard tracks the performance of the Artificial Intelligence Discovery Platform (AIDP) against the Historical Replay Benchmark Suite. It evaluates whether AIDP can prioritize historically correct paradigm shifts over plausible contemporary decoys.",
        "",
        "## Overall Leaderboard",
        "",
        "| Case ID | Domain | AIDP Status | Outperforms Baseline? |",
        "|---------|--------|-------------|-----------------------|"
    ]
    
    total_cases = len(results)
    populated = sum(1 for r in results if r["status"] != "PENDING_LITERATURE_REVIEW")
    passed = sum(1 for r in results if r.get("status") in ["PASS", "PARTIAL"])
    failed = sum(1 for r in results if r.get("status") == "FAIL")
    pending = total_cases - populated
    
    baseline_wins = sum(1 for r in results if r.get("outperforms_baseline"))
    
    populated_results = [r for r in results if r["status"] != "PENDING_LITERATURE_REVIEW"]
    if populated_results:
        mean_percentile = sum(r.get("aidp_percentile", 0) for r in populated_results) / populated
        sorted_percentiles = sorted(r.get("aidp_percentile", 0) for r in populated_results)
        mid = populated // 2
        median_percentile = (sorted_percentiles[mid] + sorted_percentiles[~mid]) / 2.0
    else:
        mean_percentile = 0.0
        median_percentile = 0.0

    for r in results:
        case_id = r["case_id"]
        domain = r["domain"]
        status = r["status"]
        
        if status == "PENDING_LITERATURE_REVIEW":
            baseline_str = "N/A"
            status_str = "⏳ PENDING"
        else:
            baseline_str = "✅ YES" if r.get("outperforms_baseline") else "❌ NO"
            if status == "PASS":
                status_str = "🟢 PASS (Top 10%)"
            elif status == "PARTIAL":
                status_str = "🟡 PARTIAL (Top 50%)"
            else:
                status_str = "🔴 FAIL"
                
        md.append(f"| {case_id} | {domain} | {status_str} | {baseline_str} |")

    if populated < 5:
        confidence_level = f"Preliminary (N={populated})"
    elif populated < 10:
        confidence_level = f"Early Evidence (N={populated})"
    elif populated < 20:
        confidence_level = f"Moderate Evidence (N={populated})"
    else:
        confidence_level = f"Strong Evidence (N={populated})"
        
    last_updated_date = datetime.now().strftime('%Y-%m-%d')

    md.extend([
        "",
        "## Summary Metrics",
        "",
        "| Metric | Current |",
        "|--------|---------|",
        f"| Populated Cases | {populated} / {total_cases} |",
        f"| Pass Rate | {passed} / {populated} |",
        f"| Mean Percentile Rank | {mean_percentile:.1f} |",
        f"| Median Percentile Rank | {median_percentile:.1f} |",
        f"| Baseline Win Rate | {baseline_wins} / {populated} |",
        f"| Failure Count | {failed} |",
        f"| Pending Cases | {pending} |",
        f"| **Confidence Level** | {confidence_level} |",
        f"| **Last Updated** | {last_updated_date} |",
        "",
        "## Detailed Analysis (Populated Cases)",
        ""
    ])
    
    for r in results:
        if r["status"] != "PENDING_LITERATURE_REVIEW":
            md.extend([
                f"### {r['case_id']} ({r['domain']}, {r['time_window']})",
                f"- **Historical Winner:** {r['historical_winner']}",
                f"- **AIDP Rank:** {r['aidp_rank']} / {r['total_candidates']} ({r['aidp_percentile']:.1f}th Percentile)",
                f"- **Baseline Rank:** {r['baseline_rank']} / {r['total_candidates']} ({r['baseline_percentile']:.1f}th Percentile)",
            ])
            if r["status"] == "FAIL" and r.get("failure_analysis"):
                md.extend([
                    "> [!WARNING]",
                    "> **Failure Analysis:**",
                    f"> {r['failure_analysis']}"
                ])
            md.append("")
            
    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
        
    print(f"Generated dashboard at {DASHBOARD_PATH}")

if __name__ == "__main__":
    generate_dashboard()
