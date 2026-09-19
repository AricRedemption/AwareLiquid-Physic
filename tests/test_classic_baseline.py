"""CLASSIC-BASELINE 单元测试(轮 99):经典估计臂的数学契约。"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from benchmarks.classic_baseline_eval import (boundary_state, omega_lsq,
                                              omega_stlsq, rollout_mse)
from benchmarks.m1_semigroup_eval import gen_spring


def _traj(omega=1.3, steps=160, dt=0.1, seed=3):
    g = torch.Generator().manual_seed(seed)
    qs, _, _ = gen_spring(1, steps, dt, 1, omega, omega, g)
    return qs[0, :, 0]


def test_fd_lsq_recovers_omega_within_5pct():
    for w in (0.7, 1.3, 1.8):
        q = _traj(w)
        w_hat = omega_lsq(q[:25], 0.1)
        assert abs(w_hat - w) / w < 0.05      # 预注册判负①阈值


def test_stlsq_recovers_linear_support():
    q = _traj(1.1)
    w_hat = omega_stlsq(q[:25], 0.1)
    assert abs(w_hat - 1.1) / 1.1 < 0.05


def test_exact_omega_yields_near_zero_rollout_mse():
    """真值 ω 下解析边界态 + Verlet 滚出 ≪ 预测量级(管道正确性锚)。
    注意:残余 MSE 是 Verlet 在 dt=0.1 的离散化相位误差(O(dt²) 随 k 积累),
    不是估计误差——真值 ω 滚出与连续真值的偏差由积分器决定。"""
    dt, k = 0.1, 100
    q = _traj(1.2)
    q_T, p_T = boundary_state(q[:25], 1.2, dt)
    # 解析边界态应与 gen_spring 闭式末态一致(LS 拟合精度)
    assert abs(q_T - q[24].item()) < 1e-5
    mse = rollout_mse(q[24:24 + k + 1], 1.2, q_T, p_T, dt, k)
    assert mse < 1e-4
