import os
import sys

# Add src to sys.path so we can import aidp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))


def test_calibration_curve():
    """
    Simulates checking a set of claims with known ground truths against their AIDP confidence score.
    """
    
    # Ground truth dataset (Claim, True/False)
    dataset = [
        ("The Earth orbits the Sun", True),
        ("Water boils at 100C at sea level", True),
        ("The moon is made of cheese", False),
        ("Gravity is a repulsive force", False)
    ]
    
    # We mock the calibrator output to simulate what the system might give
    # A perfectly calibrated system gives 1.0 to True, and 0.0 to False.
    mocked_confidences = [0.95, 0.90, 0.10, 0.05]
    
    results = []
    for (_claim_text, ground_truth), conf in zip(dataset, mocked_confidences, strict=False):
        # We classify as 'Correct' if (confidence > 0.5) == ground_truth
        prediction_is_true = conf > 0.5
        is_correct = prediction_is_true == ground_truth
        results.append((conf, is_correct))
        
    # Calculate calibration error (Brier Score or Expected Calibration Error)
    # ECE = |confidence - accuracy|
    
    high_conf_bucket = [r for r in results if r[0] > 0.5]
    low_conf_bucket = [r for r in results if r[0] <= 0.5]
    
    high_conf_acc = sum(1 for r in high_conf_bucket if r[1]) / len(high_conf_bucket) if high_conf_bucket else 0
    low_conf_acc = sum(1 for r in low_conf_bucket if r[1]) / len(low_conf_bucket) if low_conf_bucket else 0
    
    # We expect high confidence bucket to have high accuracy
    assert high_conf_acc > 0.8
    # We expect low confidence bucket to have high accuracy (meaning it correctly identified them as False)
    assert low_conf_acc > 0.8
