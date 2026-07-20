import logging

logger = logging.getLogger(__name__)

class LeakageThreatMath:
    """
    Statistically calculates the dataset contamination ratio across
    the entire benchmark.
    """
    
    @staticmethod
    def calculate_dataset_integrity(contamination_results: list[dict]) -> dict:
        total_samples = len(contamination_results)
        if total_samples == 0:
            return {"contamination_ratio": 0.0, "integrity_score": 0.0, "verdict": "No Data"}
            
        contaminated_samples = sum(1 for res in contamination_results if res["is_contaminated"])
        
        contamination_ratio = contaminated_samples / total_samples
        integrity_score = 1.0 - contamination_ratio
        
        if contamination_ratio == 0.0:
            verdict = "100% Mathematically Pure (Flagship Standard)"
        elif contamination_ratio < 0.01:
            verdict = "Acceptable (<1% Contamination)"
        elif contamination_ratio < 0.05:
            verdict = "Warning (5% Contamination Leak)"
        else:
            verdict = "FATAL: Dataset is Memorized (Corrupted Benchmark)"
            
        return {
            "total_samples_scanned": total_samples,
            "contaminated_samples_found": contaminated_samples,
            "contamination_ratio": float(contamination_ratio),
            "integrity_score": float(integrity_score),
            "verdict": verdict
        }
