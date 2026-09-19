"""R1C-AGG 先决探针的单元测试(轮 95):mean-pool Fisher 的数学性质。

1. Cauchy-Schwarz 不变式:0 <= J_pool <= J_full(均值泛函是全场泛函的
   线性投影,信息不增)。
2. 均值场恒等式(轮 95 机制发现):周期网格上离散拉普拉斯加速度的
   空间均值恒为零(Σc_i²(q_{i+1}−q_i) 与 reindex 后的 Σc_{i-1}²(q_i−q_{i-1})
   逐项抵消)⇒ 均值场 m(t) 严格匀速(m(0)+t·p̄(0)),与介质 c(x) 完全
   无关——聚合层对 c 一切模式(含 k=0)的信息保留恒等零,非均匀介质
   下亦然(恒等式不依赖 c 形状)。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from benchmarks.field_identifiability_probe import fisher_pair, mode_field, rollout


def test_meanpool_fisher_never_exceeds_full_field():
    g = torch.Generator().manual_seed(0)
    N, steps = 16, 60
    q0 = torch.randn(N, generator=g) * 0.1
    p0 = torch.randn(N, generator=g) * 0.1
    c = 1.0 + 0.5 * mode_field(N, 1)          # 非均匀介质
    for k in (0, 1, 3):
        j_full, j_pool = fisher_pair(
            lambda a: rollout(q0, p0, c + a * mode_field(N, k), steps, 0.05)[:17],
            a_pert=1e-3)
        assert j_full > 0.0
        assert 0.0 <= j_pool <= j_full * (1 + 1e-9)


def test_mean_field_is_medium_independent_ballistic():
    """均值场恒等式:加速度的空间均值恒为零 ⇒ m(t) 与 c 无关。"""
    g = torch.Generator().manual_seed(1)
    N, steps = 16, 60
    q0 = torch.randn(N, generator=g) * 0.1
    p0 = torch.randn(N, generator=g) * 0.1
    for c in (torch.ones(N), 1.0 + 0.5 * mode_field(N, 1),
              1.0 + 0.5 * mode_field(N, 3)):
        u1 = rollout(q0, p0, c, steps, 0.05)
        u2 = rollout(q0, p0, 2.0 * c, steps, 0.05)   # 介质翻倍
        m1, m2 = u1.mean(dim=1), u2.mean(dim=1)
        assert torch.allclose(m1, m2, atol=1e-6)     # 均值轨迹与介质无关
        # 匀速性:m(t) = m(0) + (t·dt)·p̄(0) 线性(Verlet 每步位移 dt·p̄)
        t = torch.arange(steps + 1, dtype=torch.float32)
        fit = m1[0] + t * 0.05 * p0.mean()
        assert torch.allclose(m1, fit, atol=1e-5)


def test_all_modes_annihilated_under_spatial_pooling():
    g = torch.Generator().manual_seed(2)
    N, steps = 16, 60
    q0 = torch.randn(N, generator=g) * 0.1
    p0 = torch.randn(N, generator=g) * 0.1
    c = 1.0 + 0.5 * mode_field(N, 2)           # 非均匀介质
    for k in (0, 1, 2, 5):                     # 含 k=0: 恒等式不豁免常数模式
        j_full, j_pool = fisher_pair(
            lambda a: rollout(q0, p0, c + a * mode_field(N, k), steps, 0.05)[:17],
            a_pert=1e-3)
        assert j_full > 0.0
        assert j_pool < 1e-10                  # FD 噪声级: 精确湮灭
