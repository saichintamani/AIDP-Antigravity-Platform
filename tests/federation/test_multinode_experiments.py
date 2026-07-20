import asyncio

import pytest

from aidp.federation.websocket_node import WebSocketFederationNode
from aidp.intelligence.epistemic_models import EpistemicClaim as Claim
from aidp.intelligence.epistemic_models import EpistemicEvidence, VerificationStatus


def strict_multievidence_verifier(claim: Claim, local_pool: list[EpistemicEvidence]) -> VerificationStatus:
    """
    Verifies that ALL evidence required by the claim is present in the local pool.
    For this test, we know the claim requires exactly 3 pieces of evidence.
    """
    if len(claim.evidence) < 3:
        return VerificationStatus.PENDING
        
    required_ids = [ev.source_id for ev in claim.evidence]
    pool_ids = [ev.source_id for ev in local_pool]
    
    for req_id in required_ids:
        if req_id not in pool_ids:
            return VerificationStatus.PENDING # Cannot verify yet
            
    return VerificationStatus.VERIFIED

@pytest.mark.asyncio
async def test_emergent_knowledge_synthesis():
    """
    Tests the 'Fragmented Knowledge' problem.
    5 nodes. A claim requires Evidence X, Y, and Z.
    Node A has X. Node B has Y. Node C has Z. 
    Node A broadcasts the claim.
    Nodes broadcast their evidence.
    Assert all nodes eventually arrive at VERIFIED independently.
    """
    
    # 1. Setup 5 nodes on ports 8010 - 8014
    nodes = []
    for i in range(5):
        node = WebSocketFederationNode(
            node_id=f"Node_{i}", 
            host="localhost", 
            port=8010 + i, 
            local_verifier=strict_multievidence_verifier
        )
        nodes.append(node)
        
    try:
        # 2. Start Servers
        for node in nodes:
            await node.start_server()
            
        # 3. Connect as a fully connected mesh
        for a in nodes:
            for b in nodes:
                if a.port != b.port:
                    a.add_peer(f"ws://localhost:{b.port}")
                    
        # 4. Create the Evidence Fragments
        ev_x = EpistemicEvidence(source_id="EV_X", source_type="Obs", extracted_text="Gene A active")
        ev_y = EpistemicEvidence(source_id="EV_Y", source_type="Obs", extracted_text="Gene B suppressed")
        ev_z = EpistemicEvidence(source_id="EV_Z", source_type="Obs", extracted_text="Protein C folded")
        
        # 5. Inject Fragments into different nodes
        node_a = nodes[0]
        node_b = nodes[1]
        node_c = nodes[2]
        
        node_a.evidence_pool["EV_X"] = ev_x
        node_b.evidence_pool["EV_Y"] = ev_y
        node_c.evidence_pool["EV_Z"] = ev_z
        
        # 6. Node A creates the claim (Requires X, Y, Z)
        paradigm_claim = Claim(
            claim_id="PARADIGM_01",
            claim_text="Pathway confirmed via Gene A, B and Protein C",
            generated_by="Node_0",
            assumptions=[],
            evidence=[ev_x, ev_y, ev_z],
            verification_status=VerificationStatus.PENDING # Node A only has X, so it can't verify it locally yet
        )
        
        # Node A broadcasts the claim
        await node_a.broadcast_claim(paradigm_claim)
        
        # Give mesh time to propagate
        await asyncio.sleep(0.2)
        
        # Check that nodes received the claim but marked it PENDING because they lack evidence
        # (Node A doesn't process its own broadcasts, so we check B through E)
        for node in nodes[1:]:
            assert len(node.accepted_claims) == 0, f"{node.node_id} accepted claim too early!"
            
        # 7. Nodes broadcast their fragments to the collective
        await node_a.broadcast_evidence(ev_x)
        await node_b.broadcast_evidence(ev_y)
        await node_c.broadcast_evidence(ev_z)
        
        # Give mesh time to propagate evidence
        await asyncio.sleep(0.5)
        
        # 8. Trigger a re-evaluation of pending claims
        # In a real system, the node would re-evaluate on every new evidence receipt.
        # Since our simple websocket_node only evaluates claims upon ClaimBroadcast receipt,
        # we will re-broadcast the claim to trigger re-evaluation now that the evidence is present.
        await node_a.broadcast_claim(paradigm_claim)
        
        await asyncio.sleep(0.2)
        
        # 9. Assert Emergent Intelligence
        # All receiving nodes (B, C, D, E) should now have successfully verified the claim independently.
        for node in nodes[1:]:
            assert len(node.accepted_claims) == 1, f"{node.node_id} failed to verify the claim!"
            assert node.accepted_claims[0].claim_id == "PARADIGM_01"
            assert node.accepted_claims[0].verification_status == VerificationStatus.VERIFIED
            
    finally:
        # Cleanup
        for node in nodes:
            await node.stop_server()
