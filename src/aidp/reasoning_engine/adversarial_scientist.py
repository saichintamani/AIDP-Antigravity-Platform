from aidp.reasoning.subjective_logic import Opinion
from aidp.reasoning_engine.debate_graph import DebateGraph


class AdversarialScientist:
    """
    The 'Devil's Advocate'. Purposefully searches for hidden assumptions
    and attacks hypotheses to break confirmation bias.
    """

    def generate_attack(self, graph: DebateGraph, target_node_id: str) -> None:
        """
        Injects a high-disbelief critique into the debate graph.
        """
        # Mocking the LLM's analytical attack
        attack_content = "[Adversarial Attack] Hidden assumption detected: Linearity assumed."
        attack_op = Opinion(belief=0.1, disbelief=0.8, uncertainty=0.1, base_rate=0.5)

        graph.add_critique(target_node_id, "AdversarialScientist", attack_content, attack_op)
