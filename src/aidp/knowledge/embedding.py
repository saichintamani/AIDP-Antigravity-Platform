import importlib.util
from typing import Any


# We use optional import to not strictly depend on it during basic unit tests,
# but our integration benchmarks will require it.
def has_sentence_transformers() -> bool:
    return importlib.util.find_spec("sentence_transformers") is not None


SentenceTransformer: Any
if has_sentence_transformers():
    from sentence_transformers import SentenceTransformer as _SentenceTransformer
    SentenceTransformer = _SentenceTransformer
else:
    SentenceTransformer = None


class EmbeddingService:
    """
    Generates dense vector embeddings using sentence-transformers.
    Defaults to all-MiniLM-L6-v2 which yields a 384-dimensional vector.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        if not has_sentence_transformers():
            raise RuntimeError("sentence-transformers is not installed.")
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        """Embeds a single string into a vector."""
        embedding = self.model.encode(text)
        return list(embedding.tolist())
