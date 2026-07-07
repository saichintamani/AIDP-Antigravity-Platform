from aidp.intelligence.agent import BaseAgent
from aidp.intelligence.agents.personas import (
    EthicsOfficerAgent,
    ExperimentalScientistAgent,
    HypothesisScientistAgent,
    LiteratureScientistAgent,
    MethodologistAgent,
    ReviewerAgent,
    StatisticianAgent,
)
from aidp.intelligence.protocol import ScientificMessage
from aidp.intelligence.providers.base import BaseProvider


class ScientificTeam:
    """
    A collection of specialized agents that work together on a specific phase of the research cycle.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.members: dict[str, BaseAgent] = {}

    def add_member(self, role: str, agent: BaseAgent) -> None:
        self.members[role] = agent

    def process_message(self, message: ScientificMessage) -> ScientificMessage:
        """
        Processes a message by delegating to the appropriate team member.
        In a real implementation, this might trigger a local debate among team members.
        """
        # Simplistic routing to the first member for demonstration
        # A real team would have internal routing logic
        if not self.members:
            raise RuntimeError(f"Team {self.name} has no members.")

        role, agent = list(self.members.items())[0]

        # Team does its work (mocked perception here)
        result_text = agent.perceive(str(message.payload))

        # Return a response message
        return ScientificMessage(
            sender=self.name,
            receiver=message.sender,
            goal=message.goal,
            required_action="review_team_output",
            payload={"result": result_text},
            evidence_ids=message.evidence_ids,
            confidence=0.8,
            uncertainty=0.2,
        )


class ChiefScientistAI:
    """
    The central coordinator of the Autonomous Scientific Organization.
    Routes structured ScientificMessages between Specialized Teams.
    """

    def __init__(self, provider: BaseProvider) -> None:
        self.provider = provider
        self.teams: dict[str, ScientificTeam] = {}

        self._initialize_organization()

    def _initialize_organization(self) -> None:
        # 1. Literature Team
        lit_team = ScientificTeam("LiteratureTeam")
        lit_team.add_member("LiteratureScientist", LiteratureScientistAgent(self.provider))
        self.teams["LiteratureTeam"] = lit_team

        # 2. Hypothesis Team
        hyp_team = ScientificTeam("HypothesisTeam")
        hyp_team.add_member("HypothesisScientist", HypothesisScientistAgent(self.provider))
        self.teams["HypothesisTeam"] = hyp_team

        # 3. Experiment Team
        exp_team = ScientificTeam("ExperimentTeam")
        exp_team.add_member("ExperimentalScientist", ExperimentalScientistAgent(self.provider))
        self.teams["ExperimentTeam"] = exp_team

        # 4. Peer Review Team (Contains multiple critics)
        review_team = ScientificTeam("PeerReviewTeam")
        review_team.add_member("Statistician", StatisticianAgent(self.provider))
        review_team.add_member("Methodologist", MethodologistAgent(self.provider))
        review_team.add_member("Reviewer", ReviewerAgent(self.provider))
        review_team.add_member("EthicsOfficer", EthicsOfficerAgent(self.provider))
        self.teams["PeerReviewTeam"] = review_team

    def route_message(self, message: ScientificMessage) -> ScientificMessage:
        """
        Routes a ScientificMessage to the target team and returns their response.
        """
        message.validate()

        target_team = self.teams.get(message.receiver)
        if not target_team:
            raise ValueError(f"Unknown receiver team: {message.receiver}")

        return target_team.process_message(message)
