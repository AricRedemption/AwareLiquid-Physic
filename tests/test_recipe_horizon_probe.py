"""Tests for RECIPE-HORIZON (round 252) preregistered verdict."""

import math

from benchmarks.recipe_horizon_probe import (
    FRAGILE_GATE,
    ROBUST_GATE,
    SENTINEL,
    RECIPE,
    classify_horizon,
    median,
)


def _mses(b_last):
    """A wins all horizons at 1.0; B per-horizon values [b100, b200,
    b400] scaled around it."""
    return ({100: [1.0, 1.0, 1.0], 200: [1.0, 1.0, 1.0],
             400: [1.0, 1.0, 1.0]},
            {100: [b_last, b_last, b_last], 200: [b_last, b_last, b_last],
             400: [b_last, b_last, b_last]})


def test_robust():
    ma, mb = _mses(0.9)
    ratios = {k: 0.9 for k in (100, 200, 400)}
    verdict, d = classify_horizon(ratios, ma, mb)
    assert verdict == "HORIZON_ROBUST"
    assert all(r < ROBUST_GATE for r in d["ratios"].values())
    assert "scope confirmed" in d["decision"]


def test_limited():
    ma, mb = _mses(1.0)
    ratios = {100: 0.9, 200: 0.93, 400: 1.0}
    verdict, d = classify_horizon(ratios, ma, mb)
    assert verdict == "HORIZON_LIMITED"
    assert "k100-200" in d["decision"]


def test_fragile():
    ma, mb = _mses(1.0)
    ratios = {100: 0.9, 200: 1.0, 400: 1.2}
    verdict, d = classify_horizon(ratios, ma, mb)
    assert verdict == "HORIZON_FRAGILE"
    assert "fragile" in d["decision"]


def test_divergence_checked_first():
    ma = {100: [1.0, math.inf, 1.0], 200: [1.0, 1.0, 1.0],
          400: [1.0, 1.0, 1.0]}
    mb = {100: [0.9, 0.9, 0.9], 200: [0.9, 0.9, 0.9],
          400: [0.9, 0.9, 0.9]}
    ratios = {100: 0.9, 200: 0.9, 400: 0.9}
    verdict, d = classify_horizon(ratios, ma, mb)
    assert verdict == "HORIZON_ARM_DIVERGED"
    assert "arm A" in d["reason"]


def test_per_horizon_consistency_and_spread():
    ma = {100: [1.0, 1.0, 1.0], 200: [1.0, 1.0, 1.0],
          400: [1.0, 1.0, 1.0]}
    mb = {100: [0.9, 0.9, 1.2], 200: [0.9, 0.9, 0.9],
          400: [0.9, 0.9, 0.9]}
    ratios = {100: 1.0, 200: 0.9, 400: 0.9}
    verdict, d = classify_horizon(ratios, ma, mb)
    assert verdict == "HORIZON_LIMITED"
    assert d["per_horizon"][100]["direction_consistency"] == "2/3"
    assert math.isclose(d["per_horizon"][100]["seed_spread_B"],
                        1.2 / 0.9)


def test_sentinel_and_recipe():
    assert SENTINEL == 3.5581917762756348
    assert RECIPE == {"depth": 4, "lr_decay": 0.999,
                      "weight_decay": 1e-4, "warmup_steps": 200,
                      "k_train": 4}


def test_median():
    assert median([1.0, 2.0, 3.0]) == 2.0
