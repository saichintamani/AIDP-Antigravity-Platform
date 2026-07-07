import ast
from pathlib import Path

import pytest


def get_python_files(directory: str) -> list[Path]:
    return list(Path(directory).rglob("*.py"))


def check_imports(file_path: Path, forbidden_imports: list[str]) -> list[str]:
    with open(file_path, encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=str(file_path))
        except SyntaxError:
            return []

    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if any(alias.name.startswith(fi) for fi in forbidden_imports):
                    violations.append(f"Forbidden import '{alias.name}' at line {node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            if node.module and any(node.module.startswith(fi) for fi in forbidden_imports):
                violations.append(f"Forbidden from-import '{node.module}' at line {node.lineno}")

    return violations


def test_gate_8_architecture_fitness() -> None:
    """
    Gate 8: Architecture Fitness.
    Enforces that internal subsystems do not cross boundaries.
    """
    src_dir = Path("src/aidp")
    if not src_dir.exists():
        pytest.skip("Source directory not found, skipping architecture tests.")

    # 1. Retrieval must not access Parser internals
    retrieval_files = get_python_files("src/aidp/knowledge/retrieval")
    # if the folder doesn't exist yet, this is fine
    for f in retrieval_files:
        violations = check_imports(f, ["aidp.knowledge.extraction", "aidp.knowledge.parser"])
        assert not violations, f"Architecture violation in {f}: {violations}"

    # 2. Embedding must not access Storage (Qdrant)
    embedding_file = Path("src/aidp/knowledge/embedding.py")
    if embedding_file.exists():
        violations = check_imports(embedding_file, ["qdrant_client", "aidp.knowledge.storage"])
        assert not violations, f"Architecture violation in {embedding_file}: {violations}"

    # 3. Execution (orchestration) must not import Knowledge directly
    # (they communicate via schemas)
    execution_files = get_python_files("src/aidp/execution")
    for f in execution_files:
        violations = check_imports(f, ["aidp.knowledge.storage", "aidp.knowledge.embedding"])
        assert not violations, f"Architecture violation in {f}: {violations}"
