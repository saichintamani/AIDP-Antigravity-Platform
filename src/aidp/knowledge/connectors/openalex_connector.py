import json
import urllib.parse
import urllib.request
from typing import Any

from aidp.knowledge.provenance import ProvenanceEntry


class OpenAlexConnector:
    """
    Connects to the OpenAlex API to fetch literature metadata and abstracts.
    Wraps the extracted data into AIDP ProvenanceEntry objects.
    """

    BASE_URL = "https://api.openalex.org/works"

    def __init__(self, max_results: int = 5, email: str = "aidp_research@example.com") -> None:
        self.max_results = max_results
        self.email = email

    def _fetch_abstracts(self, query: str) -> list[dict[str, Any]]:
        """Searches OpenAlex and returns metadata including abstract."""
        url = f"{self.BASE_URL}?search={urllib.parse.quote(query)}&per-page={self.max_results}&mailto={self.email}"

        results = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AIDP-Research-Bot/1.0"})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())

                for item in data.get("results", []):
                    title = item.get("title", "No Title")

                    # OpenAlex abstracts are often inverted index
                    abstract_inverted = item.get("abstract_inverted_index", {})
                    abstract = "No Abstract"
                    if abstract_inverted:
                        # Reconstruct abstract
                        word_index = []
                        for word, positions in abstract_inverted.items():
                            for pos in positions:
                                word_index.append((pos, word))
                        word_index.sort(key=lambda x: x[0])
                        abstract = " ".join([word for pos, word in word_index])

                    doi = item.get("doi")

                    results.append(
                        {"id": item.get("id"), "doi": doi, "title": title, "abstract": abstract}
                    )
        except Exception as e:
            print(f"Error fetching article details from OpenAlex: {e}")

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
                source_url=art["id"],
                retriever_metadata={
                    "connector": "OpenAlexConnector",
                    "query": query,
                    "title": art["title"],
                },
                confidence_score=0.5,
            )
            provenance_entries.append(entry)

        return provenance_entries
