import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from aidp.knowledge.provenance import ProvenanceEntry


class ArxivConnector:
    """
    Connects to the arXiv API to fetch pre-print literature metadata and abstracts.
    Wraps the extracted data into AIDP ProvenanceEntry objects to ensure strict epistemic tracking.
    """

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self, max_results: int = 5) -> None:
        self.max_results = max_results

    def _fetch_abstracts(self, query: str) -> list[dict[str, Any]]:
        """Searches arXiv and returns metadata including abstract."""
        url = f"{self.BASE_URL}?search_query=all:{urllib.parse.quote(query)}&start=0&max_results={self.max_results}"

        results = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AIDP-Research-Bot/1.0"})
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)

                # Namespaces in arXiv XML
                ns = {
                    "atom": "http://www.w3.org/2005/Atom",
                    "arxiv": "http://arxiv.org/schemas/atom",
                }

                for entry in root.findall("atom:entry", ns):
                    id_elem = entry.find("atom:id", ns)
                    arxiv_id = id_elem.text if id_elem is not None else ""
                    title_elem = entry.find("atom:title", ns)
                    title = title_elem.text.replace("\n", " ").strip() if title_elem is not None and title_elem.text else ""
                    summary_elem = entry.find("atom:summary", ns)
                    summary = summary_elem.text.replace("\n", " ").strip() if summary_elem is not None and summary_elem.text else ""

                    # Extract DOI if present
                    doi = None
                    for link in entry.findall("atom:link", ns):
                        if link.attrib.get("title") == "doi":
                            doi = link.attrib.get("href")
                            break

                    results.append(
                        {"id": arxiv_id, "doi": doi, "title": title, "abstract": summary}
                    )
        except Exception as e:
            print(f"Error fetching article details from arXiv: {e}")

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
                    "connector": "ArxivConnector",
                    "query": query,
                    "title": art["title"],
                },
                confidence_score=0.4,  # Slightly lower base confidence for pre-prints vs PubMed
            )
            provenance_entries.append(entry)

        return provenance_entries
