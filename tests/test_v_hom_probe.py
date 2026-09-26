"""Tests for V-HOM (round 261) preregistered verdict."""

import math

import torch

from benchmarks.v_hom_probe import (
    LO_GATE,
    REL_GATE,
    SENTINEL_A,
    HomVHead,
    ScaledQuadratic,
    classify_vhom,
)


def test_repairs():
    verdict, d = classify_vhom([1.0, 1.0, 1.0], [1.0, 1.0, 1.0],
                               [9.0, 9.1, 9.05], [2.0, 2.1, 1.9])
    assert verdict == "VHOM_REPAIRS"
    assert "candidate upgrade" in d["decision"]


def test_partial():
    verdict, d = classify_vhom([1.0, 1.0, 1.0], [1.0, 1.0, 1.0],
                               [9.0, 9.1, 9.05], [5.0, 5.5, 5.2])
    assert verdict == "VHOM_PARTIAL"
    assert "context channel" in d["decision"]


def test_null():
    verdict, d = classify_vhom([1.0, 1.0, 1.0], [1.0, 1.0, 1.0],
                               [9.0, 9.1, 9.05], [8.8, 9.0, 8.9])
    assert verdict == "VHOM_NULL"
    assert "redirects" in d["decision"]


def test_out_of_band_is_null_even_if_reduced():
    # B materially better in-dist: outside the parity band => NULL
    verdict, _ = classify_vhom([1.0, 1.0, 1.0], [0.8, 0.8, 0.8],
                               [9.0, 9.1, 9.05], [2.0, 2.1, 1.9])
    assert verdict == "VHOM_NULL"


def test_divergence_checked_first():
    verdict, d = classify_vhom([1.0, math.inf, 1.0], [1.0, 1.0, 1.0],
                               [9.0, 9.1, 9.05], [2.0, 2.1, 1.9])
    assert verdict == "VHOM_ARM_DIVERGED"
    assert "arm A" in d["reason"]


def test_sentinel():
    assert SENTINEL_A == 2.7786638736724854


def test_scaled_quadratic_exact_homogeneity():
    # ‖q‖²·s(q̂, ctx) is exactly degree-2 homogeneous for ANY s
    inner = torch.nn.Sequential(torch.nn.Linear(3, 4), torch.nn.Tanh(),
                                torch.nn.Linear(4, 1))
    wrap = ScaledQuadratic(inner, dim=1)
    q = torch.randn(6, 1)
    ctx = torch.randn(6, 2)
    x = torch.cat([q, ctx], dim=-1)
    v1 = wrap(x)
    for s in (0.3, 3.0, 40.0):
        v_s = wrap(torch.cat([s * q, ctx], dim=-1))  # ctx unchanged
        assert torch.allclose(v_s, s ** 2 * v1, rtol=1e-4), s


def test_hom_v_head_gradients_flow():
    head = HomVHead(1, hidden_dim=8, depth=1, context_dim=2)
    q = torch.randn(4, 1, requires_grad=True)
    ctx = torch.randn(4, 2)
    e = head.energy(q, p=torch.randn(4, 1), context=ctx)
    e.sum().backward()
    assert head.V.inner[0].weight.grad is not None
