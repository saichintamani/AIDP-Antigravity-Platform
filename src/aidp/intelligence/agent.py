from abc import ABC, abstractmethod

from aidp.intelligence.cognition.genome import AgentGenome, ScientistIdentity
from aidp.intelligence.cognition.memory import HierarchicalMemory
from aidp.intelligence.providers.base import BaseProvider
from aidp.knowledge.serialization import Provenance, serialize_to_cognitive_object
from aidp.reasoning.subjective_logic import Opinion, consensus_fusion


class BaseAgent(ABC):
    """
    Base cognitive agent.
    Now backed by a version-controlled AgentGenome and HierarchicalMemory.
    """

    def __init__(
        self,
        provider: BaseProvider,
        genome: AgentGenome | None = None,
        memory: HierarchicalMemory | None = None,
    ):
        self.provider = provider

        # Give a generic identity if none provided
        if not genome:
            identity = ScientistIdentity(role="Generic Agent", specialization="Generalist")
            self.genome = AgentGenome(identity=identity)
        else:
            self.genome = genome

        self.memory = memory or HierarchicalMemory()
        self.internal_state = Opinion(belief=0.0, disbelief=0.0, uncertainty=1.0, base_rate=0.5)

    @abstractmethod
    def perceive(self, payload: str) -> str:
        """Parses the incoming payload into a local prompt format."""
        pass

    def store_working_memory(self, payload: str) -> None:
        """Stores the payload in working memory."""
        self.memory.add_to_working_memory({"event": "perceive", "payload": payload})

    def reason(self, prompt: str) -> Opinion:
        """
        Fuses the LLM's generated opinion with the Agent's internal state
        using Subjective Logic.
        """
        response = self.provider.generate(prompt)
        llm_opinion = response.opinion

        # We can only fuse if uncertainty is not perfectly 1.0 on both sides.
        # But if internal is 1.0, and LLM is not 1.0, consensus works.
        # Let's handle the initial perfectly uncertain state:
        if self.internal_state.uncertainty == 1.0:
            self.internal_state = llm_opinion
        else:
            self.internal_state = consensus_fusion(self.internal_state, llm_opinion)

        return self.internal_state

    def act(self, final_opinion: Opinion) -> bytes:
        """Emits a new Cognitive Object representing the decision."""
        decision_payload = (
            f"Belief: {final_opinion.belief:.2f}, Uncertainty: {final_opinion.uncertainty:.2f}"
        )
        prov = Provenance(
            document_id="agent://base_agent",
            page_number=1,
            paragraph_id="action",
            offset_start=0,
            offset_end=len(decision_payload),
            chunk_index=0,
        )
        return serialize_to_cognitive_object(payload=decision_payload, provenance=prov)

    def execute_cycle(self, payload: str) -> bytes:
        """Runs the full perception-reasoning-action loop."""
        prompt = self.perceive(payload)
        opinion = self.reason(prompt)
        return self.act(opinion)
