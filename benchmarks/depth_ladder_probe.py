"""
benchmarks/depth_ladder_probe.py — DEPTH-LADDER (round 185): head-depth
ladder contrast on the M1 spring family (E1 calibre).

Preregistered in PRD §19 round 185 BEFORE execution. Scan §45 (Safran &
Shamir ICML depth-efficiency; Mattheakis 2022 HNN depth ablation;
Galimberti 2021 Hamiltonian-DNN stability): the house default is
depth=2; this probe sweeps depth in {1, 2, 4} (hidden fixed, parameters
grow near-linearly with depth) under the same 2000-step prefix budget.

Depth is a constructor argument of HamiltonianHead — natively
injectable (the round-181 watchdog rule: no hardcoded config inside the
reused loop).

Mechanical verdict (preregistered):
  DEPTH_UNRESOLVABLE (negative) — any arm diverged (non-finite or
      rollout > 1e6: that depth unusable, recorded as such), or spread
      (max/min across arms) < 1.05 (depth not resolvable; depth=2
      default is sufficient — recorded as such)
  DEPTH_RESOLVED — spread >= 1.05: report the best depth and direction
      (deeper beneficial / harmful / interior optimum).

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

LADDER = (1, 2, 4)  # preregistered depth values


def classify_depth(depths, mses, spread_gate: float = SPREAD_GATE,
                   cap: float = NORM_CAP):
    """Preregistered round-185 verdict (pure, test-pinned)."""
    for d, m in zip(depths, mses):
        if not math.isfinite(m) or m > cap:
            state = "non-finite" if not math.isfinite(m) else "diverged"
            return "DEPTH_UNRESOLVABLE", {
                "reason": f"depth={d} arm {state} (mse={m:.3e}): depth "
                          f"unusable, recorded as such"}
    spread = max(mses) / max(min(mses), 1e-30)
    if spread < spread_gate:
        return "DEPTH_UNRESOLVABLE", {
            "spread": spread,
            "criterion": f"spread {spread:.3f} < {spread_gate}: depth not "
                         f"resolvable (depth=2 default sufficient, "
                         f"recorded as such)"}
    best_d = depths[mses.index(min(mses))]
    if best_d == depths[0]:
        direction = "depth harmful (shallowest best; monotonic)"
    elif best_d == depths[-1]:
        direction = "depth beneficial up to ladder end (monotonic)"
    else:
        direction = "interior optimum"
    return "DEPTH_RESOLVED", {
        "spread": spread, "best_depth": best_d, "direction": direction,
        "criterion": f"spread {spread:.2f} >= {spread_gate}: depth "
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
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--depths", default="1,2,4")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/depth_ladder")
    args = ap.parse_args()
    depths = [int(x) for x in args.depths.split(",")]

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"DEPTH-LADDER | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} steps={args.train_steps} depth ladder="
          f"{depths} (seed {args.seed}, 1-seed screening)", flush=True)

    arms = {}
    for depth in depths:
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=args.n_scales, hidden_dim=args.hidden, depth=depth,
            dt=args.dt)
        train_prefix(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                     args.train_steps, args.lr, args.batch, args.seed)
        res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                       args.eval_k, args.dt)
        n_params = sum(pp.numel() for pp in model.parameters())
        res["params"] = n_params
        arms[f"d{depth}"] = res
        print(f"  [depth {depth}] rollout MSE {res['rollout_mse']:.4e} "
              f"| params {n_params}", flush=True)

    keys = [f"d{d}" for d in depths]
    mses = [arms[k]["rollout_mse"] for k in keys]
    verdict, detail = classify_depth(depths, mses)
    results = {
        "arms": {k: {"rollout_mse": arms[k]["rollout_mse"],
                     "rollout_mse_stderr": arms[k]["rollout_mse_stderr"],
                     "params": arms[k]["params"]}
                 for k in keys},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "DEPTH_UNRESOLVABLE",
            "c_resolved": verdict == "DEPTH_RESOLVED"},
        "gates": {"spread_gate": SPREAD_GATE, "norm_cap": NORM_CAP},
    }
    print(f"\nDEPTH-LADDER verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "depth_ladder.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "depth_ladder_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
