"""Tests for HOM-SAMPLE (round 277) preregistered verdict."""

import math

import torch

from benchmarks.equiv_head_probe import SENTINEL
from benchmarks.hom_sample_probe import (
    GROW_GATE,
    SIZES,
    classify_hom_sample,
)


def test_smalldata_advantage():
    verdict, d = classify_hom_sample([0.50, 0.55, 0.66])
    assert verdict == "HOM_SAMPLE_SMALLDATA_ADV"
    assert "scarce" in d["decision"]


def test_flat():
    verdict, d = classify_hom_sample([0.66, 0.66, 0.66])
    assert verdict == "HOM_SAMPLE_FLAT"
    assert "size-independent" in d["decision"]


def test_reversed():
    verdict, d = classify_hom_sample([0.90, 0.75, 0.66])
    assert verdict == "HOM_SAMPLE_REVERSED"
    assert "needs data" in d["decision"]


def test_cand_worse_checked_first():
    verdict, d = classify_hom_sample([1.2, 1.1, 1.05])
    assert verdict == "HOM_SAMPLE_CAND_WORSE"
    assert "round 269" in d["decision"]


def test_diverged():
    verdict, d = classify_hom_sample(
        [0.5, 0.55, 0.66],
        mses={"A": [[1.0, math.inf, 1.0], [1.0] * 3, [1.0] * 3],
              "B": [[1.0] * 3] * 3})
    assert verdict == "HOM_ARM_DIVERGED"
    assert "arm A seed 1" in d["reason"]


def test_growth_gate_boundary():
    # ratio_64 exactly at 0.97 x ratio_256 is NOT strict growth (flat)
    verdict, _ = classify_hom_sample([GROW_GATE * 0.66, 0.6, 0.66])
    assert verdict == "HOM_SAMPLE_FLAT"


def test_declared_anchors():
    assert SENTINEL == 3.5581917762756348
    assert SIZES == (64, 128, 256)


def test_candidate_head_constructs():
    from benchmarks.v_hom_stab_probe import HomVStabHead
    head = HomVStabHead(1, hidden_dim=8, depth=1, context_dim=2)
    q = torch.randn(4, 1, requires_grad=True)
    ctx = torch.randn(4, 2)
    e = head.energy(q, p=torch.randn(4, 1), context=ctx)
    e.sum().backward()
    assert q.grad is not None
