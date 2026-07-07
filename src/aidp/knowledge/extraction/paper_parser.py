from typing import Any

from aidp.knowledge.provenance import ProvenanceEntry
from aidp.knowledge.world_model import ScientificEntity, ScientificRelationship


class PaperParser:
    """
    Extracts structured knowledge from scientific literature.
    Pipeline: Section -> Entity -> Relation -> Method -> Result -> Limitation -> Citation
    """

    def __init__(self, llm_provider: Any = None) -> None:
        self.llm = llm_provider

    def _extract_sections(self, text: str) -> dict[str, str]:
        # Mock sectioning
        return {
            "abstract": text,
            "methods": "Mock methods section",
            "results": "Mock results section",
            "limitations": "Mock limitations section",
        }

    def _extract_entities(self, text: str) -> list[ScientificEntity]:
        # Mock entity extraction
        # In a real system, we'd use a small NLP model (like SciBERT) or an LLM here.
        # Based on user feedback, we might use the LLM Gateway for structured schema.
        return [
            ScientificEntity(id="e1", name="p53", semantic_type="Protein"),
            ScientificEntity(id="e2", name="Cancer", semantic_type="Disease"),
        ]

    def _extract_relations(
        self, text: str, entities: list[ScientificEntity]
    ) -> list[ScientificRelationship]:
        # Mock relation extraction
        return [
            ScientificRelationship(
                id="r1",
                source_entity_id="e1",
                target_entity_id="e2",
                relation_type="Inhibits",
                provenance=ProvenanceEntry(
                    claim_text=text,
                    source_paper_doi="mock",
                    source_url="mock",
                    retriever_metadata={},
                    confidence_score=0.5,
                ),
            )
        ]

    def _extract_methods(self, methods_text: str) -> list[str]:
        return ["CRISPR-Cas9", "Western Blot"]

    def _extract_results(self, results_text: str) -> list[str]:
        return ["p53 overexpression reduced tumor size."]

    def _extract_limitations(self, limitations_text: str) -> list[str]:
        return ["Small sample size", "In vitro only"]

    def _extract_citations(self, text: str) -> list[str]:
        return ["10.1038/s41586-020-2169-0"]

    def parse_paper(self, paper_text: str) -> dict[str, Any]:
        """
        Runs the full extraction pipeline on a paper's text.
        """
        sections = self._extract_sections(paper_text)

        # We usually extract knowledge primarily from the abstract and results.
        core_text = sections.get("abstract", "") + " " + sections.get("results", "")

        entities = self._extract_entities(core_text)
        relations = self._extract_relations(core_text, entities)
        methods = self._extract_methods(sections.get("methods", ""))
        results = self._extract_results(sections.get("results", ""))
        limitations = self._extract_limitations(sections.get("limitations", ""))
        citations = self._extract_citations(paper_text)

        return {
            "entities": entities,
            "relations": relations,
            "methods": methods,
            "results": results,
            "limitations": limitations,
            "citations": citations,
        }
