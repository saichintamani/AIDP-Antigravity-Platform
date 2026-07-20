import re
import uuid
from enum import StrEnum

from pydantic import BaseModel, Field


class DocumentSource(StrEnum):
    PUBMED = "PUBMED"
    CLINICAL_TRIALS = "CLINICAL_TRIALS"
    INTERNAL = "INTERNAL"
    WEB = "WEB"

class RawEvidenceDocument(BaseModel):
    document_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: DocumentSource
    external_id: str | None = None  # e.g., PMID
    title: str
    abstract: str
    full_text: str | None = None
    authors: list[str] = Field(default_factory=list)
    publication_year: int | None = None
    normalized_entities: list[str] = Field(default_factory=list, description="Entities identified and standardized from text")

class EntityNormalizer:
    """
    Normalizes raw text entities into standard ontology terms.
    This prevents the graph from creating disjoint nodes for "Tylenol" and "Acetaminophen".
    """
    def __init__(self):
        # Mock ontology dictionary for the MVP.
        # In production, this would hook into UMLS, ChEMBL, or a graph DB.
        self._ontology_map: dict[str, str] = {
            "tylenol": "Acetaminophen",
            "paracetamol": "Acetaminophen",
            "advil": "Ibuprofen",
            "motrin": "Ibuprofen",
            "covid-19": "SARS-CoV-2",
            "covid": "SARS-CoV-2",
            "coronavirus": "SARS-CoV-2",
            "heart attack": "Myocardial Infarction"
        }

    def normalize(self, text: str) -> list[str]:
        """
        Scans text and returns a list of normalized standard entities.
        """
        normalized = set()
        
        # Super naive tokenization for MVP
        # Strip punctuation and lower
        clean_text = re.sub(r'[^\w\s-]', '', text).lower()
        
        # Check against map (this is naive substring matching for POC)
        for synonym, standard in self._ontology_map.items():
            # word boundary matching
            pattern = r'\b' + re.escape(synonym) + r'\b'
            if re.search(pattern, clean_text):
                normalized.add(standard)
                
        return list(normalized)

class DocumentIngestor:
    """
    Takes a raw unstructured string or mock payload, normalizes it, and builds a RawEvidenceDocument.
    """
    def __init__(self):
        self.normalizer = EntityNormalizer()
        
    def ingest_mock_pubmed(self, pmid: str, title: str, abstract: str, year: int) -> RawEvidenceDocument:
        combined_text = f"{title} {abstract}"
        entities = self.normalizer.normalize(combined_text)
        
        return RawEvidenceDocument(
            source=DocumentSource.PUBMED,
            external_id=pmid,
            title=title,
            abstract=abstract,
            publication_year=year,
            normalized_entities=entities
        )
