def dempster_combine(
    mass1: dict[frozenset[str], float], mass2: dict[frozenset[str], float]
) -> dict[frozenset[str], float]:
    """
    Combines two mass functions using Dempster's Rule of Combination.
    """
    combined: dict[frozenset[str], float] = {}
    conflict = 0.0

    for a, mass_a in mass1.items():
        for b, mass_b in mass2.items():
            intersection = a.intersection(b)
            product = mass_a * mass_b

            if not intersection:
                conflict += product
            else:
                combined[intersection] = combined.get(intersection, 0.0) + product

    if conflict == 1.0:
        raise ValueError("Mass functions are completely conflicting.")

    normalization = 1.0 - conflict

    # Normalize
    for k in combined:
        combined[k] /= normalization

    return combined
