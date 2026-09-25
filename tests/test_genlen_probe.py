"""Tests for GENLEN-PROBE (round 255) preregistered verdict."""

import math

from benchmarks.genlen_probe import (
    SENTINEL_160,
    SENTINEL_301,
    SPREAD_GATE,
    classify_genlen,
    median,
)


def test_unresolvable():
    verdict, d = classify_genlen({160: 3.55, 301: 3.60, 450: 3.57})
    assert verdict == "GENLEN_UNRESOLVABLE"
    assert d["spread"] < SPREAD_GATE
    assert "saturated" in d["decision"]


def test_resolved():
    verdict, d = classify_genlen({160: 3.55, 301: 2.90, 450: 2.80})
    assert verdict == "GENLEN_RESOLVED"
    assert d["spread"] >= SPREAD_GATE
    assert d["best_gen_steps"] == 450
    assert "free improvement candidate" in d["decision"]


def test_gate_boundary():
    # spread exactly at the gate resolves (preregistered >=)
    _, d = classify_genlen({160: 1.0, 301: 1.05})
    assert d["spread"] == SPREAD_GATE


def test_divergence_checked_first():
    verdict, d = classify_genlen({160: float("nan"), 301: 2.9})
    assert verdict == "GENLEN_ARM_DIVERGED"
    assert "gen160" in d["reason"]


def test_sentinels():
    assert SENTINEL_160 == 3.5581917762756348
    assert SENTINEL_301 == 2.9031009674072266


def test_median():
    assert median([1.0, 2.0, 3.0]) == 2.0
