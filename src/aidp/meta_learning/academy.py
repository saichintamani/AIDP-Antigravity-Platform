from aidp.meta_learning.skill_graph import ScientificSkillGraph


class AutonomousResearchAcademy:
    """
    Tests and certifies new agents, or agents with low skill scores,
    via simulated trials before they can be scheduled for live experiments (E7, E10).
    """

    def __init__(self, skill_graph: ScientificSkillGraph) -> None:
        self.skill_graph = skill_graph
        self.certified_agents: set[str] = set()

    def requires_certification(
        self, agent_id: str, required_skill: str, threshold: float = 0.8
    ) -> bool:
        if agent_id in self.certified_agents:
            return False

        current_skill = self.skill_graph.get_skill_level(agent_id, required_skill)
        return current_skill < threshold

    def run_certification_trial(self, agent_id: str, skill: str) -> bool:
        """
        Runs a mock trial. If the agent passes, their skill goes up.
        """
        # Mocking the LLM trial evaluation
        passed_trial = True

        if passed_trial:
            self.skill_graph.update_skill(agent_id, skill, 0.3)
            self.certified_agents.add(agent_id)
            return True
        return False
