import pytest

try:
    import ray

    from aidp.core.actor import AIDPActor

    HAS_RAY = True
except ImportError:
    HAS_RAY = False

pytestmark = pytest.mark.skipif(
    not HAS_RAY,
    reason="Skipping Ray actor tests on platforms without Ray (e.g., native Windows - see TD-001)",
)


@pytest.fixture(scope="module", autouse=True)
def setup_ray():  # type: ignore[no-untyped-def]
    if HAS_RAY:
        ray.init(ignore_reinit_error=True, num_cpus=2)
        yield
        ray.shutdown()
    else:
        yield


def test_aidp_actor_ping() -> None:
    actor = AIDPActor.remote("TestAgent")  # type: ignore[attr-defined]
    result = ray.get(actor.ping.remote())

    assert "ACK from TestAgent" in result
    assert "invocations: 1" in result

    result_2 = ray.get(actor.ping.remote())
    assert "invocations: 2" in result_2


def test_aidp_actor_state() -> None:
    actor = AIDPActor.remote("StateAgent")  # type: ignore[attr-defined]
    ray.get([actor.ping.remote() for _ in range(5)])

    invocations = ray.get(actor.get_invocations.remote())
    assert invocations == 5
