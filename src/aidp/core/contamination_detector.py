import logging
import re
import numpy as np

logger = logging.getLogger(__name__)

class ContaminationDetector:
    """
    Detects if benchmark datasets have leaked into the pre-training data
    of target models using exact N-gram matching and memorization probing.
    """
    def __init__(self, n_gram_size: int = 7):
        self.n_gram_size = n_gram_size

    def scan_for_memorization(self, benchmark_text: str, generated_text: str) -> dict:
        """
        Calculates exact N-gram overlap between a benchmark test case 
        and the model's unprompted generation. High overlap = contamination.
        """
        def get_ngrams(text: str, n: int):
            # Clean and tokenize
            words = re.sub(r'[^a-zA-Z0-9\\s]', '', text.lower()).split()
            return set(tuple(words[i:i+n]) for i in range(len(words)-n+1))

        bench_ngrams = get_ngrams(benchmark_text, self.n_gram_size)
        gen_ngrams = get_ngrams(generated_text, self.n_gram_size)

        if not bench_ngrams:
            return {"contamination_score": 0.0, "is_contaminated": False, "overlapping_ngrams": []}

        overlap = bench_ngrams.intersection(gen_ngrams)
        overlap_ratio = len(overlap) / len(bench_ngrams)

        # Flagship standard: If even 10% of 7-grams exactly overlap, it's memorized.
        is_contaminated = overlap_ratio > 0.10

        return {
            "contamination_score": float(overlap_ratio),
            "is_contaminated": is_contaminated,
            "overlapping_ngrams": [" ".join(ngram) for ngram in overlap]
        }
