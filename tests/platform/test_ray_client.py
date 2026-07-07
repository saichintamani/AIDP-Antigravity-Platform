from aidp.platform.orchestration.ray_client import RayOrchestrator


def dummy_task(x: int) -> int:
    return x * x


def test_ray_client_local_fallback() -> None:
    # Force local fallback
    orchestrator = RayOrchestrator(enable_ray=False)

    result = orchestrator.dispatch_task(dummy_task, 5)
    resolved = orchestrator.resolve_result(result)

    assert resolved == 25
