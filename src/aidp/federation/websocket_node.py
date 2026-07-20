import json
from collections.abc import Callable

import websockets

from aidp.federation.enp import ClaimBroadcast, EvidenceBroadcast
from aidp.intelligence.epistemic_models import EpistemicClaim as Claim
from aidp.intelligence.epistemic_models import EpistemicEvidence, VerificationStatus


class WebSocketFederationNode:
    """
    An asynchronous physical transport layer for the Epistemic Network Protocol (ENP).
    Wraps local verification logic, hosts a WebSocket server, and acts as a client to peers.
    """
    def __init__(self, node_id: str, host: str, port: int, local_verifier: Callable[[Claim, list[EpistemicEvidence]], VerificationStatus]):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.local_verifier = local_verifier
        
        # Local state
        self.peers: list[str] = [] # List of ws:// URIs
        self.accepted_claims: list[Claim] = []
        self.rejected_claims: list[Claim] = []
        
        # Local knowledge base to store incoming evidence
        self.evidence_pool: dict[str, EpistemicEvidence] = {}
        
        self.server: websockets.WebSocketServer | None = None
        
    async def start_server(self):
        """Starts the WebSocket server listening for inbound ENP messages."""
        self.server = await websockets.serve(self._handle_inbound, self.host, self.port)
        
    async def stop_server(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            
    def add_peer(self, peer_uri: str):
        if peer_uri not in self.peers:
            self.peers.append(peer_uri)
            
    async def broadcast_evidence(self, ev: EpistemicEvidence):
        """Broadcasts evidence to all peers via ENP EvidenceBroadcast."""
        broadcast = EvidenceBroadcast(
            evidence_id=ev.source_id,
            source=ev.source_type,
            payload=ev.extracted_text,
            is_retracted=getattr(ev, 'is_retracted', False)
        )
        await self._broadcast_payload({"type": "EvidenceBroadcast", "data": broadcast.model_dump()})
        
    async def broadcast_claim(self, claim: Claim):
        """Broadcasts a claim using the ENP strict serializer."""
        broadcast = ClaimBroadcast.from_local_claim(claim)
        await self._broadcast_payload({"type": "ClaimBroadcast", "data": broadcast.model_dump()})
        
    async def _broadcast_payload(self, payload: dict):
        message = json.dumps(payload)
        for peer_uri in self.peers:
            try:
                async with websockets.connect(peer_uri) as websocket:
                    await websocket.send(message)
            except Exception as e:
                # Log failure, continue to next peer
                print(f"[{self.node_id}] Failed to send to {peer_uri}: {e}")
                
    async def _handle_inbound(self, websocket):
        """Handles incoming WebSocket messages."""
        async for message in websocket:
            try:
                payload = json.loads(message)
                msg_type = payload.get("type")
                data = payload.get("data")
                
                if msg_type == "EvidenceBroadcast":
                    enp_ev = EvidenceBroadcast(**data)
                    # Convert ENP to local EpistemicEvidence
                    local_ev = EpistemicEvidence(
                        source_id=enp_ev.evidence_id,
                        source_type=enp_ev.source,
                        extracted_text=enp_ev.payload
                    )
                    if hasattr(local_ev, "is_retracted"):
                        local_ev.is_retracted = enp_ev.is_retracted
                    self.evidence_pool[local_ev.source_id] = local_ev
                    
                elif msg_type == "ClaimBroadcast":
                    enp_claim = ClaimBroadcast(**data)
                    
                    # Resolve evidence from local pool
                    claim_evidence = []
                    for ev_id in enp_claim.evidence_ids:
                        if ev_id in self.evidence_pool:
                            claim_evidence.append(self.evidence_pool[ev_id])
                            
                    # Construct a pending local claim
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
                print(f"[{self.node_id}] Error processing message: {e}")
