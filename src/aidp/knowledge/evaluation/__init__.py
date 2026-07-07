import math
import time
from typing import Any, Dict


def compute_knowledge_score(
    provenance_completeness: float,
    semantic_similarity: float,
    structural_completeness: float,
    citation_validity: float,
    confidence: float,
    timestamp: float,
    retrieval_rank: int,
) -> float:
    """
    Computes a quantifiable 'Knowledge Score' out of 100 based on
    multiple dimensions of a retrieved cognitive object.

    Weights (example):
    - Provenance Completeness: 20%
    - Semantic Similarity: 30%
    - Structural Completeness: 10%
    - Citation Validity: 10%
    - Confidence: 10%
    - Freshness: 10%
    - Retrieval Rank Penalty: 10%
    """
    # 1. Provenance Completeness (0.0 to 1.0) * 20
    score_prov = max(0.0, min(1.0, provenance_completeness)) * 20.0

    # 2. Semantic Similarity (assuming cosine 0.0 to 1.0) * 30
    score_sem = max(0.0, min(1.0, semantic_similarity)) * 30.0

    # 3. Structural Completeness (0.0 to 1.0) * 10
    score_struct = max(0.0, min(1.0, structural_completeness)) * 10.0

    # 4. Citation Validity (0.0 to 1.0) * 10
    score_cite = max(0.0, min(1.0, citation_validity)) * 10.0

    # 5. Confidence (0.0 to 1.0) * 10
    score_conf = max(0.0, min(1.0, confidence)) * 10.0

    # 6. Freshness (decay over time) * 10
    # Let's say half-life is 365 days.
    age_seconds = time.time() - timestamp
    age_days = age_seconds / (60 * 60 * 24)
    # Simple exponential decay
    freshness = math.exp(-0.001 * max(0, age_days))
    score_fresh = max(0.0, min(1.0, freshness)) * 10.0

    # 7. Retrieval Rank Penalty (rank 1 = 1.0, rank 10 = 0.1) * 10
    rank_factor = 1.0 / max(1, retrieval_rank)
    score_rank = rank_factor * 10.0

    total_score = (
        score_prov + score_sem + score_struct + score_cite + score_conf + score_fresh + score_rank
    )
    return total_score


def calculate_retrieval_metrics(
    retrieved_ids: list[str], relevant_ids: list[str], k: int = 10
) -> dict[str, float]:
    """Calculates standard IR metrics."""
    if not relevant_ids:
        return {"precision": 0.0, "recall": 0.0, "mrr": 0.0, "hit_rate": 0.0}

    retrieved_k = retrieved_ids[:k]

    hits = sum(1 for doc_id in retrieved_k if doc_id in relevant_ids)

    precision_at_k = hits / k if k > 0 else 0.0
    recall_at_k = hits / len(relevant_ids) if relevant_ids else 0.0

    mrr = 0.0
    for i, doc_id in enumerate(retrieved_k):
        if doc_id in relevant_ids:
            mrr = 1.0 / (i + 1)
            break

    hit_rate = 1.0 if hits > 0 else 0.0

    # MAP (Simplified for a single query)
    ap = 0.0
    hits_so_far = 0
    for i, doc_id in enumerate(retrieved_k):
        if doc_id in relevant_ids:
            hits_so_far += 1
            ap += hits_so_far / (i + 1)

    map_score = ap / len(relevant_ids) if relevant_ids else 0.0

    return {
        f"precision@{k}": precision_at_k,
        f"recall@{k}": recall_at_k,
        "mrr": mrr,
        "map": map_score,
        "hit_rate": hit_rate,
    }
