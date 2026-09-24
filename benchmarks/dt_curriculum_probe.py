"""
benchmarks/dt_curriculum_probe.py — DT-CURRICULUM (round 165): a dt-
resolution curriculum contrast on the single-frequency spring pool.

Preregistered in PRD §19 round 165 BEFORE execution. Scan §40 (Wu et al.
ICLR 2021, arXiv:2012.03107: curricula help mainly under constrained
budgets; random ordering is a strong baseline): on a 2000-step constrained
budget, does a dt curriculum (coarse dt=0.1 for 1000 steps, then fine
dt=0.05 for 1000 steps, weights carried over; fresh optimizer state —
recorded) beat a constant fine dt=0.05 for 2000 steps on the ω=2 pool?

Both arms are evaluated identically: dt=0.05 data, k=200 (physical
horizon T=10), held-out 128 trajectories. Arm loops reuse the prefix
train loop verbatim (round-149 loss-calibre rule).

Mechanical verdict (preregistered): diff = (A-B)/max(A,B);
  CURRICULUM_UNRESOLVABLE (negative) — |diff| < 5%
      (consistent with Wu's "random ordering is a strong baseline")
  CURRICULUM_BENEFICIAL — diff >= +5%  (A worse; curriculum helps)
  CURRICULUM_HARMFUL    — diff <= -5%  (A better; recorded as such)
Divergence of either arm (non-finite / > 1e6) takes precedence as the
negative branch.

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

DIFF_GATE = 0.05       # preregistered: |diff| below this => unresolved
DIVERGENCE_CAP = 1e6   # preregistered: arm failure threshold


def classify_curriculum(mse_a: float, mse_b: float,
                        gate: float = DIFF_GATE,
                        cap: float = DIVERGENCE_CAP):
    """Preregistered round-165 verdict (pure, test-pinned)."""
    for name, m in (("A", mse_a), ("B", mse_b)):
        if not math.isfinite(m) or m > cap:
            return "CURRICULUM_UNRESOLVABLE", {
                "reason": f"arm {name} diverged (mse={m:.3e} > {cap:.0e} "
                          f"or non-finite): preregistered negative branch"}
    diff = (mse_a - mse_b) / max(mse_a, mse_b, 1e-30)
    if abs(diff) < gate:
        return "CURRICULUM_UNRESOLVABLE", {
            "diff": diff,
            "criterion": f"|diff| < {gate:.0%}: dt curriculum not "
                         f"resolvable (consistent with Wu 2021 'random "
                         f"ordering is a strong baseline')"}
    if diff > 0:
        return "CURRICULUM_BENEFICIAL", {
            "diff": diff,
            "criterion": f"constant fine-dt arm worse by {diff:.1%}: "
                         f"curriculum beneficial under constrained budget "
                         f"(Wu 2021 direction)"}
    return "CURRICULUM_HARMFUL", {
        "diff": diff,
        "criterion": f"curriculum arm worse by {abs(diff):.1%}: recorded "
                     f"as such (honest registration)"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=301)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--omega", type=float, default=2.0)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--steps_fine", type=int, default=2000,
                    help="arm A total / arm B second phase")
    ap.add_argument("--steps_coarse", type=int, default=1000,
                    help="arm B first phase (coarse dt)")
    ap.add_argument("--dt_fine", type=float, default=0.05)
    ap.add_argument("--dt_coarse", type=float, default=0.1)
    ap.add_argument("--eval_k", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/dt_curriculum")
    ap.add_argument("--out_name", default="dt_curriculum.json",
                    help="round 167 (DT-CURRICULUM-2) writes its own "
                         "filename on the stacked branch")
    ap.add_argument("--arm_b_reverse", action="store_true",
                    help="round 167 (DT-CURRICULUM-2): arm B becomes the "
                         "REVERSE curriculum (fine dt first, then coarse); "
                         "evaluated on a fine-dt model after weight "
                         "re-mount; v1 default unchanged")
    args = ap.parse_args()

    # dt=0.05 data for BOTH training (arm A and arm B phase 2) and eval;
    # arm B phase 1 trains on dt=0.1 data of the SAME omega.
    g = torch.Generator().manual_seed(args.seed)
    qs_fine, ps_fine, om_fine = gen_spring(
        args.n_train + args.n_eval, args.gen_steps, args.dt_fine, 1,
        args.omega, args.omega, g, device=args.device)
    g = torch.Generator().manual_seed(args.seed)
    qs_coarse, ps_coarse, _ = gen_spring(
        args.n_train, args.gen_steps, args.dt_coarse, 1,
        args.omega, args.omega, g, device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"DT-CURRICULUM | omega={args.omega} hidden={args.hidden} "
          f"A=dt{args.dt_fine}x{args.steps_fine} B=dt{args.dt_coarse}x"
          f"{args.steps_coarse}->dt{args.dt_fine}x"
          f"{args.steps_fine - args.steps_coarse} (seed {args.seed}, "
          f"1-seed screening)", flush=True)

    arms = {}
    for name in ("A", "B"):
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
            dt=args.dt_fine)
        if name == "A":
            train_prefix(model, qs_fine[tr], ps_fine[tr], args.t_obs,
                         args.k_train, args.steps_fine, args.lr,
                         args.batch, args.seed)
            loss = float("nan")
        elif args.arm_b_reverse:
            # REVERSE curriculum: fine dt first, then coarse; weights
            # re-mounted on a fine-dt model so ALL arms evaluate on the
            # same dt=dt_fine model (round-165 weight-carry method).
            fine_model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
                dt=args.dt_fine)
            train_prefix(fine_model, qs_fine[tr], ps_fine[tr],
                         args.t_obs, args.k_train, args.steps_coarse,
                         args.lr, args.batch, args.seed)
            model.load_state_dict(fine_model.state_dict())
            coarse_model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
                dt=args.dt_coarse)
            coarse_model.load_state_dict(model.state_dict())
            train_prefix(coarse_model, qs_coarse[tr], ps_coarse[tr],
                         args.t_obs, args.k_train,
                         args.steps_fine - args.steps_coarse, args.lr,
                         args.batch, args.seed)
            model.load_state_dict(coarse_model.state_dict())
            loss = float("nan")
        else:
            # phase 1 on coarse-dt data: model.dt must match the training
            # grid, so the coarse model is trained with dt=dt_coarse and
            # its weights are re-mounted on a fine-dt model afterwards.
            coarse_model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
                dt=args.dt_coarse)
            train_prefix(coarse_model, qs_coarse[tr], ps_coarse[tr],
                         args.t_obs, args.k_train, args.steps_coarse,
                         args.lr, args.batch, args.seed)
            model.load_state_dict(coarse_model.state_dict())
            train_prefix(model, qs_fine[tr], ps_fine[tr], args.t_obs,
                         args.k_train,
                         args.steps_fine - args.steps_coarse, args.lr,
                         args.batch, args.seed)
            loss = float("nan")
        res = evaluate(model, qs_fine[ev], ps_fine[ev], om_fine[ev],
                       args.t_obs, args.eval_k, args.dt_fine)
        res["train_loss"] = loss
        arms[name] = res
        print(f"  [{name}] rollout MSE {res['rollout_mse']:.4e}",
              flush=True)

    verdict, detail = classify_curriculum(arms["A"]["rollout_mse"],
                                          arms["B"]["rollout_mse"])
    results = {
        "arms": arms,
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "CURRICULUM_UNRESOLVABLE",
            "c_beneficial": verdict == "CURRICULUM_BENEFICIAL",
            "c_harmful": verdict == "CURRICULUM_HARMFUL"},
        "gates": {"diff_gate": DIFF_GATE, "divergence_cap": DIVERGENCE_CAP},
        "optimizer_note": "arm B phase 2 starts a fresh Adam state "
                          "(weights carried over, optimizer state not) — "
                          "recorded, not controlled",
    }
    print(f"\nDT-CURRICULUM verdict {verdict} | {detail.get('criterion')}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, args.out_name), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "dt_curriculum_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
