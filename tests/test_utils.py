from aidp.core.utils import get_platform_version


def test_get_platform_version() -> None:
    assert get_platform_version() == "AIDP-v0.1.0"
