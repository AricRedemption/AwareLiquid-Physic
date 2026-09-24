"""
benchmarks/kspan_ladder_probe.py — KSPAN-LADDER (round 191): training
rollout-span (k_train) ladder contrast on the M1 spring family.

Preregistered in PRD §19 round 191 BEFORE execution. Scan §46: k_train
is the train/deploy mismatch knob — larger training spans closer to the
long-horizon deployment (Brandstetter ICLR 2023 pushforward context; Q
Li MDPI 2026 one-step/long-horizon tension). The house default is
k_train=8; this probe sweeps k_train in {4, 8, 16} under the same
2000-step prefix budget, evaluating same-distribution held-out rollout
MSE at k=100.

k_train is a direct argument of the prefix train loop — natively
injectable (the round-181 watchdog rule applies cleanly).

Mechanical verdict (preregistered):
  KSPAN_UNRESOLVABLE (negative) — any arm diverged (non-finite or
      rollout > 1e6: that span unusable, recorded as such), or spread
      (max/min across arms) < 1.05 (span not resolvable; k=8 default
      sufficient — recorded as such)
  KSPAN_RESOLVED — spread >= 1.05: report the best k_train and direction
      (longer spans beneficial / harmful / interior optimum).

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

LADDER = (4, 8, 16)  # preregistered k_train values


def classify_kspan(spans, mses, spread_gate: float = SPREAD_GATE,
                   cap: float = NORM_CAP):
    """Preregistered round-191 verdict (pure, test-pinned)."""
    for s, m in zip(spans, mses):
        if not math.isfinite(m) or m > cap:
            state = "non-finite" if not math.isfinite(m) else "diverged"
            return "KSPAN_UNRESOLVABLE", {
                "reason": f"k_train={s} arm {state} (mse={m:.3e}): span "
                          f"unusable, recorded as such"}
    spread = max(mses) / max(min(mses), 1e-30)
    if spread < spread_gate:
        return "KSPAN_UNRESOLVABLE", {
            "spread": spread,
            "criterion": f"spread {spread:.3f} < {spread_gate}: training "
                         f"span not resolvable (k_train=8 default "
                         f"sufficient, recorded as such)"}
    best = spans[mses.index(min(mses))]
    if best == spans[0]:
        direction = "shorter spans beneficial (monotonic)"
    elif best == spans[-1]:
        direction = "longer spans beneficial (monotonic)"
    else:
        direction = "interior optimum"
    return "KSPAN_RESOLVED", {
        "spread": spread, "best_k_train": best, "direction": direction,
        "criterion": f"spread {spread:.2f} >= {spread_gate}: span "
                     f"resolvable"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--t_obs", type=int, default=24)
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
    ap.add_argument("--spans", default="4,8,16")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/kspan_ladder")
    args = ap.parse_args()
    spans = sorted(int(x) for x in args.spans.split(","))

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"KSPAN-LADDER | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} steps={args.train_steps} k_train ladder="
          f"{spans} (seed {args.seed}, 1-seed screening)", flush=True)

    arms = {}
    for span in spans:
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
            dt=args.dt)
        train_prefix(model, qs[tr], ps[tr], args.t_obs, span,
                     args.train_steps, args.lr, args.batch, args.seed)
        res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                       args.eval_k, args.dt)
        arms[f"k{span}"] = res
        print(f"  [k_train {span:>2}] rollout MSE {res['rollout_mse']:.4e}",
              flush=True)

    keys = [f"k{s}" for s in spans]
    mses = [arms[k]["rollout_mse"] for k in keys]
    verdict, detail = classify_kspan(spans, mses)
    results = {
        "arms": {k: {"k_train": s, "rollout_mse": arms[k]["rollout_mse"],
                     "rollout_mse_stderr": arms[k]["rollout_mse_stderr"]}
                 for k, s in zip(keys, spans)},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "KSPAN_UNRESOLVABLE",
            "c_resolved": verdict == "KSPAN_RESOLVED"},
        "gates": {"spread_gate": SPREAD_GATE, "norm_cap": NORM_CAP},
    }
    print(f"\nKSPAN-LADDER verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "kspan_ladder.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "kspan_ladder_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
