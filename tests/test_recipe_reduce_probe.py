"""RECIPE-REDUCE verdict classification tests (round 440, preregistered)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from benchmarks.recipe_reduce_probe import (  # noqa: E402
    ARM_A, ARM_B, ARM_B2, OK_GATE, WEAK_GATE, classify_reduce)


def _mses(mean_a=2.96, mean_b=2.64, mean_b2=2.70):
    return ([mean_a * 1.1, mean_a, mean_a * 0.9],
            [mean_b * 1.1, mean_b, mean_b * 0.9],
            [mean_b2 * 1.1, mean_b2, mean_b2 * 0.9])


def test_arm_b2_is_two_axis_composite():
    # reduced composite keeps only the two load-bearing axes (r434)
    assert ARM_B2["depth"] == ARM_B["depth"] == 4
    assert ARM_B2["warmup_steps"] == ARM_B["warmup_steps"] == 200
    for axis in ("lr_decay", "weight_decay", "k_train"):
        assert ARM_B2[axis] == ARM_A[axis]
        assert ARM_B2[axis] != ARM_B[axis]


def test_reduce_ok():
    verdict, stats = classify_reduce(*_mses(mean_b2=2.64))
    assert verdict == "RECIPE_REDUCE_OK"
    assert "trim" in stats["decision"]
    assert abs(stats["ratio_red"] - 1.0) < 1e-9


def test_reduce_weak_band():
    verdict, stats = classify_reduce(*_mses(mean_b2=2.85))
    assert verdict == "RECIPE_REDUCE_WEAK"
    assert "not gate-passing" in stats["decision"]


def test_reduce_no_interaction():
    verdict, stats = classify_reduce(*_mses(mean_b2=3.30))
    assert verdict == "RECIPE_REDUCE_NO"
    assert "interaction" in stats["decision"]


def test_ratio_b2_vs_a_reported():
    _, stats = classify_reduce(*_mses())
    assert stats["ratio_B2_vs_A"] < 1.0  # reduced composite still beats default
    assert stats["direction_consistency_B2_A"].endswith("(B2<A)")


def test_divergence_negative():
    a, b, b2 = _mses()
    b2[1] = float("nan")
    verdict, stats = classify_reduce(a, b, b2)
    assert verdict == "RECIPE_ARM_DIVERGED"
    assert "arm B2 seed 1" in stats["reason"]


def test_gate_values_preregistered():
    assert OK_GATE == 1.05
    assert WEAK_GATE == 1.15
