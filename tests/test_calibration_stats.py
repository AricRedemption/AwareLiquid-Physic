"""D-1 校准统计函数测试(calibration_stats,AMM-010 T1 直跑前置)。"""
import math

import torch

from benchmarks.probabilistic_eval import calibration_stats


def test_perfectly_calibrated_sampler_hits_95():
    g = torch.Generator().manual_seed(0)
    n = 200_000
    mu = torch.randn(n, generator=g)
    logvar = torch.zeros(n)          # sigma=1, mu 本身就是 z
    s = calibration_stats(mu, logvar, torch.zeros(n))
    assert abs(s["calib_coverage_95"] - 0.95) < 0.002
    assert abs(s["calib_z_mean"]) < 0.01
    assert abs(s["calib_z_std"] - 1.0) < 0.01


def test_overconfident_narrow_sigma_drops_coverage():
    # 真误差 ~N(0,1) 但模型声明 sigma=0.5 ⇒ z=2·N(0,1), 覆盖 2Φ(0.98)−1≈0.673
    g = torch.Generator().manual_seed(1)
    n = 100_000
    mu = torch.randn(n, generator=g)
    logvar = 2 * math.log(0.5)
    s = calibration_stats(mu, logvar, torch.zeros(n))
    assert abs(s["calib_coverage_95"] - 0.673) < 0.01
    assert s["calib_z_std"] > 1.5


def test_underconfident_wide_sigma_overcovers():
    g = torch.Generator().manual_seed(2)
    n = 100_000
    mu = torch.randn(n, generator=g)
    logvar = 2 * math.log(2.0)                # sigma=2
    s = calibration_stats(mu, logvar, torch.zeros(n))
    assert s["calib_coverage_95"] > 0.99
    assert s["calib_z_std"] < 0.6


def test_bias_shifts_z_mean():
    mu = torch.full((1000,), 0.3)
    logvar = torch.zeros(1000)
    s = calibration_stats(mu, logvar, torch.zeros(1000))
    assert abs(s["calib_z_mean"] - 0.3) < 1e-6
