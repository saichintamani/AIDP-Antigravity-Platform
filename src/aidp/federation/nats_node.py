import json
from collections.abc import Callable

from aidp.federation.enp import (
    ClaimBroadcast,
    EvidenceBroadcast,
)
from aidp.intelligence.epistemic_models import EpistemicClaim as Claim
from aidp.intelligence.epistemic_models import EpistemicEvidence, VerificationStatus


class NatsFederationNode:
    """
    An asynchronous physical transport layer for the Epistemic Network Protocol (ENP)
    using a NATS Pub/Sub broker for horizontal scalability.
    """
    def __init__(self, node_id: str, nats_client, local_verifier: Callable[[Claim, list[EpistemicEvidence]], VerificationStatus]):
        self.node_id = node_id
        # nats_client could be a real nats.aio.client.Client or a MockNatsClient
        self.nc = nats_client 
        self.local_verifier = local_verifier
        
        # Local state
        self.accepted_claims: list[Claim] = []
        self.rejected_claims: list[Claim] = []
        self.evidence_pool: dict[str, EpistemicEvidence] = {}
        
    async def start(self):
        """Subscribes to all ENP topics on the NATS broker."""
        await self.nc.subscribe("aidp.evidence.broadcast", cb=self._handle_evidence)
        await self.nc.subscribe("aidp.claim.broadcast", cb=self._handle_claim)
        await self.nc.subscribe("aidp.contradiction.report", cb=self._handle_contradiction)
        await self.nc.subscribe("aidp.opportunity.broadcast", cb=self._handle_opportunity)
        
    async def broadcast_evidence(self, ev: EpistemicEvidence):
        """Publishes evidence to the NATS cluster."""
        broadcast = EvidenceBroadcast(
            evidence_id=ev.source_id,
            source=ev.source_type,
            payload=ev.extracted_text,
            is_retracted=getattr(ev, 'is_retracted', False)
        )
        await self.nc.publish("aidp.evidence.broadcast", json.dumps(broadcast.model_dump()).encode())
        
    async def broadcast_claim(self, claim: Claim):
        """Publishes a claim to the NATS cluster, strictly serialized via ENP."""
        broadcast = ClaimBroadcast.from_local_claim(claim)
        await self.nc.publish("aidp.claim.broadcast", json.dumps(broadcast.model_dump()).encode())
        
    async def _handle_evidence(self, msg):
        try:
            data = json.loads(msg.data.decode())
            enp_ev = EvidenceBroadcast(**data)
            
            local_ev = EpistemicEvidence(
                source_id=enp_ev.evidence_id,
                source_type=enp_ev.source,
                extracted_text=enp_ev.payload
            )
            if hasattr(local_ev, "is_retracted"):
                local_ev.is_retracted = enp_ev.is_retracted
                
            self.evidence_pool[local_ev.source_id] = local_ev
        except Exception as e:
            print(f"[{self.node_id}] Evidence parse error: {e}")
            
    async def _handle_claim(self, msg):
        try:
            data = json.loads(msg.data.decode())
            enp_claim = ClaimBroadcast(**data)
            
            # Resolve evidence from local pool
            claim_evidence = []
            for ev_id in enp_claim.evidence_ids:
                if ev_id in self.evidence_pool:
                    claim_evidence.append(self.evidence_pool[ev_id])
                    
            local_claim = Claim(
                claim_id=enp_claim.claim_id,
                claim_text=enp_claim.claim_text,
                generated_by="Network",
                assumptions=enp_claim.assumptions,
                evidence=claim_evidence,
                verification_status=VerificationStatus.PENDING
            )
            
            # Pass through independent local verifier
            status = self.local_verifier(local_claim, list(self.evidence_pool.values()))
            local_claim.verification_status = status
            
            if status == VerificationStatus.VERIFIED:
                self.accepted_claims.append(local_claim)
            elif status == VerificationStatus.REJECTED:
                self.rejected_claims.append(local_claim)
                
        except Exception as e:
            print(f"[{self.node_id}] Claim parse error: {e}")
            
    async def _handle_contradiction(self, msg):
        # To be implemented by the TMS
        pass
        
    async def _handle_opportunity(self, msg):
        # To be implemented by the Strategic Intelligence Layer
        pass
