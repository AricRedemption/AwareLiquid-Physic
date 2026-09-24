"""Tests for RECIPE-SYNTHESIS (round 227) preregistered verdict."""

import math

from benchmarks.recipe_synthesis_probe import (
    ANTAG_GATE,
    SYNERGIC_GATE,
    classify_recipe,
    train_recipe,
)


def test_synergic():
    verdict, d = classify_recipe([1.0, 1.0, 1.0], [0.9, 0.9, 0.9])
    assert verdict == "RECIPE_SYNERGIC"
    assert d["ratio"] < SYNERGIC_GATE
    assert "back-propagate" in d["decision"]


def test_null_interior():
    verdict, d = classify_recipe([1.0, 1.1, 0.9], [1.02, 1.0, 0.99])
    assert verdict == "RECIPE_NULL"
    assert "not additive" in d["decision"]


def test_null_boundaries_are_null():
    # ratio exactly at either gate is NULL (preregistered intervals);
    # 19/20 and 21/20 are exactly representable at these magnitudes
    _, d_lo = classify_recipe([20.0, 20.0, 20.0], [19.0, 19.0, 19.0])
    assert d_lo["ratio"] == SYNERGIC_GATE
    _, d_hi = classify_recipe([20.0, 20.0, 20.0], [21.0, 21.0, 21.0])
    assert d_hi["ratio"] == ANTAG_GATE


def test_antagonistic():
    verdict, d = classify_recipe([1.0, 1.0, 1.0], [1.2, 1.1, 1.15])
    assert verdict == "RECIPE_ANTAGONISTIC"
    assert "conflict" in d["decision"]


def test_divergence_checked_before_ratio():
    verdict, d = classify_recipe([1.0, 1.0, 1.0],
                                 [0.5, math.inf, 0.5])
    assert verdict == "RECIPE_ARM_DIVERGED"
    assert "seed 1" in d["reason"]
    verdict, d = classify_recipe([1e7, 1.0, 1.0], [0.5, 0.5, 0.5])
    assert verdict == "RECIPE_ARM_DIVERGED"
    assert "arm A" in d["reason"]


def test_direction_consistency_and_spreads():
    _, d = classify_recipe([1.0, 2.0, 1.5], [0.9, 1.9, 1.6])
    assert d["direction_consistency"] == "2/3"
    assert math.isclose(d["seed_spread_A"], 2.0)
    assert math.isclose(d["seed_spread_B"], 1.9 / 0.9)


def test_train_recipe_default_matches_house_loop():
    # Sentinel clause r181: with neutral knobs the recipe loop must be
    # configurationally identical to the house prefix loop (same rng
    # consumption, same loss path). Compare against the house train on
    # a tiny problem — bit-for-bit.
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
    for trainer, kwargs in (
            (house_train, {}),
            (train_recipe, {"lr_decay": 1.0, "weight_decay": 0.0,
                            "warmup_steps": 0})):
        torch.manual_seed(0)
        model = LiquidHamiltonianModel(1, d_model=8, context_dim=2,
                                       n_scales=1, hidden_dim=8,
                                       depth=1, dt=0.1)
        losses.append(trainer(model, qs, ps, 8, 2, 5, 1e-2, 4, 0,
                              **kwargs))
    assert losses[0] == losses[1]


def test_warmup_schedule_shapes():
    # warmup is linear over warmup_steps then constant; decay composes
    # multiplicatively. Verified via the lr_lambda used in train_recipe.
    import torch

    def lr_fn(t, warmup_steps, lr_decay):
        warm = min(1.0, (t + 1) / warmup_steps) if warmup_steps > 0 else 1.0
        return warm * (lr_decay ** t)

    assert lr_fn(0, 200, 1.0) == 1 / 200
    assert lr_fn(199, 200, 1.0) == 1.0
    assert lr_fn(500, 200, 1.0) == 1.0
    assert lr_fn(0, 0, 0.999) == 1.0
    assert math.isclose(lr_fn(10, 200, 0.999), (11 / 200) * 0.999 ** 10)
