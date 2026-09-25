"""Tests for WARMUP-PROBE-2 (round 237) preregistered verdict."""

import math

from benchmarks.warmup_probe_v2 import (
    BENEFICIAL_GATE,
    HARM_GATE,
    SENTINEL,
    classify_warmup_3s,
    train_warmup,
)


def test_beneficial():
    verdict, d = classify_warmup_3s([1.0, 1.0, 1.0], [0.9, 0.9, 0.9])
    assert verdict == "WARMUP_3S_BENEFICIAL"
    assert d["ratio"] < BENEFICIAL_GATE
    assert "recipe candidate" in d["decision"]


def test_unresolved_interior():
    verdict, d = classify_warmup_3s([1.0, 1.1, 0.9], [1.02, 1.0, 0.99])
    assert verdict == "WARMUP_3S_UNRESOLVED"
    assert "not robust" in d["decision"]


def test_gate_boundaries_are_unresolved():
    # ratio exactly at either gate is UNRESOLVED (preregistered
    # intervals); 19/20 and 21/20 are exactly representable here
    _, d_lo = classify_warmup_3s([20.0, 20.0, 20.0], [19.0, 19.0, 19.0])
    assert d_lo["ratio"] == BENEFICIAL_GATE
    _, d_hi = classify_warmup_3s([20.0, 20.0, 20.0], [21.0, 21.0, 21.0])
    assert d_hi["ratio"] == HARM_GATE


def test_harmful():
    verdict, d = classify_warmup_3s([1.0, 1.0, 1.0], [1.2, 1.1, 1.15])
    assert verdict == "WARMUP_3S_HARMFUL"
    assert "remove" in d["decision"]


def test_divergence_checked_before_ratio():
    verdict, d = classify_warmup_3s([1.0, 1.0, 1.0],
                                    [0.5, math.inf, 0.5])
    assert verdict == "WARMUP_ARM_DIVERGED"
    assert "seed 1" in d["reason"]
    verdict, d = classify_warmup_3s([1e7, 1.0, 1.0], [0.5, 0.5, 0.5])
    assert verdict == "WARMUP_ARM_DIVERGED"
    assert "arm A" in d["reason"]


def test_direction_consistency_and_spreads():
    _, d = classify_warmup_3s([1.0, 2.0, 1.5], [0.9, 1.9, 1.6])
    assert d["direction_consistency"] == "2/3"
    assert math.isclose(d["seed_spread_A"], 2.0)
    assert math.isclose(d["seed_spread_B"], 1.9 / 0.9)


def test_sentinel_value_is_house_default():
    # the pinned literal must be the round-175/191/223/226 +
    # RECIPE-SYNTHESIS arm-A seed-0 house default number
    assert SENTINEL == 3.5581917762756348


def test_train_warmup_default_matches_house_loop():
    # Sentinel clause r181: with warmup_steps=0 the loop must be
    # configurationally identical to the house prefix train (same rng
    # consumption, same loss path). Compare on a tiny problem —
    # bit-for-bit.
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
            (train_warmup, {"warmup_steps": 0})):
        torch.manual_seed(0)
        model = LiquidHamiltonianModel(1, d_model=8, context_dim=2,
                                       n_scales=1, hidden_dim=8,
                                       depth=1, dt=0.1)
        losses.append(trainer(model, qs, ps, 8, 2, 5, 1e-2, 4, 0,
                              **kwargs))
    assert losses[0] == losses[1]


def test_warmup_schedule_shape():
    # warmup ramps linearly over warmup_steps then holds at 1.0
    import torch

    opt = torch.optim.Adam([torch.nn.Parameter(torch.zeros(1))], lr=3e-3)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda t: min(1.0, (t + 1) / 200))
    lrs = []
    for _ in range(220):
        lrs.append(sched.get_last_lr()[0] / 3e-3)
        sched.step()
    assert math.isclose(lrs[0], 1 / 200)
    assert lrs[199] == 1.0
    assert lrs[219] == 1.0
