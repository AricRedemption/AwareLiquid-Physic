"""
benchmarks/tosa_ladder_probe.py — TOSA-LADDER (round 223): training
observation-window (t_obs) ladder contrast on the M1 spring family.

Preregistered in PRD §19 round 223 BEFORE execution. Scan §52: t_obs=24
is house-wide default and never ablated. D6 (identifiability_probe)
gives the closed-form Fisher-information window lower bound for omega
identification; this probe measures the TRAINING-side effect — how the
observation window length affects end-to-end rollout generalization
(ctx inference quality + network window utilization) — for a
preregistered D6 cross-table.

Mechanical verdict (preregistered):
  TOSA_UNRESOLVABLE (negative) — any arm diverged (non-finite or
      rollout > 1e6: that window unusable, recorded as such), or spread
      (max/min across arms) < 1.05 (window length not resolvable;
      t_obs=24 default sufficient — recorded as such)
  TOSA_RESOLVED — spread >= 1.05: report the best t_obs and the curve
      shape (monotonic / non-monotonic / plateau).

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

LADDER = (8, 16, 24, 48)  # preregistered t_obs values


def classify_tosa(values, mses, spread_gate: float = SPREAD_GATE,
                  cap: float = NORM_CAP):
    """Preregistered round-223 verdict (pure, test-pinned)."""
    for v, m in zip(values, mses):
        if not math.isfinite(m) or m > cap:
            state = "non-finite" if not math.isfinite(m) else "diverged"
            return "TOSA_UNRESOLVABLE", {
                "reason": f"t_obs={v} arm {state} (mse={m:.3e}): window "
                          f"length unusable, recorded as such"}
    spread = max(mses) / max(min(mses), 1e-30)
    if spread < spread_gate:
        return "TOSA_UNRESOLVABLE", {
            "spread": spread,
            "criterion": f"spread {spread:.3f} < {spread_gate}: window "
                         f"length not resolvable (t_obs=24 default "
                         f"sufficient, recorded as such)"}
    best = values[mses.index(min(mses))]
    lo, hi = min(values), max(values)
    if best == lo:
        direction = "shorter windows beneficial (monotonic)"
    elif best == hi:
        direction = "longer windows beneficial (monotonic)"
    elif mses.index(min(mses)) == 1 or mses.index(min(mses)) == 2:
        direction = "interior optimum"
    else:
        direction = "non-monotonic"
    return "TOSA_RESOLVED", {
        "spread": spread, "best_t_obs": best, "direction": direction,
        "criterion": f"spread {spread:.2f} >= {spread_gate}: window "
                     f"length resolvable"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
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
    ap.add_argument("--t_obs_list", default="8,16,24,48")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/tosa_ladder")
    args = ap.parse_args()
    t_obs_list = sorted(int(x) for x in args.t_obs_list.split(","))

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"TOSA-LADDER | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} steps={args.train_steps} t_obs ladder="
          f"{t_obs_list} (seed {args.seed}, 1-seed screening)", flush=True)

    arms = {}
    for t_obs in t_obs_list:
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
            dt=args.dt)
        train_prefix(model, qs[tr], ps[tr], t_obs, args.k_train,
                     args.train_steps, args.lr, args.batch, args.seed)
        res = evaluate(model, qs[ev], ps[ev], om[ev], t_obs,
                       args.eval_k, args.dt)
        arms[f"t{t_obs}"] = res
        print(f"  [t_obs {t_obs:>2}] rollout MSE {res['rollout_mse']:.4e}",
              flush=True)

    keys = [f"t{v}" for v in t_obs_list]
    mses = [arms[k]["rollout_mse"] for k in keys]
    verdict, detail = classify_tosa(t_obs_list, mses)
    results = {
        "arms": {k: {"t_obs": v, "rollout_mse": arms[k]["rollout_mse"],
                     "rollout_mse_stderr": arms[k]["rollout_mse_stderr"]}
                 for k, v in zip(keys, t_obs_list)},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "TOSA_UNRESOLVABLE",
            "c_resolved": verdict == "TOSA_RESOLVED"},
        "gates": {"spread_gate": SPREAD_GATE, "norm_cap": NORM_CAP},
    }
    print(f"\nTOSA-LADDER verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "tosa_ladder.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "tosa_ladder_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
