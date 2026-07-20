import math

from aidp.reasoning.subjective_logic import Opinion


def calculate_entropy(opinion: Opinion) -> float:
    """
    Calculates the Shannon Entropy of an Opinion.
    In Subjective Logic, we can map the projected probability to entropy.
    P(x) = belief + (base_rate * uncertainty)
    """
    p = opinion.belief + (opinion.base_rate * opinion.uncertainty)
    
    # Avoid log(0)
    if p <= 0.0 or p >= 1.0:
        return 0.0
        
    entropy = - (p * math.log2(p) + (1 - p) * math.log2(1 - p))
    return entropy

def calculate_eig(prior: Opinion, expected_posterior: Opinion) -> float:
    """
    Calculates Expected Information Gain (EIG).
    EIG = H(Prior) - H(Expected Posterior)
    
    If the posterior has lower entropy (uncertainty is reduced), the EIG is positive.
    """
    prior_entropy = calculate_entropy(prior)
    posterior_entropy = calculate_entropy(expected_posterior)
    
    eig = prior_entropy - posterior_entropy
    return max(0.0, eig) # EIG shouldn't be negative in this context, floor it at 0
