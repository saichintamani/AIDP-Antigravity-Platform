import uuid
from dataclasses import dataclass, field
from enum import Enum


class GoalState(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    EVALUATING_EVIDENCE = "EVALUATING_EVIDENCE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class SubGoal:
    description: str
    state: GoalState = GoalState.PENDING
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class ResearchGoal:
    description: str
    subgoals: list[SubGoal] = field(default_factory=list)
    state: GoalState = GoalState.PENDING
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


class GoalManager:
    """
    Manages the state machine of a high-level research campaign.
    Goal -> Subgoals -> Experiments -> Evidence -> Update Goal -> Finish Goal
    """

    def __init__(self) -> None:
        self.active_goals: list[ResearchGoal] = []

    def add_goal(self, goal: ResearchGoal) -> None:
        self.active_goals.append(goal)

    def add_subgoal(self, goal_id: str, subgoal: SubGoal) -> None:
        goal = next((g for g in self.active_goals if g.id == goal_id), None)
        if goal:
            goal.subgoals.append(subgoal)
            if goal.state == GoalState.PENDING:
                goal.state = GoalState.IN_PROGRESS

    def update_subgoal_state(self, subgoal_id: str, new_state: GoalState) -> None:
        """Updates subgoal state and evaluates parent goal state."""
        for goal in self.active_goals:
            for sg in goal.subgoals:
                if sg.id == subgoal_id:
                    sg.state = new_state
                    self._evaluate_goal_state(goal)
                    return

    def _evaluate_goal_state(self, goal: ResearchGoal) -> None:
        """
        Determines if the overarching goal is complete based on subgoals.
        """
        if not goal.subgoals:
            return

        all_completed = all(sg.state == GoalState.COMPLETED for sg in goal.subgoals)
        any_failed = any(sg.state == GoalState.FAILED for sg in goal.subgoals)

        if any_failed:
            goal.state = GoalState.FAILED
        elif all_completed:
            goal.state = GoalState.COMPLETED
        else:
            goal.state = GoalState.IN_PROGRESS
