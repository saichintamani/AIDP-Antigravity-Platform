from aidp.intelligence.agent import BaseAgent


class PrincipalInvestigatorAgent(BaseAgent):
    """Sets research agenda, prioritizes goals, allocates resources."""

    def perceive(self, payload: str) -> str:
        return f"[System: You are the Principal Investigator.] Evaluate these hypotheses and prioritize based on impact.\nData: {payload}"


class LiteratureScientistAgent(BaseAgent):
    """Reads new papers, updates world model."""

    def perceive(self, payload: str) -> str:
        return f"[System: You are the Literature Scientist.] Extract structured claims from this text.\nData: {payload}"


class HypothesisScientistAgent(BaseAgent):
    """Generates new hypotheses."""

    def perceive(self, payload: str) -> str:
        return f"[System: You are the Hypothesis Scientist.] Generate novel hypotheses based on these world model gaps.\nData: {payload}"


class ExperimentalScientistAgent(BaseAgent):
    """Designs experiments."""

    def perceive(self, payload: str) -> str:
        return f"[System: You are the Experimental Scientist.] Design a robust experimental protocol to test this hypothesis.\nData: {payload}"


class StatisticianAgent(BaseAgent):
    """Validates methodology and statistical power."""

    def perceive(self, payload: str) -> str:
        return f"[System: You are the Statistician.] Evaluate the statistical rigor and power of this proposed experiment.\nData: {payload}"


class MethodologistAgent(BaseAgent):
    """Reviews experimental rigor."""

    def perceive(self, payload: str) -> str:
        return f"[System: You are the Methodologist.] Scrutinize this experimental design for confounds and biases.\nData: {payload}"


class ReviewerAgent(BaseAgent):
    """Challenges conclusions."""

    def perceive(self, payload: str) -> str:
        return f"[System: You are the Peer Reviewer.] Play the adversarial role and challenge these conclusions.\nData: {payload}"


class EthicsOfficerAgent(BaseAgent):
    """Flags ethical issues."""

    def perceive(self, payload: str) -> str:
        return f"[System: You are the Ethics Officer.] Review this protocol for dual-use concerns or ethical violations.\nData: {payload}"


class ResourcePlannerAgent(BaseAgent):
    """Estimates time and cost."""

    def perceive(self, payload: str) -> str:
        return f"[System: You are the Resource Planner.] Estimate the computational and laboratory costs for this campaign.\nData: {payload}"


class PublicationScientistAgent(BaseAgent):
    """Drafts reports and papers."""

    def perceive(self, payload: str) -> str:
        return f"[System: You are the Publication Scientist.] Synthesize these findings into an academic manuscript section.\nData: {payload}"
