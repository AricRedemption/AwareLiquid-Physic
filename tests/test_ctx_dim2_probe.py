"""Tests for CTX-DIM-2 (round 239) preregistered verdict."""

import math

from benchmarks.ctx_dim2_probe import (
    CONFIRM_GATE,
    REVERSE_GATE,
    SENTINEL_A,
    SENTINEL_B,
    classify_ctx2,
    median_iqr,
    omega_semantic,
    train_ctx,
)


def test_confirm():
    verdict, d = classify_ctx2([1.0, 1.0, 1.0], [0.9, 0.9, 0.9])
    assert verdict == "CTX2_CONFIRM"
    assert d["ratio"] < CONFIRM_GATE
    assert "confirmed" in d["decision"]


def test_unresolved_interior():
    verdict, d = classify_ctx2([1.0, 1.1, 0.9], [1.02, 1.0, 0.99])
    assert verdict == "CTX2_UNRESOLVED"
    assert "downgraded" in d["decision"]


def test_gate_boundaries_are_unresolved():
    # ratio exactly at either gate is UNRESOLVED (preregistered
    # intervals); 19/20 and 21/20 are exactly representable here
    _, d_lo = classify_ctx2([20.0, 20.0, 20.0], [19.0, 19.0, 19.0])
    assert d_lo["ratio"] == CONFIRM_GATE
    _, d_hi = classify_ctx2([20.0, 20.0, 20.0], [21.0, 21.0, 21.0])
    assert d_hi["ratio"] == REVERSE_GATE


def test_reversed():
    verdict, d = classify_ctx2([1.0, 1.0, 1.0], [1.2, 1.1, 1.15])
    assert verdict == "CTX2_REVERSED"
    assert "reversal" in d["decision"]


def test_divergence_checked_before_ratio():
    verdict, d = classify_ctx2([1.0, 1.0, 1.0],
                               [0.5, math.inf, 0.5])
    assert verdict == "CTX_ARM_DIVERGED"
    assert "seed 1" in d["reason"]
    verdict, d = classify_ctx2([1e7, 1.0, 1.0], [0.5, 0.5, 0.5])
    assert verdict == "CTX_ARM_DIVERGED"
    assert "arm A" in d["reason"]


def test_direction_consistency_and_spreads():
    _, d = classify_ctx2([1.0, 2.0, 1.5], [0.9, 1.9, 1.6])
    assert d["direction_consistency"] == "2/3"
    assert math.isclose(d["seed_spread_A"], 2.0)
    assert math.isclose(d["seed_spread_B"], 1.9 / 0.9)


def test_sentinel_values():
    assert SENTINEL_A == 3.5581917762756348
    assert SENTINEL_B == 1.9746309518814087


def test_omega_semantic_perfect_carrier():
    # ctx = omega exactly: |corr| = 1 and R^2 = 1
    import torch

    omega = torch.linspace(0.7, 1.8, 32)
    ctx = omega.unsqueeze(1).repeat(1, 2)          # 2 channels, both omega
    s = omega_semantic(ctx, omega)
    assert abs(s["max_abs_corr"] - 1.0) < 1e-5
    assert s["linear_readout_r2"] > 0.999


def test_omega_semantic_independent_noise():
    # ctx = symmetric noise: |corr| near 0, R^2 near 0
    import torch

    g = torch.Generator().manual_seed(0)
    omega = torch.linspace(0.7, 1.8, 64)
    ctx = torch.randn(64, 3, generator=g)
    s = omega_semantic(ctx, omega)
    assert s["max_abs_corr"] < 0.35
    assert abs(s["linear_readout_r2"]) < 0.2


def test_median_iqr_odd_and_even():
    assert median_iqr([1.0, 2.0, 3.0])["median"] == 2.0
    assert median_iqr([1.0, 2.0, 3.0, 4.0])["median"] == 2.5
    assert median_iqr([1.0, 2.0, 3.0])["iqr"] == 2.0


def test_train_ctx_matches_house_loop():
    # Sentinel clause r181: verbatim rng consumption vs the house
    # prefix train on a tiny problem — bit-for-bit.
    import os
    import sys

    import torch

    sys.path.insert(0, os.path.join(os.path.dirname(
        os.path.abspath(__file__)), ".."))
    from awareliquid_physics.model import LiquidHamiltonianModel
    from benchmarks.liquid_physics_eval import train as house_train
    from benchmarks.sample_efficiency_eval import gen_spring

    g = torch.Generator().manual_seed(0)
    qs, ps, _ = gen_spring(16, 40, 0.1, 1, 0.7, 1.8, g)
    losses = []
    for trainer in (house_train, train_ctx):
        torch.manual_seed(0)
        model = LiquidHamiltonianModel(1, d_model=8, context_dim=2,
                                       n_scales=1, hidden_dim=8,
                                       depth=1, dt=0.1)
        losses.append(trainer(model, qs, ps, 8, 2, 5, 1e-2, 4, 0))
    assert losses[0] == losses[1]
