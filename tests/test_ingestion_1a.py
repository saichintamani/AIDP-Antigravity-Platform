from aidp.retrieval.ingestion import (
    DocumentIngestor,
    DocumentSource,
    EntityNormalizer,
    RawEvidenceDocument,
)


def test_entity_normalizer():
    normalizer = EntityNormalizer()
    
    # Test synonym resolution
    text = "The patient was given Tylenol and advil for pain."
    entities = normalizer.normalize(text)
    
    assert "Acetaminophen" in entities
    assert "Ibuprofen" in entities
    assert "tylenol" not in entities
    assert "advil" not in entities
    
    # Test punctuation handling
    text2 = "COVID-19 affects the lungs!"
    entities2 = normalizer.normalize(text2)
    assert "SARS-CoV-2" in entities2

def test_document_ingestor():
    ingestor = DocumentIngestor()
    
    doc = ingestor.ingest_mock_pubmed(
        pmid="12345",
        title="Effects of Paracetamol on Fever",
        abstract="The study shows that paracetamol reduces fever.",
        year=2025
    )
    
    assert isinstance(doc, RawEvidenceDocument)
    assert doc.source == DocumentSource.PUBMED
    assert doc.external_id == "12345"
    assert "Acetaminophen" in doc.normalized_entities
    assert doc.publication_year == 2025

if __name__ == "__main__":
    test_entity_normalizer()
    test_document_ingestor()
    print("Compartment 1A tests passed.")
