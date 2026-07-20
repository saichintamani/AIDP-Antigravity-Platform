import asyncio
import time
from typing import Any

from aidp.cognitive_core.curiosity_engine import CuriosityEngine
from aidp.cognitive_core.strategy_planner import StrategyPlanner
from aidp.knowledge.connectors.arxiv_connector import ArxivConnector
from aidp.knowledge.connectors.pubmed_connector import PubMedConnector
from aidp.knowledge.evaluation.evidence_scorer import EvidenceScorer
from aidp.knowledge.evolution.belief_revision import BeliefReviser
from aidp.knowledge.evolution.conflict_resolution import ContradictionDetector
from aidp.knowledge.evolution.versioning import WorldStateSnapshot
from aidp.knowledge.extraction.paper_parser import PaperParser
from aidp.knowledge.world_model import WorldModel


class SyncLoop:
    """
    Automated asynchronous loop fetching, extracting, revising, hypothesizing, and planning.
    Upgraded for Phase 12 Scale to support massively parallel discovery sessions.
    """

    def __init__(
        self,
        world_model: WorldModel,
        belief_reviser: BeliefReviser,
        detector: ContradictionDetector,
    ):
        self.pubmed = PubMedConnector(max_results=2)
        self.arxiv = ArxivConnector(max_results=2)
        self.parser = PaperParser()
        self.scorer = EvidenceScorer()

        self.world_model = world_model
        self.belief_reviser = belief_reviser
        self.detector = detector

        self.curiosity = CuriosityEngine()
        self.planner = StrategyPlanner()

    async def run_discovery_session_async(self, query: str) -> dict[str, Any]:
        """
        Runs a single discovery session asynchronously. 
        In Phase 12, this fetches real data and processes it.
        """
        print(f"[{query}] Starting Async Discovery Session...")
        
        # Simulate network IO for external APIs
        await asyncio.sleep(0.1)
        
        all_provenance = self.pubmed.fetch_literature_provenance(query)
        all_provenance.extend(self.arxiv.fetch_literature_provenance(query))

        print(f"[{query}] Fetched {len(all_provenance)} papers.")

        extracted_data: list[dict[str, Any]] = []
        for prov in all_provenance:
            parsed = self.parser.parse_paper(prov.claim_text)
            scores = self.scorer.score_paper(parsed, prov.claim_text)
            prov.confidence_score = scores.get("base_confidence", 0.5)
            extracted_data.append({"provenance": prov, "structured": parsed, "scores": scores})

        # Simulate heavy compute (e.g. LLM debate)
        await asyncio.sleep(0.1)

        state = WorldStateSnapshot(
            version_id=f"sync_head_{query}",
            parent_version_id=None,
            timestamp=time.time(),
            reason="sync",
            entities=self.world_model.entities,
            relationships=self.world_model.relationships
        )
        conflicts = self.detector.detect_conflicts(state)
        
        new_hypotheses = [{"id": f"h_new_{query}", "target_entity": query, "impact": 0.8, "cost": 0.3}]
        selected = self.planner.rank_and_select(new_hypotheses, top_n=1)
        
        return {"query": query, "hypotheses": selected, "conflicts": len(conflicts)}

    async def run_parallel_batch(self, queries: list[str]) -> list[dict[str, Any]]:
        """
        Executes multiple discovery sessions in parallel using asyncio.gather.
        """
        print(f"Executing parallel batch for {len(queries)} queries...")
        tasks = [self.run_discovery_session_async(q) for q in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    def run_sync_cycle(self, queries: list[str]) -> list[dict[str, Any]]:
        """
        Synchronous wrapper for backwards compatibility.
        """
        return asyncio.run(self.run_parallel_batch(queries))

    async def start_daemon_async(self, queries: list[str], interval_seconds: int = 3600) -> None:
        """Runs the async sync loop continuously."""
        while True:
            await self.run_parallel_batch(queries)
            await asyncio.sleep(interval_seconds)
