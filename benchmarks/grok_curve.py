"""
benchmarks/grok_curve.py — GROK-CURVE (round 146): the shape of the
training-budget-to-generalization curve on the M1 spring family.

Preregistered in PRD §19 round 146 BEFORE execution. Round 143
(FASTSLOW-2) found BUDGET_DOMINANT: 1-step fit saturated while rollout
generalization kept improving with budget. Scan §35 supplies the
literature face (grokking / delayed generalization; Davies et al.
arXiv:2303.06173 two-speed unification). This probe asks WHICH narrative
the house family follows:

  SMOOTH_ASYMPTOTE  — rel MSE descends smoothly (power-law-ish) with
                      training steps: single-solution convergence story;
                      grokking naming NOT applicable (preregistered
                      negative branch, N1 does not introduce the term).
  GROKKING_SIGNATURE— an adjacent-step drop >= ratio_gate (3x) occurring
                      AFTER the fit has saturated (train_loss <= 1e-4):
                      two-speed competition story (fast memorizing vs
                      slow generalizing circuits).

Protocol = the E1 sample-efficiency口径 on the STEPS axis: one shared
pool (omega in [0.7, 1.8], 256 train + 128 held-out trajectories, dt=0.1,
t_obs=24), the standard prefix loop, hidden=64, ONE seed (screening
tier; multi-seed finals PARKED). Reuses run_one/gen_spring from
sample_efficiency_eval verbatim so the numbers are protocol-compatible.

Results JSON follows the audit schema (top-level "results" key); meta
carries exec_tier passthrough from probe_run.
"""

import argparse
import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from benchmarks.sample_efficiency_eval import gen_spring, run_one  # noqa: E402
from awareliquid_physics.observability import run_metadata  # noqa: E402

RATIO_GATE = 3.0    # preregistered: adjacent-step rel-MSE drop for a transition
SAT_LOSS = 1e-4     # preregistered: train_loss saturation level


def classify_grok(steps, mses, losses,
                  ratio_gate: float = RATIO_GATE,
                  sat_loss: float = SAT_LOSS):
    """Preregistered round-146 shape classifier (pure, test-pinned).

    GROKKING_SIGNATURE requires BOTH a >= ratio_gate adjacent-step drop
    AND fit saturation at the drop point (train_loss <= sat_loss) — a big
    drop from a still-improving fit is ordinary convergence, not grokking.
    """
    ratios = [mses[i] / max(mses[i + 1], 1e-30)
              for i in range(len(mses) - 1)]
    for i, r in enumerate(ratios):
        if r >= ratio_gate and losses[i + 1] <= sat_loss:
            return "GROKKING_SIGNATURE", {
                "transition_at_steps": steps[i + 1],
                "drop_ratio": r,
                "train_loss_at_transition": losses[i + 1],
                "criterion":
                    f"adjacent-step rel-MSE drop >= {ratio_gate}x with "
                    f"train_loss <= {sat_loss} (fit saturated; two-speed "
                    f"competition story)"}
    return "SMOOTH_ASYMPTOTE", {
        "max_ratio": max(ratios) if ratios else 1.0,
        "criterion":
            f"no adjacent-step drop >= {ratio_gate}x => smooth descent; "
            f"grokking naming not applicable (preregistered negative "
            f"branch; record asymptotic improvement only)"}


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
    ap.add_argument("--lr_decay", type=float, default=1.0)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--semigroup_frac", type=float, default=0.8)
    ap.add_argument("--start_mix", type=float, default=0.0)
    ap.add_argument("--start_mix_window", type=int, default=1)
    ap.add_argument("--steps", default="2500,5000,10000,20000,40000",
                    help="training-steps ladder (the probe axis)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/grok_curve")
    args = ap.parse_args()
    steps = sorted(int(s) for s in args.steps.split(","))

    g = torch.Generator().manual_seed(args.seed)
    pool_qs, pool_ps, pool_om = gen_spring(
        args.n_train + args.n_eval, args.gen_steps, args.dt, 1,
        args.omega_lo, args.omega_hi, g, device=args.device)
    print(f"GROK-CURVE | M1 spring family omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} prefix loop, steps "
          f"ladder {steps} (seed {args.seed}, 1-seed screening)",
          flush=True)

    ladder = []
    for s in steps:
        run_args = argparse.Namespace(
            **{**vars(args), "train_steps": s,
               "two_stage": False, "adaptive_sampling": False,
               "probe_context": False, "start_probe": False,
               "eval_ks_list": [args.eval_k]})
        res = run_one("prefix", args.n_train, pool_qs, pool_ps, pool_om,
                      args.seed, run_args)
        ladder.append({"steps": s, "rollout_mse": res["rollout_mse"],
                       "rollout_mse_stderr": res["rollout_mse_stderr"],
                       "train_loss": res["train_loss"],
                       "params": res["params"]})
        print(f"  [steps {s:>5}] rollout MSE {res['rollout_mse']:.4e} "
              f"| train_loss {res['train_loss']:.3e}", flush=True)

    mses = [pt["rollout_mse"] for pt in ladder]
    losses = [pt["train_loss"] for pt in ladder]
    verdict, detail = classify_grok(steps, mses, losses)
    results = {
        "ladder": ladder,
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_smooth_no_transition": verdict == "SMOOTH_ASYMPTOTE",
            "c_transition_after_saturation": verdict ==
            "GROKKING_SIGNATURE"},
        "gates": {"ratio_gate": RATIO_GATE, "sat_loss": SAT_LOSS},
    }
    print(f"\nGROK-CURVE verdict {verdict} | {detail.get('criterion')}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "grok_curve.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "grok_curve",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
