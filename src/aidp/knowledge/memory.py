import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ScientificInsight:
    """A generalized rule or observation learned from past workflows."""

    description: str
    confidence: float
    context: str
    id: str = field(default_factory=lambda: f"ins_{uuid.uuid4()}")


@dataclass
class FailedHypothesis:
    """Records a hypothesis that failed validation or experimentation."""

    claim: str
    failure_reason: str
    workflow_id: str
    id: str = field(default_factory=lambda: f"fh_{uuid.uuid4()}")


@dataclass
class RejectedExperiment:
    """Records an experimental design that was rejected by the Debate Engine."""

    design_summary: str
    rejection_reason: str
    reviewer_role: str
    workflow_id: str
    id: str = field(default_factory=lambda: f"re_{uuid.uuid4()}")


class PersistentScientificMemory:
    """
    Cumulative memory storing failed/successful hypotheses, rejected experiments,
    and scientific insights. Operates orthogonally to the World Model to store
    'experience' rather than facts.
    """

    def __init__(self, storage_path: str = ".memory") -> None:
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        self.insights_file = os.path.join(self.storage_path, "insights.jsonl")
        self.failed_hypotheses_file = os.path.join(self.storage_path, "failed_hypotheses.jsonl")
        self.rejected_experiments_file = os.path.join(
            self.storage_path, "rejected_experiments.jsonl"
        )

    def _append_to_file(self, filepath: str, data: dict[str, Any]) -> None:
        with open(filepath, "a") as f:
            f.write(json.dumps(data) + "\n")

    def record_insight(self, insight: ScientificInsight) -> None:
        self._append_to_file(self.insights_file, asdict(insight))

    def record_failed_hypothesis(self, fh: FailedHypothesis) -> None:
        self._append_to_file(self.failed_hypotheses_file, asdict(fh))

    def record_rejected_experiment(self, re: RejectedExperiment) -> None:
        self._append_to_file(self.rejected_experiments_file, asdict(re))

    def get_all_insights(self) -> list[ScientificInsight]:
        insights = []
        if os.path.exists(self.insights_file):
            with open(self.insights_file) as f:
                for line in f:
                    insights.append(ScientificInsight(**json.loads(line)))
        return insights
