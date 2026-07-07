import ast
from pathlib import Path


def test_database_isolation() -> None:
    """
    Architecture Fitness Function:
    Ensures that no module outside of `aidp.knowledge` imports `qdrant_client`.
    This enforces strict boundary isolation for vector storage.
    """
    project_root = Path(__file__).parent.parent.parent
    src_dir = project_root / "src" / "aidp"

    violators = []

    for py_file in src_dir.rglob("*.py"):
        # Allow imports within the knowledge domain
        if "knowledge" in py_file.parts:
            continue

        with open(py_file, encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read(), filename=str(py_file))
            except SyntaxError:
                continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("qdrant_client"):
                        violators.append((py_file, node.lineno))
            elif (
                isinstance(node, ast.ImportFrom)
                and node.module
                and node.module.startswith("qdrant_client")
            ):
                violators.append((py_file, node.lineno))

    assert not violators, (
        f"Architecture Violation: Direct Qdrant access detected outside Knowledge Service: {violators}"
    )
