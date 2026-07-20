"""
Multi-Domain Scaled Runner (R3 Compartment 2)
=============================================
Orchestrates the execution of the Generative Engine across all 10 historical cases.
Implements timeouts, retries, constraint validation, and multi-dimensional rubric scoring.
"""
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any

from aidp.evaluation.constraint_engine import ConstraintValidator
from aidp.evaluation.generative_harness import GenerativeHarness
from aidp.evaluation.rubric_judge import RubricJudge
from tests.evaluation.datasets.historical_cases import ALL_CASES


class ScaledDiscoveryRunner:
    """Orchestrates generation and evaluation across multiple domains."""

    def __init__(self, use_mock: bool = False, gateway=None):
        self.use_mock = use_mock
        self.gateway = gateway
        self.harness = GenerativeHarness()
        self.constraint_validator = ConstraintValidator(gateway=gateway)
        self.rubric_judge = RubricJudge(gateway=gateway if not use_mock else None)

    def run_single_case(self, case) -> Dict[str, Any]:
        """Runs the full R3 pipeline on a single case."""
        start_time = time.time()
        
        # 1. Generation
        result = self.harness.generate_hypothesis(case)
        generation_time = time.time() - start_time
        
        if result["status"] != "success":
            return {
                "case_id": case.case_id,
                "domain": case.domain,
                "status": "failed",
                "error": result.get("error_message"),
                "runtime_sec": round(generation_time, 2)
            }
            
        hypothesis = result["generated_hypothesis"]
        
        # 2. Constraint Validation (C1)
        constraints = getattr(case, 'constraints', [])
        constraint_report = self.constraint_validator.validate(hypothesis, constraints)
        
        # 3. Rubric Judge (A1)
        evidence_text = "\n".join([e.extracted_text for e in case.known_evidence])
        verdict = self.rubric_judge.evaluate(
            hypothesis_text=hypothesis,
            historical_winner=case.historical_winner,
            constraints=constraints,
            evidence_summary=evidence_text
        )
        
        # Override constraint compliance score with deterministic constraint engine if failed
        if not constraint_report.is_fully_compliant:
            verdict.constraint_compliance = constraint_report.compliance_score
            if verdict.is_match:
                verdict.is_match = False
                verdict.failure_mode = "CONSTRAINT_VIOLATION"
                verdict.reasoning += " (Overridden: Deterministic constraint engine found violations)"

        return {
            "case_id": case.case_id,
            "domain": case.domain,
            "status": "success",
            "runtime_sec": round(time.time() - start_time, 2),
            "generation_stats": {
                "retries": 0
            },
            "hypothesis": hypothesis,
            "constraints_report": constraint_report.model_dump(),
            "judge_verdict": verdict.model_dump(),
            "aidp_rank": 1 if verdict.is_match else 4
        }

    def run_all(self, max_workers: int = 2, output_path: str = None) -> list[Dict[str, Any]]:
        """Runs all cases and aggregates results."""
        results = []
        print(f"Starting Scaled Discovery Runner on {len(ALL_CASES)} cases...")
        
        # Sequential if mock to avoid console log overlap, parallel if live
        if self.use_mock:
            for case in ALL_CASES:
                print(f"  Running {case.case_id}...")
                results.append(self.run_single_case(case))
        else:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_case = {executor.submit(self.run_single_case, case): case for case in ALL_CASES}
                for future in as_completed(future_to_case):
                    case = future_to_case[future]
                    try:
                        res = future.result()
                        results.append(res)
                        print(f"  Completed {case.case_id}: {res['status']}")
                    except Exception as e:
                        print(f"  Failed {case.case_id} with exception: {e}")
                        results.append({"case_id": case.case_id, "status": "exception", "error": str(e)})

        # Save to JSON
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            print(f"\nSaved R3 Scaled Results to {output_path}")
            
        return results
