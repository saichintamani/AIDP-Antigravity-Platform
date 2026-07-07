import time
from typing import Any

from aidp.cognitive_core.curiosity_engine import CuriosityEngine
from aidp.cognitive_core.strategy_planner import StrategyPlanner
from aidp.knowledge.connectors.arxiv_connector import ArxivConnector
from aidp.knowledge.connectors.pubmed_connector import PubMedConnector
from aidp.knowledge.evaluation.evidence_scorer import EvidenceScorer
from aidp.knowledge.evolution.belief_revision import BeliefReviser
from aidp.knowledge.evolution.conflict_resolution import ContradictionDetector
from aidp.knowledge.extraction.paper_parser import PaperParser
from aidp.knowledge.world_model import WorldModel
from aidp.knowledge.evolution.versioning import WorldStateSnapshot


class SyncLoop:
    """
    Automated loop fetching, extracting, revising, hypothesizing, and planning.
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

    def run_sync_cycle(self, queries: list[str]) -> list[dict[str, Any]]:
        """
        Executes one full tick of the synchronization loop.
        """
        print("Starting Sync Cycle...")

        # 1. Fetch Papers
        all_provenance = []
        for q in queries:
            all_provenance.extend(self.pubmed.fetch_literature_provenance(q))
            all_provenance.extend(self.arxiv.fetch_literature_provenance(q))

        print(f"Fetched {len(all_provenance)} papers.")

        # 2. Extract & Score Knowledge
        extracted_data: list[dict[str, Any]] = []
        for prov in all_provenance:
            # Parse structured knowledge
            parsed = self.parser.parse_paper(prov.claim_text)

            # Score evidence quality
            scores = self.scorer.score_paper(parsed, prov.claim_text)

            # Update provenance base confidence based on evidence score
            prov.confidence_score = scores.get("base_confidence", 0.5)

            extracted_data.append({"provenance": prov, "structured": parsed, "scores": scores})

        # 3. Compare with World Model & Belief Revision
        for data in extracted_data:
            relations = data["structured"]["relations"]
            for rel in relations:
                # Mock adding to world model via belief revision
                # In real system, this checks if relationship already exists
                # and runs Subjective Logic consensus_fusion
                pass

        # 4. Conflict Detection
        state = WorldStateSnapshot(
            version_id="sync_head",
            parent_version_id=None,
            timestamp=time.time(),
            reason="sync",
            entities=self.world_model.entities,
            relationships=self.world_model.relationships
        )
        conflicts = self.detector.detect_conflicts(state)
        if conflicts:
            print(f"Detected {len(conflicts)} contradictions. Flagging for Debate.")

        # 5. Hypothesis Generation (Mocked for sync loop structure)
        new_hypotheses = [{"id": "h_new1", "target_entity": "p53", "impact": 0.8, "cost": 0.3}]

        # 6. Curiosity Ranking & Planning
        selected = self.planner.rank_and_select(new_hypotheses, top_n=1)
        print(f"Selected {len(selected)} hypotheses for next experiment phase.")

        return selected

    def start_daemon(self, queries: list[str], interval_seconds: int = 3600) -> None:
        """Runs the sync loop continuously."""
        while True:
            self.run_sync_cycle(queries)
            time.sleep(interval_seconds)
