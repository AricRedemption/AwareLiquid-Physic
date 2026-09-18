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
    for i in range(args.n_traj):
        q0, p0, c = qs[i, 0, :, 0], ps[i, 0, :, 0], cs[i]
        support.append(torch.fft.rfft(c - c.mean()).abs())
        row = []
        for k in range(half + 1):
            mk = mode_field(N, k)

            def base_u_fn(a):
                u = rollout(q0, p0, c + a * mk, args.steps, args.dt)
                return u[:args.t_obs + 1]     # observation window only

            row.append(fisher_for_mode(base_u_fn, args.a_pert))
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


if __name__ == "__main__":
    main()
