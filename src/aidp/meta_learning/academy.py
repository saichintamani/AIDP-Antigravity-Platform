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
        Runs a simulated trial. The agent must demonstrate minimum competence
        (skill level > 0.3) to pass. Failed agents must accumulate more
        experience before being re-certified.
        """
        current_skill = self.skill_graph.get_skill_level(agent_id, skill)
        
        # Agent must have minimum skill level to pass certification
        passed_trial = current_skill > 0.3

        if passed_trial:
            self.skill_graph.update_skill(agent_id, skill, 0.15)  # Reward for passing
            self.certified_agents.add(agent_id)
            return True
        return False
        
    def penalize_agent_for_failure(self, agent_id: str, failure_type: str, penalty: float = 0.2) -> None:
        """
        Triggered when FormalVerification or Debate rejects an agent's protocol.
        Decreases their skill graph and revokes certification.
        """
        current_skill = self.skill_graph.get_skill_level(agent_id, failure_type)
        new_skill = max(0.0, current_skill - penalty)
        self.skill_graph.update_skill(agent_id, failure_type, new_skill)
        
        if agent_id in self.certified_agents:
            self.certified_agents.remove(agent_id)
            
        print(f"Meta-Learning Academy: Agent {agent_id} penalized {penalty} for {failure_type}. Certification revoked.")
