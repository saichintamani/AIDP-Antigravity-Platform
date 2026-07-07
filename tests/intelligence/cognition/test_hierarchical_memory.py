from aidp.intelligence.cognition.memory import HierarchicalMemory


def test_memory_partitions() -> None:
    memory = HierarchicalMemory()

    # Working memory
    memory.add_to_working_memory({"data": "test"})
    assert len(memory.working_memory) == 1

    # Episodic migration
    memory.archive_to_episodic("camp_1")
    assert len(memory.working_memory) == 0
    assert len(memory.episodic_memory) == 1

    # Reflection memory
    memory.add_failure_reflection("goal", "mistake", "correction")
    assert len(memory.reflection_memory) == 1
