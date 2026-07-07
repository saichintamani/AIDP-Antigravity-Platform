from aidp.intelligence.cognition.genome import AgentGenome
from aidp.intelligence.cognition.memory import HierarchicalMemory


class ReflectionLoop:
    """
    Evaluates agent performance at the end of a research cycle and updates memory.
    """

    def __init__(self) -> None:
        pass

    def reflect_on_failure(
        self,
        genome: AgentGenome,
        memory: HierarchicalMemory,
        goal: str,
        mistake: str,
        correction: str,
    ) -> None:
        """
        Processes a failed attempt, updates reflection memory, and penalizes confidence calibration.
        """
        # Lower confidence calibration since they failed
        genome.identity.confidence_calibration = max(
            0.1, genome.identity.confidence_calibration - 0.05
        )

        # Log to reflection memory to avoid repeating
        memory.add_failure_reflection(goal, mistake, correction)

        # Log to performance history
        genome.performance_history.append(
            {
                "status": "failure",
                "mistake": mistake,
                "new_calibration": genome.identity.confidence_calibration,
            }
        )

    def reflect_on_success(self, genome: AgentGenome, memory: HierarchicalMemory, goal: str) -> None:
        """
        Processes a successful attempt, slightly increasing confidence calibration if accurate.
        """
        genome.identity.confidence_calibration = min(
            1.0, genome.identity.confidence_calibration + 0.02
        )

        genome.performance_history.append(
            {
                "status": "success",
                "goal": goal,
                "new_calibration": genome.identity.confidence_calibration,
            }
        )


class PromptEvolutionEngine:
    """
    Allows agents to rewrite their own internal prompts based on historical performance.
    """

    def evolve_prompt(self, genome: AgentGenome, memory: HierarchicalMemory) -> AgentGenome:
        """
        Analyzes the reflection memory to create a better prompt.
        Spawns a child genome for A/B testing.
        """
        if not memory.reflection_memory:
            return genome  # No need to evolve if no mistakes

        # In a full LLM implementation, we would pass reflection_memory to the LLM
        # and ask it to rewrite the base_prompt. We mock this here.
        new_prompt = genome.base_prompt + "\n[System Added Rule: Avoid previous mistakes.]"

        # Spawn child
        child_genome = genome.spawn_child_version(new_prompt=new_prompt)
        return child_genome
