"""ANCHOR-PRECISION verdict tests (round 406): preregistered round-405
classification, pure-function pinned. Gate 0.10 = POOL-BITS 1.10
caliber; non-finite spread counts as fragile."""
import math

import pytest

from benchmarks.anchor_precision_probe import (
    PRECISION_GATE, classify_anchor_precision)


def _spreads(**vals):
    return {"A_pool160_k100": vals}


def test_robust_below_gate():
    v, s = classify_anchor_precision(_spreads(
        rollout_mse=1e-7, energy_drift_final=1e-9, energy_drift_max=0.05))
    assert v == "PRECISION_ANCHOR_ROBUST"
    assert s["max_spread"] <= PRECISION_GATE
    assert s["violations"] == {}


def test_fragile_single_violation():
    v, s = classify_anchor_precision(_spreads(
        rollout_mse=1e-7, energy_drift_final=0.11, energy_drift_max=1e-8))
    assert v == "PRECISION_ANCHOR_FRAGILE"
    assert s["max_spread"] == pytest.approx(0.11)
    assert s["violations"]["A_pool160_k100"]["readout"] == "energy_drift_final"


def test_nonfinite_counts_as_fragile():
    v, s = classify_anchor_precision(_spreads(
        rollout_mse=float("nan"), energy_drift_final=0.0,
        energy_drift_max=0.0))
    assert v == "PRECISION_ANCHOR_FRAGILE"
    assert s["violations"]["A_pool160_k100"]["finite"] is False


def test_gate_equals_pool_bits_caliber():
    assert PRECISION_GATE == pytest.approx(0.10)


def test_max_spread_across_arms():
    spreads = {"A_pool160_k100": {"rollout_mse": 0.01,
                                  "energy_drift_final": 0.02,
                                  "energy_drift_max": 0.03},
               "B_pool1100_k400": {"rollout_mse": 0.20,
                                   "energy_drift_final": 0.01,
                                   "energy_drift_max": 0.01}}
    v, s = classify_anchor_precision(spreads)
    assert v == "PRECISION_ANCHOR_FRAGILE"
    assert s["max_spread"] == pytest.approx(0.20)
    assert math.isfinite(s["max_spread"])
