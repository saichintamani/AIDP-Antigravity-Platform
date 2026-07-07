import ast
from pathlib import Path


def test_provider_isolation() -> None:
    """
    Architecture Fitness Function (Gate 1):
    Ensures that no module outside of `aidp.intelligence.providers` and `aidp.intelligence.evaluation`
    imports or uses provider implementations directly.
    """
    project_root = Path(__file__).parent.parent.parent
    src_dir = project_root / "src" / "aidp"

    violators = []

    for py_file in src_dir.rglob("*.py"):
        # Allow imports within the providers and evaluation domains
        if "providers" in py_file.parts or "evaluation" in py_file.parts:
            continue

        with open(py_file, encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read(), filename=str(py_file))
            except SyntaxError:
                continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith(
                        "aidp.intelligence.providers.llm"
                    ) or alias.name.startswith("aidp.intelligence.providers.mock"):
                        violators.append((py_file, node.lineno))
            elif (
                isinstance(node, ast.ImportFrom)
                and node.module
                and (
                    node.module.startswith("aidp.intelligence.providers.llm")
                    or node.module.startswith("aidp.intelligence.providers.mock")
                )
            ):
                violators.append((py_file, node.lineno))

    assert not violators, (
        f"Architecture Violation: Direct Provider implementation access detected outside Intelligence Service: {violators}"
    )
