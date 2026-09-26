"""Tests for HOM-DEFAULT (round 269) preregistered verdict."""

import math

import torch

from benchmarks.equiv_head_probe import SENTINEL
from benchmarks.hom_default_probe import (
    B_EXPECTED_MSE,
    EXTRAP_GATE,
    LO_GATE,
    classify_hom_default,
)


def test_dominates():
    verdict, d = classify_hom_default([3.5, 3.4, 3.6], [2.0, 1.6, 2.2],
                                      [3.3, 3.4, 3.2], [1.4, 1.7, 1.5])
    assert verdict == "HOM_DEFAULT_DOMINATES"
    assert "replacement candidate" in d["decision"]


def test_indist_only():
    verdict, d = classify_hom_default([3.5, 3.4, 3.6], [2.0, 1.6, 2.2],
                                      [3.3, 3.4, 3.2], [3.4, 3.5, 3.3])
    assert verdict == "HOM_DEFAULT_INDIST_ONLY"
    assert "in-dist gain only" in d["decision"]


def test_extrap_only():
    verdict, d = classify_hom_default([3.5, 3.4, 3.6], [3.45, 3.35, 3.55],
                                      [3.3, 3.4, 3.2], [1.4, 1.7, 1.5])
    assert verdict == "HOM_DEFAULT_EXTRAP_ONLY"
    assert "extrapolation gain only" in d["decision"]


def test_parity():
    verdict, d = classify_hom_default([3.5, 3.4, 3.6], [3.45, 3.35, 3.55],
                                      [3.3, 3.4, 3.2], [2.8, 2.9, 2.85])
    assert verdict == "HOM_DEFAULT_PARITY"
    assert "downgrade" in d["decision"]


def test_worse():
    verdict, d = classify_hom_default([3.5, 3.4, 3.6], [4.5, 4.4, 4.6],
                                      [3.3, 3.4, 3.2], [1.4, 1.7, 1.5])
    assert verdict == "HOM_DEFAULT_WORSE"
    assert "downgrade" in d["decision"]


def test_divergence_checked_first():
    verdict, d = classify_hom_default([3.5, math.inf, 3.6],
                                      [2.0, 1.6, 2.2],
                                      [3.3, 3.4, 3.2], [1.4, 1.7, 1.5])
    assert verdict == "HOM_ARM_DIVERGED"
    assert "arm A" in d["reason"]


def test_sentinels_are_declared_anchors():
    assert SENTINEL == 3.5581917762756348
    assert B_EXPECTED_MSE == [2.0023648738861084, 1.6420986652374268,
                              2.2025928497314453]


def test_extrap_gate_is_material():
    # exactly 0.7x median is NOT a material extrapolation improvement
    verdict, _ = classify_hom_default([3.5, 3.4, 3.6], [3.45, 3.35, 3.55],
                                      [3.3, 3.4, 3.2],
                                      [EXTRAP_GATE * 3.3] * 3)
    assert verdict == "HOM_DEFAULT_PARITY"
