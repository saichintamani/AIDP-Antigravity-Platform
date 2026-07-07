from typing import Any


class ExperimentReviser:
    """
    Autonomously modifies weak variables in an experiment if its Discovery Value
    is too low or its Risk is too high.
    """

    def revise(self, experiment_design: dict[str, Any], feedback: str) -> dict[str, Any]:
        """
        Takes an existing design and applies a modification to improve it.
        """
        # Mocking LLM revision
        revised_design = experiment_design.copy()

        # Example heuristic: if power was missing or low, increase it.
        if revised_design.get("power", 0.0) < 0.8:
            revised_design["power"] = 0.9
            revised_design["revision_notes"] = (
                f"Increased statistical power based on feedback: {feedback}"
            )

        return revised_design
