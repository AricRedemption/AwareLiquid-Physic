"""
benchmarks/amp_extrap_probe.py — AMP-EXTRAP (round 216): initial-
amplitude extrapolation contrast on the M1 spring family.

Preregistered in PRD §19 round 216 BEFORE execution. Scan §42.2 (Li
Nature 2025 interpolation/extrapolation critique): the house generator
draws q0, p0 ~ N(0, 1); scaling them by a factor s scales the initial
energy by s^2. Train on scale=1 (the standard pool), evaluate on
scale in {1, 2, 4} — the relative-calibre comparison (rel_mse =
rollout MSE / mean true signal energy, since absolute MSE grows with
energy) measures whether the model extrapolates in initial-condition
amplitude or only interpolates.

Mechanical verdict (preregistered): rel_comp = rel_mse(s=4)/rel_mse(s=1);
  AMPEX_UNRESOLVABLE (negative) — any pool's rollout non-finite or > 1e6
  AMPEX_ROBUST    — rel_comp < 3   (amplitude extrapolation robust)
  AMPEX_DEGRADES  — rel_comp >= 3  (interpolation-domain boundary hit)

Scale-parameterised generator is verified bit-identical to the original
at scale=1 (round-181 watchdog rule). 1-seed screening tier; multi-seed
finals PARKED per AMM-024. Results JSON follows the audit schema
(top-level "results" key); meta carries exec_tier passthrough.
"""

import argparse
import json
import math
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from awareliquid_physics.model import LiquidHamiltonianModel  # noqa: E402
from awareliquid_physics.observability import run_metadata  # noqa: E402
from benchmarks.liquid_physics_eval import (  # noqa: E402
    evaluate, train as train_prefix)
from benchmarks.m1_semigroup_eval import gen_spring  # noqa: E402

REL_GATE = 3.0  # preregistered: relative-comp gate
NORM_CAP = 1e6  # preregistered: divergence threshold


def gen_spring_scaled(n_traj, steps, dt, omega_lo, omega_hi, g, scale,
                      device="cpu"):
    """M1 spring gen with amplitude-scaled initial conditions.

    Verbatim copy of m1_semigroup_eval.gen_spring except q0/p0 are drawn
    from N(0, scale) — at scale=1 bit-identical to the original (the
    round-181 watchdog: verified by test)."""
    omega = omega_lo + (omega_hi - omega_lo) * torch.rand(
        n_traj, generator=g, device=device)
    q0 = torch.randn(n_traj, 1, generator=g, device=device) * scale
    p0 = torch.randn(n_traj, 1, generator=g, device=device) * scale
    t = torch.arange(steps + 1, dtype=torch.float32, device=device) * dt
    wt = omega.view(-1, 1) * t.view(1, -1)
    c, s = torch.cos(wt).unsqueeze(-1), torch.sin(wt).unsqueeze(-1)
    w = omega.view(-1, 1, 1)
    qs = q0.unsqueeze(1) * c + (p0.unsqueeze(1) / w) * s
    ps = -q0.unsqueeze(1) * w * s + p0.unsqueeze(1) * c
    return qs, ps, omega


def classify_amp(rel_mses, rel_gate: float = REL_GATE,
                 cap: float = NORM_CAP):
    """Preregistered round-216 verdict (pure, test-pinned)."""
    for m in rel_mses:
        if not math.isfinite(m) or m > cap:
            return "AMPEX_UNRESOLVABLE", {
                "reason": f"rel_mse={m:.3e} non-finite or > {cap:.0e}: "
                          f"preregistered negative branch"}
    rel_comp = rel_mses[-1] / max(rel_mses[0], 1e-30)
    if rel_comp < rel_gate:
        return "AMPEX_ROBUST", {
            "rel_comp": rel_comp,
            "criterion": f"rel_comp {rel_comp:.2f} < {rel_gate}: amplitude "
                         f"extrapolation robust (relative error flat)"}
    return "AMPEX_DEGRADES", {
        "rel_comp": rel_comp,
        "criterion": f"rel_comp {rel_comp:.2f} >= {rel_gate}: amplitude "
                     f"extrapolation degrades (interpolation-domain "
                     f"boundary)"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--scales", default="1,2,4")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/amp_extrap")
    args = ap.parse_args()
    scales = [float(x) for x in args.scales.split(",")]

    print(f"AMP-EXTRAP | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} train scale=1, eval scales={scales} "
          f"(seed {args.seed}, 1-seed screening)", flush=True)

    # train on the standard scale=1 pool
    g = torch.Generator().manual_seed(args.seed)
    qs_tr, ps_tr, _ = gen_spring_scaled(args.n_train, args.gen_steps,
                                        args.dt, args.omega_lo,
                                        args.omega_hi, g, scale=1.0,
                                        device=args.device)
    torch.manual_seed(args.seed)
    model = LiquidHamiltonianModel(
        1, d_model=args.d_model, context_dim=args.context_dim,
        n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
        dt=args.dt)
    train_prefix(model, qs_tr, ps_tr, args.t_obs, args.k_train,
                 args.train_steps, args.lr, args.batch, args.seed)

    # evaluate on amplitude-scaled held-out pools
    arms = {}
    rel_mses = []
    for scale in scales:
        g = torch.Generator().manual_seed(args.seed)
        qs_ev, ps_ev, _ = gen_spring_scaled(args.n_eval, args.gen_steps,
                                            args.dt, args.omega_lo,
                                            args.omega_hi, g, scale=scale,
                                            device=args.device)
        model.eval()
        q_obs = qs_ev[:, :args.t_obs]
        p_obs = ps_ev[:, :args.t_obs]
        fut = slice(args.t_obs - 1, args.t_obs + args.eval_k)
        q_true = qs_ev[:, fut].permute(1, 0, 2)
        p_true = ps_ev[:, fut].permute(1, 0, 2)
        with torch.enable_grad():
            qs_pred, ps_pred, _ = model(q_obs, p_obs, args.eval_k)
        qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
        mse = ((qs_pred - q_true) ** 2 + (ps_pred - p_true) ** 2).mean().item()
        signal = (q_true ** 2 + p_true ** 2).mean().item()
        rel = mse / max(signal, 1e-30)
        arms[f"scale{scale:g}"] = {"rollout_mse": mse,
                                   "signal_energy": signal,
                                   "rel_mse": rel}
        rel_mses.append(rel)
        print(f"  [scale {scale:g}] abs MSE {mse:.4e} | signal "
              f"{signal:.3f} | rel MSE {rel:.4f}", flush=True)

    verdict, detail = classify_amp(rel_mses)
    results = {
        "arms": arms,
        "rel_comp": rel_mses[-1] / max(rel_mses[0], 1e-30),
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "AMPEX_UNRESOLVABLE",
            "c_robust": verdict == "AMPEX_ROBUST",
            "c_degrades": verdict == "AMPEX_DEGRADES"},
        "gates": {"rel_gate": REL_GATE, "norm_cap": NORM_CAP},
    }
    print(f"\nAMP-EXTRAP verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "amp_extrap.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "amp_extrap_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
