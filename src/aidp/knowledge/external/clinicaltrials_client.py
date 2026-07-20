import json
import urllib.parse
import urllib.request


class ClinicalTrialsClient:
    """
    Client for retrieving real-world clinical trial protocols from ClinicalTrials.gov API v2
    to test the Formal Verification Engine.
    """
    BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

    def search_trials(self, condition: str, max_results: int = 5) -> list[dict]:
        """
        Searches for clinical trials by condition and returns parsed methodology data.
        """
        try:
            # Query param for condition is 'query.cond'
            encoded_condition = urllib.parse.quote(condition)
            
            # Request specific fields to minimize payload size
            # Fields: protocolSection.designModule
            url = f"{self.BASE_URL}?query.cond={encoded_condition}&pageSize={max_results}&fields=NCTId,BriefTitle,DesignModule"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'AIDP-System/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            return self._parse_ct_json(data)
            
        except Exception as e:
            print(f"ClinicalTrials API Error: {e}")
            return []

    def _parse_ct_json(self, data: dict) -> list[dict]:
        results = []
        studies = data.get("studies", [])
        for study in studies:
            protocol = study.get("protocolSection", {})
            ident = protocol.get("identificationModule", {})
            design = protocol.get("designModule", {})
            
            nct_id = ident.get("nctId", "UNKNOWN")
            title = ident.get("briefTitle", "No Title")
            
            # Extract methodological components for formal verification
            phases = design.get("phases", [])
            design_info = design.get("designInfo", {})
            allocation = design_info.get("allocation", "")
            masking = design_info.get("maskingInfo", {}).get("masking", "")
            
            results.append({
                "nct_id": nct_id,
                "title": title,
                "phases": phases,
                "allocation": allocation,
                "masking": masking,
                "source": "ClinicalTrials.gov"
            })
        return results
