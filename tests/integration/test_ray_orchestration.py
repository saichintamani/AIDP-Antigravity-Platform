import importlib.util

import pytest

from aidp.knowledge.serialization import deserialize_cognitive_object


def has_ray() -> bool:
    return importlib.util.find_spec("ray") is not None


@pytest.mark.skipif(
    not has_ray(),
    reason="Skipping Ray actor tests on platforms without Ray (e.g., native Windows - see TD-001)",
)
def test_ray_orchestration_e2e() -> None:
    from aidp.core.orchestration import AgentOrchestrator

    # 1. Initialize the orchestrator
    orchestrator = AgentOrchestrator(num_workers=2)

    # 2. Simulate parallel payloads (e.g. chunks extracted from a Markdown document)
    payloads = [
        "Chunk 1 of the architecture document",
        "Chunk 2 of the mathematical formulas",
        "Chunk 3 of the systems engineering design",
        "Chunk 4 of the distributed execution layer",
    ]

    # 3. Distribute payloads across the Actor pool
    results: list[bytes] = orchestrator.map_payloads(payloads)

    assert len(results) == 4

    # 4. Verify that every returned byte array is a valid Cognitive Object
    for res_bytes in results:
        assert isinstance(res_bytes, bytes)
        assert len(res_bytes) > 0

        # We can deserialize it to prove it's a valid Cap'n proto object
        obj = deserialize_cognitive_object(res_bytes)
        assert obj.provenance == b"agent://base_agent"
        # Check that belief strings are present indicating the LLM and Subjective Logic fusion ran
        assert b"Belief:" in obj.payload
