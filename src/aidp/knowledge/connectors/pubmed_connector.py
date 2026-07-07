import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from aidp.knowledge.provenance import ProvenanceEntry


class PubMedConnector:
    """
    Connects to the NCBI E-utilities API to fetch biomedical literature metadata and abstracts.
    Wraps the extracted data into AIDP ProvenanceEntry objects to ensure strict epistemic tracking.
    """

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, email: str = "aidp_research@example.com", max_results: int = 5) -> None:
        self.email = email
        self.max_results = max_results

    def _search_pmids(self, query: str) -> list[str]:
        """Searches PubMed and returns a list of PMIDs."""
        url = f"{self.BASE_URL}/esearch.fcgi?db=pubmed&term={urllib.parse.quote(query)}&retmax={self.max_results}&retmode=json&email={self.email}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AIDP-Research-Bot/1.0"})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                return list(data.get("esearchresult", {}).get("idlist", []))
        except Exception as e:
            print(f"Error fetching PMIDs: {e}")
            return []

    def _fetch_abstracts(self, pmids: list[str]) -> list[dict[str, Any]]:
        """Fetches title, abstract, and DOI for a list of PMIDs."""
        if not pmids:
            return []

        id_str = ",".join(pmids)
        url = f"{self.BASE_URL}/efetch.fcgi?db=pubmed&id={id_str}&retmode=xml&email={self.email}"

        results = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AIDP-Research-Bot/1.0"})
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)

                for article in root.findall(".//PubmedArticle"):
                    pmid_node = article.find(".//PMID")
                    pmid = pmid_node.text if pmid_node is not None else None
                    title_node = article.find(".//ArticleTitle")
                    title = title_node.text if title_node is not None else "No Title"

                    abstract_texts = article.findall(".//AbstractText")
                    abstract = (
                        " ".join([t.text for t in abstract_texts if t.text])
                        if abstract_texts
                        else "No Abstract"
                    )

                    doi_node = article.find('.//ArticleId[@IdType="doi"]')
                    doi = doi_node.text if doi_node is not None else None

                    results.append({"pmid": pmid, "doi": doi, "title": title, "abstract": abstract})
        except Exception as e:
            print(f"Error fetching article details: {e}")

        return results

    def fetch_literature_provenance(self, query: str) -> list[ProvenanceEntry]:
        """
        Executes a search and returns raw ProvenanceEntry objects containing the literature metadata.
        This provides the raw material for the Knowledge Evolution Engine.
        """
        pmids = self._search_pmids(query)
        articles = self._fetch_abstracts(pmids)

        provenance_entries = []
        for art in articles:
            entry = ProvenanceEntry(
                claim_text=art["abstract"],  # The raw text from which claims will be extracted
                source_paper_doi=art["doi"] or f"PMID:{art['pmid']}",
                source_url=f"https://pubmed.ncbi.nlm.nih.gov/{art['pmid']}/",
                retriever_metadata={
                    "connector": "PubMedConnector",
                    "query": query,
                    "title": art["title"],
                },
                confidence_score=0.5,  # Base confidence before Debate/Fusion
            )
            provenance_entries.append(entry)

        return provenance_entries
