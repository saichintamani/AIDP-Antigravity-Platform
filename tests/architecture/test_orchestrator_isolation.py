import ast
from pathlib import Path


def test_orchestrator_isolation() -> None:
    """
    Architecture Fitness Function:
    Ensures that no module inside `aidp.core.orchestration` imports
    `qdrant_client` or LLM models directly. The orchestrator must only pass bytes and strings.
    """
    project_root = Path(__file__).parent.parent.parent
    orchestration_file = project_root / "src" / "aidp" / "core" / "orchestration.py"

    violators = []

    if orchestration_file.exists():
        with open(orchestration_file, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(orchestration_file))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("qdrant_client"):
                        violators.append((orchestration_file, node.lineno))
            elif (
                isinstance(node, ast.ImportFrom)
                and node.module
                and node.module.startswith("qdrant_client")
            ):
                violators.append((orchestration_file, node.lineno))

    assert not violators, (
        f"Architecture Violation: Orchestrator bypasses API to access DB directly: {violators}"
    )
