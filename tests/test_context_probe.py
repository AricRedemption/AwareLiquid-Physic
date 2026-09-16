"""D1 诊断的最小单元测试(wave-10):context_probe 的线性解码口径。

探针协议:context→ω 线性读出在 eval 前半拟合,在另一半上报逐轨迹
相对误差 |ω̂−ω|/ω 与相关系数。这里用可解析构造的玩具模型钉死:
① context 线性含 ω 时误差≈0、相关≈1;② context 与 ω 无关时误差大、
相关低。防回归点:NaN/Inf 相关系数必须落成 0(strict-JSON 安全)。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from benchmarks.sample_efficiency_eval import context_probe


class _ToyModel:
    """Forward returns a FIXED context regardless of input (probe target)."""

    def __init__(self, ctx):
        self.ctx = ctx

    def eval(self):
        return self

    def __call__(self, q_obs, p_obs, k):
        return None, None, self.ctx


def _run(ctx, omega):
    n = ctx.shape[0]
    qs = torch.zeros(n, 24, 1)
    ps = torch.zeros(n, 24, 1)
    return context_probe(_ToyModel(ctx), qs, ps, omega, t_obs=24)


def test_probe_recovers_linear_relation():
    torch.manual_seed(0)
    n = 64
    omega = 0.7 + 1.1 * torch.rand(n, 1)
    ctx = torch.cat([omega, torch.randn(n, 7)], dim=1)   # ctx[:,0] = omega
    out = _run(ctx, omega)
    assert out["ctx_rel_err_mean"] < 1e-3
    assert out["ctx_corr"] > 0.999


def test_probe_reports_high_error_for_uninformative_context():
    torch.manual_seed(0)
    n = 64
    omega = 0.7 + 1.1 * torch.rand(n, 1)
    out = _run(torch.randn(n, 8), omega)   # context independent of omega
    assert out["ctx_rel_err_mean"] > 0.05
    assert abs(out["ctx_corr"]) < 0.6


def test_probe_nan_corr_is_json_safe():
    n = 8
    omega = torch.full((n, 1), 1.0)        # constant true omega -> corr undefined
    out = _run(torch.randn(n, 8), omega)
    assert out["ctx_corr"] == 0.0          # NaN folded to 0, no NaN/Inf in JSON
