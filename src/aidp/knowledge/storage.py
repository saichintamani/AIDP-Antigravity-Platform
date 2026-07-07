import json
import os
import uuid
from dataclasses import asdict
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from aidp.knowledge.world_model import ScientificEntity, ScientificRelationship


class KnowledgeStorage:
    def __init__(self) -> None:
        # In-memory storage for the vertical slice validation
        self.client = QdrantClient(location=":memory:")
        self.collection_name = "cognitive_objects"

        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

    def store_cognitive_object(
        self, capnp_bytes: bytes, embedding: list[float], document_id: str
    ) -> str:
        """
        Stores the binary Cognitive Object with its semantic dense vector.
        """
        point_id = str(uuid.uuid4())

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={"capnp_data": capnp_bytes.hex(), "document_id": document_id},
                )
            ],
        )
        return point_id

    def search(
        self, query_vector: list[float], limit: int = 10, doc_filter: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Retrieves the Top-K cognitive objects matching the dense vector.
        Returns a list of payloads.
        """
        # In a full hybrid scenario, we would use sparse vectors + dense vectors here.
        # For M7, we implement the dense retrieval vector search first.
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            # query_filter can be added here using `models.Filter` if doc_filter is provided
        )

        results = []
        for hit in search_result.points:
            if hit.payload:
                results.append(hit.payload)
        return results

    def count(self) -> int:
        response = self.client.count(collection_name=self.collection_name)
        return response.count


class KnowledgeGraphStorage:
    """
    Persists the World Model entities and relationships.
    Currently uses JSONL for immediate persistence, but designed to be swapped
    for SQLite/GraphDB in the future.
    """

    def __init__(self, storage_path: str = ".world_model") -> None:
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        self.entities_file = os.path.join(self.storage_path, "entities.jsonl")
        self.relationships_file = os.path.join(self.storage_path, "relationships.jsonl")

    def _append(self, filepath: str, data: dict[str, Any]) -> None:
        with open(filepath, "a") as f:
            f.write(json.dumps(data) + "\n")

    def store_entity(self, entity: ScientificEntity) -> None:
        entity.validate()
        self._append(self.entities_file, asdict(entity))

    def store_relationship(self, relationship: ScientificRelationship) -> None:
        relationship.validate()
        self._append(self.relationships_file, asdict(relationship))
