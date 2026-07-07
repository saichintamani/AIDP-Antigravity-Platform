from aidp.cognitive_core.goal_manager import GoalManager, GoalState, ResearchGoal, SubGoal


def test_goal_manager_state_machine() -> None:
    manager = GoalManager()

    goal = ResearchGoal("Understand p53")
    manager.add_goal(goal)

    sg1 = SubGoal("Read papers")
    sg2 = SubGoal("Run experiment")

    manager.add_subgoal(goal.id, sg1)
    manager.add_subgoal(goal.id, sg2)

    assert goal.state == GoalState.IN_PROGRESS

    manager.update_subgoal_state(sg1.id, GoalState.COMPLETED)
    assert goal.state == GoalState.IN_PROGRESS

    manager.update_subgoal_state(sg2.id, GoalState.FAILED)
    assert goal.state == GoalState.FAILED

    manager.update_subgoal_state(sg2.id, GoalState.COMPLETED)
    assert goal.state == GoalState.COMPLETED
