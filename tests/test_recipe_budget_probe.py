"""RECIPE-BUDGET verdict classification tests (round 460, preregistered)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from benchmarks.recipe_budget_probe import (  # noqa: E402
    ANTAG_GATE, ARM_A, ARM_B, SYNERGIC_GATE, classify_budget)


def _mses(mean_a=2.96, mean_b=2.64):
    return ([mean_a * 1.1, mean_a, mean_a * 0.9],
            [mean_b * 1.1, mean_b, mean_b * 0.9])


def test_arms_match_round227_composite():
    assert ARM_A == {"depth": 2, "lr_decay": 1.0, "weight_decay": 0.0,
                     "warmup_steps": 0, "k_train": 8}
    assert ARM_B == {"depth": 4, "lr_decay": 0.999, "weight_decay": 1e-4,
                     "warmup_steps": 200, "k_train": 4}


def test_budget_robust():
    verdict, stats = classify_budget(*_mses())
    assert verdict == "RECIPE_BUDGET_ROBUST"
    assert "budget-robust" in stats["decision"]
    assert stats["direction_consistency"] == "3/3"


def test_budget_null_band():
    verdict, stats = classify_budget(*_mses(mean_b=2.90))
    assert verdict == "RECIPE_BUDGET_NULL"
    assert "2000-step regime only" in stats["decision"]


def test_budget_reversed():
    verdict, stats = classify_budget(*_mses(mean_b=3.30))
    assert verdict == "RECIPE_BUDGET_REVERSED"
    assert "budget-interaction" in stats["decision"]


def test_divergence_negative():
    a, b = _mses()
    b[2] = float("nan")
    verdict, stats = classify_budget(a, b)
    assert verdict == "RECIPE_ARM_DIVERGED"
    assert "arm B seed 2" in stats["reason"]


def test_gate_values_preregistered():
    assert SYNERGIC_GATE == 0.95
    assert ANTAG_GATE == 1.05
