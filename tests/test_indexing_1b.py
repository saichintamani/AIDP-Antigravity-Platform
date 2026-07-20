from aidp.knowledge.provenance import ProvenanceEntry
from aidp.knowledge.world_model import ScientificEntity, ScientificRelationship
from aidp.retrieval.indexing import KnowledgeGraphIndexer


def test_knowledge_graph_indexer():
    indexer = KnowledgeGraphIndexer()
    
    # Mock Provenance
    prov = ProvenanceEntry(
        source_paper_doi="test_1",
        claim_text="test",
        source_url="test",
        retriever_metadata={},
        confidence_score=1.0
    )
    
    # Paper 1 connects Drug A -> Protein X
    entities_1 = [
        ScientificEntity(name="Drug A", semantic_type="CHEMICAL"),
        ScientificEntity(name="Protein X", semantic_type="GENE")
    ]
    rels_1 = [
        ScientificRelationship(
            source_entity_id=entities_1[0].id,
            target_entity_id=entities_1[1].id,
            relation_type="INHIBITS",
            is_causal=True,
            provenance=prov
        )
    ]
    
    # Paper 2 connects Protein X -> Disease Y
    entities_2 = [
        ScientificEntity(name="Protein X", semantic_type="GENE"),
        ScientificEntity(name="Disease Y", semantic_type="DISEASE")
    ]
    rels_2 = [
        ScientificRelationship(
            source_entity_id=entities_2[0].id,
            target_entity_id=entities_2[1].id,
            relation_type="CAUSES",
            is_causal=True,
            provenance=prov
        )
    ]
    
    indexer.index_entities_and_relationships(entities_1, rels_1)
    indexer.index_entities_and_relationships(entities_2, rels_2)
    
    # Check that topological traversal works!
    # Even though Drug A and Disease Y are not in the same paper, the graph should find a path.
    path = indexer.find_path("Drug A", "Disease Y")
    assert path is not None
    assert path == ["Drug A", "Protein X", "Disease Y"]
    
    # Verify non-existent path
    assert indexer.find_path("Drug A", "Unknown Z") is None

if __name__ == "__main__":
    test_knowledge_graph_indexer()
    print("Compartment 1B topological indexing tests passed.")
