"""Tests for EQUIV-HEAD (round 249) preregistered verdict."""

import math

import torch

from benchmarks.equiv_head_probe import (
    HI_GATE,
    LO_GATE,
    REL_GATE,
    SENTINEL,
    AnalyticTHead,
    classify_equiv,
    median,
)


def test_resolved():
    verdict, d = classify_equiv([1.0, 1.0, 1.0], [1.0, 1.0, 1.0],
                                [4.1, 4.0, 4.2], [2.0, 2.1, 1.9])
    assert verdict == "EQUIV_RESOLVED"
    assert LO_GATE <= d["ratio"] <= HI_GATE
    assert d["rel_comp_median_B"] < REL_GATE
    assert "architecture-line candidate" in d["decision"]


def test_tradeoff_worse():
    verdict, d = classify_equiv([1.0, 1.0, 1.0], [1.3, 1.2, 1.25],
                                [4.1, 4.0, 4.2], [2.0, 2.1, 1.9])
    assert verdict == "EQUIV_TRADEOFF"
    assert "trade-off" in d["decision"]


def test_tradeoff_better_counts_too():
    verdict, _ = classify_equiv([1.0, 1.0, 1.0], [0.7, 0.75, 0.72],
                                [4.1, 4.0, 4.2], [2.0, 2.1, 1.9])
    assert verdict == "EQUIV_TRADEOFF"


def test_attrib():
    verdict, d = classify_equiv([1.0, 1.0, 1.0], [1.0, 1.0, 1.0],
                                [4.1, 4.0, 4.2], [4.0, 4.1, 4.05])
    assert verdict == "EQUIV_ATTRIB"
    assert "not in T" in d["decision"]


def test_divergence_checked_first():
    verdict, d = classify_equiv([1.0, math.inf, 1.0], [1.0, 1.0, 1.0],
                                [4.1, 4.0, 4.2], [2.0, 2.1, 1.9])
    assert verdict == "EQUIV_ARM_DIVERGED"
    assert "arm A" in d["reason"]


def test_sentinel():
    assert SENTINEL == 3.5581917762756348


def test_median():
    assert median([1.0, 2.0, 3.0]) == 2.0


def test_analytic_t_head_gradients_and_scaling():
    # the analytic T's dT_dp is exactly p (homogeneous degree 1) and
    # its energy drops the T term; V still receives gradients.
    head = AnalyticTHead(1, hidden_dim=8, depth=1, context_dim=2)
    p = torch.randn(4, 1)
    assert torch.equal(head.dT_dp(p), p)
    q = torch.randn(4, 1)
    ctx = torch.randn(4, 2)
    e = head.energy(q, p, context=ctx)
    v = head.V(torch.cat([q, ctx], dim=-1)).squeeze(-1)
    assert torch.equal(e, v)
    e.sum().backward()
    assert head.V[0].weight.grad is not None
