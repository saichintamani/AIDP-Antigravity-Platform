

class ScientificSkillGraph:
    """
    Tracks measurable proficiency for agents across multiple domains (E4).
    """

    def __init__(self) -> None:
        # Maps agent_id to a dict of skills and scores (0.0 to 1.0)
        self.agent_skills: dict[str, dict[str, float]] = {}

    def initialize_agent(self, agent_id: str) -> None:
        if agent_id not in self.agent_skills:
            self.agent_skills[agent_id] = {
                "statistics": 0.5,
                "causal_reasoning": 0.5,
                "experimental_design": 0.5,
            }

    def update_skill(self, agent_id: str, skill: str, delta: float) -> None:
        # Auto-initialize agent if not tracked yet
        if agent_id not in self.agent_skills:
            self.initialize_agent(agent_id)
        # Auto-initialize skill dimension if not tracked yet
        if skill not in self.agent_skills[agent_id]:
            self.agent_skills[agent_id][skill] = 0.5  # default baseline
        current = self.agent_skills[agent_id][skill]
        self.agent_skills[agent_id][skill] = min(max(current + delta, 0.0), 1.0)

    def get_skill_level(self, agent_id: str, skill: str) -> float:
        return self.agent_skills.get(agent_id, {}).get(skill, 0.0)
