"""
benchmarks/pool_width_probe.py — POOL-WIDTH (round 175): training-pool
distribution-width contrast on the M1 spring family.

Preregistered in PRD §19 round 175 BEFORE execution. Scan §42 (Kumar
AAAI 2023: task diversity does not necessarily help; Li Nature 2025:
distribution coverage as an explicit dimension; Zhang ICML 2023: overly
wide distributions hurt accuracy). Two arms, same 2000-step prefix
budget, each evaluated on its OWN distribution's held-out set:

  A — NARROW pool omega in [0.95, 1.05]  (near single-frequency)
  B — WIDE pool   omega in [0.7, 1.8]    (the E1 default)

ratio = mse_B / mse_A:
  WIDTH_UNRESOLVABLE (negative) — ratio in [0.95, 1.05] (width not
      resolvable; consistent with Kumar's anti-intuition) or any arm
      non-finite/divergent
  WIDTH_COST    — ratio > 1.05 (wide pool costs same-distribution
      accuracy, §42.3 direction)
  WIDTH_BENEFIT — ratio < 0.95 (wide pool helps, classic diversity gain)

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

WIDTH_GATE = 0.05  # preregistered: |ratio-1| below this => unresolved
NORM_CAP = 1e6     # preregistered: divergence threshold

POOLS = {"A": (0.95, 1.05), "B": (0.7, 1.8)}


def classify_width(ratio: float, gate: float = WIDTH_GATE,
                   cap: float = NORM_CAP):
    """Preregistered round-175 verdict (pure, test-pinned)."""
    if not math.isfinite(ratio) or ratio > cap:
        return "WIDTH_UNRESOLVABLE", {
            "reason": f"ratio={ratio} non-finite or > {cap:.0e}: "
                      f"preregistered negative branch"}
    if abs(ratio - 1.0) < gate:
        return "WIDTH_UNRESOLVABLE", {
            "ratio": ratio,
            "criterion": f"ratio {ratio:.3f} in [1-{gate}, 1+{gate}]: "
                         f"pool width not resolvable (consistent with "
                         f"Kumar 2023 anti-intuition)"}
    if ratio > 1.0:
        return "WIDTH_COST", {
            "ratio": ratio,
            "criterion": f"ratio {ratio:.3f} > 1: wide pool costs "
                         f"same-distribution accuracy ({(ratio - 1):.1%} "
                         f"penalty; §42.3 direction)"}
    return "WIDTH_BENEFIT", {
        "ratio": ratio,
        "criterion": f"ratio {ratio:.3f} < 1: wide pool gains "
                     f"({(1 - ratio):.1%}; classic diversity direction)"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/pool_width")
    args = ap.parse_args()

    print(f"POOL-WIDTH | M1 spring prefix hidden={args.hidden} "
          f"steps={args.train_steps} arms=narrow[0.95,1.05]/wide[0.7,1.8] "
          f"(seed {args.seed}, 1-seed screening)", flush=True)

    arms = {}
    for name, (lo, hi) in POOLS.items():
        g = torch.Generator().manual_seed(args.seed)
        pool_qs, pool_ps, pool_om = gen_spring(
            args.n_train + args.n_eval, args.gen_steps, args.dt, 1,
            lo, hi, g, device=args.device)
        tr, ev = slice(0, args.n_train), slice(args.n_train, None)
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
            dt=args.dt)
        train_prefix(model, pool_qs[tr], pool_ps[tr], args.t_obs,
                     args.k_train, args.train_steps, args.lr,
                     args.batch, args.seed)
        res = evaluate(model, pool_qs[ev], pool_ps[ev], pool_om[ev],
                       args.t_obs, args.eval_k, args.dt)
        arms[name] = res
        print(f"  [{name} width {lo}-{hi}] rollout MSE "
              f"{res['rollout_mse']:.4e}", flush=True)

    ratio = arms["B"]["rollout_mse"] / max(arms["A"]["rollout_mse"], 1e-30)
    verdict, detail = classify_width(ratio)
    results = {
        "arms": {k: {"rollout_mse": v["rollout_mse"],
                     "rollout_mse_stderr": v["rollout_mse_stderr"]}
                 for k, v in arms.items()},
        "ratio": ratio,
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "WIDTH_UNRESOLVABLE",
            "c_cost": verdict == "WIDTH_COST",
            "c_benefit": verdict == "WIDTH_BENEFIT"},
        "gates": {"width_gate": WIDTH_GATE, "norm_cap": NORM_CAP},
        "pools": {k: {"omega_lo": lo, "omega_hi": hi}
                  for k, (lo, hi) in POOLS.items()},
    }
    print(f"\nPOOL-WIDTH verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "pool_width.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "pool_width_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
