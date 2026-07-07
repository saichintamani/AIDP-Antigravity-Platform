from dataclasses import dataclass, field
from typing import Optional, Any
import datetime
import json
from pathlib import Path

@dataclass
class BenchmarkCase:
    """
    Ground-truth schema for a DiscoveryBench scientific test case.
    """
    id: str
    domain: str
    query: str
    historical_cutoff_date: datetime.date
    expected_findings: list[str]
    known_contradictions: list[str] = field(default_factory=list)
    required_evidence_sources: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

class DiscoveryBenchDataset:
    """
    Dataset for DiscoveryBench, loading from a curated JSON file of historical cases.
    """
    def __init__(self, data_path: Optional[str] = None) -> None:
        if not data_path:
            # Default path assuming script is run from project root or inside aidp
            base_dir = Path(__file__).parent
            data_path = str(base_dir / "data" / "discovery_bench_v1.json")
            
        self.cases: list[BenchmarkCase] = []
        self._load_dataset(data_path)

    def _load_dataset(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        for item in raw_data:
            dt_obj = datetime.datetime.strptime(item["historical_cutoff_date"], "%Y-%m-%d").date()
            case = BenchmarkCase(
                id=item["id"],
                domain=item["domain"],
                query=item["query"],
                historical_cutoff_date=dt_obj,
                expected_findings=item["expected_findings"],
                known_contradictions=item.get("known_contradictions", []),
                required_evidence_sources=item.get("required_evidence_sources", []),
                metadata=item.get("metadata", {})
            )
            self.cases.append(case)

    def get_cases(self) -> list[BenchmarkCase]:
        return self.cases

    def get_case_by_id(self, case_id: str) -> Optional[BenchmarkCase]:
        for case in self.cases:
            if case.id == case_id:
                return case
        return None
