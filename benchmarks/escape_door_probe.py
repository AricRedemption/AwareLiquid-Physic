"""
benchmarks/escape_door_probe.py — ESC-DOOR-VAB (round 110): escape-door #3 A/B.

Preregistered in PRD §19 round 110 BEFORE execution: does the Nonseparable
head actually OPEN where the separable head cannot go — same data pool,
same training budget, seed 0 (1-seed screening tier; multi-seed finals are
PARKED per AMM-024 and are NOT run here).

  arm A  HamiltonianHead (separable H = T(p)+V(q), context_dim=0)
         + velocity-Verlet — the architecture class that CANNOT represent
         a velocity-dependent Lorentz force (dV/dq has no p dependence).
  arm B  NonseparableHamiltonianHead (H = T+V+C) + implicit midpoint —
         the registered escape door for exactly this failure (round 86).

Truth: gen_magnetic (RK4, B=2.0, magnetic force does no work). Negative
criteria ①-④ are preregistered in PRD §19; drift thresholds (0.10) are
calibrated to the wave-4 trained-house record 5.97e-2 (round-74 rule:
thresholds from house history, not absolute magic numbers).

Results JSON follows the audit schema: top-level "results" key required.
meta carries exec_tier passthrough from probe_run (PROBE_TIER env).
"""

import argparse
import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.datasets import gen_magnetic
from awareliquid_physics.hamiltonian import (HamiltonianHead,
                                             NonseparableHamiltonianHead)
from awareliquid_physics.observability import rollout_mse_stderr, run_metadata


def true_H(q, p, B):
    x, y = q[..., 0], q[..., 1]
    px, py = p[..., 0], p[..., 1]
    return 0.5 * ((px + 0.5 * B * y) ** 2 + (py - 0.5 * B * x) ** 2)


def train(head, qs, ps, dt, steps, lr, batch, seed, lr_decay, curve_every):
    """1-step supervised MSE on random (t0, t0+1) pairs — the same training
    form as nonseparable_eval.py; identical batch sequence for both arms
    (same seed) so the budget comparison is fair."""
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(head.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda t: lr_decay ** t)
    N, S = qs.shape[0], qs.shape[1]
    head.train()
    loss = float("nan")
    curve = []
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
        sched.step()
        if curve_every and ((i + 1) % curve_every == 0 or i == 0):
            curve.append({"step": i + 1, "loss": loss.item()})
    return loss.item(), curve


def eval_arm(head, energy_fn, qs, ps, ev, dt, eval_k):
    """k-step rollout MSE vs truth + relative energy drift of the arm's OWN
    learned H along its own rollout (house convention: max |E-E0|/|E0|)."""
    head.eval()
    q0, p0 = qs[ev, 0], ps[ev, 0]
    with torch.enable_grad():
        qs_pred, ps_pred = head.rollout(q0, p0, eval_k, dt)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    q_true = qs[ev, :eval_k + 1].permute(1, 0, 2)
    p_true = ps[ev, :eval_k + 1].permute(1, 0, 2)
    mse = ((qs_pred - q_true).pow(2).mean()
           + (ps_pred - p_true).pow(2).mean()).item()
    E = energy_fn(qs_pred, ps_pred)
    E0 = E[0].abs().clamp_min(1e-6)
    drift = ((E - E[0]).abs() / E0).max().item()
    return {"rollout_mse": mse,
            "rollout_mse_stderr": rollout_mse_stderr(qs_pred, q_true,
                                                     ps_pred, p_true),
            "energy_drift_max": drift}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=64)
    ap.add_argument("--gen_steps", type=int, default=200)
    ap.add_argument("--dt", type=float, default=0.01)
    ap.add_argument("--B", type=float, default=2.0)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--iters", type=int, default=4)
    ap.add_argument("--train_steps", type=int, default=10000)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--lr_decay", type=float, default=1.0)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--curve_every", type=int, default=2000)
    ap.add_argument("--drift_gate", type=float, default=0.10,
                    help="preregistered ③④ threshold (house-calibrated)")
    ap.add_argument("--ratio_gate", type=float, default=2.0,
                    help="preregistered ② necessity threshold")
    ap.add_argument("--device", default="cpu", help="cpu | cuda")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/escape_door_probe")
    args = ap.parse_args()

    g = torch.Generator(device=args.device).manual_seed(args.seed)
    qs, ps = gen_magnetic(args.n_train + args.n_eval, args.gen_steps,
                          args.dt, args.B, g, device=args.device)
    ev = slice(args.n_train, None)
    print(f"ESC-DOOR-VAB | magnetic B={args.B} dt={args.dt} "
          f"steps={args.train_steps} (equal budget, seed {args.seed}, "
          f"1-seed screening)", flush=True)

    results = {}
    curves = {}

    torch.manual_seed(args.seed)
    head_a = HamiltonianHead(dim=2, hidden_dim=args.hidden,
                             depth=args.depth, context_dim=0).to(args.device)
    floss_a, curve_a = train(head_a, qs, ps, args.dt, args.train_steps,
                             args.lr, args.batch, args.seed, args.lr_decay,
                             args.curve_every)
    res_a = eval_arm(head_a, lambda q, p: head_a.energy(q, p),
                     qs, ps, ev, args.dt, args.eval_k)
    res_a.update({"params": sum(p.numel() for p in head_a.parameters()),
                  "train_loss": floss_a, "integrator": "velocity-verlet"})
    results["arm_A_separable"] = res_a
    curves["arm_A_separable"] = curve_a
    print(f"  [A separable  ] {res_a['params']:>6,} par | train {floss_a:.3e} "
          f"| k{args.eval_k} MSE {res_a['rollout_mse']:.3e} "
          f"| own-H drift {res_a['energy_drift_max']:.3e}", flush=True)

    torch.manual_seed(args.seed)
    head_b = NonseparableHamiltonianHead(dim=2, hidden_dim=args.hidden,
                                         depth=args.depth,
                                         iters=args.iters).to(args.device)
    floss_b, curve_b = train(head_b, qs, ps, args.dt, args.train_steps,
                             args.lr, args.batch, args.seed, args.lr_decay,
                             args.curve_every)
    res_b = eval_arm(head_b, lambda q, p: head_b.energy(q, p),
                     qs, ps, ev, args.dt, args.eval_k)
    res_b.update({"params": sum(p.numel() for p in head_b.parameters()),
                  "train_loss": floss_b, "integrator": "implicit-midpoint"})
    results["arm_B_nonseparable"] = res_b
    curves["arm_B_nonseparable"] = curve_b
    print(f"  [B nonseparable] {res_b['params']:>6,} par | train {floss_b:.3e} "
          f"| k{args.eval_k} MSE {res_b['rollout_mse']:.3e} "
          f"| own-H drift {res_b['energy_drift_max']:.3e}", flush=True)

    ratio = res_a["rollout_mse"] / res_b["rollout_mse"]
    results["ratio_A_over_B"] = ratio
    # Preregistered negative criteria ①-④ (PRD §19 round 110) — mechanical.
    results["criteria"] = {
        "c1_door_not_open": res_b["rollout_mse"] >= res_a["rollout_mse"],
        "c2_necessity_weak": ratio < args.ratio_gate,
        "c3_symplectic_lost_B": res_b["energy_drift_max"] > args.drift_gate,
        "c4_symplectic_lost_A": res_a["energy_drift_max"] > args.drift_gate,
    }
    results["gates"] = {"ratio_gate": args.ratio_gate,
                        "drift_gate": args.drift_gate}
    verdict = "PASS" if not any(results["criteria"].values()) else "NEGATIVE"
    print(f"\nESC-DOOR verdict {verdict} | A/B ratio {ratio:.1f}x "
          f"| criteria {results['criteria']}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "escape_door_probe.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "escape_door_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN", "")}),
                   "results": results, "loss_curves": curves}, f, indent=2)


if __name__ == "__main__":
    main()
