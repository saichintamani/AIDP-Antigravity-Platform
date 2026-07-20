import json
import os
from datetime import datetime


def generate_report():
    raw_path = os.path.join("tests", "evaluation", "results", "historical_benchmarks", "latest_raw_results.json")
    
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} not found. Run pytest tests/evaluation/track_b/test_historical_suite.py first.")
        return
        
    with open(raw_path) as f:
        results = json.load(f)
        
    report_lines = [
        "# Historical Replay Benchmark Report",
        f"Generated: {datetime.now().isoformat()}",
        "---"
    ]
    
    for res in results:
        report_lines.append(f"## Case: {res['case_id']}")
        report_lines.append(f"**Domain:** {res['domain']}")
        
        if res['status'] == "PENDING_LITERATURE_REVIEW":
            report_lines.append("**Result:** PENDING (Awaiting Literature Population)\n")
            continue
            
        report_lines.append(f"**Cutoff Date:** {res['time_window']}")
        report_lines.append(f"**Number of Candidate Experiments:** {res['total_candidates']}")
        report_lines.append(f"**Historical Breakthrough Experiment:** {res['historical_winner']}")
        report_lines.append("")
        report_lines.append("### Metrics")
        report_lines.append(f"- **AIDP Rank:** {res['aidp_rank']} ({res['aidp_percentile']:.1f}%)")
        report_lines.append(f"- **Baseline Rank:** {res['baseline_rank']} ({res['baseline_percentile']:.1f}%)")
        report_lines.append(f"- **Outperforms Baseline:** {res.get('outperforms_baseline', False)}")
        report_lines.append("")
        report_lines.append(f"**Result:** {res['status']}")
        
        if res['status'] == "FAIL" and res.get('failure_analysis'):
            report_lines.append("")
            report_lines.append("### Failure Analysis")
            report_lines.append(f"> {res['failure_analysis']}")
            
        report_lines.append("\n---")
        
    out_dir = os.path.join("tests", "evaluation", "results", "historical_benchmarks")
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    out_path = os.path.join(out_dir, filename)
    
    with open(out_path, "w") as f:
        f.write("\n".join(report_lines))
        
    print(f"Generated Benchmark Report: {out_path}")

if __name__ == "__main__":
    generate_report()
