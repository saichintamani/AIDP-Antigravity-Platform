import json
import os
from abc import ABC, abstractmethod

from pydantic import TypeAdapter

from aidp.memory.institutional_models import (
    LongitudinalAssumption,
    LongitudinalFailureMode,
    LongitudinalReviewerStats,
    StrategyMemoryRecord,
)
from aidp.meta_learning.adaptation_models import AdaptationRecord


class InstitutionalMemoryRepository(ABC):
    """Abstract interface for longitudinal storage."""
    
    @abstractmethod
    def save_adaptation(self, record: AdaptationRecord) -> None: pass
    
    @abstractmethod
    def get_failure_mode(self, constraint_key: str) -> LongitudinalFailureMode | None: pass
    
    @abstractmethod
    def save_failure_mode(self, failure: LongitudinalFailureMode) -> None: pass
    
    @abstractmethod
    def get_reviewer_stats(self, persona: str) -> LongitudinalReviewerStats | None: pass
    
    @abstractmethod
    def save_reviewer_stats(self, stats: LongitudinalReviewerStats) -> None: pass

    @abstractmethod
    def get_assumption(self, assumption: str) -> LongitudinalAssumption | None: pass
    
    @abstractmethod
    def save_assumption(self, assumption: LongitudinalAssumption) -> None: pass
    
    @abstractmethod
    def save_strategy(self, strategy: StrategyMemoryRecord) -> None: pass


class JsonMemoryRepository(InstitutionalMemoryRepository):
    """A simple JSON file-based repository for proof-of-capability."""
    
    def __init__(self, base_dir: str = ".memory"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        
        self.adaptations_file = os.path.join(self.base_dir, "adaptations.json")
        self.failures_file = os.path.join(self.base_dir, "failures.json")
        self.reviewers_file = os.path.join(self.base_dir, "reviewers.json")
        self.assumptions_file = os.path.join(self.base_dir, "assumptions.json")
        self.strategies_file = os.path.join(self.base_dir, "strategies.json")
        
        self._init_files()
        
    def _init_files(self):
        for f in [self.adaptations_file, self.strategies_file]:
            if not os.path.exists(f):
                with open(f, 'w') as file:
                    json.dump([], file)
        
        for f in [self.failures_file, self.reviewers_file, self.assumptions_file]:
            if not os.path.exists(f):
                with open(f, 'w') as file:
                    json.dump({}, file)
                    
    # File I/O Helpers
    def _read_list(self, filepath: str, model):
        with open(filepath) as f:
            data = json.load(f)
            adapter = TypeAdapter(list[model])
            return adapter.validate_python(data)
            
    def _write_list(self, filepath: str, items: list):
        with open(filepath, 'w') as f:
            json.dump([item.model_dump(mode='json') for item in items], f, indent=2)
            
    def _read_dict(self, filepath: str, model):
        with open(filepath) as f:
            data = json.load(f)
            adapter = TypeAdapter(dict[str, model])
            return adapter.validate_python(data)
            
    def _write_dict(self, filepath: str, d: dict):
        with open(filepath, 'w') as f:
            out = {k: v.model_dump(mode='json') for k, v in d.items()}
            json.dump(out, f, indent=2)

    # Implementations
    def save_adaptation(self, record: AdaptationRecord) -> None:
        records = self._read_list(self.adaptations_file, AdaptationRecord)
        records.append(record)
        self._write_list(self.adaptations_file, records)

    def get_failure_mode(self, constraint_key: str) -> LongitudinalFailureMode | None:
        failures = self._read_dict(self.failures_file, LongitudinalFailureMode)
        return failures.get(constraint_key)

    def save_failure_mode(self, failure: LongitudinalFailureMode) -> None:
        failures = self._read_dict(self.failures_file, LongitudinalFailureMode)
        failures[failure.constraint_key] = failure
        self._write_dict(self.failures_file, failures)

    def get_reviewer_stats(self, persona: str) -> LongitudinalReviewerStats | None:
        stats = self._read_dict(self.reviewers_file, LongitudinalReviewerStats)
        return stats.get(persona)

    def save_reviewer_stats(self, stats: LongitudinalReviewerStats) -> None:
        all_stats = self._read_dict(self.reviewers_file, LongitudinalReviewerStats)
        all_stats[stats.persona] = stats
        self._write_dict(self.reviewers_file, all_stats)

    def get_assumption(self, assumption: str) -> LongitudinalAssumption | None:
        assumptions = self._read_dict(self.assumptions_file, LongitudinalAssumption)
        return assumptions.get(assumption)

    def save_assumption(self, assumption: LongitudinalAssumption) -> None:
        assumptions = self._read_dict(self.assumptions_file, LongitudinalAssumption)
        assumptions[assumption.assumption] = assumption
        self._write_dict(self.assumptions_file, assumptions)

    def save_strategy(self, strategy: StrategyMemoryRecord) -> None:
        strategies = self._read_list(self.strategies_file, StrategyMemoryRecord)
        strategies.append(strategy)
        self._write_list(self.strategies_file, strategies)

class ChromaMemoryRepository(JsonMemoryRepository):
    """
    A Vector DB implementation of Institutional Memory.
    Uses ChromaDB to store and retrieve past failures and strategies semantically.
    Falls back to JsonMemoryRepository for simple dict/list storage.
    """
    def __init__(self, base_dir: str = ".memory"):
        super().__init__(base_dir)
        import chromadb
        self.chroma_client = chromadb.PersistentClient(path=os.path.join(base_dir, "chroma"))
        self.failure_collection = self.chroma_client.get_or_create_collection(name="failures")
        self.strategy_collection = self.chroma_client.get_or_create_collection(name="strategies")
        
    def save_failure_mode(self, failure: LongitudinalFailureMode, case_year: int = None) -> None:
        super().save_failure_mode(failure)
        # Also save to Chroma for semantic recall
        doc_text = f"Constraint Failed: {failure.constraint_key}. Occurrences: {failure.total_occurrences}."
        metadata = {"constraint": failure.constraint_key, "count": failure.total_occurrences}
        if case_year:
            metadata["year"] = case_year
            
        self.failure_collection.upsert(
            documents=[doc_text],
            metadatas=[metadata],
            ids=[failure.constraint_key]
        )
        
    def save_strategy(self, strategy: StrategyMemoryRecord) -> None:
        super().save_strategy(strategy)
        doc_text = f"Lesson Learned: {strategy.lesson_learned}. Context: {strategy.question}"
        # We need a stable ID, we can use hash or just a uuid
        import uuid
        s_id = str(uuid.uuid4())
        self.strategy_collection.upsert(
            documents=[doc_text],
            metadatas=[{"lesson": strategy.lesson_learned}],
            ids=[s_id]
        )
        
    def query_relevant_failures(self, query_text: str, n_results: int = 3, current_year: int = None) -> list[str]:
        if self.failure_collection.count() == 0:
            return []
        
        n = min(n_results, self.failure_collection.count())
        query_kwargs = {
            "query_texts": [query_text],
            "n_results": n
        }
        
        if current_year is not None:
            query_kwargs["where"] = {"year": {"$lt": current_year}}
            
        try:
            results = self.failure_collection.query(**query_kwargs)
        except Exception as e:
            # Fallback if where filter fails due to empty metadata
            print(f"ChromaDB Query Warning: {e}")
            results = self.failure_collection.query(query_texts=[query_text], n_results=n)
            
        return results["documents"][0] if results and "documents" in results and results["documents"] else []
