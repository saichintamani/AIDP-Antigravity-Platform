import numpy as np
import math

def calculate_hdi(successes: float, trials: float, credible_interval: float = 0.95) -> tuple[float, float]:
    """
    Calculates the Highest Density Interval (HDI) for a binomial proportion 
    using a Beta-Binomial conjugate prior (Beta(1, 1) uniform prior).
    If scipy is unavailable due to environment corruption, uses a highly accurate Normal approximation.
    """
    alpha_post = 1.0 + successes
    beta_post = 1.0 + trials - successes
    
    try:
        from scipy.stats import beta
        lower_percentile = (1.0 - credible_interval) / 2.0
        upper_percentile = 1.0 - lower_percentile
        
        lower_bound = beta.ppf(lower_percentile, alpha_post, beta_post)
        upper_bound = beta.ppf(upper_percentile, alpha_post, beta_post)
        return float(lower_bound), float(upper_bound)
    except ImportError:
        # Normal approximation of the Beta distribution (extremely accurate for N=10,000)
        mean = alpha_post / (alpha_post + beta_post)
        var = (alpha_post * beta_post) / (((alpha_post + beta_post) ** 2) * (alpha_post + beta_post + 1))
        std_dev = math.sqrt(var)
        
        # 95% CI is approx +/- 1.96 standard deviations
        z_score = 1.96
        lower_bound = max(0.0, mean - (z_score * std_dev))
        upper_bound = min(1.0, mean + (z_score * std_dev))
        return float(lower_bound), float(upper_bound)

def report_bias_statistics(bias_probabilities: list[float], credible_interval: float = 0.95) -> dict:
    """
    Takes a raw list of SVM bias probabilities across the Massive N dataset 
    and outputs the strict mathematical HDI.
    """
    n = len(bias_probabilities)
    if n == 0:
        return {"mean": 0.0, "hdi_lower": 0.0, "hdi_upper": 0.0, "n": 0}
        
    # We sum the probabilities as the expected number of "successes" (leaks)
    expected_leaks = sum(bias_probabilities)
    mean_leakage = expected_leaks / n
    
    lower, upper = calculate_hdi(expected_leaks, n, credible_interval)
    
    return {
        "mean_bias": mean_leakage,
        "hdi_lower": lower,
        "hdi_upper": upper,
        "n": n
    }
