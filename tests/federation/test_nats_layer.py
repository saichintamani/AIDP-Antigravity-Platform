import asyncio
from collections.abc import Callable

import pytest

from aidp.federation.nats_node import NatsFederationNode
from aidp.intelligence.epistemic_models import EpistemicClaim as Claim
from aidp.intelligence.epistemic_models import EpistemicEvidence, VerificationStatus


class MockNatsMessage:
    def __init__(self, data: bytes):
        self.data = data

class MockNatsClient:
    """
    A lightweight in-memory pub/sub broker simulating NATS for unit testing.
    """
    def __init__(self):
        self.subscriptions: dict[str, list[Callable]] = {}
        
    async def subscribe(self, subject: str, cb: Callable):
        if subject not in self.subscriptions:
            self.subscriptions[subject] = []
        self.subscriptions[subject].append(cb)
        
    async def publish(self, subject: str, payload: bytes):
        if subject in self.subscriptions:
            for cb in self.subscriptions[subject]:
                msg = MockNatsMessage(payload)
                # Ensure callback is run asynchronously to mimic real NATS client behavior
                asyncio.create_task(cb(msg))


def mock_verifier(claim: Claim, local_pool: list[EpistemicEvidence]) -> VerificationStatus:
    if len(claim.evidence) < 1:
        return VerificationStatus.PENDING
        
    required_ids = [ev.source_id for ev in claim.evidence]
    pool_ids = [ev.source_id for ev in local_pool]
    
    for req_id in required_ids:
        if req_id not in pool_ids:
            return VerificationStatus.PENDING
            
    return VerificationStatus.VERIFIED

@pytest.mark.asyncio
async def test_nats_pubsub_synchronization():
    """
    Tests that NatsFederationNode can successfully decouple communication 
    via Pub/Sub and still solve the evidence synchronization problem.
    """
    # 1. Setup Mock Broker
    broker = MockNatsClient()
    
    # 2. Setup Nodes using the shared broker
    node_a = NatsFederationNode("Node_A", broker, mock_verifier)
    node_b = NatsFederationNode("Node_B", broker, mock_verifier)
    
    # 3. Nodes subscribe to the broker topics
    await node_a.start()
    await node_b.start()
    
    # 4. Create Evidence and Claim on Node A
    ev = EpistemicEvidence(source_id="EV_NATS_1", source_type="PubSubObs", extracted_text="Decoupled data")
    claim = Claim(
        claim_id="CLAIM_NATS_1",
        claim_text="PubSub works",
        generated_by="Node_A",
        assumptions=[],
        evidence=[ev],
        verification_status=VerificationStatus.VERIFIED
    )
    
    # Initially Node B is ignorant
    assert "EV_NATS_1" not in node_b.evidence_pool
    assert len(node_b.accepted_claims) == 0
    
    # 5. Node A publishes Evidence to 'aidp.evidence.broadcast'
    await node_a.broadcast_evidence(ev)
    
    # Wait for async propagation
    await asyncio.sleep(0.1)
    
    # Verify Node B received it via the topic
    assert "EV_NATS_1" in node_b.evidence_pool
    
    # 6. Node A publishes Claim to 'aidp.claim.broadcast'
    await node_a.broadcast_claim(claim)
    
    # Wait for async propagation
    await asyncio.sleep(0.1)
    
    # Verify Node B evaluated and verified the claim based on the topic broadcast
    assert len(node_b.accepted_claims) == 1
    assert node_b.accepted_claims[0].claim_id == "CLAIM_NATS_1"
    assert node_b.accepted_claims[0].verification_status == VerificationStatus.VERIFIED
