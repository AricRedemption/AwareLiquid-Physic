"""Tests for TOSA-CTX-DECOUPLE (round 241) preregistered verdict."""

import math

from benchmarks.tosa_decouple_probe import (
    BENEFICIAL_GATE,
    HARM_GATE,
    SENTINEL_T24,
    SENTINEL_T8,
    classify_decouple,
    mean,
)


def test_beneficial():
    verdict, d = classify_decouple([0.9, 0.9, 0.9], [1.0, 1.0, 1.0])
    assert verdict == "DEC_TRAIN_BENEFICIAL"
    assert d["ratio"] < BENEFICIAL_GATE
    assert "recipe-candidate" in d["decision"]


def test_null_interior():
    verdict, d = classify_decouple([1.02, 1.0, 0.99], [1.0, 1.1, 0.9])
    assert verdict == "DEC_TRAIN_NULL"
    assert "artifact" in d["decision"]


def test_gate_boundaries_are_null():
    # ratio exactly at either gate is NULL (preregistered intervals);
    # 19/20 and 21/20 are exactly representable at these magnitudes
    _, d_lo = classify_decouple([19.0, 19.0, 19.0], [20.0, 20.0, 20.0])
    assert d_lo["ratio"] == BENEFICIAL_GATE
    _, d_hi = classify_decouple([21.0, 21.0, 21.0], [20.0, 20.0, 20.0])
    assert d_hi["ratio"] == HARM_GATE


def test_harmful():
    verdict, d = classify_decouple([1.2, 1.1, 1.15], [1.0, 1.0, 1.0])
    assert verdict == "DEC_TRAIN_HARMFUL"
    assert "harmful" in d["decision"]


def test_divergence_checked_before_ratio():
    verdict, d = classify_decouple([0.5, math.inf, 0.5],
                                   [1.0, 1.0, 1.0])
    assert verdict == "DEC_ARM_DIVERGED"
    assert "t8" in d["reason"] and "seed 1" in d["reason"]
    verdict, d = classify_decouple([0.5, 0.5, 0.5], [1e7, 1.0, 1.0])
    assert verdict == "DEC_ARM_DIVERGED"
    assert "t24" in d["reason"]


def test_direction_consistency_and_spreads():
    # t8 wins on seeds 0/1, loses seed 2
    _, d = classify_decouple([0.9, 0.95, 1.5], [1.0, 1.0, 1.0])
    assert d["direction_consistency"] == "2/3"
    assert math.isclose(d["seed_spread_t24"], 1.0)
    assert math.isclose(d["seed_spread_t8"], 1.5 / 0.9)


def test_sentinel_values():
    assert SENTINEL_T24 == 3.5581917762756348
    assert SENTINEL_T8 == 3.4044134616851807


def test_mean():
    assert mean([1.0, 2.0, 3.0]) == 2.0
