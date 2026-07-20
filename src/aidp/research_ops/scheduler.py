import heapq
from typing import Any

from aidp.research_ops.economics_engine import ScientificTaskProposal


class IntelligentScheduler:
    """
    Dependency-aware priority queue for laboratory execution.
    Replaces naive FIFO execution.
    """

    def __init__(self) -> None:
        # Min-heap in Python, so we store negative priority for Max-heap behavior
        self.priority_queue: list[Any] = []
        self.dependencies: dict[str, list[str]] = {}
        self.completed_tasks: set[str] = set()

    def enqueue(
        self, task: ScientificTaskProposal, priority_score: float, depends_on: list[str] | None = None
    ) -> None:
        """Adds a task to the queue with its calculated economics priority."""
        if depends_on:
            self.dependencies[task.id] = depends_on

        # heapq uses first element for sorting
        heapq.heappush(self.priority_queue, (-priority_score, task))

    def get_next_runnable_task(self) -> ScientificTaskProposal | None:
        """Pops the highest priority task whose dependencies are satisfied."""
        temp_list = []
        next_task = None

        while self.priority_queue:
            priority, task = heapq.heappop(self.priority_queue)

            # Check dependencies
            deps = self.dependencies.get(task.id, [])
            if all(d in self.completed_tasks for d in deps):
                next_task = task
                break
            else:
                # Dependencies not met, hold it aside
                temp_list.append((priority, task))

        # Put back tasks that couldn't run
        for item in temp_list:
            heapq.heappush(self.priority_queue, item)

        return next_task

    def mark_completed(self, task_id: str) -> None:
        self.completed_tasks.add(task_id)
