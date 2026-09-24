"""
benchmarks/nscales_ladder_probe.py — NSCALES-LADDER (round 197):
LTC-core n_scales (number of liquid time-constant scales) ladder contrast
on the M1 spring family.

Preregistered in PRD §19 round 197 BEFORE execution. Scan §47: n_scales
is the LTC core's internal architecture hyperparameter (multi-timescale
channels), fixed at 4 house-wide and never ablated (§47.1 hierarchical
timescale lineage: Hihi & Bengio NIPS 1995; Chung HM-RNN; Quax 2020
fixed-vs-learnable). n_scales is a constructor argument of
LiquidHamiltonianModel — natively injectable (the round-181 watchdog
rule applies cleanly).

Mechanical verdict (preregistered):
  NSCALES_UNRESOLVABLE (negative) — any arm diverged (non-finite or
      rollout > 1e6: that scale count unusable, recorded as such), or
      spread (max/min across arms) < 1.05 (scale count not resolvable;
      n_scales=4 default sufficient — recorded as such)
  NSCALES_RESOLVED — spread >= 1.05: report the best n_scales and
      direction (monotonically beneficial / harmful / interior optimum).

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

LADDER = (1, 2, 4, 8)  # preregistered n_scales values


def classify_nscales(values, mses, spread_gate: float = SPREAD_GATE,
                     cap: float = NORM_CAP):
    """Preregistered round-197 verdict (pure, test-pinned)."""
    for v, m in zip(values, mses):
        if not math.isfinite(m) or m > cap:
            state = "non-finite" if not math.isfinite(m) else "diverged"
            return "NSCALES_UNRESOLVABLE", {
                "reason": f"n_scales={v} arm {state} (mse={m:.3e}): scale "
                          f"count unusable, recorded as such"}
    spread = max(mses) / max(min(mses), 1e-30)
    if spread < spread_gate:
        return "NSCALES_UNRESOLVABLE", {
            "spread": spread,
            "criterion": f"spread {spread:.3f} < {spread_gate}: scale "
                         f"count not resolvable (n_scales=4 default "
                         f"sufficient, recorded as such)"}
    best = values[mses.index(min(mses))]
    if best == values[0]:
        direction = "fewer scales beneficial (monotonic)"
    elif best == values[-1]:
        direction = "more scales beneficial (monotonic)"
    else:
        direction = "interior optimum"
    return "NSCALES_RESOLVED", {
        "spread": spread, "best_n_scales": best, "direction": direction,
        "criterion": f"spread {spread:.2f} >= {spread_gate}: scale count "
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
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--n_scales_list", default="1,2,4,8")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/nscales_ladder")
    args = ap.parse_args()
    scales = sorted(int(x) for x in args.n_scales_list.split(","))

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"NSCALES-LADDER | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] steps={args.train_steps} n_scales ladder="
          f"{scales} (seed {args.seed}, 1-seed screening)", flush=True)

    arms = {}
    for ns in scales:
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=ns, hidden_dim=args.hidden, depth=2, dt=args.dt)
        train_prefix(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                     args.train_steps, args.lr, args.batch, args.seed)
        res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                       args.eval_k, args.dt)
        n_params = sum(pp.numel() for pp in model.parameters())
        res["params"] = n_params
        arms[f"ns{ns}"] = res
        print(f"  [n_scales {ns}] rollout MSE {res['rollout_mse']:.4e} "
              f"| params {n_params}", flush=True)

    keys = [f"ns{v}" for v in scales]
    mses = [arms[k]["rollout_mse"] for k in keys]
    verdict, detail = classify_nscales(scales, mses)
    results = {
        "arms": {k: {"n_scales": v, "rollout_mse": arms[k]["rollout_mse"],
                     "rollout_mse_stderr": arms[k]["rollout_mse_stderr"],
                     "params": arms[k]["params"]}
                 for k, v in zip(keys, scales)},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "NSCALES_UNRESOLVABLE",
            "c_resolved": verdict == "NSCALES_RESOLVED"},
        "gates": {"spread_gate": SPREAD_GATE, "norm_cap": NORM_CAP},
    }
    print(f"\nNSCALES-LADDER verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "nscales_ladder.json"),
              "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "nscales_ladder_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
