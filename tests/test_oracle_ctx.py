"""D2-CAPACITY E1 的最小单元测试(wave-10 G4-E1):oracle 投影、指纹查表、场探针。"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from awareliquid_physics.hamiltonian import OperatorHamiltonianHead
from benchmarks.field_eval import (OracleOperatorWrapper, field_context_probe,
                                   mlp_context_probe, oracle_ctx_matrix)


def test_oracle_projection_roundtrip_and_scale():
    """投影必须精确恢复族的线性系数(sin/cos 基在整周期上正交)。"""
    torch.manual_seed(0)
    N, n_modes = 32, 4
    x = torch.arange(N, dtype=torch.float32)
    amps = torch.rand(1, n_modes) * (0.5 / torch.arange(1, n_modes + 1))
    phases = torch.rand(1, n_modes) * 2 * math.pi
    field = torch.zeros(1, N)
    for m in range(1, n_modes + 1):
        field += amps[:, m - 1: m] * torch.sin(
            2 * math.pi * m * x / N + phases[:, m - 1: m])
    ctx = oracle_ctx_matrix(field, 8, scale=1.0)
    expected = []
    for m in range(1, n_modes + 1):
        expected.append(amps[:, m - 1] * torch.cos(phases[:, m - 1]))
        expected.append(amps[:, m - 1] * torch.sin(phases[:, m - 1]))
    exp = torch.stack(expected, dim=1)
    assert ctx.shape == (1, 8)
    assert torch.allclose(ctx, exp, atol=1e-5)
    # scale 归一:c_var=0.5 即翻倍
    assert torch.allclose(oracle_ctx_matrix(field, 8, scale=0.5), 2 * ctx,
                          atol=1e-6)
    try:
        oracle_ctx_matrix(field, 7)
        raise AssertionError("odd context_dim must raise")
    except ValueError:
        pass


def test_oracle_wrapper_lookup_and_miss():
    """批 gather 按前缀指纹找回行号;表外轨迹(分辨率测试族)得零 ctx。"""
    torch.manual_seed(0)
    n, S, N, t_obs = 5, 8, 4, 4
    qs = torch.randn(n, S, N, 1)
    ps = torch.randn(n, S, N, 1)
    row_ctx = torch.arange(n * 4, dtype=torch.float32).reshape(n, 4)
    ham = OperatorHamiltonianHead(dim=1, width=8, modes=4, fno_depth=1,
                                  context_dim=4, hidden_dim=8, t_depth=1,
                                  reflect_pad=0)
    w = OracleOperatorWrapper(ham, 0.1, qs, t_obs, row_ctx)
    bi = [3, 0, 3]
    q_obs = qs[bi, :t_obs]
    assert w.lookup_rows(q_obs) == [3, 0, 3]
    ctx = w.infer_context(q_obs, ps[bi, :t_obs])
    assert torch.equal(ctx, row_ctx[[3, 0, 3]])
    q_new = torch.randn(1, t_obs, N, 1)
    ctx2 = w.infer_context(q_new, torch.randn(1, t_obs, N, 1))
    assert torch.equal(ctx2, torch.zeros(1, 4))


def test_field_context_probe_high_corr_and_json_safe():
    """线性混叠的 ctx 可被线性探针恢复(corr≈1);常数目标折叠为有限计数。"""
    torch.manual_seed(0)
    n, S, ctx_dim, out_dim = 32, 6, 8, 4
    coeffs = torch.randn(n, out_dim)
    qs = coeffs.reshape(n, 1, out_dim, 1).expand(n, S, out_dim, 1).contiguous()
    ps = torch.randn(n, S, out_dim, 1)

    class Stub(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.w = torch.randn(ctx_dim, out_dim * out_dim)
            self.b = torch.randn(ctx_dim)

        def forward(self, q_obs, p_obs, k):
            feats = q_obs.reshape(q_obs.shape[0], -1)
            return None, None, feats @ self.w.T + self.b

    res = field_context_probe(Stub(), qs, ps, coeffs, t_obs=4)
    assert res["ctx_probe_n_finite"] == out_dim
    assert res["ctx_probe_corr_mean"] > 0.95
    res2 = field_context_probe(Stub(), qs, ps, torch.ones(n, out_dim), t_obs=4)
    assert res2["ctx_probe_n_finite"] == 0
    assert res2["ctx_probe_corr_mean"] == 0.0


def test_mlp_probe_captures_nonlinear_encoding_linear_misses():
    """E3 的 MLP 探针必须读出纯二次编码(积/平方),而线性探针读不出——
    收口'信息在但非线性编码'的判别漏洞。"""
    torch.manual_seed(0)
    n, S = 64, 6
    z = torch.randn(n, 2)
    coeffs = torch.stack([z[:, 0] * z[:, 1], z[:, 0] ** 2, z[:, 1] ** 2], dim=1)
    qs = z.reshape(n, 1, 2, 1).expand(n, S, 2, 1).contiguous()
    ps = torch.randn(n, S, 2, 1)

    class Stub(torch.nn.Module):
        def forward(self, q_obs, p_obs, k):
            return None, None, q_obs.reshape(q_obs.shape[0], -1)[:, :2]

    lin = field_context_probe(Stub(), qs, ps, coeffs, t_obs=4)
    mlp = mlp_context_probe(Stub(), qs, ps, coeffs, t_obs=4, seed=0)
    assert lin["ctx_probe_corr_mean"] < 0.3
    assert mlp["ctx_mlp_n_finite"] == 3
    assert mlp["ctx_mlp_corr_mean"] > 0.7
