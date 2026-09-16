"""D3 (wave-10 round 10): identifiability of the hidden omega in the M1
spring family — Fisher information of the observation window.

P3 ledger gap: "hidden-parameter identifiability vs liquid gain is unmodelled;
task selection currently relies on intuition." This probe makes the
identifiability axis quantitative on the family where liquid system-ID gains
the most. For the harmonic ground-truth engine,

    q(t) = q0 cos(wt) + (p0/w) sin(wt)
    p(t) = p0 cos(wt) - q0 w sin(wt),

the per-trajectory Fisher information (unit observation noise) over the
t_obs prefix window is J(w; q0, p0) = sum_t [(dq/dw)^2 + (dp/dw)^2], with the
closed-form sensitivities

    dq/dw = -q0 t sin(wt) + p0 (t cos(wt)/w - sin(wt)/w^2)
    dp/dw = -p0 t sin(wt) - q0 (sin(wt) + w t cos(wt))

We report J over an omega grid (mean/std over random initial states) — zero
training — plus the dynamic range across the family. Next round correlates
per-trajectory J with per-trajectory rollout error of a trained model
(the preregistered correlation experiment).

Usage:
    python benchmarks/identifiability_probe.py   # instant, CPU
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from awareliquid_physics.observability import run_metadata


def fisher_j(omega: float, q0: float, p0: float, t_obs: int, dt: float) -> float:
    """Closed-form J for one (omega, q0, p0); grid t = dt * (1..t_obs)."""
    total = 0.0
    for i in range(1, t_obs + 1):
        t = dt * i
        s, c = math.sin(omega * t), math.cos(omega * t)
        dq = -q0 * t * s + p0 * (t * c / omega - s / omega ** 2)
        dp = -p0 * t * s - q0 * (s + omega * t * c)
        total += dq * dq + dp * dp
    return total


def fisher_j_fd(omega: float, q0: float, p0: float, t_obs: int, dt: float,
                eps: float = 1e-6) -> float:
    """Central-difference reference: J via numerical dq/dw, dp/dw."""

    def traj(om):
        pts = []
        for i in range(1, t_obs + 1):
            t = dt * i
            pts.append((q0 * math.cos(om * t) + p0 / om * math.sin(om * t),
                        p0 * math.cos(om * t) - q0 * om * math.sin(om * t)))
        return pts

    up, lo = traj(omega + eps), traj(omega - eps)
    return sum(((u[0] - l[0]) / (2 * eps)) ** 2 + ((u[1] - l[1]) / (2 * eps)) ** 2
               for u, l in zip(up, lo))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--n_grid", type=int, default=45)
    ap.add_argument("--n_draws", type=int, default=200,
                    help="random (q0, p0) draws averaged per omega")
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu", choices=["cpu"])
    ap.add_argument("--out_dir", default="benchmarks/physics_out_v02/d3_identifiability")
    args = ap.parse_args()

    g = torch.Generator().manual_seed(args.seed)
    draws = [(torch.randn(1, generator=g).item(),
              torch.randn(1, generator=g).item()) for _ in range(args.n_draws)]
    grid = [args.omega_lo + (args.omega_hi - args.omega_lo) * i / (args.n_grid - 1)
            for i in range(args.n_grid)]

    j_mean, j_std = [], []
    for om in grid:
        js = [fisher_j(om, q0, p0, args.t_obs, args.dt) for q0, p0 in draws]
        m = sum(js) / len(js)
        j_mean.append(m)
        j_std.append((sum((j - m) ** 2 for j in js) / len(js)) ** 0.5)

    peak = grid[max(range(len(j_mean)), key=lambda i: j_mean[i])]
    trough = grid[min(range(len(j_mean)), key=lambda i: j_mean[i])]
    dynamic_range = max(j_mean) / max(min(j_mean), 1e-300)

    # closed form vs finite differences on a fixed spot
    j_a = fisher_j(1.2, 0.8, -0.5, args.t_obs, args.dt)
    j_f = fisher_j_fd(1.2, 0.8, -0.5, args.t_obs, args.dt)
    rel_err = abs(j_a - j_f) / j_a

    results = {"omega_grid": grid, "j_mean": j_mean, "j_std": j_std,
               "argmax_omega": peak, "argmin_omega": trough,
               "dynamic_range": dynamic_range,
               "closed_form_vs_fd_relerr": rel_err,
               "seed_note": "J curve is deterministic; draws averaged"}
    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "identifiability.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({"benchmark": "identifiability_probe",
                                         "device": args.device}),
                   "results": results}, f, indent=2)

    print(f"D3 identifiability | J(omega) over [{args.omega_lo}, {args.omega_hi}], "
          f"t_obs={args.t_obs}, dt={args.dt}")
    print(f"  peak J at omega={peak:.3f} | trough at {trough:.3f} | "
          f"dynamic range {dynamic_range:.1f}x")
    print(f"  closed form vs central-difference rel err: {rel_err:.2e}")
    print(f"  -> {os.path.join(args.out_dir, 'identifiability.json')}")


if __name__ == "__main__":
    main()
