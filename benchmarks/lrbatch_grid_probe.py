"""
benchmarks/lrbatch_grid_probe.py — LRBATCH-GRID (round 205): the Smith
equivalence (batch up == lr down) tested on the M1 spring family.

Preregistered in PRD §19 round 205 BEFORE execution. Scan §43.3 (Smith
et al. ICLR 2018: decaying lr == growing batch): the house trains at
batch=64, lr=3e-3, constant. This probe runs a 2x2 (batch, lr) grid and
checks the two preregistered scaling rules between the linear-equivalence
pair (16, 3e-3) vs (64, 1.2e-2) [lr proportional to batch] and the
sqrt-equivalence pair (16, 3e-3) vs (64, 6e-3) [lr proportional to
sqrt(batch)].

Mechanical verdict (preregistered):
  LRBATCH_UNRESOLVABLE (negative) — any cell diverged (non-finite or
      rollout > 1e6: that combination unusable, recorded as such)
  LINEAR_RULE / SQRT_RULE / SCALING_BROKEN — which preregistered rule
      (if either) holds on the equivalent pair, reported honestly.

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

DIFF_GATE = 0.05  # preregistered: equivalence threshold
NORM_CAP = 1e6    # preregistered: divergence threshold

GRID = ((16, 3e-3), (64, 3e-3), (16, 1.2e-2), (64, 1.2e-2),
        (64, 6e-3))  # last cell needed by the sqrt-equivalence pair


def classify_scaling(cells, linear_pair, sqrt_pair,
                     gate: float = DIFF_GATE, cap: float = NORM_CAP):
    """Preregistered round-205 verdict (pure, test-pinned). cells =
    {(batch, lr): mse}."""
    for key, mse in cells.items():
        if not math.isfinite(mse) or mse > cap:
            return "LRBATCH_UNRESOLVABLE", {
                "reason": f"cell {key} non-finite or > {cap:.0e}: "
                          f"preregistered negative branch"}
    lin = abs(cells[linear_pair[0]] - cells[linear_pair[1]]) \
        / max(cells[linear_pair[0]], cells[linear_pair[1]], 1e-30)
    sqr = abs(cells[sqrt_pair[0]] - cells[sqrt_pair[1]]) \
        / max(cells[sqrt_pair[0]], cells[sqrt_pair[1]], 1e-30)
    if lin >= gate and sqr >= gate:
        closer = "linear" if lin < sqr else "sqrt"
        return "SCALING_BROKEN", {
            "linear_diff": lin, "sqrt_diff": sqr,
            "criterion": f"both preregistered rules broken (linear "
                         f"{lin:.1%}, sqrt {sqr:.1%}); {closer} rule "
                         f"closer — recorded honestly"}
    if lin < gate:
        return "LINEAR_RULE", {
            "linear_diff": lin,
            "criterion": f"linear-equivalence pair within {gate:.0%} "
                         f"(lr proportional to batch)"}
    return "SQRT_RULE", {
        "sqrt_diff": sqr,
        "criterion": f"sqrt-equivalence pair within {gate:.0%} "
                     f"(lr proportional to sqrt(batch))"}


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
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/lrbatch_grid")
    args = ap.parse_args()

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"LRBATCH-GRID | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} grid={GRID} steps={args.train_steps} "
          f"(seed {args.seed}, 1-seed screening)", flush=True)

    cells = {}
    for batch, lr in GRID:
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
            dt=args.dt)
        train_prefix(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                     args.train_steps, lr, batch, args.seed)
        res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                       args.eval_k, args.dt)
        cells[(batch, lr)] = res["rollout_mse"]
        print(f"  [batch {batch:>2} lr {lr:.1e}] rollout MSE "
              f"{res['rollout_mse']:.4e}", flush=True)

    verdict, detail = classify_scaling(cells, linear_pair=((16, 3e-3),
                                                           (64, 1.2e-2)),
                                       sqrt_pair=((16, 3e-3), (64, 6e-3)))
    results = {
        "cells": {f"b{b}_lr{lr:g}": {"batch": b, "lr": lr,
                                     "rollout_mse": mse}
                  for (b, lr), mse in cells.items()},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "LRBATCH_UNRESOLVABLE",
            "c_scaling_broken": verdict == "SCALING_BROKEN",
            "c_rule_holds": verdict in ("LINEAR_RULE", "SQRT_RULE")},
        "gates": {"diff_gate": DIFF_GATE, "norm_cap": NORM_CAP},
    }
    print(f"\nLRBATCH-GRID verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "lrbatch_grid.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "lrbatch_grid_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
