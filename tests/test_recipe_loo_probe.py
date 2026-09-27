"""RECIPE-LOO verdict classification tests (round 434, preregistered)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from benchmarks.recipe_loo_probe import (  # noqa: E402
    ARM_A, ARM_B, HARM_GATE, LOAD_GATE, LOO_AXES, classify_loo, loo_arm)


def _mses(mean_b=2.0, loo_mult=1.0, mean_a=2.96, per_axis=None):
    """Build a synthetic mse dict: arm A/B plus one LOO arm per axis.

    loo_mult scales every LOO arm mean; per_axis overrides single axes
    with an explicit multiplier.
    """
    return {"A": [mean_a * 1.1, mean_a, mean_a * 0.9],
            "B": [mean_b * 1.1, mean_b, mean_b * 0.9],
            **{f"B\\{axis}": [mean_b * m * 1.1, mean_b * m,
                              mean_b * m * 0.9]
               for axis, m in ((a, (per_axis or {}).get(a, loo_mult))
                               for a in LOO_AXES)}}


def test_loo_arm_reverts_single_axis():
    for axis in LOO_AXES:
        arm = loo_arm(axis)
        assert arm[axis] == ARM_A[axis]
        assert sum(1 for a in LOO_AXES if arm[a] != ARM_B[a]) == 1
        others = [a for a in LOO_AXES if a != axis]
        assert all(arm[a] == ARM_B[a] for a in others)


def test_all_load_bearing():
    verdict, stats = classify_loo(_mses(loo_mult=1.2))
    assert verdict == "RECIPE_LOO_ALL_LOAD"
    assert stats["harmful_axes"] == []
    assert sorted(stats["load_bearing_axes"]) == sorted(LOO_AXES)
    assert "synergy" in stats["decision"]


def test_harmful_axis_trims_candidate():
    verdict, stats = classify_loo(_mses(per_axis={"warmup_steps": 0.8}))
    assert verdict == "RECIPE_LOO_HARMFUL"
    assert stats["harmful_axes"] == ["warmup_steps"]
    assert "trim" in stats["decision"]
    # non-harmful axes still classified
    assert stats["axes"]["depth"]["class"] in ("LOAD_BEARING", "NEUTRAL")


def test_partial_mixed():
    verdict, stats = classify_loo(_mses(loo_mult=1.0))
    assert verdict == "RECIPE_LOO_PARTIAL"
    assert stats["harmful_axes"] == []
    assert "unchanged" in stats["decision"]
    for axis in LOO_AXES:
        assert stats["axes"][axis]["class"] == "NEUTRAL"


def test_per_axis_stats_carry_am028_g3_fields():
    _, stats = classify_loo(_mses(loo_mult=1.2))
    for axis in LOO_AXES:
        entry = stats["axes"][axis]
        assert entry["direction_consistency"].endswith("/3 (loo>B)")
        assert entry["seed_spread_loo"] > 0
        assert len(entry["mses_loo"]) == 3


def test_divergence_negative():
    mses = _mses(loo_mult=1.2)
    mses["B\\depth"] = [float("nan"), 2.0, 2.1]
    verdict, stats = classify_loo(mses)
    assert verdict == "RECIPE_ARM_DIVERGED"
    assert "non-finite" in stats["reason"]


def test_gate_values_preregistered():
    assert LOAD_GATE == 1.05
    assert HARM_GATE == 0.95
    assert len(LOO_AXES) == 5
