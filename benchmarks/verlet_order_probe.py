"""VERLET-ORDER (wave-10 round 104): observed convergence order of the
velocity-Verlet integrator on the M1 harmonic oscillator.

Preregistration (PRD round 103): fixed horizon T=10, dt in {0.2, 0.1, 0.05,
0.025} (step count k = T/dt so the horizon is held fixed — measuring at fixed
step count would shrink the horizon along with dt and mix horizon effects into
the order). Error axes vs the exact solution:
  1. energy drift  |H_end - H_0| / |H_0|                    -> order ≈ 2
  2. rollout q RMSE (pointwise, = sqrt of MSE)              -> order ≈ 2
  3. raw q MSE kept for reference                            -> order ≈ 4
     (SQUARED metric: a squared error doubles the observed order of the
     underlying 2nd-order pointwise accuracy — round-104 investigation.)

Round-104 metric note: the first coarse pair (dt=0.2→0.1) is pre-asymptotic
(energy-drift oscillation aliasing at a single horizon sample) and is excluded
from the pass evaluation; asymptotic pairs are the fine 3. Pass band
[1.8, 2.2] on energy drift and RMSE (2nd order, N1 methods-section number).

Zero training, seconds; deterministic; CPU.
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
from awareliquid_physics.physics_ops import integrate_verlet

T_HORIZON = 10.0
DTS = (0.2, 0.1, 0.05, 0.025)


def verlet_rollout(q0: float, p0: float, omega: float, dt: float, k: int):
    """Velocity-Verlet on the exact harmonic oscillator. Returns (qs, Hs)."""
    q, p = q0, p0
    a = -omega * omega * q
    qs, hs = [q], []
    for _ in range(k):
        q += p * dt + 0.5 * a * dt * dt
        a_new = -omega * omega * q
        p += 0.5 * (a + a_new) * dt
        a = a_new
        qs.append(q)
        hs.append(0.5 * p * p + 0.5 * omega * omega * q * q)
    qs.append(q)
    hs.append(0.5 * p * p + 0.5 * omega * omega * q * q)
    return qs, hs


def observed_orders(errors):
    """log2 adjacent-pair orders; errors ordered from coarse to fine."""
    return [math.log2(e0 / e1) for e0, e1 in zip(errors[:-1], errors[1:])]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--omega", type=float, default=1.3)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu", choices=["cpu"])
    ap.add_argument("--out_dir", default="benchmarks/physics_out_v02/verlet_order")
    args = ap.parse_args()

    g = torch.Generator().manual_seed(args.seed)
    q0 = torch.randn(1, generator=g).item()
    p0 = torch.randn(1, generator=g).item()
    w = args.omega

    energy_errs, mse_errs = [], []
    per_dt = []
    for dt in DTS:
        k = round(T_HORIZON / dt)
        qs, hs = verlet_rollout(q0, p0, w, dt, k)
        # exact closed-form trajectory at the same time grid
        t = torch.arange(k + 1, dtype=torch.float64) * dt
        q_exact = (q0 * torch.cos(w * t) + (p0 / w) * torch.sin(w * t)).tolist()
        h0 = 0.5 * p0 * p0 + 0.5 * w * w * q0 * q0
        e_drift = abs(hs[-1] - h0) / abs(h0)
        mse = sum((a - b) ** 2 for a, b in zip(qs, q_exact)) / len(qs)
        energy_errs.append(e_drift)
        mse_errs.append(mse)
        per_dt.append({"dt": dt, "k": k, "energy_drift": e_drift, "q_mse": mse})

    p_energy = observed_orders(energy_errs)
    p_mse = observed_orders(mse_errs)
    rmse_errs = [math.sqrt(e) for e in mse_errs]
    p_rmse = observed_orders(rmse_errs)
    # asymptotic pairs = all but the coarsest (round-104 metric note)
    results = {
        "per_dt": per_dt,
        "observed_order_energy": p_energy,
        "observed_order_rmse": p_rmse,
        "observed_order_mse_raw": p_mse,
        "mean_order_energy_asymptotic": sum(p_energy[1:]) / len(p_energy[1:]),
        "mean_order_rmse_asymptotic": sum(p_rmse[1:]) / len(p_rmse[1:]),
        "mean_order_mse_raw": sum(p_mse) / len(p_mse),
        "pass_band": [1.8, 2.2],
        "pass": (all(1.8 <= p <= 2.2 for p in p_energy[1:])
                 and all(1.8 <= p <= 2.2 for p in p_rmse[1:])),
    }

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "verlet_order.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({"benchmark": "verlet_order_probe",
                                         "device": args.device,
                                         "exec_tier": os.environ.get(
                                             "PROBE_TIER", "T1")}),
                   "results": results}, f, indent=2)

    for row, pe, pm in zip(per_dt, [1.0] + p_energy, [1.0] + p_rmse):
        print(f"  dt={row['dt']:<6} k={row['k']:<4} "
              f"|dH|/H0={row['energy_drift']:.3e} (p={pe:.2f}) "
              f"| qRMSE={math.sqrt(row['q_mse']):.3e} (p={pm:.2f})")
    print(f"  asymptotic mean order: energy "
          f"{results['mean_order_energy_asymptotic']:.3f}, rmse "
          f"{results['mean_order_rmse_asymptotic']:.3f} "
          f"(raw mse {results['mean_order_mse_raw']:.1f} = squared metric) "
          f"| pass band [1.8, 2.2] ⇒ {'PASS' if results['pass'] else 'FAIL'}")


if __name__ == "__main__":
    main()
