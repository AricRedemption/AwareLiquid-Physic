"""Tests for HOM-DRIFT (round 273) preregistered verdict."""

import math

import torch

from benchmarks.equiv_head_probe import SENTINEL
from benchmarks.hom_drift_probe import (
    B_EXPECTED_K100,
    HORIZONS,
    PARITY,
    classify_hom_drift,
)


def test_robust():
    verdict, d = classify_hom_drift(
        [[3.5, 3.4, 3.6], [4.0, 4.1, 4.05], [5.0, 5.2, 5.1]],
        [[2.0, 1.6, 2.2], [2.4, 2.0, 2.6], [3.0, 3.2, 3.1]],
        [[0.05, 0.04, 0.06], [0.10, 0.11, 0.10], [0.20, 0.22, 0.21]],
        [[0.04, 0.05, 0.045], [0.09, 0.10, 0.095], [0.19, 0.21, 0.20]])
    assert verdict == "HOM_DRIFT_ROBUST"
    assert "adopts the long-horizon anchors" in d["decision"]


def test_mse_only():
    verdict, d = classify_hom_drift(
        [[3.5, 3.4, 3.6], [4.0, 4.1, 4.05], [5.0, 5.2, 5.1]],
        [[2.0, 1.6, 2.2], [2.4, 2.0, 2.6], [3.0, 3.2, 3.1]],
        [[0.05, 0.04, 0.06], [0.10, 0.11, 0.10], [0.20, 0.22, 0.21]],
        [[0.04, 0.05, 0.045], [0.30, 0.30, 0.31], [0.60, 0.62, 0.61]])
    assert verdict == "HOM_DRIFT_MSE_ONLY"
    assert "conservative note" in d["decision"]


def test_degrades():
    verdict, d = classify_hom_drift(
        [[3.5, 3.4, 3.6], [4.0, 4.1, 4.05], [5.0, 5.2, 5.1]],
        [[2.0, 1.6, 2.2], [5.0, 5.2, 5.1], [8.0, 8.2, 8.1]],
        [[0.05, 0.04, 0.06], [0.10, 0.11, 0.10], [0.20, 0.22, 0.21]],
        [[0.04, 0.05, 0.045], [0.09, 0.10, 0.095], [0.19, 0.21, 0.20]])
    assert verdict == "HOM_DRIFT_DEGRADES"
    assert "keeps default-head readings" in d["decision"]


def test_divergence_checked_first():
    verdict, d = classify_hom_drift(
        [[3.5, math.inf, 3.6], [4.0, 4.1, 4.05], [5.0, 5.2, 5.1]],
        [[2.0, 1.6, 2.2], [2.4, 2.0, 2.6], [3.0, 3.2, 3.1]],
        [[0.05, 0.04, 0.06], [0.10, 0.11, 0.10], [0.20, 0.22, 0.21]],
        [[0.04, 0.05, 0.045], [0.09, 0.10, 0.095], [0.19, 0.21, 0.20]])
    assert verdict == "HOM_ARM_DIVERGED"
    assert "arm A seed 1" in d["reason"]


def test_parity_boundary_is_not_robust():
    # ratio exactly at parity (>= gate) counts as degrading (strict <)
    verdict, _ = classify_hom_drift(
        [[2.0, 2.0, 2.0]] * 3,
        [[PARITY * 2.0] * 3] * 3,
        [[0.05] * 3] * 3,
        [[0.05] * 3] * 3)
    assert verdict == "HOM_DRIFT_DEGRADES"


def test_declared_anchors():
    assert SENTINEL == 3.5581917762756348
    assert B_EXPECTED_K100 == [2.0023648738861084, 1.6420986652374268,
                               2.2025928497314453]
    assert HORIZONS == (100, 400, 1000)


def test_candidate_head_constructs():
    from benchmarks.v_hom_stab_probe import HomVStabHead
    head = HomVStabHead(1, hidden_dim=8, depth=1, context_dim=2)
    q = torch.randn(4, 1, requires_grad=True)
    ctx = torch.randn(4, 2)
    e = head.energy(q, p=torch.randn(4, 1), context=ctx)
    e.sum().backward()
    assert q.grad is not None
