"""D3 cross-task extrapolation (wave-10 round 42): spectral identifiability
of the hidden c(x) FIELD in the M2 inhomogeneous string family.

P3 ledger, cross-task axis: the D3 probe showed the spring family's
scalar-omega identifiability is uniform within the band (1.5x) and the
window-length axis is the real lever. This probe asks the same question for
the FIELD family: which SPATIAL FREQUENCIES of the hidden wave-speed field
c(x) does the t_obs observation window actually constrain?

Method: for each of m trajectories drawn exactly as in
gen_wave_1d_inhomogeneous, compute the Fisher information of the
observation window w.r.t. the amplitude a_k of each real Fourier mode of
c(x), J_k = sum_t sum_j (du_j(t)/da_k)^2, via central differences on a
velocity-Verlet rollout replicated from datasets.py (accel:
c_i^2 (q_{i+1}-q_i) - c_{i-1}^2 (q_i - q_{i-1})). Also reports the family's
own spectral support |FFT(c)| per mode (the family draws only n_modes=4 low
modes). Zero training; instant.

Preregistered readings (either is a valid P3-extrapolation data point):
  1. J_k decays with mode index -> low frequencies identifiable, high ones
     not; prediction: liquid context gains on M2 concentrate on low-frequency
     c-structure. Cross-check: the family's 4-mode support sits in the
     identifiable band (task well-posed).
  2. J_k flat -> all frequencies equally identifiable; cross-task gain
     differences must come from parameter dimensionality, not identifiability.

Usage:
    python benchmarks/field_identifiability_probe.py   # instant, CPU
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from awareliquid_physics.datasets import gen_wave_1d_inhomogeneous
from awareliquid_physics.observability import run_metadata
from awareliquid_physics.physics_ops import integrate_verlet


def rollout(q0: torch.Tensor, p0: torch.Tensor, c: torch.Tensor,
            steps: int, dt: float) -> torch.Tensor:
    """Verlet rollout with a custom speed field c (N,), replicating the
    inhomogeneous accel in datasets.gen_wave_1d_inhomogeneous.
    Returns u over time (steps+1, N)."""
    c2 = (c * c).unsqueeze(-1)
    c2_shift = torch.roll(c2, 1, dims=0)

    def accel(pos: torch.Tensor) -> torch.Tensor:
        dq_f = torch.roll(pos, -1, dims=0) - pos
        dq_b = pos - torch.roll(pos, 1, dims=0)
        return c2 * dq_f - c2_shift * dq_b

    pos = q0.reshape(-1, 1)
    vel = p0.reshape(-1, 1)
    a = accel(pos)
    out = [pos.squeeze(-1)]
    for _ in range(steps):
        pos, vel, a = integrate_verlet(pos, vel, accel, dt, accel=a)
        out.append(pos.squeeze(-1))
    return torch.stack(out)   # (steps+1, N)


def mode_field(N: int, k: int) -> torch.Tensor:
    """Unit-amplitude real Fourier mode on the periodic grid (cos for k=0)."""
    x = torch.arange(N, dtype=torch.float32)
    if k == 0:
        return torch.ones(N)
    return torch.cos(2 * math.pi * k * x / N)


def fisher_for_mode(base_u_fn, a_pert: float):
    up = base_u_fn(+a_pert)
    lo = base_u_fn(-a_pert)
    du = (up - lo) / (2 * a_pert)
    return (du ** 2).sum().item()


def fisher_pair(base_u_fn, a_pert: float):
    """R1C-AGG 先决探针 (wave-10 轮 95): full-field Fisher 与 mean-pool
    (空间均值) Fisher 的成对中心差分。

    模型编码器对共享线性层先做空间均值池化 (model.py:104,119-120:
    mean_N(node_enc(o)) == node_enc(mean_N(o)), 线性可交换), 故聚合层
    输入恰为均值场轨迹 m(t)。J_meanpool = sum_t (mean_j du_j(t))^2 度量
    该均值泛函对 c(x) 第 k 模式的可辨识性; 由 Cauchy-Schwarz 恒有
    0 <= J_meanpool <= J_full。

    机制发现 (轮 95, 比预注册更强的形态): 周期网格上加速度的空间均值
    恒为零——Σ_i c_i²(q_{i+1}−q_i) 与 reindex 后的 Σ c_{i-1}²(q_i−q_{i-1})
    逐项抵消 (对任意 c(x) 成立) ⇒ m(t) = m(0)+t·p̄(0) 严格匀速且与介质
    无关。聚合层对 c(x) 一切模式 (含 k=0) 的信息保留为**精确零** (FD
    噪声级), 非均匀介质的模态耦合也不改变该恒等式。
    """
    up = base_u_fn(+a_pert)
    lo = base_u_fn(-a_pert)
    du = (up - lo) / (2 * a_pert)          # (t_obs+1, N)
    j_full = (du ** 2).sum().item()
    j_pool = ((du.mean(dim=1)) ** 2).sum().item()
    return j_full, j_pool


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_traj", type=int, default=8)
    ap.add_argument("--n_modes_gen", type=int, default=4,
                    help="modes drawn by the FAMILY generator (its support)")
    ap.add_argument("--n_nodes", type=int, default=32)
    ap.add_argument("--steps", type=int, default=120)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--c_mean", type=float, default=1.0)
    ap.add_argument("--c_var", type=float, default=0.5)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--a_pert", type=float, default=1e-3,
                    help="FD amplitude of the mode coefficient")
    ap.add_argument("--meanpool", action="store_true",
                    help="R1C-AGG 先决: 同时计算空间均值池化的 Fisher 谱"
                         "(模型聚合层信息保留率, 轮 95)")
    ap.add_argument("--device", default="cpu", choices=["cpu"])
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/d3_field_identifiability")
    args = ap.parse_args()

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, cs = gen_wave_1d_inhomogeneous(
        args.n_traj, args.steps, args.dt, args.n_nodes, args.c_mean,
        args.c_var, g, n_modes=args.n_modes_gen, device=args.device)
    # qs: (n_traj, steps+1, N, 1); use only the t_obs window for J
    N = args.n_nodes
    half = N // 2                     # real field: unique cos frequencies
    j_means, j_stds, support = [], [], []
    j_pool_means = []
    for i in range(args.n_traj):
        q0, p0, c = qs[i, 0, :, 0], ps[i, 0, :, 0], cs[i]
        support.append(torch.fft.rfft(c - c.mean()).abs())
        row = []
        row_pool = []
        for k in range(half + 1):
            mk = mode_field(N, k)

            def base_u_fn(a):
                u = rollout(q0, p0, c + a * mk, args.steps, args.dt)
                return u[:args.t_obs + 1]     # observation window only

            if args.meanpool:
                j_full, j_pool = fisher_pair(base_u_fn, args.a_pert)
                row.append(j_full)
                row_pool.append(j_pool)
            else:
                row.append(fisher_for_mode(base_u_fn, args.a_pert))
        j_pool_means.append(row_pool)
        j_means.append(row)
    J = torch.tensor(j_means)
    j_mean = J.mean(dim=0)
    j_std = J.std(dim=0) if J.shape[0] > 1 else torch.zeros_like(J[0])
    j_frac = j_mean / j_mean.sum()
    sup_mean = torch.stack(support).mean(dim=0)
    sup_frac = sup_mean / sup_mean.sum()

    results = {
        "mode_k": list(range(half + 1)),
        "j_mean_window": j_mean.tolist(),
        "j_std_window": j_std.tolist(),
        "j_frac_window": j_frac.tolist(),
        "family_spectral_support_frac": sup_frac.tolist(),
        "dynamic_range_j": (j_mean.max() / max(j_mean.min(), 1e-300)).item(),
    }
    if args.meanpool:
        JP = torch.tensor(j_pool_means)
        jp_mean = JP.mean(dim=0)
        retention = [jp / max(jf, 1e-300)
                     for jp, jf in zip(jp_mean.tolist(), j_mean.tolist())]
        total_retention = (jp_mean.sum() / max(j_mean.sum().item(), 1e-300)).item()
        results.update({
            "j_meanpool_window": jp_mean.tolist(),
            "meanpool_retention_frac_per_mode": retention,
            "meanpool_total_retention_frac": total_retention,
        })
    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "field_identifiability.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({"benchmark": "field_identifiability_probe",
                                         "device": args.device}),
                   "results": results}, f, indent=2)

    print(f"D3 field identifiability | J(a_k) spectrum over {half + 1} cos "
          f"modes, t_obs={args.t_obs}, N={N}, {args.n_traj} trajectories")
    for k in range(half + 1):
        bar = "#" * max(1, int(40 * j_frac[k]))
        print(f"  k={k:>2}: J {j_mean[k]:10.3e} ({j_frac[k] * 100:5.1f}%) "
              f"| family support {sup_frac[k] * 100:5.1f}% | {bar}")
    print(f"  dynamic range: {results['dynamic_range_j']:.1f}x")
    if args.meanpool:
        print("  mean-pool retention per mode (J_pool / J_full):")
        for k in range(half + 1):
            print(f"    k={k:>2}: {retention[k]:8.4f} "
                  f"({results['j_frac_window'][k] * 100:5.1f}% of full-field J)")
        print(f"  total retention (sum_k J_pool / sum_k J_full): "
              f"{total_retention:.4f}")


if __name__ == "__main__":
    main()
