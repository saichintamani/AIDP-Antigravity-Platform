import math
from dataclasses import dataclass


@dataclass
class Opinion:
    belief: float
    disbelief: float
    uncertainty: float
    base_rate: float

    def __post_init__(self) -> None:
        if not math.isclose(self.belief + self.disbelief + self.uncertainty, 1.0, abs_tol=1e-5):
            raise ValueError(
                f"b + d + u must equal 1.0. Got: {self.belief + self.disbelief + self.uncertainty}"
            )


def consensus_fusion(op1: Opinion, op2: Opinion) -> Opinion:
    """
    Combines two subjective logic opinions using the Consensus Operator.
    Useful when fusing independent evidence from two sources.
    """
    denominator = op1.uncertainty + op2.uncertainty - (op1.uncertainty * op2.uncertainty)

    if denominator == 0:
        # Handling the case of absolute dogmatic certainty (simplified)
        # In full SL theory, limit handling is required.
        raise ValueError("Cannot fuse two perfectly dogmatic opinions without limit resolution.")

    b = (op1.belief * op2.uncertainty + op2.belief * op1.uncertainty) / denominator
    d = (op1.disbelief * op2.uncertainty + op2.disbelief * op1.uncertainty) / denominator
    u = (op1.uncertainty * op2.uncertainty) / denominator

    # Base rates are combined based on relative uncertainty
    a = (
        op1.base_rate * op2.uncertainty
        + op2.base_rate * op1.uncertainty
        - (op1.base_rate + op2.base_rate) * op1.uncertainty * op2.uncertainty
    ) / denominator

    return Opinion(belief=b, disbelief=d, uncertainty=u, base_rate=a)
