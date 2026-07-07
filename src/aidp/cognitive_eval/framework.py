from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from aidp.cognitive_eval.evaluator import CognitiveEvaluator


@dataclass
class CognitiveTestCase:
    id: str
    input_facts: list[str]
    expected_hypothesis: str
    # A lambda or function to validate the generated trace against the expected hypothesis
    validation_fn: Callable[[Any, str], bool]


class CognitiveUnitTestSuite:
    """
    Framework for executing Cognitive Unit Tests.
    Unlike software unit tests (which assert code paths), these assert reasoning paths.
    """

    def __init__(self) -> None:
        self.evaluator = CognitiveEvaluator()
        self.cases: list[CognitiveTestCase] = []

    def add_case(self, case: CognitiveTestCase) -> None:
        self.cases.append(case)

    def run_suite(self, reasoning_engine_mock: Callable[[list[str]], Any]) -> bool:
        """
        Executes the suite of cognitive tests.
        Returns True if all pass, False otherwise.
        """
        all_passed = True
        for case in self.cases:
            print(f"Running Cognitive Test: {case.id}")
            # Generate the trace using the engine
            trace = reasoning_engine_mock(case.input_facts)

            # Run the architectural scorecard
            scorecard = self.evaluator.evaluate_trace(trace.steps, trace.finalDecision)

            if not scorecard.passed:
                print(f"  [FAIL] Architectural constraints violated: {scorecard}")
                all_passed = False
                continue

            # Run the case-specific validation (e.g. did it reach the expected hypothesis?)
            passed = case.validation_fn(trace, case.expected_hypothesis)
            if passed:
                print("  [PASS]")
            else:
                print("  [FAIL] Logic diverged from expected hypothesis.")
                all_passed = False

        return all_passed
