"""Tests for AMM-031 (round 267): spectral low-band residual ratio in
house evaluate()."""

import math

import torch

from benchmarks.liquid_physics_eval import residual_low_band_ratio


def _spec_ratio(resid, omega_max=1.8, dt=0.1):
    return residual_low_band_ratio(resid, omega_max, dt)


def test_low_freq_dominant_ratio_near_one():
    # residual = pure slow sine at bin k=1 (0.025 cyc/step = 1/(N*dt),
    # below hf_cut 0.0573; freq resolution round-104 lesson: the window
    # must RESOLVE the frequency — bin spacing here is 0.025)
    t = torch.arange(400, dtype=torch.float32).view(-1, 1, 1)
    resid = torch.sin(2 * math.pi * 0.025 * t) * torch.ones(1, 8, 2)
    r = _spec_ratio(resid)
    assert r > 0.95


def test_high_freq_dominant_ratio_near_zero():
    # residual = pure fast sine (0.3 cyc/step >> hf_cut 0.0573)
    t = torch.arange(400, dtype=torch.float32).view(-1, 1, 1)
    resid = torch.sin(2 * math.pi * 0.4 * t) * torch.ones(1, 8, 2)
    r = _spec_ratio(resid)
    assert r < 0.05


def test_mixed_residual_in_between():
    t = torch.arange(400, dtype=torch.float32).view(-1, 1, 1)
    low = torch.sin(2 * math.pi * 0.025 * t)
    high = torch.sin(2 * math.pi * 0.4 * t)
    resid = (low + 0.2 * high) * torch.ones(1, 8, 2)
    r = _spec_ratio(resid)
    assert 0.8 < r < 1.0


def test_finite_on_tiny_residual():
    resid = torch.full((50, 4, 2), 1e-12)
    r = _spec_ratio(resid)
    assert math.isfinite(r)
