"""
benchmarks/lrdecay_ladder_probe.py — LRDECAY-LADDER (round 201):
learning-rate decay schedule ladder contrast on the M1 spring family.

Preregistered in PRD §19 round 201 BEFORE execution. Scan §48: train.py's
own docstring asserts "Constant lr overfits long schedules", yet
lr_decay=1.0 (constant) is the house-wide default and has never been
ablated. This probe sweeps the prefix loop's exponential decay factor
(LambdaLR) in {1.0, 0.999, 0.99} under the same 2000-step budget,
evaluating same-distribution held-out rollout MSE.

lr_decay is a direct argument of the prefix train loop — natively
injectable (the round-181 watchdog rule applies cleanly).

Mechanical verdict (preregistered):
  LRDECAY_UNRESOLVABLE (negative) — any arm diverged (non-finite or
      rollout > 1e6: that decay rate unusable, recorded as such), or
      spread (max/min across arms) < 1.05 (schedule shape not
      resolvable; constant-lr default sufficient — recorded as such,
      consistent with the d2l textbook note that decay reduces
      overfitting only when overfitting is present)
  LRDECAY_RESOLVED — spread >= 1.05: report the best decay rate and
      direction (faster decay beneficial / harmful / interior optimum).

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

LADDER = (1.0, 0.999, 0.99)  # preregistered decay factors


def classify_lrdecay(decays, mses, spread_gate: float = SPREAD_GATE,
                     cap: float = NORM_CAP):
    """Preregistered round-201 verdict (pure, test-pinned)."""
    for d, m in zip(decays, mses):
        if not math.isfinite(m) or m > cap:
            state = "non-finite" if not math.isfinite(m) else "diverged"
            return "LRDECAY_UNRESOLVABLE", {
                "reason": f"lr_decay={d} arm {state} (mse={m:.3e}): decay "
                          f"rate unusable, recorded as such"}
    spread = max(mses) / max(min(mses), 1e-30)
    if spread < spread_gate:
        return "LRDECAY_UNRESOLVABLE", {
            "spread": spread,
            "criterion": f"spread {spread:.3f} < {spread_gate}: schedule "
                         f"shape not resolvable (constant-lr default "
                         f"sufficient, recorded as such)"}
    best = decays[mses.index(min(mses))]
    if best == decays[0]:
        direction = "constant lr best (decay harmful)"
    elif best == decays[-1]:
        direction = "faster decay beneficial (monotonic)"
    else:
        direction = "interior optimum"
    return "LRDECAY_RESOLVED", {
        "spread": spread, "best_decay": best, "direction": direction,
        "criterion": f"spread {spread:.2f} >= {spread_gate}: schedule "
                     f"shape resolvable"}


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
    ap.add_argument("--decays", default="1.0,0.999,0.99")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/lrdecay_ladder")
    args = ap.parse_args()
    decays = sorted((float(x) for x in args.decays.split(",")), reverse=True)

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"LRDECAY-LADDER | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} steps={args.train_steps} "
          f"decay ladder={decays} (seed {args.seed}, 1-seed screening)",
          flush=True)

    arms = {}
    for decay in decays:
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
            dt=args.dt)
        train_prefix(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                     args.train_steps, args.lr, args.batch, args.seed,
                     lr_decay=decay)
        res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                       args.eval_k, args.dt)
        arms[f"d{decay:g}"] = res
        print(f"  [lr_decay {decay:g}] rollout MSE "
              f"{res['rollout_mse']:.4e}", flush=True)

    keys = [f"d{d:g}" for d in decays]
    mses = [arms[k]["rollout_mse"] for k in keys]
    verdict, detail = classify_lrdecay(decays, mses)
    results = {
        "arms": {k: {"lr_decay": d, "rollout_mse": arms[k]["rollout_mse"],
                     "rollout_mse_stderr": arms[k]["rollout_mse_stderr"]}
                 for k, d in zip(keys, decays)},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "LRDECAY_UNRESOLVABLE",
            "c_resolved": verdict == "LRDECAY_RESOLVED"},
        "gates": {"spread_gate": SPREAD_GATE, "norm_cap": NORM_CAP},
    }
    print(f"\nLRDECAY-LADDER verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "lrdecay_ladder.json"),
              "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "lrdecay_ladder_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
