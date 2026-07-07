import ast
import os
from pathlib import Path


def test_agent_isolation() -> None:
    """
    Architecture Fitness Function:
    Ensures that no module inside `aidp.intelligence` imports `qdrant_client`.
    Agents must not manage their own persistence layer directly.
    """
    project_root = Path(__file__).parent.parent.parent
    intelligence_dir = project_root / "src" / "aidp" / "intelligence"

    violators = []

    for root, _, files in os.walk(intelligence_dir):
        for file in files:
            if file.endswith(".py"):
                py_file = Path(root) / file
                with open(py_file, encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=str(py_file))

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
        f"Architecture Violation: Agent bypasses Knowledge API to access DB directly: {violators}"
    )
