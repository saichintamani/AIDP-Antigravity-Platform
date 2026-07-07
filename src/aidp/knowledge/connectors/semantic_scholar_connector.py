import json
import urllib.parse
import urllib.request
from typing import Optional, Any

from aidp.knowledge.provenance import ProvenanceEntry


class SemanticScholarConnector:
    """
    Connects to the Semantic Scholar API to fetch literature metadata and abstracts.
    Wraps the extracted data into AIDP ProvenanceEntry objects.
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def __init__(self, max_results: int = 5, api_key: Optional[str] = None) -> None:
        self.max_results = max_results
        self.api_key = api_key

    def _fetch_abstracts(self, query: str) -> list[dict[str, Any]]:
        """Searches Semantic Scholar and returns metadata including abstract."""
        url = f"{self.BASE_URL}?query={urllib.parse.quote(query)}&limit={self.max_results}&fields=title,abstract,url,externalIds"

        results = []
        try:
            headers = {"User-Agent": "AIDP-Research-Bot/1.0"}
            if self.api_key:
                headers["x-api-key"] = self.api_key

            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())

                for item in data.get("data", []):
                    title = item.get("title", "No Title")
                    abstract = item.get("abstract") or "No Abstract"
                    url_link = item.get("url")
                    external_ids = item.get("externalIds", {})
                    doi = external_ids.get("DOI")

                    results.append(
                        {
                            "id": item.get("paperId"),
                            "doi": doi,
                            "url": url_link,
                            "title": title,
                            "abstract": abstract,
                        }
                    )
        except Exception as e:
            print(f"Error fetching article details from Semantic Scholar: {e}")

        return results

    def fetch_literature_provenance(self, query: str) -> list[ProvenanceEntry]:
        """
        Executes a search and returns raw ProvenanceEntry objects containing the literature metadata.
        """
        articles = self._fetch_abstracts(query)

        provenance_entries = []
        for art in articles:
            entry = ProvenanceEntry(
                claim_text=art["abstract"],
                source_paper_doi=art["doi"] or art["id"],
                source_url=art["url"] or f"https://www.semanticscholar.org/paper/{art['id']}",
                retriever_metadata={
                    "connector": "SemanticScholarConnector",
                    "query": query,
                    "title": art["title"],
                },
                confidence_score=0.5,
            )
            provenance_entries.append(entry)

        return provenance_entries
