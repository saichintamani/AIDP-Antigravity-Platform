"""
Confidence Calibration Analyzer (R3 Compartment 5)
==================================================
Calculates Expected Calibration Error (ECE) to determine if the engine's 
internal confidence scores align with its actual correctness.
"""
from typing import Dict, List, Any


class CalibrationAnalyzer:
    def analyze(self, scaled_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates a simplified ECE (Expected Calibration Error).
        """
        # In this mock, we assume the engine outputs a 'confidence' score 
        # (or we proxy it using the overall rubric score if confidence isn't explicit)
        
        bins = {
            "0.0-0.2": {"count": 0, "correct": 0, "conf_sum": 0.0},
            "0.2-0.4": {"count": 0, "correct": 0, "conf_sum": 0.0},
            "0.4-0.6": {"count": 0, "correct": 0, "conf_sum": 0.0},
            "0.6-0.8": {"count": 0, "correct": 0, "conf_sum": 0.0},
            "0.8-1.0": {"count": 0, "correct": 0, "conf_sum": 0.0},
        }
        
        valid_results = [r for r in scaled_results if r.get("status") == "success" and "judge_verdict" in r]
        
        for res in valid_results:
            verdict = res["judge_verdict"]
            # Proxy confidence via overall_score if engine confidence isn't explicitly passed
            conf = verdict.get("overall_score", 0.5) 
            is_correct = 1 if verdict.get("is_match", False) else 0
            
            if conf <= 0.2: b = "0.0-0.2"
            elif conf <= 0.4: b = "0.2-0.4"
            elif conf <= 0.6: b = "0.4-0.6"
            elif conf <= 0.8: b = "0.6-0.8"
            else: b = "0.8-1.0"
            
            bins[b]["count"] += 1
            bins[b]["correct"] += is_correct
            bins[b]["conf_sum"] += conf

        ece = 0.0
        total = len(valid_results)
        
        bin_stats = {}
        if total > 0:
            for b_name, b_data in bins.items():
                if b_data["count"] > 0:
                    acc = b_data["correct"] / b_data["count"]
                    avg_conf = b_data["conf_sum"] / b_data["count"]
                    weight = b_data["count"] / total
                    ece += weight * abs(acc - avg_conf)
                    
                    bin_stats[b_name] = {
                        "accuracy": acc,
                        "avg_confidence": avg_conf,
                        "samples": b_data["count"]
                    }

        return {
            "expected_calibration_error": round(ece, 4),
            "is_well_calibrated": ece < 0.15,
            "bin_statistics": bin_stats
        }
