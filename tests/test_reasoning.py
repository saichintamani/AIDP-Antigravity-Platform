import pytest

from aidp.reasoning.bayesian import bayesian_update
from aidp.reasoning.dempster_shafer import dempster_combine
from aidp.reasoning.subjective_logic import Opinion, consensus_fusion


def test_bayesian_update() -> None:
    result = bayesian_update(prior=0.01, likelihood_given_h=0.9, likelihood_given_not_h=0.09)
    assert abs(result - 0.0917) < 0.001

    result_zero = bayesian_update(prior=0.01, likelihood_given_h=0.0, likelihood_given_not_h=0.0)
    assert result_zero == 0.01


def test_dempster_combine() -> None:
    mass1 = {frozenset(["A"]): 0.4, frozenset(["A", "B"]): 0.6}
    mass2 = {frozenset(["B"]): 0.5, frozenset(["A", "B"]): 0.5}

    res = dempster_combine(mass1, mass2)
    assert frozenset(["A"]) in res
    assert frozenset(["B"]) in res
    assert frozenset(["A", "B"]) in res

    conflict_mass1 = {frozenset(["A"]): 1.0}
    conflict_mass2 = {frozenset(["B"]): 1.0}
    with pytest.raises(ValueError, match="conflicting"):
        dempster_combine(conflict_mass1, conflict_mass2)


def test_subjective_logic() -> None:
    op1 = Opinion(0.5, 0.0, 0.5, 0.5)
    op2 = Opinion(0.8, 0.1, 0.1, 0.5)

    res = consensus_fusion(op1, op2)
    assert res.belief > 0.8

    with pytest.raises(ValueError):
        Opinion(0.5, 0.5, 0.5, 0.5)

    dog1 = Opinion(1.0, 0.0, 0.0, 0.5)
    dog2 = Opinion(0.0, 1.0, 0.0, 0.5)
    with pytest.raises(ValueError):
        consensus_fusion(dog1, dog2)
