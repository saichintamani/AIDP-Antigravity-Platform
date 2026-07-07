class DiscoveryValueEngine:
    """
    Calculates the master objective function for the laboratory.
    """

    def calculate_discovery_value(
        self, novelty: float, impact: float, eig: float, publication_prob: float
    ) -> float:
        """
        Calculates value: Novelty × Scientific Impact × Expected Information Gain × Publication Probability
        Returns a score from 0.0 to 1.0
        """
        # All inputs should be 0.0 to 1.0
        return novelty * impact * eig * publication_prob
