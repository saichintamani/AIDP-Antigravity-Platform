"""
R3 Final Report Generator (R3 Compartment 6)
============================================
Aggregates outputs from the Scaled Runner and analyzers (Transfer, Genomics, Calibration)
into a structured final report JSON that can be consumed by the UI dashboard.
"""
import json
import os
from typing import Dict, Any

from aidp.evaluation.calibration_analyzer import CalibrationAnalyzer
from aidp.evaluation.failure_genomics import FailureGenomics
from aidp.evaluation.transfer_analyzer import TransferAnalyzer


class R3ReportGenerator:
    def __init__(self):
        self.transfer_analyzer = TransferAnalyzer()
        self.failure_genomics = FailureGenomics()
        self.calibration_analyzer = CalibrationAnalyzer()

    def generate(self, scaled_results_path: str, output_report_path: str = None) -> Dict[str, Any]:
        """Reads scaled results and generates the final R3 multi-compartment report."""
        if not os.path.exists(scaled_results_path):
            return {"error": f"Results file not found: {scaled_results_path}"}
            
        with open(scaled_results_path, 'r', encoding='utf-8') as f:
            results = json.load(f)

        # Basic Stats
        total_cases = len(results)
        successes = len([r for r in results if r.get("status") == "success" and r.get("judge_verdict", {}).get("is_match", False)])
        accuracy = successes / total_cases if total_cases > 0 else 0.0
        
        # Dimensions Avg
        rubric_sums = {
            "scientific_grounding": 0.0,
            "mechanistic_accuracy": 0.0,
            "testability": 0.0,
            "novelty": 0.0,
            "constraint_compliance": 0.0,
            "overall_score": 0.0
        }
        
        valid_results = [r for r in results if r.get("status") == "success" and "judge_verdict" in r]
        v_count = len(valid_results)
        
        if v_count > 0:
            for r in valid_results:
                v = r["judge_verdict"]
                for k in rubric_sums:
                    rubric_sums[k] += v.get(k, 0.0)
            
            for k in rubric_sums:
                rubric_sums[k] /= v_count

        # Run Analyzers
        transfer_report = self.transfer_analyzer.analyze(results)
        genomics_report = self.failure_genomics.analyze(results)
        calibration_report = self.calibration_analyzer.analyze(results)

        report = {
            "meta": {
                "phase": "R3 Scaled Generative Discovery",
                "total_cases_evaluated": total_cases
            },
            "aggregate_metrics": {
                "top1_accuracy": round(accuracy * 100, 2),
                "average_rubric_scores": {k: round(v, 3) for k, v in rubric_sums.items()}
            },
            "failure_genomics": genomics_report,
            "confidence_calibration": calibration_report,
            "cross_domain_transfer": transfer_report,
            "raw_results_path": scaled_results_path
        }
        
        if output_report_path:
            os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
            with open(output_report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            print(f"R3 Final Report saved to {output_report_path}")

        return report

if __name__ == "__main__":
    generator = R3ReportGenerator()
    results_path = os.path.join(os.path.dirname(__file__), '../../../tests/evaluation/results/test_r3_scaled_mock.json')
    report_path = os.path.join(os.path.dirname(__file__), '../../../tests/evaluation/results/r3_final_report.json')
    
    if os.path.exists(results_path):
        generator.generate(results_path, report_path)
    else:
        print("Mock results not found. Run test_r3_scaled.py first.")
