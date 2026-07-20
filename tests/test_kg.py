import os
import sys

# Add src to sys.path so we can import aidp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from aidp.discovery.contradiction import ContradictionDetectionEngine
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.mock import MockProvider
from aidp.knowledge.provenance import ProvenanceEntry
from aidp.knowledge.world_model import ScientificEntity, ScientificRelationship, WorldModel


def test_kg_contradiction():
    print("Testing Knowledge Graph Contradiction Engine...")
    
    # 1. Setup Mock Gateway that returns opposing relations
    mock_provider = MockProvider()
    IntelligenceGateway(mock_provider)
    
    # 2. Simulate extraction (injecting mock extraction results directly since MockLLM doesn't do real extraction)
    # Let's say Paper A claims DrugX inhibits TargetY
    # Paper B claims DrugX activates TargetY
    
    graph_data = {
        "entities": [
            {"name": "DrugX", "semantic_type": "Chemical"},
            {"name": "TargetY", "semantic_type": "Gene"}
        ],
        "relationships": [
            {
                "source_entity_name": "DrugX",
                "target_entity_name": "TargetY",
                "relation_type": "Inhibits",
                "is_causal": True,
                "source_id": "10.1000/paperA"
            },
            {
                "source_entity_name": "DrugX",
                "target_entity_name": "TargetY",
                "relation_type": "Activates",
                "is_causal": True,
                "source_id": "10.1000/paperB"
            }
        ]
    }
    
    # 3. Hydrate WorldModel
    world_model = WorldModel()
    
    for e in graph_data.get("entities", []):
        world_model.add_entity(ScientificEntity(
            name=e.get("name"),
            semantic_type=e.get("semantic_type")
        ))
        
    for r in graph_data.get("relationships", []):
        source_ent = world_model.get_entity_by_name(r.get("source_entity_name"))
        target_ent = world_model.get_entity_by_name(r.get("target_entity_name"))
        if source_ent and target_ent:
            world_model.add_relationship(ScientificRelationship(
                source_entity_id=source_ent.id,
                target_entity_id=target_ent.id,
                relation_type=r.get("relation_type"),
                is_causal=r.get("is_causal", False),
                provenance=ProvenanceEntry(
                    source_paper_doi=r.get("source_id", "unknown"),
                    claim_text="",
                    source_url="",
                    retriever_metadata={},
                    confidence_score=1.0
                )
            ))
            
    # 4. Scan for contradictions
    engine = ContradictionDetectionEngine()
    contradictions = engine.scan_for_contradictions(world_model)
    
    print(f"Found {len(contradictions)} contradictions.")
    assert len(contradictions) == 1
    
    c = contradictions[0]
    print(f"Contradiction: {c['claimA']} (Source: {c['sourceAId']}) vs {c['claimB']} (Source: {c['sourceBId']})")
    
    assert c["sourceAId"] in ["10.1000/paperA", "10.1000/paperB"]
    assert c["sourceBId"] in ["10.1000/paperA", "10.1000/paperB"]
    assert c["sourceAId"] != c["sourceBId"]
    
    print("Test passed successfully!")
    
if __name__ == "__main__":
    test_kg_contradiction()
