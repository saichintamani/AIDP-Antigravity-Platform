def bayesian_update(
    prior: float, likelihood_given_h: float, likelihood_given_not_h: float
) -> float:
    """
    Computes P(H|E) using Bayes' Theorem.

    P(H|E) = [P(E|H) * P(H)] / [P(E|H) * P(H) + P(E|~H) * P(~H)]
    """
    p_h = prior
    p_not_h = 1.0 - prior

    p_e = (likelihood_given_h * p_h) + (likelihood_given_not_h * p_not_h)

    if p_e == 0:
        return prior  # Avoid division by zero

    return (likelihood_given_h * p_h) / p_e
