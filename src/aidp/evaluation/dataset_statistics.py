import json
from pathlib import Path

class DatasetStatistics:
    """
    Computes summary statistics for a DiscoveryBench dataset.
    """
    
    def __init__(self, data_path: str) -> None:
        self.data_path = Path(data_path)
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def generate_report(self) -> str:
        total_cases = len(self.data)
        
        domain_counts = {}
        difficulty_counts = {}
        total_evidence_sources = 0
        
        for case in self.data:
            domain = case.get("domain", "Unknown")
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
            
            diff = case.get("metadata", {}).get("difficulty", "unknown")
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
            
            total_evidence_sources += len(case.get("required_evidence_sources", []))
            
        md = f"# DiscoveryBench v1 Dataset Statistics\n\n"
        md += f"**Total Benchmark Cases**: {total_cases}\n"
        md += f"**Total Curated Evidence Sources**: {total_evidence_sources}\n"
        md += f"**Average Sources per Case**: {total_evidence_sources / max(1, total_cases):.1f}\n\n"
        
        md += "## Domain Distribution\n"
        for dom, count in sorted(domain_counts.items()):
            md += f"- **{dom}**: {count} cases ({(count/total_cases)*100:.1f}%)\n"
            
        md += "\n## Difficulty Estimates\n"
        for diff, count in sorted(difficulty_counts.items()):
            md += f"- **{diff.capitalize()}**: {count} cases ({(count/total_cases)*100:.1f}%)\n"
            
        return md


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    dataset_path = base_dir / "data" / "discovery_bench_v1.json"
    stats = DatasetStatistics(str(dataset_path))
    report = stats.generate_report()
    
    report_path = base_dir / "data" / "statistics.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(report)
    print(f"\nSaved statistics to {report_path}")
