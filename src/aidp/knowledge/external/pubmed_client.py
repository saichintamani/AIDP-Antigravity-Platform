import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


class PubMedClient:
    """
    Client for retrieving real-world empirical evidence from the NCBI PubMed database
    using the E-utilities API.
    """
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, email="aidp.system@example.com"):
        self.email = email

    def search_abstracts(self, query: str, max_results: int = 5) -> list[dict]:
        """
        Searches PubMed and returns a list of dictionaries containing title, abstract, and PMID.
        """
        try:
            # 1. ESearch to get PMIDs
            encoded_query = urllib.parse.quote(query)
            esearch_url = f"{self.BASE_URL}/esearch.fcgi?db=pubmed&term={encoded_query}&retmax={max_results}&retmode=json&email={self.email}"
            
            with urllib.request.urlopen(esearch_url, timeout=10) as response:
                search_data = json.loads(response.read().decode())
                
            pmids = search_data.get("esearchresult", {}).get("idlist", [])
            if not pmids:
                return []

            # 2. EFetch to get Abstract text (XML format is easiest to parse for abstracts)
            pmid_str = ",".join(pmids)
            efetch_url = f"{self.BASE_URL}/efetch.fcgi?db=pubmed&id={pmid_str}&retmode=xml&email={self.email}"
            
            with urllib.request.urlopen(efetch_url, timeout=10) as response:
                xml_data = response.read()
                
            return self._parse_pubmed_xml(xml_data)
            
        except Exception as e:
            # Fallback for network issues / rate limiting
            print(f"PubMed API Error: {e}")
            return []

    def _parse_pubmed_xml(self, xml_string: bytes) -> list[dict]:
        results = []
        try:
            root = ET.fromstring(xml_string)
            for article in root.findall(".//PubmedArticle"):
                pmid = article.findtext(".//PMID")
                title = article.findtext(".//ArticleTitle")
                
                abstract_texts = article.findall(".//AbstractText")
                abstract = " ".join([elem.text for elem in abstract_texts if elem.text])
                
                if abstract:
                    results.append({
                        "pmid": pmid,
                        "title": title,
                        "abstract": abstract,
                        "source": "PubMed"
                    })
        except Exception:
            pass
        return results
