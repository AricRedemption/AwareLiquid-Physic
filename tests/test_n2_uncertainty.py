"""N2 的最小单元测试(wave-10 轮 22):不确定性代理的形状与归一。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from awareliquid_physics.model import LiquidHamiltonianModel
from awareliquid_physics.train import _start_uncertainty
from benchmarks.m1_semigroup_eval import gen_spring


def test_start_uncertainty_shapes_and_normalization():
    torch.manual_seed(0)
    g = torch.Generator().manual_seed(0)
    qs, ps, _ = gen_spring(16, 160, 0.1, 1, 0.7, 1.8, g)
    model = LiquidHamiltonianModel(1, d_model=8, context_dim=4, n_scales=2,
                                   hidden_dim=8, depth=1, dt=0.1)
    cand_t, w = _start_uncertainty(model, qs, ps, t_obs=8, k_train=4,
                                   cand_cap=16, n_pert=3)
    assert cand_t.shape == w.shape
    assert abs(w.sum().item() - 1.0) < 1e-5          # softmax normalized
    # contract: starts stay within [t_obs, S - k_train - 1] where S is the
    # ACTUAL trajectory length (gen_spring returns steps+1 points) — targets
    # reach t0 + k_train during training
    S = qs.shape[1]
    assert bool((cand_t >= 8).all()) and bool((cand_t <= S - 4 - 1).all())
    assert bool((w > 0).all())                       # strictly positive weights
    model.train()                                    # helper must restore state
