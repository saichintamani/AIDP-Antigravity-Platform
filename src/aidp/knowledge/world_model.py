import uuid
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
    provenance: ProvenanceEntry | None = None
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

    def get_entity_by_name(self, name: str) -> ScientificEntity | None:
        name_lower = name.lower()
        for ent in self.entities.values():
            if ent.name.lower() == name_lower or name_lower in [a.lower() for a in ent.aliases]:
                return ent
        return None

    def get_relationships_between(self, source_id: str, target_id: str) -> list[ScientificRelationship]:
        return [
            r for r in self.relationships.values()
            if r.source_entity_id == source_id and r.target_entity_id == target_id
        ]

    def find_contradictions(self) -> list[tuple[ScientificRelationship, ScientificRelationship]]:
        """
        Finds pairs of relationships that assert contradictory claims about the same entity pair.
        """
        contradictions = []
        
        # Simple heuristic: Opposing relationship types
        opposing_pairs = {
            "upregulates": "downregulates",
            "downregulates": "upregulates",
            "activates": "inhibits",
            "inhibits": "activates",
            "increases": "decreases",
            "decreases": "increases"
        }

        # Group relationships by (source, target)
        grouped: dict[tuple[str, str], list[ScientificRelationship]] = {}
        for r in self.relationships.values():
            key = (r.source_entity_id, r.target_entity_id)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(r)
            
        for key, rels in grouped.items():
            if len(rels) > 1:
                # Check all pairs in this group
                for i in range(len(rels)):
                    for j in range(i + 1, len(rels)):
                        r1 = rels[i]
                        r2 = rels[j]
                        t1 = r1.relation_type.lower()
                        t2 = r2.relation_type.lower()
                        
                        if opposing_pairs.get(t1) == t2 or (t1 != t2 and t1 not in ["associatedwith", "interacts"] and t2 not in ["associatedwith", "interacts"]):
                            contradictions.append((r1, r2))
                            
        return contradictions
