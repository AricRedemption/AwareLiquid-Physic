"""
benchmarks/recipe_budget_probe.py — RECIPE-BUDGET (round 460):
composite-recipe vs default at the 8000-step training budget, 3 seeds
each, on the M1 spring family.

Preregistered in PRD §19 round 460 BEFORE execution. Round 227
registered "double budget point (2000+8000) as a slow-axis candidate,
not mandatory"; AMM-044 (round 459) supply obligation converts the
first registered candidate into a queue item (RECIPE-BUDGET) instead
of inventing a new goal. Decision coupling: the back-propagation PR
scope must state the budget regime the 10.7% composite gain is valid
in — the 2000-step reading already has RECIPE_SYNERGIC (ratio 0.893)
and RECIPE-HORIZON confirmed robustness across evaluation horizons
k100-400; this probe covers the training-budget axis.

Mechanical verdict (preregistered):
  RECIPE_ARM_DIVERGED  — any arm/seed non-finite or rollout > 1e6
  RECIPE_BUDGET_ROBUST — ratio = mean_B/mean_A < 0.95: composite gain
      holds at 8000 steps; back-propagation PR scope = budget-robust
      (2000+8000)
  RECIPE_BUDGET_NULL   — 0.95 <= ratio <= 1.05: gain does not transfer
      to the larger budget; PR scope = 2000-step regime only
  RECIPE_BUDGET_REVERSED — ratio > 1.05: composite harmful at 8000
      steps; PR scope = 2000-step regime only + budget-interaction
      note

Anchors (deterministic CPU, same machine): arm A seed 0 is NOT the
3.5582 sentinel here — the sentinel pins the 2000-step house default
run; at 8000 steps a fresh anchor applies and is recorded as such
(no historical value exists; recorded for future replay). Arm B at
8000 steps likewise has no historical anchor; both are honestly noted
as new-baseline readings (round 228 reproduction sentinel does NOT
apply at 8000 steps — the rng stream differs).

Verdict lines carry per-seed values, direction-consistency count and
seed spreads (AMM-028 gate 3). Results JSON follows the audit schema
(top-level "results" key); meta carries exec_tier passthrough from
probe_run.
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
    evaluate, rollout_mse_loss)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

NORM_CAP = 1e6        # preregistered: divergence threshold
SYNERGIC_GATE = 0.95  # preregistered: ratio < gate => gain holds
ANTAG_GATE = 1.05     # preregistered: ratio > gate => reversed
SEEDS = (0, 1, 2)     # preregistered: AMM-028 gate-3 3-seed minimum

# preregistered arms (round 227 composite; budget axis = 8000 steps)
ARM_A = {"depth": 2, "lr_decay": 1.0, "weight_decay": 0.0,
         "warmup_steps": 0, "k_train": 8}
ARM_B = {"depth": 4, "lr_decay": 0.999, "weight_decay": 1e-4,
         "warmup_steps": 200, "k_train": 4}


def train_recipe(model, qs, ps, t_obs, k_train, steps, lr, batch, seed,
                 lr_decay: float = 1.0, weight_decay: float = 0.0,
                 warmup_steps: int = 0):
    """House prefix loop with the three recipe knobs composed.

    Identical rng consumption to benchmarks.liquid_physics_eval.train;
    copied verbatim from benchmarks/recipe_loo_probe.py (round 434).
    """
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr,
                           weight_decay=weight_decay)

    def lr_fn(t):
        warm = min(1.0, (t + 1) / warmup_steps) if warmup_steps > 0 else 1.0
        return warm * (lr_decay ** t)

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_fn)
    N, S = qs.shape[0], qs.shape[1]
    model.train()
    loss = torch.tensor(float("nan"))
    for _ in range(steps):
        bi = torch.randint(0, N, (batch,), generator=g)
        t0 = torch.randint(0, S - t_obs - k_train, (1,), generator=g).item()
        q_obs = qs[bi, t0:t0 + t_obs]; p_obs = ps[bi, t0:t0 + t_obs]
        fut = slice(t0 + t_obs - 1, t0 + t_obs + k_train)        # incl. last observed
        q_true = qs[bi, fut]; p_true = ps[bi, fut]
        qs_pred, ps_pred, _ = model(q_obs, p_obs, k_train)
        loss = rollout_mse_loss(qs_pred, ps_pred, q_true, p_true)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        sched.step()
    return loss.item()


def classify_budget(mses_a, mses_b,
                    synergic_gate: float = SYNERGIC_GATE,
                    antag_gate: float = ANTAG_GATE,
                    cap: float = NORM_CAP):
    """Preregistered round-460 verdict (pure, test-pinned)."""
    for tag, vals in (("A", mses_a), ("B", mses_b)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "RECIPE_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} {state} "
                              f"(mse={m:.3e}): arm unusable, "
                              f"recorded as such"}
    mean_a = sum(mses_a) / len(mses_a)
    mean_b = sum(mses_b) / len(mses_b)
    ratio = mean_b / max(mean_a, 1e-30)
    consistent = sum(1 for a, b in zip(mses_a, mses_b) if b < a)
    stats = {"ratio": ratio, "mean_A": mean_a, "mean_B": mean_b,
             "mses_A": mses_a, "mses_B": mses_b,
             "direction_consistency": f"{consistent}/{len(mses_a)}",
             "seed_spread_A": max(mses_a) / max(min(mses_a), 1e-30),
             "seed_spread_B": max(mses_b) / max(min(mses_b), 1e-30)}
    if ratio < synergic_gate:
        verdict = "RECIPE_BUDGET_ROBUST"
        stats["decision"] = ("composite gain holds at 8000 steps: "
                             "back-propagation PR scope = budget-robust "
                             "(2000+8000)")
    elif ratio <= antag_gate:
        verdict = "RECIPE_BUDGET_NULL"
        stats["decision"] = ("gain does not transfer to the larger "
                             "budget: PR scope = 2000-step regime only")
    else:
        verdict = "RECIPE_BUDGET_REVERSED"
        stats["decision"] = ("composite harmful at 8000 steps: PR scope "
                             "= 2000-step regime only + budget-"
                             "interaction note")
    return verdict, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=8000)
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/recipe_budget")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"RECIPE-BUDGET | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} "
          f"steps={args.train_steps} A=default{ARM_A} B=composite{ARM_B} "
          f"(seeds {seeds}, AMM-028 g3 3-seed)", flush=True)

    arm_specs = (("A", ARM_A), ("B", ARM_B))
    mses: dict = {tag: [] for tag, _ in arm_specs}
    for seed in seeds:
        for tag, recipe in arm_specs:
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=recipe["depth"], dt=args.dt)
            train_recipe(model, qs[tr], ps[tr], args.t_obs,
                         recipe["k_train"], args.train_steps, args.lr,
                         args.batch, seed,
                         lr_decay=recipe["lr_decay"],
                         weight_decay=recipe["weight_decay"],
                         warmup_steps=recipe["warmup_steps"])
            res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                           args.eval_k, args.dt)
            mses[tag].append(res["rollout_mse"])
            print(f"  [arm {tag} seed {seed}] rollout MSE "
                  f"{res['rollout_mse']:.4e}", flush=True)

    verdict, detail = classify_budget(mses["A"], mses["B"])
    results = {
        "arms": {tag: {"recipe": recipe,
                       "mses": dict(zip(seeds, mses[tag]))}
                 for tag, recipe in arm_specs},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_diverged": verdict == "RECIPE_ARM_DIVERGED",
            "c_robust": verdict == "RECIPE_BUDGET_ROBUST",
            "c_null": verdict == "RECIPE_BUDGET_NULL",
            "c_reversed": verdict == "RECIPE_BUDGET_REVERSED"},
        "gates": {"synergic_gate": SYNERGIC_GATE,
                  "antag_gate": ANTAG_GATE, "norm_cap": NORM_CAP},
        "anchor": ("8000-step budget: no historical sentinel applies "
                   "(the 3.5582 sentinel pins the 2000-step house "
                   "default; rng stream differs) — arm values are "
                   "recorded as new baselines for future replay")}
    print(f"\nRECIPE-BUDGET verdict {verdict} | ratio="
          f"{detail.get('ratio', float('nan')):.3f} | "
          f"{detail.get('decision', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "recipe_budget.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "recipe_budget_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
