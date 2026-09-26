"""Tests for HOM-BOUND (round 271) preregistered verdict."""

import math

import torch

from benchmarks.hom_bound_probe import (
    PARITY,
    HomPowerHead,
    HomPowerV,
    classify_hom_bound,
    gen_quartic,
)


def test_degree_matched():
    verdict, d = classify_hom_bound([2.0, 2.1, 2.05], [8.0, 8.2, 8.1],
                                    [1.9, 2.0, 2.05])
    assert verdict == "HOM_BOUND_DEGREE_MATCHED"
    assert "degree axis" in d["decision"]


def test_all_tolerant():
    verdict, d = classify_hom_bound([2.0, 2.1, 2.05], [2.0, 2.1, 2.05],
                                    [1.95, 2.05, 2.0])
    assert verdict == "HOM_BOUND_ALL_TOLERANT"
    assert "void" in d["decision"]


def test_measured():
    verdict, d = classify_hom_bound([2.0, 2.1, 2.05], [8.0, 8.2, 8.1],
                                    [4.0, 4.2, 4.1])
    assert verdict == "HOM_BOUND_MEASURED"
    assert "spring-line" in d["decision"]


def test_divergence_checked_first():
    verdict, d = classify_hom_bound([2.0, math.inf, 2.05],
                                    [2.0, 2.1, 2.05],
                                    [1.95, 2.05, 2.0])
    assert verdict == "HOM_ARM_DIVERGED"
    assert "arm A" in d["reason"]


def test_parity_boundary():
    # r4 exactly at parity (>=) and r2 at parity (not >) => MEASURED
    verdict, d = classify_hom_bound([2.0, 2.0, 2.0],
                                    [PARITY * 2.0] * 3,
                                    [PARITY * 2.0] * 3)
    assert verdict == "HOM_BOUND_MEASURED"
    assert d["r2"] == PARITY and d["r4"] == PARITY


def test_gen_quartic_conserves_energy():
    g = torch.Generator().manual_seed(3)
    qs, ps = gen_quartic(16, 160, 0.1, g)
    e = 0.5 * ps ** 2 + 0.25 * qs ** 4            # (16, 161, 1)
    drift = ((e - e[:, :1]).abs() / e[:, :1].abs().clamp_min(1e-6)).mean()
    assert drift.item() < 0.02
    assert torch.isfinite(qs).all() and torch.isfinite(ps).all()


def test_degree4_exactly_homogeneous():
    torch.manual_seed(4)
    inner = torch.nn.Sequential(torch.nn.Linear(3, 4), torch.nn.Tanh(),
                                torch.nn.Linear(4, 1)).double()
    wrap = HomPowerV(inner, dim=1, degree=2).double()
    q = torch.randn(6, 1, dtype=torch.float64)
    ctx = torch.randn(6, 2, dtype=torch.float64)
    v1 = wrap(torch.cat([q, ctx], dim=-1))
    for s in (0.3, 3.0, 40.0):
        v_s = wrap(torch.cat([s * q, ctx], dim=-1))
        assert torch.allclose(v_s, s ** 4 * v1, rtol=1e-9), s


def test_degree4_represents_pure_quartic_truth():
    # s = const 1/4 => V = ‖q‖⁴·(1/4) = q⁴/4 exactly
    w = torch.nn.Linear(2, 1)
    with torch.no_grad():
        w.weight.zero_()
        w.bias.fill_(0.25)
    wrap = HomPowerV(w, dim=1, degree=2).double()
    q = torch.tensor([[0.5], [1.3], [2.0]], dtype=torch.float64)
    ctx = torch.zeros(3, 1, dtype=torch.float64)
    v = wrap(torch.cat([q, ctx], dim=-1))
    assert torch.allclose(v.squeeze(-1), 0.25 * q.squeeze(-1) ** 4,
                          rtol=1e-12)


def test_hom_power_head_grads_flow():
    head = HomPowerHead(2, 1, hidden_dim=8, depth=1, context_dim=2)
    q = torch.randn(4, 1, requires_grad=True)
    ctx = torch.randn(4, 2)
    e = head.energy(q, p=torch.randn(4, 1), context=ctx)
    e.sum().backward()
    assert head.V.inner[0].weight.grad is not None
    assert q.grad is not None
