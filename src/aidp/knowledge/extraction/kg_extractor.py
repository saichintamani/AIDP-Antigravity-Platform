from pydantic import BaseModel, Field

from aidp.intelligence.providers.capabilities import ReasoningTier
from aidp.intelligence.providers.middleware import IntelligenceGateway


class KREntity(BaseModel):
    name: str = Field(..., description="The name of the entity, e.g., 'p53', 'Apoptosis'")
    semantic_type: str = Field(..., description="The type of the entity, e.g., 'Gene', 'Pathway', 'Chemical', 'Disease'")

class KRRelationship(BaseModel):
    source_entity_name: str = Field(..., description="The name of the source entity")
    target_entity_name: str = Field(..., description="The name of the target entity")
    relation_type: str = Field(..., description="The type of relationship, e.g., 'Upregulates', 'Downregulates', 'Inhibits', 'Activates', 'AssociatedWith'")
    is_causal: bool = Field(False, description="Whether the relationship implies direct causality")

class KnowledgeGraphExtraction(BaseModel):
    entities: list[KREntity] = Field(default_factory=list, description="List of unique scientific entities mentioned")
    relationships: list[KRRelationship] = Field(default_factory=list, description="List of relationships between entities")

class KnowledgeGraphExtractor:
    """
    Uses an LLM Gateway to extract structured entities and relationships from raw scientific text.
    """
    def __init__(self, gateway: IntelligenceGateway) -> None:
        self.gateway = gateway

    def extract_from_text(self, text: str, source_id: str) -> KnowledgeGraphExtraction:
        prompt = f"""
You are a highly capable scientific knowledge extraction system.
Extract all relevant biological, chemical, or medical entities from the following text, and any relationships between them.
Relationships should be directionally precise. Common relationship types include:
- Upregulates
- Downregulates
- Inhibits
- Activates
- AssociatedWith

Text to process:
\"\"\"{text}\"\"\"
"""
        try:
            result = self.gateway.query(
                prompt=prompt,
                schema_hint=KnowledgeGraphExtraction,
                prompt_version="kg_extract_v1.0",
                min_tier=ReasoningTier.COMPLEX
            )
            if isinstance(result, KnowledgeGraphExtraction):
                return result
            # Fallback if Gateway returns a dict for some reason
            return KnowledgeGraphExtraction.model_validate(result)
        except Exception as e:
            print(f"Extraction failed for source {source_id}: {e}")
            return KnowledgeGraphExtraction()
