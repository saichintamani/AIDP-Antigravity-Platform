import uuid
from typing import Any

from aidp.intelligence.agents.personas import (
    EthicsOfficerAgent,
    ExperimentalScientistAgent,
    HypothesisScientistAgent,
    LiteratureScientistAgent,
    MethodologistAgent,
    PrincipalInvestigatorAgent,
    PublicationScientistAgent,
    ResourcePlannerAgent,
    ReviewerAgent,
    StatisticianAgent,
)
from aidp.intelligence.providers.base import BaseProvider


class LaboratoryOrchestrator:
    """
    Coordinates messaging (blackboard style) between sub-agents.
    """

    def __init__(self, default_provider: BaseProvider) -> None:
        if not default_provider:
            raise ValueError("LaboratoryOrchestrator requires a valid BaseProvider.")

        # Instantiate the laboratory staff
        self.staff = {
            "pi": PrincipalInvestigatorAgent(default_provider),
            "literature": LiteratureScientistAgent(default_provider),
            "hypothesis": HypothesisScientistAgent(default_provider),
            "experimental": ExperimentalScientistAgent(default_provider),
            "statistician": StatisticianAgent(default_provider),
            "methodologist": MethodologistAgent(default_provider),
            "reviewer": ReviewerAgent(default_provider),
            "ethics": EthicsOfficerAgent(default_provider),
            "resource": ResourcePlannerAgent(default_provider),
            "publication": PublicationScientistAgent(default_provider),
        }

        self.blackboard: list[dict[str, Any]] = []

    def post_to_blackboard(self, source: str, topic: str, payload: Any) -> dict[str, Any]:
        """Posts a message to the shared blackboard."""
        message = {"id": str(uuid.uuid4()), "source": source, "topic": topic, "payload": payload}
        self.blackboard.append(message)
        return message

    def process_blackboard(self) -> int:
        """
        Agents observe the blackboard and pick up tasks relevant to their specialty.
        """
        # Very simple mock pub-sub routing logic for the prototype
        events_processed = 0
        for msg in list(self.blackboard):
            topic = msg["topic"]

            if topic == "new_literature":
                self.staff["literature"].execute_cycle(msg["payload"])
                self.post_to_blackboard("literature", "extracted_claims", "claims_data")
                self.blackboard.remove(msg)
                events_processed += 1

            elif topic == "extracted_claims":
                self.staff["hypothesis"].execute_cycle(msg["payload"])
                self.post_to_blackboard("hypothesis", "new_hypothesis", "hyp_data")
                self.blackboard.remove(msg)
                events_processed += 1

            elif topic == "new_hypothesis":
                self.staff["experimental"].execute_cycle(msg["payload"])
                self.post_to_blackboard("experimental", "draft_experiment", "exp_data")
                self.blackboard.remove(msg)
                events_processed += 1

            elif topic == "draft_experiment":
                # Multiple agents review the experiment
                self.staff["methodologist"].execute_cycle(msg["payload"])
                self.staff["statistician"].execute_cycle(msg["payload"])
                self.staff["ethics"].execute_cycle(msg["payload"])
                self.staff["resource"].execute_cycle(msg["payload"])

                self.post_to_blackboard("orchestrator", "experiment_reviewed", "approved_exp_data")
                self.blackboard.remove(msg)
                events_processed += 1

        return events_processed

    def run_campaign(self, initial_goal: str) -> None:
        """Kicks off a multi-agent campaign."""
        self.post_to_blackboard("external", "new_literature", initial_goal)

        # Run until the blackboard stabilizes (no new events processed)
        while self.process_blackboard() > 0:
            pass
