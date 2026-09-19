"""R1C-AGG 池化参数化的单元测试(轮 95)。

判据背景(PR D §19 轮 95 预注册):mean 池化是聚合层信息湮灭点(均值场
恒等式),attn 聚合是修复候选。测试钉三条契约:
1. pool="mean" 与历史实现逐位一致(重构不变式);
2. pool="attn" 零初始化分数 ⇒ 起始严格等价 mean;扰动分数后偏离且梯度
   流经 pool_score 与 node_enc;
3. 非法 pool 值在构造期拒绝。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import torch

from awareliquid_physics.model import LiquidOperatorHamiltonianModel


KW = dict(phase_dim=1, d_model=16, context_dim=4, n_scales=2, modes=4,
          width=8, fno_depth=1, hidden_dim=8, t_depth=1,
          dt=0.05, core_dt=1.0, reflect_pad=2)


def _inputs(seed=0, B=2, T=6, N=8):
    g = torch.Generator().manual_seed(seed)
    q = torch.randn(B, T, N, 1, generator=g)
    p = torch.randn(B, T, N, 1, generator=g)
    return q, p


def test_mean_pool_bitwise_matches_legacy_reference():
    torch.manual_seed(7)
    model = LiquidOperatorHamiltonianModel(pool="mean", **KW)
    q, p = _inputs()
    with torch.no_grad():
        y = model.infer_context(q, p)
        # legacy 公式手工复算:cat -> node_enc -> mean over N -> core -> proj
        h = model.node_enc(torch.cat([q, p], dim=-1))
        ref = model.context_proj(model.core.encode(h.mean(dim=2)))
    assert torch.equal(y, ref)
    # mean 池化不引入新参数(状态字典与历史结构同构)
    assert not any("pool_score" in k for k in model.state_dict())


def test_attn_zero_init_equals_mean_then_learns_to_deviate():
    torch.manual_seed(7)
    mean_model = LiquidOperatorHamiltonianModel(pool="mean", **KW)
    attn_model = LiquidOperatorHamiltonianModel(pool="attn", **KW)
    # 载入同一 trunk 权重(pool_score 零初始化不参与比较)
    attn_model.load_state_dict(mean_model.state_dict(), strict=False)
    q, p = _inputs()
    with torch.no_grad():
        y_mean = mean_model.infer_context(q, p)
        y_attn0 = attn_model.infer_context(q, p)
    assert torch.allclose(y_attn0, y_mean, atol=1e-6)  # 零分 ⇒ 均匀 softmax = mean
    # 扰动分数后偏离,且梯度到达 pool_score / node_enc
    with torch.no_grad():
        attn_model.pool_score.weight.add_(0.05 * torch.randn_like(
            attn_model.pool_score.weight))
    y_attn = attn_model.infer_context(q, p)
    assert not torch.allclose(y_attn, y_mean, atol=1e-6)
    loss = y_attn.pow(2).sum()
    loss.backward()
    assert attn_model.pool_score.weight.grad is not None
    assert attn_model.pool_score.weight.grad.abs().sum() > 0
    assert attn_model.node_enc.weight.grad is not None


def test_invalid_pool_rejected():
    with pytest.raises(ValueError):
        LiquidOperatorHamiltonianModel(pool="sum", **KW)
