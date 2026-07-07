import ast
from pathlib import Path


def test_cognitive_object_emission() -> None:
    """
    Architecture Fitness Function:
    Ensures that the serialization module exists and correctly returns
    the strictly typed bytes of a Canonical Cognitive Object.
    """
    project_root = Path(__file__).parent.parent.parent
    serialization_file = project_root / "src" / "aidp" / "knowledge" / "serialization.py"

    with open(serialization_file, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(serialization_file))

    found_factory = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "serialize_to_cognitive_object":
            found_factory = True
            # Verify return annotation is bytes
            assert getattr(node.returns, "id", None) == "bytes", (
                "Serialization factory must return strict bytes"
            )

    assert found_factory, (
        "Architecture Violation: No canonical serialization factory found in knowledge domain"
    )
