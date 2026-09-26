"""Tests for V-HOM-STAB (round 268) preregistered verdict."""

import math

import torch

from benchmarks.v_hom_stab_probe import (
    CAT_GATE,
    REF_EXPECTED_MSE,
    QuadraticDirectionFree,
    HomVStabHead,
    classify_stab,
)


def test_repairs():
    verdict, d = classify_stab([2456.6, 2.4, 701.8], [2.5, 2.6, 2.4],
                               [1.4, 1.5, 1.45])
    assert verdict == "STAB_REPAIRS"
    assert "candidate upgrade" in d["decision"]


def test_stable_only():
    verdict, d = classify_stab([2456.6, 2.4, 701.8], [2.5, 2.6, 2.4],
                               [5.0, 5.5, 5.2])
    assert verdict == "STAB_STABLE_ONLY"
    assert "downgrade" in d["decision"]


def test_partial():
    verdict, d = classify_stab([2456.6, 2.4, 701.8], [2.5, 400.0, 2.4],
                               [1.4, 9.0, 1.45])
    assert verdict == "STAB_PARTIAL"
    assert "mitigated" in d["decision"]


def test_null():
    verdict, d = classify_stab([2.5, 2.4, 2.6], [800.0, 900.0, 700.0],
                               [9.0, 9.1, 9.05])
    assert verdict == "STAB_NULL"
    assert "parking" in d["decision"]


def test_divergence_checked_first():
    verdict, d = classify_stab([2.5, math.inf, 2.6], [2.5, 2.6, 2.4],
                               [1.4, 1.5, 1.45])
    assert verdict == "STAB_ARM_DIVERGED"
    assert "arm REF" in d["reason"]


def test_catastrophe_gate_boundary():
    # exactly at the gate is NOT catastrophic (strict >)
    verdict, d = classify_stab([2.5, 2.4, 2.6],
                               [CAT_GATE, CAT_GATE, CAT_GATE],
                               [1.4, 1.5, 1.45])
    assert verdict == "STAB_REPAIRS"
    assert d["n_catastrophic_STAB"] == 0


def test_ref_expected_values_are_round261_stored():
    assert REF_EXPECTED_MSE == [2456.613037109375, 2.3841938972473145,
                                701.840576171875]


def test_direction_free_exactly_homogeneous():
    # V(λq) = λ²V(q) for ANY inner (float64 per round-110 clause)
    torch.manual_seed(1)
    inner = torch.nn.Sequential(torch.nn.Linear(3, 4), torch.nn.Tanh(),
                                torch.nn.Linear(4, 1)).double()
    wrap = QuadraticDirectionFree(inner, dim=1).double()
    q = torch.randn(6, 1, dtype=torch.float64)
    ctx = torch.randn(6, 2, dtype=torch.float64)
    v1 = wrap(torch.cat([q, ctx], dim=-1))
    for s in (0.3, 3.0, 40.0):
        v_s = wrap(torch.cat([s * q, ctx], dim=-1))
        assert torch.allclose(v_s, s ** 2 * v1, rtol=1e-10), s


def test_direction_free_is_even_in_q():
    # zeroed direction block => V(q) == V(−q): continuity at q=0 by
    # construction (the round-261 instability candidate removed)
    torch.manual_seed(2)
    inner = torch.nn.Sequential(torch.nn.Linear(3, 4), torch.nn.Tanh(),
                                torch.nn.Linear(4, 1))
    wrap = QuadraticDirectionFree(inner, dim=1)
    q = torch.randn(6, 1)
    ctx = torch.randn(6, 2)
    v_plus = wrap(torch.cat([q, ctx], dim=-1))
    v_minus = wrap(torch.cat([-q, ctx], dim=-1))
    assert torch.allclose(v_plus, v_minus, rtol=1e-6)


def test_gradient_is_2q_times_s():
    # dV/dq == 2q·s(0, ctx) exactly (only the ‖q‖² prefactor path)
    w = torch.nn.Linear(2, 1).double()
    with torch.no_grad():
        w.weight.copy_(torch.tensor([[1.5, -0.7]], dtype=torch.float64))
        w.bias.copy_(torch.tensor([0.4], dtype=torch.float64))
    q = torch.tensor([[0.9], [1.3]], dtype=torch.float64,
                     requires_grad=True)
    ctx = torch.tensor([[0.2], [-0.5]], dtype=torch.float64)
    wrap = QuadraticDirectionFree(w, dim=1).double()
    wrap(torch.cat([q, ctx], dim=-1)).sum().backward()
    s = -0.7 * ctx + 0.4
    expected = 2 * q.detach() * s
    assert torch.allclose(q.grad, expected, rtol=1e-12)


def test_stab_head_energy_grads_flow():
    head = HomVStabHead(1, hidden_dim=8, depth=1, context_dim=2)
    q = torch.randn(4, 1, requires_grad=True)
    ctx = torch.randn(4, 2)
    e = head.energy(q, p=torch.randn(4, 1), context=ctx)
    e.sum().backward()
    assert head.V.inner[0].weight.grad is not None
    assert q.grad is not None
