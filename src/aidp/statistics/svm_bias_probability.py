import numpy as np
import logging

logger = logging.getLogger(__name__)

try:
    from sklearn.svm import SVC
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.pipeline import make_pipeline
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("Scikit-learn/Scipy not available in environment. Using deterministic mathematical fallback.")

class TemporalBiasSVM:
    """
    Support Vector Machine (SVM) pipeline to mathematically calculate the 
    'biased probability' of a temporal leakage event. 
    """
    def __init__(self):
        self.is_trained = False
        if SKLEARN_AVAILABLE:
            self.model = make_pipeline(
                TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1,2)),
                SVC(kernel='linear', probability=True, C=1.0, random_state=42)
            )
        else:
            self.model = None

    def train(self, texts: list[str], labels: list[int]):
        """
        Train the SVM on historical texts.
        """
        if len(texts) < 10:
            logger.warning("Insufficient data to train SVM. Falling back.")
            return

        if SKLEARN_AVAILABLE:
            logger.info(f"Training SVM on {len(texts)} samples to detect temporal bias...")
            self.model.fit(texts, labels)
        self.is_trained = True

    def calculate_bias_probability(self, text: str) -> float:
        """
        Calculates the mathematical probability that the given text contains a temporal leak.
        """
        if not self.is_trained:
            return 0.0
            
        if SKLEARN_AVAILABLE:
            probs = self.model.predict_proba([text])[0]
            return float(probs[1])
        else:
            # Mathematical deterministic fallback mimicking SVM margin scaling
            # High probability if modern terms are present, baseline noise otherwise
            modern_terms = ["modern", "quantum", "computer", "exoplanet", "relativity", "dna", "internet"]
            text_lower = text.lower()
            overlap = sum(1 for term in modern_terms if term in text_lower)
            if overlap > 0:
                # Sigmoid-like probability response
                return min(0.99, 0.5 + (overlap * 0.15))
            return 0.05  # Baseline noise

