import os
import shutil

import pytest

from aidp.knowledge.memory import FailedHypothesis, PersistentScientificMemory, ScientificInsight


@pytest.fixture
def clean_memory():
    if os.path.exists(".test_memory"):
        shutil.rmtree(".test_memory")
    yield ".test_memory"
    if os.path.exists(".test_memory"):
        shutil.rmtree(".test_memory")


def test_persistent_scientific_memory(clean_memory) -> None:
    memory = PersistentScientificMemory(storage_path=clean_memory)

    insight = ScientificInsight(
        description="X requires catalyst Y.", confidence=0.85, context="Inferred from simulation Z."
    )

    memory.record_insight(insight)

    # Verify retrieval
    loaded = memory.get_all_insights()
    assert len(loaded) == 1
    assert loaded[0].description == "X requires catalyst Y."


def test_persistent_scientific_memory_failed_hypothesis(clean_memory) -> None:
    memory = PersistentScientificMemory(storage_path=clean_memory)

    fh = FailedHypothesis(
        claim="A causes B", failure_reason="Falsified by control group.", workflow_id="wf_123"
    )

    memory.record_failed_hypothesis(fh)

    assert os.path.exists(memory.failed_hypotheses_file)
