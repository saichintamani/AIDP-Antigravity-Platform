from aidp.intelligence.cognition.genome import AgentGenome, ScientistIdentity


def test_agent_genome_cloning() -> None:
    identity = ScientistIdentity(role="Methodologist", specialization="Design")
    genome = AgentGenome(identity=identity, base_prompt="Original Prompt")

    child = genome.spawn_child_version(new_prompt="New Prompt")

    assert genome.version == 1
    assert child.version == 2
    assert child.base_prompt == "New Prompt"
    assert genome.base_prompt == "Original Prompt"
    assert child.id != genome.id
