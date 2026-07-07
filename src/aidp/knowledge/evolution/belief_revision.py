from aidp.knowledge.world_model import ScientificRelationship
from aidp.reasoning.subjective_logic import Opinion, consensus_fusion


class BeliefReviser:
    """
    Applies Subjective Logic to merge new evidence with existing relationships.
    Never overwrites confidence directly; calculates a fused opinion.
    """

    def _extract_opinion(self, rel: ScientificRelationship) -> Opinion:
        # Simplistic mapping of confidence to Subjective Logic Opinion
        # In a real scenario, this would depend on the evidence diversity and strength.
        b = rel.provenance.confidence_score
        d = 0.0 if b > 0 else 0.5  # Simplified
        u = max(0.0, 1.0 - (b + d))
        a = 0.5
        return Opinion(belief=b, disbelief=d, uncertainty=u, base_rate=a)

    def revise_belief(
        self, existing_rel: ScientificRelationship, new_evidence_rel: ScientificRelationship
    ) -> ScientificRelationship:
        """
        Merges new evidence into an existing relationship using Subjective Logic fusion.
        Returns a newly instantiated ScientificRelationship (immutable update).
        """
        if (
            existing_rel.source_entity_id != new_evidence_rel.source_entity_id
            or existing_rel.target_entity_id != new_evidence_rel.target_entity_id
        ):
            raise ValueError("Cannot revise belief for non-matching entities.")

        op_existing = self._extract_opinion(existing_rel)
        op_new = self._extract_opinion(new_evidence_rel)

        # Perform Consensus Fusion (combining independent evidence)
        fused_op = consensus_fusion(op_existing, op_new)

        # Create a new provenance entry reflecting the update
        new_provenance = new_evidence_rel.provenance
        new_provenance.confidence_score = fused_op.belief
        new_provenance.provider_metadata["revision_history"] = [
            existing_rel.provenance.id,
            new_evidence_rel.provenance.id,
        ]

        # Return new edge instance for the SnapshotManager
        return ScientificRelationship(
            source_entity_id=existing_rel.source_entity_id,
            target_entity_id=existing_rel.target_entity_id,
            relation_type=new_evidence_rel.relation_type,
            provenance=new_provenance,
            is_causal=existing_rel.is_causal or new_evidence_rel.is_causal,
        )
