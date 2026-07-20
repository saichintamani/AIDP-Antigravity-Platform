import uuid
from collections.abc import Callable

from aidp.federation.federation_models import FederatedEpistemicObject
from aidp.intelligence.epistemic_models import Claim, VerificationStatus


class FederationNode:
    """
    Represents an independent AIDP instance in the collective.
    Ensures that incoming federated claims are independently verified before adoption.
    """
    
    def __init__(self, node_id: str, local_verifier: Callable[[Claim], bool]):
        self.node_id = node_id
        # A callback or local engine that independently verifies claims
        # In a full system, this would be the local FormalVerificationEngine + TMS
        self.local_verifier = local_verifier
        
        # Local state
        self.accepted_claims: list[Claim] = []
        self.rejected_claims: list[Claim] = []
        
        # Simulated Network Peers
        self.peers: list[FederationNode] = []
        
    def connect(self, peer: 'FederationNode'):
        if peer not in self.peers:
            self.peers.append(peer)
            
    def broadcast(self, claim: Claim):
        """
        Packages a locally accepted claim and sends it to all connected peers.
        """
        # Ensure we only broadcast verified claims
        if getattr(claim.verification_status, 'value', claim.verification_status) != "verified":
            return
            
        fed_obj = FederatedEpistemicObject(
            federation_id=f"FED-{uuid.uuid4().hex[:8]}",
            sender_node_id=self.node_id,
            claim=claim,
            evidence=claim.evidence, # Forward the raw evidence
            sender_confidence=0.9 # Mock confidence
        )
        
        for peer in self.peers:
            peer.receive(fed_obj)
            
    def receive(self, obj: FederatedEpistemicObject):
        """
        Receives an epistemic object. Strips sender's verification status
        and subjects it to local independent verification.
        """
        # 1. Strip the sender's conclusion (force local evaluation)
        local_claim = obj.claim.model_copy(deep=True)
        local_claim.verification_status = VerificationStatus.PENDING
        
        # 2. Independent Verification
        is_valid = self.local_verifier(local_claim)
        
        # 3. Verdict
        if is_valid:
            local_claim.verification_status = VerificationStatus.VERIFIED
            self.accepted_claims.append(local_claim)
        else:
            local_claim.verification_status = VerificationStatus.REJECTED
            self.rejected_claims.append(local_claim)
