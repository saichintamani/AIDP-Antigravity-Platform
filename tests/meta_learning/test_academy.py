from aidp.meta_learning.academy import AutonomousResearchAcademy
from aidp.meta_learning.skill_graph import ScientificSkillGraph


def test_academy_certification() -> None:
    graph = ScientificSkillGraph()
    graph.initialize_agent("agent_123")

    academy = AutonomousResearchAcademy(graph)

    # Needs certification because default skill is 0.5 < 0.8
    assert academy.requires_certification("agent_123", "statistics")

    # Run trial
    passed = academy.run_certification_trial("agent_123", "statistics")
    assert passed

    # After passing, should no longer require certification
    assert not academy.requires_certification("agent_123", "statistics")

    # Skill level should have increased
    assert graph.get_skill_level("agent_123", "statistics") == 0.8
