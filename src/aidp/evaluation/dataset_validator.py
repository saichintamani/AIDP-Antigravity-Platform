import json
from datetime import datetime
from pathlib import Path


class DatasetValidator:
    """
    Validates a DiscoveryBench dataset JSON file.
    """
    
    def __init__(self, data_path: str) -> None:
        self.data_path = Path(data_path)
        with open(self.data_path, encoding="utf-8") as f:
            self.data = json.load(f)
            
    def run_validation(self) -> bool:
        print(f"Validating dataset at: {self.data_path}")
        all_passed = True
        
        all_passed &= self.check_schema()
        all_passed &= self.check_duplicates()
        all_passed &= self.check_historical_consistency()
        all_passed &= self.check_provenance()
        
        if all_passed:
            print("All validation checks passed!")
        else:
            print("Validation failed. Check the logs above.")
            
        return all_passed

    def check_schema(self) -> bool:
        required_keys = ["id", "domain", "query", "historical_cutoff_date", "expected_findings", "required_evidence_sources"]
        passed = True
        for idx, case in enumerate(self.data):
            for key in required_keys:
                if key not in case:
                    print(f"[Schema Error] Case index {idx} missing required key: {key}")
                    passed = False
        return passed

    def check_duplicates(self) -> bool:
        ids = set()
        queries = set()
        passed = True
        for case in self.data:
            case_id = case.get("id")
            query = case.get("query")
            
            if case_id in ids:
                print(f"[Duplicate Error] Duplicate ID found: {case_id}")
                passed = False
            ids.add(case_id)
            
            if query in queries:
                print(f"[Duplicate Error] Duplicate query found: {query}")
                passed = False
            queries.add(query)
            
        return passed

    def check_historical_consistency(self) -> bool:
        passed = True
        for case in self.data:
            cutoff_str = case.get("historical_cutoff_date")
            if not cutoff_str:
                continue
                
            try:
                dt = datetime.strptime(cutoff_str, "%Y-%m-%d")
                if dt.year < 1950 or dt.year > 2025:
                    print(f"[Historical Error] Cutoff date out of realistic bounds for case {case.get('id')}: {cutoff_str}")
                    passed = False
            except ValueError:
                print(f"[Historical Error] Invalid date format for case {case.get('id')}: {cutoff_str}")
                passed = False
        return passed

    def check_provenance(self) -> bool:
        passed = True
        for case in self.data:
            sources = case.get("required_evidence_sources", [])
            if not sources:
                print(f"[Provenance Error] Case {case.get('id')} has no required evidence sources.")
                passed = False
                continue
                
            for source in sources:
                # E.g. "PMID:12345" or "DOI:10.123/456"
                if not source.startswith("PMID:") and not source.startswith("DOI:"):
                    print(f"[Provenance Error] Case {case.get('id')} has improperly formatted source (must be PMID: or DOI:): {source}")
                    passed = False
        return passed


if __name__ == "__main__":
    import sys
    base_dir = Path(__file__).parent
    dataset_path = base_dir / "data" / "discovery_bench_v1.json"
    validator = DatasetValidator(str(dataset_path))
    if not validator.run_validation():
        sys.exit(1)
