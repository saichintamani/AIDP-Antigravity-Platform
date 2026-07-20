import os
try:
    from supabase import create_client, Client
except ImportError:
    create_client = None
    Client = None
from aidp.intelligence.epistemic_models import EpistemicClaim

class EpistemicLedger:
    """
    Hackathon Upgrade: 
    Replaced local SQLite with Supabase PostgreSQL for cloud-native persistence.
    """
    def __init__(self) -> None:
        # Load from environment in production (e.g., Render)
        supabase_url: str = os.environ.get("SUPABASE_URL", "https://mock-supabase-url.supabase.co")
        supabase_key: str = os.environ.get("SUPABASE_KEY", "mock-anon-key")
        
        try:
            self.supabase: Client = create_client(supabase_url, supabase_key)
            self.cloud_enabled = True
        except Exception:
            self.cloud_enabled = False
            
    def append_claim(self, claim: EpistemicClaim) -> None:
        """Appends a claim directly to the Supabase Postgres ledger."""
        if not self.cloud_enabled:
            print("[Ledger] Supabase keys missing. Simulating write.")
            return

        data = {
            "claim_id": claim.claim_id,
            "claim_text": claim.claim_text,
            "generated_by": claim.generated_by,
            "timestamp": str(claim.timestamp),
            "assumptions": [a.model_dump() for a in claim.assumptions],
            "evidence": [e.model_dump() for e in claim.evidence],
            "confidence": claim.confidence.model_dump() if claim.confidence else None,
            "verification_status": claim.verification_status.value
        }
        
        # Insert into Supabase table 'claims'
        try:
            self.supabase.table("claims").insert(data).execute()
            print(f"[Ledger] Claim {claim.claim_id} synced to Supabase!")
        except Exception as e:
            print(f"[Ledger ERROR] Failed to sync to Supabase: {e}")

    def get_all_claims(self) -> list[dict]:
        """Retrieves all claims from Supabase."""
        if not self.cloud_enabled:
            return [{"mock": "data pending supabase auth"}]
            
        try:
            response = self.supabase.table("claims").select("*").execute()
            return response.data
        except Exception as e:
            print(f"[Ledger ERROR] Fetch failed: {e}")
            return []
