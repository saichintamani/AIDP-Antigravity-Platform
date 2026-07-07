from aidp.knowledge.world_model import ScientificEntity


class OntologyManager:
    """
    Manages the semantic hierarchy and constraints of the Scientific World Model.
    Ensures that traversals map correctly (e.g. Gene -> Protein -> Pathway).
    """

    # Allowed entity semantic types
    VALID_TYPES = {"Gene", "Protein", "Pathway", "Disease", "Drug", "ClinicalTrial", "Chemical"}

    # Valid causal/associative edge mappings
    # e.g., "Drug" can "Inhibit" a "Protein"
    VALID_EDGE_CONSTRAINTS = {
        ("Drug", "Inhibits", "Protein"),
        ("Protein", "Activates", "Pathway"),
        ("Gene", "Expresses", "Protein"),
        ("Pathway", "Causes", "Disease"),
    }

    def validate_entity(self, entity: ScientificEntity) -> bool:
        return entity.semantic_type in self.VALID_TYPES

    def validate_relationship_semantics(
        self, source_type: str, relation_type: str, target_type: str
    ) -> bool:
        """
        Validates if an edge is ontologically sound.
        """
        # In a real dynamic system, this would use a graph database or OWL ontology.
        # For AIDP v2 A2, we enforce a strict rule set.
        return (source_type, relation_type, target_type) in self.VALID_EDGE_CONSTRAINTS

    def get_descendants(self, entity_type: str) -> list[str]:
        # Placeholder for ontology hierarchy traversal
        return [entity_type]
