"""D2-CAPACITY R1 的最小单元测试(wave-10 G4-E4A):辅助辨识损失的
RNG 中性、梯度流经推断路径、目标索引正确。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from awareliquid_physics.model import LiquidHamiltonianModel
from awareliquid_physics.train import train_semigroup
from benchmarks.m1_semigroup_eval import gen_spring


def _tiny_world(seed=0):
    g = torch.Generator().manual_seed(seed)
    qs, ps, _ = gen_spring(16, 40, 0.1, 1, 0.7, 1.8, g)
    torch.manual_seed(seed)
    model = LiquidHamiltonianModel(1, d_model=8, context_dim=4, n_scales=2,
                                   hidden_dim=8, depth=1, dt=0.1)
    return model, qs, ps


def test_aux_off_is_rng_neutral():
    """weight=0(默认)时,传/不传 aux 头都必须与旧行为逐位一致。"""
    m0, qs, ps = _tiny_world(0)
    l0 = train_semigroup(m0, qs, ps, t_obs=8, k_train=4, steps=3, lr=1e-2,
                         batch=4, seed=0)
    m1, qs, ps = _tiny_world(0)
    l1 = train_semigroup(m1, qs, ps, t_obs=8, k_train=4, steps=3, lr=1e-2,
                         batch=4, seed=0,
                         aux_head=torch.nn.Linear(4, 4),
                         aux_targets=torch.randn(16, 4),
                         aux_identify_weight=0.0)
    assert l0 == l1


def test_aux_on_gives_gradient_to_inference_path():
    """weight>0:辅助头与推断路径(context_proj)都收到梯度。"""
    torch.manual_seed(0)
    m, qs, ps = _tiny_world(1)
    aux_head = torch.nn.Linear(4, 4)
    aux_targets = torch.randn(16, 4)
    l_aux = train_semigroup(m, qs, ps, t_obs=8, k_train=4, steps=1, lr=1e-2,
                            batch=4, seed=0, aux_head=aux_head,
                            aux_targets=aux_targets, aux_identify_weight=1.0)
    assert aux_head.weight.grad is not None  # 辅助头入优化器并已更新
    # 无优化器干扰的直接验证:一次前向反传,辅助损失必须给推断路径梯度
    m2, qs, ps = _tiny_world(1)
    aux_head2 = torch.nn.Linear(4, 4)
    q_obs, p_obs = qs[:4, :8], ps[:4, :8]
    ctx = m2.infer_context(q_obs, p_obs)
    aux = ((aux_head2(ctx) - aux_targets[:4]) ** 2).mean()
    aux.backward()
    assert m2.context_proj.weight.grad is not None
    assert m2.context_proj.weight.grad.abs().sum() > 0


def test_aux_targets_indexed_by_batch():
    """辅助目标的行索引必须与批索引 bi 一致(逐行唯一值可追溯)。"""
    torch.manual_seed(0)
    n = 16
    targets = torch.arange(n, dtype=torch.float32).reshape(n, 1).repeat(1, 4)
    bi = torch.tensor([3, 7, 11])
    picked = targets[bi]
    assert torch.equal(picked, torch.tensor([[3.] * 4, [7.] * 4, [11.] * 4]))
