import asyncio

import pytest

from aidp.federation.websocket_node import WebSocketFederationNode
from aidp.intelligence.epistemic_models import EpistemicClaim as Claim
from aidp.intelligence.epistemic_models import EpistemicEvidence, VerificationStatus


def mock_verifier(claim: Claim, local_pool: list[EpistemicEvidence]) -> VerificationStatus:
    """
    A simple verifier that checks if all required evidence exists in the local pool.
    """
    required_ids = [ev.source_id for ev in claim.evidence]
    pool_ids = [ev.source_id for ev in local_pool]
    
    for req_id in required_ids:
        if req_id not in pool_ids:
            return VerificationStatus.PENDING # Missing evidence
            
    return VerificationStatus.VERIFIED

@pytest.mark.asyncio
async def test_live_enp_exchange():
    """
    Tests live synchronization between two nodes using ENP over WebSockets.
    Node A has evidence. Node B has a claim. 
    Node A broadcasts evidence, Node B receives it, then Node A broadcasts the claim, 
    and Node B successfully verifies it.
    """
    # 1. Setup Nodes
    node_a = WebSocketFederationNode(node_id="NodeA", host="localhost", port=8001, local_verifier=mock_verifier)
    node_b = WebSocketFederationNode(node_id="NodeB", host="localhost", port=8002, local_verifier=mock_verifier)
    
    # 2. Start Servers
    await node_a.start_server()
    await node_b.start_server()
    
    try:
        # 3. Connect A to B
        node_a.add_peer("ws://localhost:8002")
        
        # 4. Create Evidence and Claim on Node A
        ev = EpistemicEvidence(source_id="EVID_01", source_type="Observation", extracted_text="Important data")
        claim = Claim(
            claim_id="CLAIM_01", 
            claim_text="Data is valid", 
            generated_by="A", 
            assumptions=[], 
            evidence=[ev],
            verification_status=VerificationStatus.VERIFIED
        )
        
        # Node B initially has NO evidence and NO accepted claims
        assert "EVID_01" not in node_b.evidence_pool
        assert len(node_b.accepted_claims) == 0
        
        # 5. Broadcast Evidence from A
        await node_a.broadcast_evidence(ev)
        
        # Give asyncio loop a moment to process the socket message
        await asyncio.sleep(0.1)
        
        # Verify Node B received the evidence
        assert "EVID_01" in node_b.evidence_pool
        assert node_b.evidence_pool["EVID_01"].extracted_text == "Important data"
        
        # 6. Broadcast Claim from A
        await node_a.broadcast_claim(claim)
        
        # Give asyncio loop a moment to process the socket message
        await asyncio.sleep(0.1)
        
        # Verify Node B received, evaluated, and accepted the claim
        assert len(node_b.accepted_claims) == 1
        accepted = node_b.accepted_claims[0]
        assert accepted.claim_id == "CLAIM_01"
        assert accepted.verification_status == VerificationStatus.VERIFIED
        
    finally:
        # 7. Cleanup
        await node_a.stop_server()
        await node_b.stop_server()
