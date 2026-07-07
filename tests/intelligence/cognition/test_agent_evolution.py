from aidp.intelligence.cognition.evolution import PromptEvolutionEngine, ReflectionLoop
from aidp.intelligence.cognition.genome import AgentGenome, ScientistIdentity
from aidp.intelligence.cognition.memory import HierarchicalMemory


def test_reflection_and_evolution() -> None:
    identity = ScientistIdentity(role="TestRole", specialization="Test")
    genome = AgentGenome(identity=identity, base_prompt="Base")
    memory = HierarchicalMemory()

    loop = ReflectionLoop()
    # Initial calibration
    assert genome.identity.confidence_calibration == 1.0

    # Reflect on failure
    loop.reflect_on_failure(
        genome, memory, "Solve P=NP", "Hallucinated proof", "Do not hallucinate"
    )

    assert genome.identity.confidence_calibration < 1.0
    assert len(memory.reflection_memory) == 1

    # Evolve prompt
    engine = PromptEvolutionEngine()
    child_genome = engine.evolve_prompt(genome, memory)

    assert child_genome.version == 2
    assert "Avoid previous mistakes" in child_genome.base_prompt
