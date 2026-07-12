import json
from pathlib import Path
from dataclasses import asdict
import sys

# Ensure aidp can be imported
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aidp.knowledge.connectors.pubmed_connector import PubMedConnector

def main():
    base_dir = Path(__file__).parent.parent
    dataset_path = base_dir / "src" / "aidp" / "evaluation" / "data" / "discovery_bench_v1.json"
    evidence_dir = base_dir / "docs" / "evaluation" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    cache_file = evidence_dir / "BENCHMARK_CORPUS_CACHE.json"
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    retrieval_cache = {}
    if cache_file.exists():
        with open(cache_file, "r") as f:
            retrieval_cache = json.load(f)
            
    connector = PubMedConnector()
    print(f"Pre-warming cache for {len(dataset)} cases...")
    
    added = 0
    for case in dataset:
        query = case["query"]
        max_date = case.get("historical_cutoff_date")
        cache_key = f"{query}_{max_date}"
        
        if cache_key in retrieval_cache:
            print(f"Skipping {case['id']} (already cached)")
            continue
            
        print(f"Fetching {case['id']}...")
        results = connector.fetch_literature_provenance(query, max_date=max_date)
        retrieval_cache[cache_key] = [asdict(r) for r in results]
        added += 1
        
    with open(cache_file, "w") as f:
        json.dump(retrieval_cache, f, indent=2)
        
    print(f"Cache pre-warming complete. Added {added} new entries. Total cached queries: {len(retrieval_cache)}")

if __name__ == "__main__":
    main()
