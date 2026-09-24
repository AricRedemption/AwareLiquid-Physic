"""
benchmarks/fastslow_probe.py — FASTSLOW-PROBE (round 137): elastic-pendulum
two-timescale probe.

Preregistered in PRD §19 round 137 BEFORE execution. The house families are
all single-timescale; this probe introduces the classic two-timescale system
(elastic pendulum: fast spring mode omega_s=10 + slow pendular swing
omega_p≈1, 10x separation) as a probe-local separable-H family
H = T(p) + V(r) with dim=2 — representable by the stock HamiltonianHead.

Question: trained at a dt that RESOLVES the fast mode (dt=0.02, omega_s*dt
=0.2), does the head capture BOTH timescales — fast oscillation (short
horizon) and the slow energy-exchange envelope (long horizon T=40 ≈ 6.4
slow periods)?

Mechanical four-way classification on signal-relative rollout MSEs
(preregistered): BOTH_CAPTURED / FAST_ONLY / SLOW_ONLY / BOTH_FAILED.
Plus documentation axis (not gate-bearing): the same head rolled at an
UNRESOLVED dt=0.5 (omega_s*dt=5) — the stiffness signature of §33.2.

1-seed screening tier; multi-seed finals PARKED per AMM-024. Results JSON
follows the audit schema (top-level "results" key); meta carries exec_tier
passthrough from probe_run.
"""

import argparse
import json
import math
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.hamiltonian import HamiltonianHead  # noqa: E402
from awareliquid_physics.observability import (  # noqa: E402
    rollout_mse_stderr, run_metadata)

# elastic pendulum parameters: m=1, k=100 (omega_s=10), L0=1, g=1
K_SPRING = 100.0
L_REST = 1.0
G_GRAV = 1.0


def accel(r: torch.Tensor) -> torch.Tensor:
    """True force field /m of the elastic pendulum at positions r=(..., 2):
    a = -(k(|r|-L0)) * r/|r| - g * y_hat."""
    norm = r.norm(dim=-1, keepdim=True)
    spring = -K_SPRING * (norm - L_REST) * r / norm
    grav = torch.zeros_like(r)
    grav[..., 1] = -G_GRAV
    return spring + grav


def gen_pendulum(n_traj: int, steps: int, dt: float, seed: int,
                 device: str = "cpu"):
    """Velocity-Verlet truth for the elastic pendulum. Returns (qs, ps)
    with shape (n_traj, steps+1, 2)."""
    g = torch.Generator(device=device).manual_seed(seed)
    # moderate amplitudes: swing mostly along x, spring stretched 20%
    ang = (torch.rand(n_traj, generator=g, device=device) * 0.6 - 0.3)
    stretch = 0.2 * torch.rand(n_traj, generator=g, device=device) + 0.1
    r0 = torch.stack([(L_REST + stretch) * torch.sin(ang),
                      -(L_REST + stretch) * torch.cos(ang)], dim=-1)
    p0 = torch.randn(n_traj, 2, generator=g, device=device) * 0.1

    q, p = r0.clone(), p0.clone()
    qs, ps = [q], [p]
    a = accel(q)
    for _ in range(steps):
        p = p + 0.5 * dt * a
        q = q + dt * p
        a_new = accel(q)
        p = p + 0.5 * dt * a_new
        a = a_new
        qs.append(q)
        ps.append(p)
    return torch.stack(qs, dim=1), torch.stack(ps, dim=1)


def true_energy(r: torch.Tensor, p: torch.Tensor) -> torch.Tensor:
    """Consistent with accel() (a_y = -g => V_grav = +g*y)."""
    norm = r.norm(dim=-1)
    kin = 0.5 * (p ** 2).sum(-1)
    pot = 0.5 * K_SPRING * (norm - L_REST) ** 2 + G_GRAV * r[..., 1]
    return kin + pot


def train_head(head, qs, ps, dt, steps, lr, batch, seed):
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(head.parameters(), lr=lr)
    N, S = qs.shape[0], qs.shape[1]
    head.train()
    loss = float("nan")
    for i in range(steps):
        bi = torch.randint(0, N, (batch,), generator=g)
        t0 = int(torch.randint(0, S - 2, (1,), generator=g).item())
        q, p = qs[bi, t0], ps[bi, t0]
        q_next, p_next = head.step(q, p, dt)
        loss = (q_next - qs[bi, t0 + 1]).pow(2).mean() \
             + (p_next - ps[bi, t0 + 1]).pow(2).mean()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    return loss.item()


def rollout_mse_rel(head, qs, ps, dt, eval_k, dt_data):
    """Rollout MSE / signal-energy ratio at fixed horizon (k steps at dt),
    evaluated against the truth of the same (dt, k)."""
    head.eval()
    q0, p0 = qs[:, 0], ps[:, 0]
    with torch.enable_grad():
        qs_pred, ps_pred = head.rollout(q0, p0, eval_k, dt)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    q_true = qs[:, :eval_k + 1].permute(1, 0, 2)
    p_true = ps[:, :eval_k + 1].permute(1, 0, 2)
    mse = ((qs_pred - q_true) ** 2).mean().item() \
        + ((ps_pred - p_true) ** 2).mean().item()
    signal = (q_true ** 2).mean().item() + (p_true ** 2).mean().item()
    _ = dt_data  # documentation alias
    return {"rollout_mse": mse, "mse_rel_to_signal": mse / max(signal, 1e-12),
            "stderr": rollout_mse_stderr(qs_pred, q_true, ps_pred, p_true)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=64)
    ap.add_argument("--dt", type=float, default=0.02,
                    help="training dt (resolves omega_s=10: omega_s*dt=0.2)")
    ap.add_argument("--gen_steps", type=int, default=2001,
                    help="truth length: T=40 at dt=0.02 (slow-envelope axis)")
    ap.add_argument("--k_fast", type=int, default=100,
                    help="fast-axis horizon steps (T=2 = 1 fast period)")
    ap.add_argument("--k_long", type=int, default=2000,
                    help="long-axis horizon steps (T=40 = ~6.4 slow periods)")
    ap.add_argument("--dt_coarse", type=float, default=0.5,
                    help="unresolved dt for the stiffness documentation axis")
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--train_steps", type=int, default=10000)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--gate_fast", type=float, default=0.01,
                    help="preregistered: fast axis captured if rel MSE <= 1%")
    ap.add_argument("--gate_long", type=float, default=0.1,
                    help="preregistered: slow axis captured if rel MSE <= 10%")
    ap.add_argument("--device", default="cpu", help="cpu | cuda")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/fastslow_probe")
    args = ap.parse_args()

    qs, ps = gen_pendulum(args.n_train + args.n_eval, args.gen_steps,
                          args.dt, args.seed, args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"FASTSLOW-PROBE | elastic pendulum omega_s=10 omega_p≈1 "
          f"dt={args.dt} steps={args.train_steps} (seed {args.seed}, "
          f"1-seed screening)", flush=True)

    torch.manual_seed(args.seed)
    head = HamiltonianHead(dim=2, hidden_dim=args.hidden,
                           depth=args.depth, context_dim=0)
    loss = train_head(head, qs[tr], ps[tr], args.dt, args.train_steps,
                      args.lr, args.batch, args.seed)
    print(f"  [head] train_loss {loss:.3e}", flush=True)

    # axis A: fast mode (T=2, k=100)
    qs_f = qs[ev, :args.k_fast + 1].contiguous()
    ps_f = ps[ev, :args.k_fast + 1].contiguous()
    e_fast = rollout_mse_rel(head, qs_f, ps_f, args.dt, args.k_fast,
                             args.dt)
    # axis B: slow exchange (T=40, k=2000)
    qs_l = qs[ev].contiguous()
    ps_l = ps[ev].contiguous()
    e_long = rollout_mse_rel(head, qs_l, ps_l, args.dt, args.k_long,
                             args.dt)
    # true-energy drift of the predicted long trajectory (diagnostic)
    head.eval()
    with torch.enable_grad():
        qs_p2, ps_p2 = head.rollout(qs_l[:, 0], ps_l[:, 0], args.k_long,
                                    args.dt)
    E = true_energy(qs_p2.detach(), ps_p2.detach())
    # scale-robust normalization: mean |E| over trajectories (|E0| can be
    # near zero by kinetic/grav/spring cancellation — round-137 lesson)
    e_scale = E.abs().mean().clamp_min(1e-6)
    drift_true = ((E - E[0]).abs() / e_scale).max().item()
    print(f"  [A fast T=2 ] rel MSE {e_fast['mse_rel_to_signal']:.4f}",
          flush=True)
    print(f"  [B long T=40] rel MSE {e_long['mse_rel_to_signal']:.4f} "
          f"| true-E drift {drift_true:.3f}", flush=True)

    # axis C: stiffness signature (unresolved dt; documentation only)
    head.eval()
    with torch.enable_grad():
        qs_c, ps_c = head.rollout(qs_l[:, 0], ps_l[:, 0],
                                  int(2 / args.dt_coarse), args.dt_coarse)
    blowup = bool(not torch.isfinite(qs_c).all()
                  or qs_c.norm() > 1e3 * qs_l[:, :qs_c.shape[0] + 1]
                  .norm().clamp_min(1e-6))
    print(f"  [C coarse dt={args.dt_coarse} (omega_s*dt="
          f"{10 * args.dt_coarse:.1f})] finite={torch.isfinite(qs_c).all().item()} "
          f"blowup={blowup}", flush=True)

    fast_ok = e_fast["mse_rel_to_signal"] <= args.gate_fast
    long_ok = e_long["mse_rel_to_signal"] <= args.gate_long
    if fast_ok and long_ok:
        verdict = "BOTH_CAPTURED"
    elif fast_ok:
        verdict = "FAST_ONLY"
    elif long_ok:
        verdict = "SLOW_ONLY"
    else:
        verdict = "BOTH_FAILED"
    criteria = {
        "c_fast_not_captured": not fast_ok,
        "c_slow_lost": not long_ok,
    }
    results = {
        "axis_A_fast": e_fast,
        "axis_B_long": e_long,
        "axis_C_stiffness_documentation": {
            "dt_coarse": args.dt_coarse,
            "finite": bool(torch.isfinite(qs_c).all().item()),
            "blowup": blowup},
        "true_energy_drift_max_long": drift_true,
        "train_loss": loss,
        "criteria": criteria,
        "gates": {"gate_fast": args.gate_fast, "gate_long": args.gate_long},
        "verdict": verdict,
        "verdict_semantics": "BOTH_CAPTURED=fast<=gate_fast and long<="
                             "gate_long (two-timescale capture, N1 timescale "
                             "clause supported at screening); FAST_ONLY/"
                             "SLOW_ONLY/BOTH_FAILED classify the failure "
                             "mode; axis C is documentation-only",
    }
    print(f"\nFASTSLOW-PROBE verdict {verdict} | criteria {criteria}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "fastslow_probe.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "fastslow_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN", "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
