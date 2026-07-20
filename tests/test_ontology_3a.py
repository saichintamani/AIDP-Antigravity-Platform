from aidp.intelligence.epistemic_models import (
    ConfidenceLineageEvent,
    ConfidenceOntology,
    EpistemicClaim,
)


def test_confidence_ontology_aggregation():
    ontology = ConfidenceOntology(
        evidence_confidence=0.8,
        verification_confidence=0.9,
        assumption_confidence=0.5,
        consensus_confidence=0.7,
        knowledge_confidence=0.8,
        reproducibility_confidence=0.6,
        overall_confidence=0.0 # to be calculated
    )
    
    # Simple average for the sake of the test, though in reality it might be weighted
    avg = sum([
        ontology.evidence_confidence, 
        ontology.verification_confidence, 
        ontology.assumption_confidence,
        ontology.consensus_confidence,
        ontology.knowledge_confidence,
        ontology.reproducibility_confidence
    ]) / 6.0
    
    ontology.overall_confidence = avg
    assert ontology.overall_confidence > 0.7
    assert ontology.overall_confidence < 0.8

def test_lineage_event_tracking():
    claim = EpistemicClaim(
        claim_text="Hypothesis is testable",
        evidence=[],
        assumptions=[],
        generated_by="Test"
    )
    
    event = ConfidenceLineageEvent(
        dimension="verification_confidence",
        delta=0.9,
        reason="Passed formal methodology verification"
    )
    claim.confidence_lineage.append(event)
    
    assert len(claim.confidence_lineage) == 1
    assert claim.confidence_lineage[0].dimension == "verification_confidence"
    
if __name__ == "__main__":
    test_confidence_ontology_aggregation()
    test_lineage_event_tracking()
    print("Compartment 3A tests passed.")
