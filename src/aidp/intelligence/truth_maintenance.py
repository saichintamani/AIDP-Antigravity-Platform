from aidp.explainability.causal_explanation import BeliefRevisionExplanation, CausalExplanation
from aidp.intelligence.dependency_graph import EvidenceDependencyGraph
from aidp.intelligence.symbolic_solver import ContradictionProof


class TruthMaintenanceSystem:
    """
    Engine that cascades confidence updates through the Evidence Dependency Graph.
    Replaces heuristic LLM review with deterministic graph traversal.
    """
    def __init__(self, graph: EvidenceDependencyGraph):
        self.graph = graph
        
    def retract_evidence(self, evidence_id: str):
        """
        Marks an evidence node as invalid (confidence = 0) and cascades the 
        update downstream to all dependent claims.
        """
        if evidence_id not in self.graph.nodes:
            raise ValueError(f"Evidence {evidence_id} not found in graph.")
            
        print(f"[TMS] Retracting evidence: {evidence_id}")
        self._update_node_confidence(evidence_id, 0.0, reason="EVIDENCE_RETRACTED")
        self.cascade_confidence_update(evidence_id)

    def _update_node_confidence(self, node_id: str, new_confidence: float, reason: str):
        node = self.graph.nodes[node_id]
        old_confidence = node.confidence
        node.confidence = new_confidence
        
        # If it's a claim, we must update its lineage via the Epistemic Ledger's attached data
        if node.node_type == "CLAIM" and hasattr(node.data, "confidence"):
            delta = new_confidence - old_confidence
            # The exact EpistemicLedger integration will append to lineage
            if hasattr(node.data, "update_confidence"):
                node.data.update_confidence(
                    dimension="evidence_confidence",
                    delta=delta,
                    reason=f"Cascading update: {reason}"
                )
            
            # Attach Belief Revision Explanation
            revision = BeliefRevisionExplanation(
                previous_confidence=old_confidence,
                new_confidence=new_confidence,
                delta=delta,
                causal_event=reason,
                summary=f"Confidence updated from {old_confidence} to {new_confidence} due to {reason}"
            )
            
            if not hasattr(node.data, "explanation") or node.data.explanation is None:
                node.data.explanation = CausalExplanation()
            node.data.explanation.revisions.append(revision)
            
    def cascade_confidence_update(self, start_node_id: str):
        """
        Topological propagation of confidence drops.
        Using proportional decay logic: child confidence is bounded by parent confidence.
        """
        # BFS traversal to propagate confidence
        queue = [start_node_id]
        
        while queue:
            curr_id = queue.pop(0)
            curr_node = self.graph.nodes[curr_id]
            
            for child_id in curr_node.children:
                child_node = self.graph.nodes[child_id]
                
                # Proportional decay: child's new confidence is min(current_confidence, parent_confidence)
                # This ensures that if a parent drops to 0, the child drops to 0 (if that parent was a strict dependency).
                # Note: In a fully Bayesian TMS, we'd weight multiple parents. For Phase 14, we use minimum bounding.
                if child_node.confidence > curr_node.confidence:
                    print(f"[TMS] Cascading drop to child {child_id}: {child_node.confidence} -> {curr_node.confidence}")
                    self._update_node_confidence(child_id, curr_node.confidence, reason=f"Upstream drop in {curr_id}")
                    queue.append(child_id)

    def process_contradiction_proof(self, proof: 'ContradictionProof'):
        """
        Accepts a ContradictionProof from the ConstraintIntelligenceEngine.
        If the proof shows UNSAT, it marks the conflicting claims with 0 confidence
        and cascades the update through the dependency graph.
        """
        if proof.is_valid:
            print("[TMS] Contradiction proof is valid (SAT). No action needed.")
            return

        print(f"[TMS] Processing contradiction proof: {proof.message}")
        for claim_id in proof.conflicting_claim_ids:
            if claim_id in self.graph.nodes:
                print(f"[TMS] Invalidating conflicting claim: {claim_id}")
                self._update_node_confidence(claim_id, 0.0, reason=f"Contradiction detected: {proof.unsat_core}")
                self.cascade_confidence_update(claim_id)
            else:
                print(f"[TMS] Warning: Conflicting claim {claim_id} not found in dependency graph.")

