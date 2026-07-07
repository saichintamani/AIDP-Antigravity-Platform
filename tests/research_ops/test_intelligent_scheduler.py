from aidp.research_ops.economics_engine import ScientificTaskProposal
from aidp.research_ops.scheduler import IntelligentScheduler


def test_intelligent_scheduler() -> None:
    scheduler = IntelligentScheduler()

    task_a = ScientificTaskProposal("A", "Dep", 1, 1, 1, 1, 1, 0.1)
    task_b = ScientificTaskProposal("B", "Target", 1, 1, 1, 1, 1, 0.1)

    # Enqueue B which depends on A
    scheduler.enqueue(task_b, priority_score=100.0, depends_on=["A"])
    # Enqueue A with lower priority
    scheduler.enqueue(task_a, priority_score=10.0)

    # The highest priority is B, but its dependency A is not met.
    # So A should run first.
    first_task = scheduler.get_next_runnable_task()
    assert first_task.id == "A"

    # Mark A completed
    scheduler.mark_completed("A")

    # Now B should be runnable
    second_task = scheduler.get_next_runnable_task()
    assert second_task.id == "B"

    # Queue is empty
    assert scheduler.get_next_runnable_task() is None
