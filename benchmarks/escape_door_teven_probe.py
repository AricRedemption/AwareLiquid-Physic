"""
benchmarks/escape_door_teven_probe.py — ESC-DOOR-TEVEN (round 120): escape-
door #2 A/B ("T-even not enforced" -> R1b conditional entry).

Preregistered in PRD §19 round 120 BEFORE execution: does the DEFAULT
architecture (T = free MLP(p), round-66 note: return-consistency requires an
even T and is NOT guaranteed) actually LOSE the flip-and-retrace protocol
that a T-even parameterization guarantees by construction — on the house
even-T family, same data pool, same training budget, seed 0 (1-seed
screening tier; multi-seed finals are PARKED per AMM-024 and NOT run here)?

  arm A  HamiltonianHead, T = free MLP(p) (default; may learn a small
         asymmetry) + velocity-Verlet.
  arm B  HamiltonianHead with T = MLP(p*p) — even in p BY CONSTRUCTION
         (the R1b escape parameterization, realized probe-locally; gradient
         dT/dp = 2p*MLP'(p^2) is odd, so every velocity-Verlet step is exactly
         flip-reversible: R Phi R = Phi^-1, the round-66 identity).

Round-trip protocol: (q0,p0) -> k steps -> flip p -> k steps -> flip p;
closure error against (q0,p0). For arm B this is a machine-precision floor
regardless of fit quality; for arm A it accumulates whatever T-asymmetry
training left behind. Forward k=100 MSE is the no-cost control (the T-even
constraint must not hurt in-distribution accuracy when the true T is even).

Truth: gen_spring (analytic harmonic family, T_true = p^2/2 exactly even,
dt=0.1, omega in [0.7,1.8] — the house M1 pool). Negative criteria ①-⑤ are
preregistered in PRD §19; drift threshold 0.10 is the round-74/110
house-calibrated gate; floor_gate = 1e-4 sits >=2 orders of magnitude above
any float32 accumulation floor (smoke-measured ~1e-8) so it can only catch
implementation-level breakage of the even parameterization.

Results JSON follows the audit schema: top-level "results" key required.
meta carries exec_tier passthrough from probe_run (PROBE_TIER env).
"""

import argparse
import json
import os
import sys

import torch
from torch import nn

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.hamiltonian import (  # noqa: E402
    HamiltonianHead, _energy_mlp)
from awareliquid_physics.observability import (  # noqa: E402
    rollout_mse_stderr, run_metadata)
from benchmarks.m1_semigroup_eval import gen_spring  # noqa: E402


class EvenKineticMLP(nn.Module):
    """T(p) = MLP(p ⊙ p) — even in p BY CONSTRUCTION.

    The R1b escape parameterization (round 66 identity; round 86 door row
    "T 偶未强制 -> R1b: T 偶参数化/一致性损失"): any even smooth T is
    representable through the squared input, while the odd part is structurally
    impossible. Parameter count equals the free _energy_mlp (same layers).
    """

    def __init__(self, base: nn.Module):
        super().__init__()
        self.base = base

    def forward(self, p: torch.Tensor) -> torch.Tensor:
        return self.base(p * p)


def train(head, qs, ps, dt, steps, lr, batch, seed, lr_decay, curve_every):
    """1-step supervised MSE on random (t0, t0+1) pairs — the same training
    form as escape_door_probe.py (round 110); identical batch sequence for
    both arms (same seed) so the budget comparison is fair."""
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


def eval_forward(head, qs, ps, ev, dt, eval_k):
    """k-step rollout MSE vs truth (q+p point-mean, round-110 series
    convention) + relative energy drift of the arm's OWN learned H along its
    own rollout (house convention: max |E-E0|/|E0|)."""
    head.eval()
    q0, p0 = qs[ev, 0], ps[ev, 0]
    with torch.enable_grad():
        qs_pred, ps_pred = head.rollout(q0, p0, eval_k, dt)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    q_true = qs[ev, :eval_k + 1].permute(1, 0, 2)
    p_true = ps[ev, :eval_k + 1].permute(1, 0, 2)
    mse = ((qs_pred - q_true).pow(2).mean()
           + (ps_pred - p_true).pow(2).mean()).item()
    E = head.energy(qs_pred, ps_pred)
    E0 = E[0].abs().clamp_min(1e-6)
    drift = ((E - E[0]).abs() / E0).max().item()
    return {"rollout_mse": mse,
            "rollout_mse_stderr": rollout_mse_stderr(qs_pred, q_true,
                                                     ps_pred, p_true),
            "energy_drift_max": drift}


def eval_roundtrip(head, qs, ps, ev, dt, k):
    """Flip-and-retrace closure: (q0,p0) -> k steps -> flip p -> k steps ->
    flip p, error against the start state. T-even head closes at the float
    floor BY CONSTRUCTION (round-66 identity); a free-T head accumulates
    whatever asymmetry training left. Returns q+p and q-only point-mean
    closure MSE."""
    head.eval()
    q0, p0 = qs[ev, 0], ps[ev, 0]
    with torch.enable_grad():
        qs_fwd, ps_fwd = head.rollout(q0, p0, k, dt)
        qs_back, ps_back = head.rollout(qs_fwd[-1], -ps_fwd[-1], k, dt)
    q_end, p_end = qs_back[-1].detach(), ps_back[-1].detach()
    per_traj_qp = ((q_end - q0) ** 2).mean(dim=-1) \
        + ((p_end + p0) ** 2).mean(dim=-1)
    per_traj_q = ((q_end - q0) ** 2).mean(dim=-1)
    return {"roundtrip_mse_qp": per_traj_qp.mean().item(),
            "roundtrip_mse_q": per_traj_q.mean().item(),
            "roundtrip_stderr": per_traj_qp.std().item()
                                / max(per_traj_qp.numel(), 1) ** 0.5}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=64)
    ap.add_argument("--gen_steps", type=int, default=200)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--dim", type=int, default=1)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--rt_ks", type=int, nargs="+", default=[50, 100, 200],
                    help="round-trip horizons; the gate reads the LARGEST")
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--train_steps", type=int, default=10000)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--lr_decay", type=float, default=1.0)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--curve_every", type=int, default=2000)
    ap.add_argument("--ratio_gate", type=float, default=2.0,
                    help="preregistered ① necessity threshold (A/B roundtrip)")
    ap.add_argument("--forward_gate", type=float, default=2.0,
                    help="preregistered ② no-cost threshold (B/A forward)")
    ap.add_argument("--drift_gate", type=float, default=0.10,
                    help="preregistered ③④ threshold (house-calibrated, "
                         "round-74/110)")
    ap.add_argument("--floor_gate", type=float, default=1e-4,
                    help="preregistered ⑤ threshold: even arm must close at "
                         "the float floor; values above signal an "
                         "implementation bug, not physics")
    ap.add_argument("--device", default="cpu", help="cpu | cuda")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/escape_door_teven")
    args = ap.parse_args()

    g = torch.Generator(device=args.device).manual_seed(args.seed)
    qs, ps, _omega = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                                args.dt, args.dim, args.omega_lo,
                                args.omega_hi, g, device=args.device)
    ev = slice(args.n_train, None)
    k_rt = max(args.rt_ks)
    print(f"ESC-DOOR-TEVEN | spring omega[{args.omega_lo},{args.omega_hi}] "
          f"dt={args.dt} steps={args.train_steps} rt_k={args.rt_ks} "
          f"(gate at k={k_rt}) (equal budget, seed {args.seed}, "
          f"1-seed screening)", flush=True)

    results = {}
    curves = {}

    # -- arm A: default free-T head ------------------------------------------
    torch.manual_seed(args.seed)
    head_a = HamiltonianHead(dim=args.dim, hidden_dim=args.hidden,
                             depth=args.depth, context_dim=0).to(args.device)
    floss_a, curve_a = train(head_a, qs, ps, args.dt, args.train_steps,
                             args.lr, args.batch, args.seed, args.lr_decay,
                             args.curve_every)
    res_a = eval_forward(head_a, qs, ps, ev, args.dt, args.eval_k)
    for k in args.rt_ks:
        res_a[f"roundtrip_k{k}"] = eval_roundtrip(head_a, qs, ps, ev,
                                                  args.dt, k)
    res_a.update({"params": sum(p.numel() for p in head_a.parameters()),
                  "train_loss": floss_a, "integrator": "velocity-verlet",
                  "kinetic": "free MLP(p)"})
    results["arm_A_free_T"] = res_a
    curves["arm_A_free_T"] = curve_a
    print(f"  [A free-T ] {res_a['params']:>6,} par | train {floss_a:.3e} "
          f"| k{args.eval_k} MSE {res_a['rollout_mse']:.3e} "
          f"| rt{k_rt} {res_a[f'roundtrip_k{k_rt}']['roundtrip_mse_qp']:.3e} "
          f"| own-H drift {res_a['energy_drift_max']:.3e}", flush=True)

    # -- arm B: T-even parameterization (R1b escape realized) -----------------
    torch.manual_seed(args.seed)
    head_b = HamiltonianHead(dim=args.dim, hidden_dim=args.hidden,
                             depth=args.depth, context_dim=0).to(args.device)
    head_b.T = EvenKineticMLP(_energy_mlp(args.dim, args.hidden, args.depth))
    floss_b, curve_b = train(head_b, qs, ps, args.dt, args.train_steps,
                             args.lr, args.batch, args.seed, args.lr_decay,
                             args.curve_every)
    res_b = eval_forward(head_b, qs, ps, ev, args.dt, args.eval_k)
    for k in args.rt_ks:
        res_b[f"roundtrip_k{k}"] = eval_roundtrip(head_b, qs, ps, ev,
                                                  args.dt, k)
    res_b.update({"params": sum(p.numel() for p in head_b.parameters()),
                  "train_loss": floss_b, "integrator": "velocity-verlet",
                  "kinetic": "even MLP(p*p)"})
    results["arm_B_teven"] = res_b
    curves["arm_B_teven"] = curve_b
    print(f"  [B teven  ] {res_b['params']:>6,} par | train {floss_b:.3e} "
          f"| k{args.eval_k} MSE {res_b['rollout_mse']:.3e} "
          f"| rt{k_rt} {res_b[f'roundtrip_k{k_rt}']['roundtrip_mse_qp']:.3e} "
          f"| own-H drift {res_b['energy_drift_max']:.3e}", flush=True)

    rt_a = res_a[f"roundtrip_k{k_rt}"]["roundtrip_mse_qp"]
    rt_b = res_b[f"roundtrip_k{k_rt}"]["roundtrip_mse_qp"]
    ratio = rt_a / rt_b
    fwd_ratio = res_b["rollout_mse"] / res_a["rollout_mse"]
    results["roundtrip_ratio_A_over_B"] = ratio
    results["forward_ratio_B_over_A"] = fwd_ratio
    # Preregistered negative criteria ①-⑤ (PRD §19 round 120) — mechanical.
    results["criteria"] = {
        "c1_necessity_weak": ratio < args.ratio_gate,
        "c2_no_cost_violated": fwd_ratio > args.forward_gate,
        "c3_symplectic_lost_B": res_b["energy_drift_max"] > args.drift_gate,
        "c4_symplectic_lost_A": res_a["energy_drift_max"] > args.drift_gate,
        "c5_teven_not_at_floor": rt_b > args.floor_gate,
    }
    results["gates"] = {"ratio_gate": args.ratio_gate,
                        "forward_gate": args.forward_gate,
                        "drift_gate": args.drift_gate,
                        "floor_gate": args.floor_gate,
                        "gate_at_rt_k": k_rt}
    verdict = "PASS" if not any(results["criteria"].values()) else "NEGATIVE"
    print(f"\nESC-DOOR-TEVEN verdict {verdict} | A/B roundtrip ratio "
          f"{ratio:.1f}x | B/A forward ratio {fwd_ratio:.3f}x "
          f"| criteria {results['criteria']}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "escape_door_teven.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "escape_door_teven_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN", "")}),
                   "results": results, "loss_curves": curves}, f, indent=2)


if __name__ == "__main__":
    main()
