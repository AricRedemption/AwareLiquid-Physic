"""Tests for SPEC3 (round 283) preregistered verdict."""

import math

import torch

from benchmarks.residual_spec3_probe import (
    A4_EXPECTED_MSE,
    B8_EXPECTED_MSE,
    TIED_GATE,
    classify_spec3,
)


def test_reproduces():
    verdict, d = classify_spec3([0.995, 0.99, 0.997], [0.98, 0.975, 0.98])
    assert verdict == "SPEC3_ORDER_REPRODUCES"
    assert "keeps its standing" in d["decision"]


def test_tied():
    verdict, d = classify_spec3([0.99, 0.991, 0.99], [0.99, 0.99, 0.989])
    assert verdict == "SPEC3_ORDER_TIED"
    assert "cutoff artifact" in d["decision"]


def test_flips():
    verdict, d = classify_spec3([0.975, 0.98, 0.978], [0.99, 0.995, 0.992])
    assert verdict == "SPEC3_ORDER_FLIPS"
    assert "reversed sign" in d["decision"]


def test_unresolvable():
    verdict, d = classify_spec3([0.99, math.nan, 0.99], [0.98] * 3)
    assert verdict == "SPEC3_UNRESOLVABLE"
    assert "k4 seed 1" in d["reason"]


def test_tied_gate_boundary():
    # diff exactly at the gate is NOT tied (strict <): the direction
    # branch catches it
    verdict, d = classify_spec3([0.99, 0.99, 0.99],
                                [0.99 - TIED_GATE] * 3)
    assert verdict == "SPEC3_ORDER_REPRODUCES"
    assert abs(d["median_diff"]) == TIED_GATE


def test_declared_anchors():
    assert A4_EXPECTED_MSE == [2.526942491531372, 3.024425745010376,
                               2.004868745803833]
    assert B8_EXPECTED_MSE == [2.9031009674072266, 2.423386812210083,
                               3.1820216178894043]


def test_probe_module_imports():
    from benchmarks.residual_spec3_probe import main  # noqa: F401
    from benchmarks.liquid_physics_eval import evaluate  # noqa: F401
