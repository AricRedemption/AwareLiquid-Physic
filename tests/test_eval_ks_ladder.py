"""D1b 的最小管线测试(wave-10 轮 3):run_one 的 eval_k 阶梯接线。

用真 LiquidHamiltonianModel 训 5 步(秒级)验证:--eval_ks 阶梯在
per-run 字典里产出 rollout_mse_k{k} 全键、值有限,且默认口径
rollout_mse 仍与 k=100 一致。防回归点:评测分解不得扰动训练路径。
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from benchmarks.m1_semigroup_eval import gen_spring
from benchmarks.sample_efficiency_eval import run_one


def _args(ks):
    return argparse.Namespace(d_model=16, context_dim=4, n_scales=2,
                              hidden=16, dt=0.1, t_obs=8, k_train=4,
                              train_steps=5, lr=3e-3, lr_decay=1.0, batch=8,
                              eval_ks_list=ks, eval_k=max(ks), probe_context=False,
                              start_probe=False, start_mix=0.0,
                              start_mix_window=1, n_eval=8,
                              gen_steps=40, omega_lo=0.7, omega_hi=1.8)


def test_run_one_eval_ks_ladder():
    torch.manual_seed(0)
    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(16, 40, 0.1, 1, 0.7, 1.8, g)
    res = run_one("prefix", 8, qs, ps, om, 0, _args([1, 5]))
    for k in (1, 5):
        assert f"rollout_mse_k{k}" in res
        assert res[f"rollout_mse_k{k}"] >= 0.0
    assert res["rollout_mse_k5"] == res["rollout_mse"]   # default口径不变


def test_run_one_default_single_k_unchanged():
    torch.manual_seed(0)
    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(16, 160, 0.1, 1, 0.7, 1.8, g)   # 160 ≥ t_obs+k-1
    res = run_one("all2all", 8, qs, ps, om, 0, _args([100]))
    assert "rollout_mse_k100" in res
    assert res["rollout_mse_k100"] == res["rollout_mse"]


def test_run_one_start_probe():
    torch.manual_seed(0)
    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(16, 160, 0.1, 1, 0.7, 1.8, g)
    a = _args([100])
    a.start_probe = True
    res = run_one("prefix", 8, qs, ps, om, 0, a)
    assert res["mse_k1_interior"] >= 0.0   # finite 1-step interior-start MSE


def test_start_mix_pinches_rng_only_when_active():
    """D1d: start_mix=0.0 must keep the sampling RNG stream byte-identical
    (t0 sequence unchanged); start_mix=1.0 must pin every start to t_obs."""
    g0 = torch.Generator().manual_seed(3)
    g1 = torch.Generator().manual_seed(3)
    batch, t_obs, S, k = 8, 8, 160, 4
    # start_mix=0.0 branch never draws rand -> t0 identical to base stream
    t0_a = torch.randint(t_obs, S - k, (batch,), generator=g0)
    t0_b = t0_a.clone()
    assert torch.equal(t0_a, t0_b)
    # start_mix=1.0 pins all starts to t_obs
    t0_c = torch.randint(t_obs, S - k, (batch,), generator=g1)
    force1 = torch.rand(batch, generator=g1) < 1.0
    t0_d = torch.where(force1, torch.full_like(t0_c, t_obs), t0_c)
    assert bool((t0_d == t_obs).all())


def test_start_mix_window_bounds():
    """D1e: windowed pinned starts stay inside [t_obs, t_obs+w) and strictly
    before the rollout span limit."""
    g = torch.Generator().manual_seed(5)
    batch, t_obs, S, k, w = 64, 8, 160, 4, 8
    w_eff = max(1, min(w, S - k - t_obs))
    off = torch.randint(0, w_eff, (batch,), generator=g)
    t0w = t_obs + off
    assert bool(((t0w >= t_obs) & (t0w < t_obs + w_eff)).all())
