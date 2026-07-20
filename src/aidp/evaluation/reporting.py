import csv
import json
from typing import Any


class EvaluationReportGenerator:
    """
    Generates structured reports from benchmark results.
    """

    def __init__(self, results: dict[str, Any]) -> None:
        self.results = results

    def to_json(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)

    def to_csv(self, filepath: str) -> None:
        if not self.results:
            return
            
        # Get all metric keys from the first baseline's aggregate
        first_baseline = list(self.results.keys())[0]
        metric_keys = list(self.results[first_baseline]["aggregate"].keys())
        
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Baseline"] + metric_keys)
            
            for baseline, data in self.results.items():
                row = [baseline]
                for key in metric_keys:
                    row.append(data["aggregate"].get(key, 0.0))
                writer.writerow(row)

    def to_markdown(self, filepath: str) -> None:
        md = "# Scientific Evaluation Report\n\n"
        md += "## Aggregate Performance\n\n"
        
        first_baseline = list(self.results.keys())[0]
        metric_keys = list(self.results[first_baseline]["aggregate"].keys())
        
        md += "| Baseline | " + " | ".join(metric_keys) + " |\n"
        md += "|----------|" + "|".join(["---" for _ in metric_keys]) + "|\n"
        
        for baseline, data in self.results.items():
            row = f"| **{baseline}** | "
            for key in metric_keys:
                val = data["aggregate"].get(key, 0.0)
                row += f"{val:.4f} | "
            md += row + "\n"
            
        md += "\n## Detailed Case Breakdown\n\n"
        for baseline, data in self.results.items():
            md += f"### {baseline}\n"
            for case in data["cases"]:
                md += f"- **{case['case_id']}**: Correctness={case['metrics']['scientific_correctness']:.2f}, Hallucination={case['metrics']['hallucination_rate']:.2f}\n"
            md += "\n"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
            
    def to_whitepaper_table(self, filepath: str) -> None:
        # LaTeX style or similar
        self.to_markdown(filepath) # For now, markdown is standard
