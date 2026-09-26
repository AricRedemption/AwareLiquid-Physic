"""Tests for POOL-BITS (round 275) preregistered verdict."""

import math

import torch

from benchmarks.pool_bits_probe import (
    A_ANCHOR_160,
    B_ANCHOR_160,
    STABLE_GATE,
    classify_pool_bits,
)


def test_candidate_stable():
    verdict, d = classify_pool_bits([1.7, 1.3, 1.5], [1.05, 1.03, 1.08])
    assert verdict == "ANCHOR_CANDIDATE_STABLE"
    assert "fewer pool variants" in d["decision"]


def test_both_fragile():
    verdict, d = classify_pool_bits([1.7, 1.3, 1.5], [1.2, 1.4, 1.15])
    assert verdict == "ANCHOR_BOTH_FRAGILE"
    assert "multi-variant" in d["decision"]


def test_no_difference():
    verdict, d = classify_pool_bits([1.05, 1.08, 1.03], [1.2, 1.04, 1.06])
    assert verdict == "ANCHOR_NO_DIFFERENCE"
    assert "neutral" in d["decision"]


def test_divergence_checked_first():
    verdict, d = classify_pool_bits([math.inf, 1.3, 1.5], [1.05, 1.03, 1.08])
    assert verdict == "HOM_ARM_DIVERGED"
    assert "arm A" in d["reason"]


def test_stable_gate_boundary():
    # median exactly at the gate is NOT below it (strict <): the
    # both-fragile branch catches it (>= on both sides)
    verdict, d = classify_pool_bits([1.7, 1.3, 1.5],
                                    [STABLE_GATE, STABLE_GATE,
                                     STABLE_GATE])
    assert verdict == "ANCHOR_BOTH_FRAGILE"
    assert d["median_spread_candidate"] == STABLE_GATE


def test_declared_anchors():
    assert A_ANCHOR_160 == 3.5581917762756348
    assert B_ANCHOR_160 == 2.0023648738861084


def test_candidate_head_constructs():
    from benchmarks.v_hom_stab_probe import HomVStabHead
    head = HomVStabHead(1, hidden_dim=8, depth=1, context_dim=2)
    q = torch.randn(4, 1, requires_grad=True)
    ctx = torch.randn(4, 2)
    e = head.energy(q, p=torch.randn(4, 1), context=ctx)
    e.sum().backward()
    assert q.grad is not None
