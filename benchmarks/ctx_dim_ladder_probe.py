"""
benchmarks/ctx_dim_ladder_probe.py — CTX-DIM-LADDER (round 226): context
dimension (capacity) ladder contrast on the M1 spring family.

Preregistered in PRD §19 round 226 BEFORE execution. Scan §53: the house
default is context_dim=8 while the true latent (omega) is 1-dimensional —
is the extra capacity redundant-harmful (interference, §53.1) or harmless
(linear redundancy)? This probe sweeps context_dim in {1, 2, 4, 8} under
the same 2000-step prefix budget.

context_dim is a constructor argument — natively injectable (the round-
181 watchdog rule applies cleanly).

Mechanical verdict (preregistered):
  CTXDIM_UNRESOLVABLE (negative) — any arm diverged (non-finite or
      rollout > 1e6: that capacity unusable, recorded as such), or
      spread (max/min across arms) < 1.05 (capacity not resolvable;
      ctx_dim=8 default sufficient — recorded as such)
  CTXDIM_RESOLVED — spread >= 1.05: report the best ctx_dim and
      direction (capacity beneficial / harmful / interior optimum).

1-seed screening tier; multi-seed finals PARKED per AMM-024. Results
JSON follows the audit schema (top-level "results" key); meta carries
exec_tier passthrough from probe_run.
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
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

SPREAD_GATE = 1.05  # preregistered: max/min across arms for resolvable
NORM_CAP = 1e6      # preregistered: divergence threshold

LADDER = (1, 2, 4, 8)  # preregistered context_dim values


def classify_ctxdim(values, mses, spread_gate: float = SPREAD_GATE,
                    cap: float = NORM_CAP):
    """Preregistered round-226 verdict (pure, test-pinned)."""
    for v, m in zip(values, mses):
        if not math.isfinite(m) or m > cap:
            state = "non-finite" if not math.isfinite(m) else "diverged"
            return "CTXDIM_UNRESOLVABLE", {
                "reason": f"ctx_dim={v} arm {state} (mse={m:.3e}): "
                          f"capacity unusable, recorded as such"}
    spread = max(mses) / max(min(mses), 1e-30)
    if spread < spread_gate:
        return "CTXDIM_UNRESOLVABLE", {
            "spread": spread,
            "criterion": f"spread {spread:.3f} < {spread_gate}: capacity "
                         f"not resolvable (ctx_dim=8 default sufficient, "
                         f"recorded as such)"}
    best = values[mses.index(min(mses))]
    if best == values[0]:
        direction = "smaller capacity beneficial (monotonic)"
    elif best == values[-1]:
        direction = "larger capacity beneficial (monotonic)"
    else:
        direction = "interior optimum"
    return "CTXDIM_RESOLVED", {
        "spread": spread, "best_ctx_dim": best, "direction": direction,
        "criterion": f"spread {spread:.2f} >= {spread_gate}: capacity "
                     f"resolvable"}


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
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--ctx_dims", default="1,2,4,8")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/ctx_dim_ladder")
    args = ap.parse_args()
    ctx_dims = sorted(int(x) for x in args.ctx_dims.split(","))

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"CTX-DIM-LADDER | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} steps={args.train_steps} "
          f"ctx_dim ladder={ctx_dims} (seed {args.seed}, 1-seed "
          f"screening)", flush=True)

    arms = {}
    for cd in ctx_dims:
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=cd,
            n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
            dt=args.dt)
        train_prefix(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                     args.train_steps, args.lr, args.batch, args.seed)
        res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                       args.eval_k, args.dt)
        n_params = sum(pp.numel() for pp in model.parameters())
        res["params"] = n_params
        arms[f"c{cd}"] = res
        print(f"  [ctx_dim {cd}] rollout MSE {res['rollout_mse']:.4e} "
              f"| params {n_params}", flush=True)

    keys = [f"c{v}" for v in ctx_dims]
    mses = [arms[k]["rollout_mse"] for k in keys]
    verdict, detail = classify_ctxdim(ctx_dims, mses)
    results = {
        "arms": {k: {"ctx_dim": v, "rollout_mse": arms[k]["rollout_mse"],
                     "rollout_mse_stderr": arms[k]["rollout_mse_stderr"],
                     "params": arms[k]["params"]}
                 for k, v in zip(keys, ctx_dims)},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "CTXDIM_UNRESOLVABLE",
            "c_resolved": verdict == "CTXDIM_RESOLVED"},
        "gates": {"spread_gate": SPREAD_GATE, "norm_cap": NORM_CAP},
    }
    print(f"\nCTX-DIM-LADDER verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "ctx_dim_ladder.json"),
              "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "ctx_dim_ladder_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
