
import networkx as nx

from aidp.knowledge.world_model import ScientificEntity, ScientificRelationship


class KnowledgeGraphIndexer:
    """
    Handles both semantic vector indexing and topological graph building.
    Compartment 1B of the Flagship architecture.
    """
    def __init__(self):
        # We use a directed graph to model relationships (e.g. A -> Inhibits -> B)
        self.graph = nx.DiGraph()
        self.vector_store: dict[str, list[float]] = {}
        
    def index_entities_and_relationships(
        self, 
        entities: list[ScientificEntity], 
        relationships: list[ScientificRelationship]
    ):
        """
        Indexes extracted knowledge into the topological graph.
        """
        id_to_name = {}
        for ent in entities:
            id_to_name[ent.id] = ent.name
            if not self.graph.has_node(ent.name):
                self.graph.add_node(
                    ent.name, 
                    type=ent.semantic_type,
                    id=ent.id
                )
            
            # Mock semantic embedding
            self.vector_store[ent.name] = self._embed_text(ent.name)
                
        # Add edges
        for rel in relationships:
            # Resolve entity names from IDs
            source_name = id_to_name.get(rel.source_entity_id, rel.source_entity_id)
            target_name = id_to_name.get(rel.target_entity_id, rel.target_entity_id)
            
            self.graph.add_edge(
                source_name, 
                target_name, 
                relation_type=rel.relation_type,
                is_causal=rel.is_causal
            )

    def find_path(self, source_entity: str, target_entity: str, max_depth: int = 3) -> list[str] | None:
        """
        Performs a topological traversal to find a connection between two entities
        that may not co-occur in the exact same paper.
        """
        try:
            # Find shortest path using networkx
            path = nx.shortest_path(self.graph, source=source_entity, target=target_entity)
            if len(path) - 1 <= max_depth:
                return path
            return None
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def _embed_text(self, text: str) -> list[float]:
        """Mock embedding generator for MVP."""
        return [0.1, 0.2, 0.3] # Dummy vector
