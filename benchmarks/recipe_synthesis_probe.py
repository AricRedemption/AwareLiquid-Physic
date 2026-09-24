"""
benchmarks/recipe_synthesis_probe.py — RECIPE-SYNTHESIS (round 227):
composite-recipe vs default two-arm contrast, 3 seeds each, on the M1
spring family.

Preregistered in PRD §19 round 227 BEFORE execution (AMM-028 gate-2
first instance: five families judged "default suboptimal" — WD r181 /
DEPTH r185 / LRDECAY r201 / TOSA r223 / CTX-DIM r226 — forced a
combined-recipe probe before any new family). Arm B synthesizes the
single-axis optima recorded by those verdicts; the probe tests whether
they are additive (AMM-028 gate-3 first 3-seed instance).

Mechanical verdict (preregistered):
  RECIPE_ARM_DIVERGED (negative) — any arm/seed non-finite or rollout
      > 1e6: that arm unusable, recorded as such
  RECIPE_SYNERGIC   — ratio = mean_B / mean_A < 0.95 (composite gain
      >= 5%): decision = recipe back-propagation, open a recipe PR
  RECIPE_NULL       — 0.95 <= ratio <= 1.05: single-axis optima not
      additive; decision = recipe axes closed out, family admission
      shut per AMM-028 gate-1
  RECIPE_ANTAGONISTIC — ratio > 1.05: axes conflict; decision =
      conflict attribution parked (1-2)

The verdict line must carry per-seed values, direction-consistency
count (# seeds with B < A) and per-arm seed spread (AMM-028 gate-3).
Cross-validation anchor: arm A seed 0 is configurationally identical
to the house default arms of rounds 175/191/223/226 (same seed, same
rng stream) and must match 3.5582 bit-for-bit (sentinel clause r181).

t_obs is excluded from the composite (evaluation-window ambiguity,
kept as its own axis); ctx_dim held at default 8 (its optimum=1 needs
inference-semantic recalibration, queued as family follow-up); the
WARMUP 44.2% contra-expectation reading is re-tested incidentally.
Results JSON follows the audit schema (top-level "results" key); meta
carries exec_tier passthrough from probe_run.
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
SYNERGIC_GATE = 0.95  # preregistered: ratio < gate => composite gain
ANTAG_GATE = 1.05     # preregistered: ratio > gate => axes conflict
SEEDS = (0, 1, 2)     # preregistered: AMM-028 gate-3 3-seed minimum

# preregistered arms (round 227)
ARM_A = {"depth": 2, "lr_decay": 1.0, "weight_decay": 0.0,
         "warmup_steps": 0, "k_train": 8}
ARM_B = {"depth": 4, "lr_decay": 0.999, "weight_decay": 1e-4,
         "warmup_steps": 200, "k_train": 4}


def train_recipe(model, qs, ps, t_obs, k_train, steps, lr, batch, seed,
                 lr_decay: float = 1.0, weight_decay: float = 0.0,
                 warmup_steps: int = 0):
    """House prefix loop with the three recipe knobs composed.

    Identical rng consumption to benchmarks.liquid_physics_eval.train:
    with lr_decay=1.0, weight_decay=0.0, warmup_steps=0 the lr schedule
    is constant 1.0 — bit-for-bit the house default arm (sentinel
    clause r181).
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
        # random window: [t0, t0+t_obs) observed, next k_train predicted
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


def classify_recipe(mses_a, mses_b,
                    synergic_gate: float = SYNERGIC_GATE,
                    antag_gate: float = ANTAG_GATE,
                    cap: float = NORM_CAP):
    """Preregistered round-227 verdict (pure, test-pinned)."""
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
    spread_a = max(mses_a) / max(min(mses_a), 1e-30)
    spread_b = max(mses_b) / max(min(mses_b), 1e-30)
    stats = {"ratio": ratio, "mean_A": mean_a, "mean_B": mean_b,
             "mses_A": mses_a, "mses_B": mses_b,
             "direction_consistency": f"{consistent}/{len(mses_a)}",
             "seed_spread_A": spread_a, "seed_spread_B": spread_b}
    if ratio < synergic_gate:
        verdict = "RECIPE_SYNERGIC"
        stats["decision"] = ("composite gain >= 5%: back-propagate "
                             "recipe B as default-config candidate, "
                             "open recipe PR")
    elif ratio <= antag_gate:
        verdict = "RECIPE_NULL"
        stats["decision"] = ("single-axis optima not additive: recipe "
                             "axes closed out (no back-propagation), "
                             "family admission shut per AMM-028 g1")
    else:
        verdict = "RECIPE_ANTAGONISTIC"
        stats["decision"] = ("axes conflict: composite harmful, "
                             "conflict attribution parked 1-2")
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
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/recipe_synthesis")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"RECIPE-SYNTHESIS | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} "
          f"steps={args.train_steps} A=default{ARM_A} B=composite{ARM_B} "
          f"(seeds {seeds}, AMM-028 g3 3-seed)", flush=True)

    arms = {"A": [], "B": []}
    for seed in seeds:
        for tag, recipe in (("A", ARM_A), ("B", ARM_B)):
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
            arms[tag].append(res["rollout_mse"])
            print(f"  [arm {tag} seed {seed}] rollout MSE "
                  f"{res['rollout_mse']:.4e}", flush=True)

    verdict, detail = classify_recipe(arms["A"], arms["B"])
    results = {
        "arms": {tag: {"recipe": recipe,
                       "mses": dict(zip(seeds, arms[tag]))}
                 for tag, recipe in (("A", ARM_A), ("B", ARM_B))},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_diverged": verdict == "RECIPE_ARM_DIVERGED",
            "c_synergic": verdict == "RECIPE_SYNERGIC",
            "c_null": verdict == "RECIPE_NULL",
            "c_antagonistic": verdict == "RECIPE_ANTAGONISTIC"},
        "gates": {"synergic_gate": SYNERGIC_GATE,
                  "antag_gate": ANTAG_GATE, "norm_cap": NORM_CAP},
        "anchor": ("arm A seed 0 expected 3.5582 (house default, "
                   "rounds 175/191/223/226 sentinel)")},
    print(f"\nRECIPE-SYNTHESIS verdict {verdict} | ratio="
          f"{detail.get('ratio', float('nan')):.3f} | "
          f"{detail.get('decision', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "recipe_synthesis.json"),
              "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "recipe_synthesis_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
