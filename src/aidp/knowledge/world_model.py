import uuid
from typing import Optional
from dataclasses import dataclass, field

from aidp.knowledge.provenance import ProvenanceEntry


@dataclass
class ScientificEntity:
    """
    A distinct concept, object, or property in the scientific world (e.g., 'p53', 'Apoptosis').
    """

    name: str
    semantic_type: str  # e.g., 'Gene', 'Pathway', 'Chemical'
    id: str = field(default_factory=lambda: f"ent_{uuid.uuid4()}")
    aliases: list[str] = field(default_factory=list)
    description: str | None = None

    def validate(self) -> None:
        if not self.name or not self.semantic_type:
            raise ValueError("ScientificEntity must have a name and semantic_type.")


@dataclass
class ScientificRelationship:
    """
    A causal or associative link between two entities.
    Strictly requires a ProvenanceEntry to exist.
    """

    source_entity_id: str
    target_entity_id: str
    relation_type: str  # e.g., 'Inhibits', 'Upregulates', 'Causes'
    provenance: ProvenanceEntry
    id: str = field(default_factory=lambda: f"rel_{uuid.uuid4()}")
    is_causal: bool = False

    def validate(self) -> None:
        if not self.source_entity_id or not self.target_entity_id or not self.relation_type:
            raise ValueError("ScientificRelationship missing core fields.")
        if not self.provenance or not isinstance(self.provenance, ProvenanceEntry):
            raise ValueError(
                "Epistemic Violation: ScientificRelationship must have a valid ProvenanceEntry."
            )
        self.provenance.validate()


@dataclass
class ScientificProcess:
    """
    A mechanism composed of multiple sequential relationships (e.g., a metabolic pathway).
    """

    name: str
    description: str
    relationships: list[ScientificRelationship] = field(default_factory=list)
    id: str = field(default_factory=lambda: f"proc_{uuid.uuid4()}")


@dataclass
class ExperimentalResult:
    """
    A documented empirical observation that provides evidence for/against a relationship.
    """

    description: str
    methodology: str
    p_value: float | None = None
    effect_size: float | None = None
    provenance: Optional[ProvenanceEntry] = None
    id: str = field(default_factory=lambda: f"exp_{uuid.uuid4()}")

    def validate(self) -> None:
        if not self.provenance or not isinstance(self.provenance, ProvenanceEntry):
            raise ValueError("ExperimentalResult must have a valid ProvenanceEntry.")
        self.provenance.validate()


@dataclass
class ScientificLaw:
    """
    A foundational constraint the system must never violate (e.g., Thermodynamics).
    """

    name: str
    constraint_logic: str
    id: str = field(default_factory=lambda: f"law_{uuid.uuid4()}")


class WorldModel:
    """
    Represents the active, working state of the agent's scientific knowledge.
    It contains entities, relationships, and processes currently believed to be true.
    """

    def __init__(self) -> None:
        self.entities: dict[str, ScientificEntity] = {}
        self.relationships: dict[str, ScientificRelationship] = {}

    def add_entity(self, entity: ScientificEntity) -> None:
        self.entities[entity.id] = entity

    def add_relationship(self, relationship: ScientificRelationship) -> None:
        self.relationships[relationship.id] = relationship
