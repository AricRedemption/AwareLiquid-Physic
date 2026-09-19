"""CLASSIC-BASELINE (wave-10 round 99): classical system-ID baselines on the
M1 same-pool eval set as the TSFM protocol (docs/classic-baseline-protocol.md).

Two arms, both exploiting the KNOWN model form (harmonic oscillator) — this is
what "classical" means here: structure-exploiting estimators, the fair
classical competitor for a linear oscillator:
  1. LSQ-omega: central finite-difference acceleration + linear least squares
     through origin (qdd = -w^2 q) -> omega-hat; analytic (A, B) fit given
     omega-hat for the boundary state (spectral accuracy, no FD boundary error).
  2. STLSQ: sequential-thresholded least squares over the polynomial library
     [q, qdot, q^2, q*qdot, qdot^2] on FD derivatives; omega-hat = sqrt(|c_q|).

Honest-positioning preregistration (PRD round 98): on NOISE-FREE linear
oscillators the classical estimator is expected to be near-oracle — the row
exists for N1 baseline-table completeness, NOT for a ranking claim (fairness
three-statement protocol, cf. scan §19.4 / round 82).

Same-pool protocol identical to tsfm_baseline_eval: last 128 trajectories of
gen_spring(n_train+128, steps=160, dt=0.1, omega in [0.7, 1.8], seed s),
s in {0,1,2}; t_obs=24; k=100; q-only observations (p reconstructed from the
fit — declared, not hidden).

Zero-to-seconds compute; deterministic; CPU.
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
from benchmarks.m1_semigroup_eval import gen_spring

N_EVAL, POOL_STEPS, DT, T_OBS, K_EVAL = 128, 160, 0.1, 24, 100
OMEGA_LO, OMEGA_HI, SEEDS = 0.7, 1.8, (0, 1, 2)
N_POOLS = (32, 64)


def omega_lsq(q: torch.Tensor, dt: float) -> float:
    """FD acceleration + LS through origin: qdd_t = -w^2 q_t.
    q: (T,) observed prefix."""
    qdd = (q[2:] - 2 * q[1:-1] + q[:-2]) / (dt * dt)
    qq = q[1:-1]
    w2 = -(qdd * qq).sum().item() / qq.pow(2).sum().item()
    return math.sqrt(max(w2, 1e-12))


def _design(q: torch.Tensor, qd: torch.Tensor) -> torch.Tensor:
    """Polynomial library (no constant term — oscillators have no drift)."""
    return torch.stack([q, qd, q * q, q * qd, qd * qd], dim=1)


def stlsq(q: torch.Tensor, qd: torch.Tensor, qdd: torch.Tensor,
          threshold: float = 1e-2, iters: int = 20) -> torch.Tensor:
    """Sequentially thresholded least squares -> coefficient vector (5,)."""
    theta = _design(q, qd)
    coef = torch.linalg.lstsq(theta, qdd.unsqueeze(-1)).solution.squeeze(-1)
    support = coef.abs() > 0
    for _ in range(iters):
        keep = coef.abs() > threshold * coef.abs().max().clamp_min(1e-12)
        if keep.sum() == 0:
            return torch.zeros_like(coef)
        coef_new = torch.linalg.lstsq(theta[:, keep], qdd.unsqueeze(-1)
                                      ).solution.squeeze(-1)
        coef = torch.zeros_like(coef)
        coef[keep] = coef_new
        if torch.equal(keep, support):
            break
        support = keep
    return coef


def omega_stlsq(q: torch.Tensor, dt: float) -> float:
    qd = (q[2:] - q[:-2]) / (2 * dt)          # central difference
    qdd = (q[2:] - 2 * q[1:-1] + q[:-2]) / (dt * dt)
    coef = stlsq(q[1:-1], qd, qdd)
    return math.sqrt(abs(coef[0].item()))


def boundary_state(q: torch.Tensor, w_hat: float, dt: float):
    """Given omega-hat, analytic LS for (A, B) in q(t)=A cos + B sin, then the
    exact (q, p) at the last observed time. p := qdot for the unit-mass spring."""
    t = torch.arange(q.numel(), dtype=torch.float64) * dt
    w = torch.full_like(t, w_hat)
    ct, st = torch.cos(w * t), torch.sin(w * t)
    A_mat = torch.stack([ct, st], dim=1)
    coef = torch.linalg.lstsq(A_mat, q.double().unsqueeze(-1)).solution.squeeze(-1)
    A, B = coef[0].item(), coef[1].item()
    T = (q.numel() - 1) * dt
    q_T = A * math.cos(w_hat * T) + B * math.sin(w_hat * T)
    p_T = -A * w_hat * math.sin(w_hat * T) + B * w_hat * math.cos(w_hat * T)
    return q_T, p_T


def rollout_mse(q_true: torch.Tensor, w_hat: float, q_T: float, p_T: float,
                dt: float, k: int) -> float:
    """Velocity-Verlet rollout of the exact oscillator with omega-hat for k
    steps from (q_T, p_T); MSE over predicted q steps 1..k vs truth."""
    steps = q_true.shape[0] - 1
    q_c, p_c = q_T, p_T
    a_c = -w_hat * w_hat * q_c
    se, n = 0.0, 0
    for i in range(1, min(k, steps) + 1):
        q_c += p_c * dt + 0.5 * a_c * dt * dt
        a_n = -w_hat * w_hat * q_c
        p_c += 0.5 * (a_c + a_n) * dt
        a_c = a_n
        se += (q_c - q_true[i].item()) ** 2
        n += 1
    return se / max(n, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out_dir", default="benchmarks/physics_out_v02/classic_baseline")
    ap.add_argument("--device", default="cpu", choices=["cpu"])
    args = ap.parse_args()

    results = {"pools": [], "arms": {}}
    per_arm = {"lsq": [], "stlsq": []}
    omega_err = {"lsq": [], "stlsq": []}
    for n_train in N_POOLS:
        for seed in SEEDS:
            g = torch.Generator().manual_seed(seed)
            qs, _, omega = gen_spring(n_train + N_EVAL, POOL_STEPS, DT, 1,
                                      OMEGA_LO, OMEGA_HI, g)
            qs_eval, omega_eval = qs[-N_EVAL:], omega[-N_EVAL:]
            for i in range(N_EVAL):
                q_obs = qs_eval[i, :T_OBS + 1, 0]
                q_true = qs_eval[i, T_OBS:T_OBS + K_EVAL + 1, 0]
                w_true = omega_eval[i].item()
                for arm, fn in (("lsq", omega_lsq), ("stlsq", omega_stlsq)):
                    w_hat = fn(q_obs, DT)
                    q_T, p_T = boundary_state(q_obs, w_hat, DT)
                    per_arm[arm].append(rollout_mse(q_true, w_hat, q_T, p_T,
                                                    DT, K_EVAL))
                    omega_err[arm].append(abs(w_hat - w_true) / w_true)
        results["pools"].append(n_train)

    # per-pool numbers are identical by construction (closed form, same seeds);
    # report per pool anyway to mirror the d1b/TSFM table shape.
    for arm in per_arm:
        vals = per_arm[arm]
        errs = omega_err[arm]
        results["arms"][arm] = {
            "rollout_mse_mean": sum(vals) / len(vals),
            "rollout_mse_max": max(vals),
            "omega_rel_err_mean": sum(errs) / len(errs),
            "omega_rel_err_max": max(errs),
            "n_traj": len(vals),
        }

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "classic_baseline.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({"benchmark": "classic_baseline_eval",
                                         "device": args.device,
                                         "exec_tier": os.environ.get(
                                             "PROBE_TIER", "T0")}),
                   "results": results}, f, indent=2)

    for arm, r in results["arms"].items():
        print(f"[{arm:>6}] k100 rollout MSE mean {r['rollout_mse_mean']:.6e} "
              f"(max {r['rollout_mse_max']:.3e}) | omega rel err mean "
              f"{r['omega_rel_err_mean']:.4%} (max {r['omega_rel_err_max']:.4%}) "
              f"| n={r['n_traj']}")


if __name__ == "__main__":
    main()
