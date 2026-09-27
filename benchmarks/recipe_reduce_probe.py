"""
benchmarks/recipe_reduce_probe.py — RECIPE-REDUCE (round 440):
reduced-composite (depth+warmup only) vs five-axis composite vs
default, 3 seeds each, on the M1 spring family.

Preregistered in PRD §19 round 440 BEFORE execution. RECIPE-LOO
(round 434) classified lr_decay/weight_decay/k_train as NEUTRAL
(removal does not degrade the composite by >=5%) but that evidence
was deliberately NOT used to trim the back-propagation candidate
(AMM-028 gate 1: candidate-definition changes need gate-passing
evidence, LOO inference is indirect). This probe supplies the direct
3-seed comparison: if the two-axis reduced composite (the two
load-bearing axes only) matches the five-axis composite, the
candidate can be trimmed with strong evidence.

Mechanical verdict (preregistered):
  RECIPE_ARM_DIVERGED — any arm/seed non-finite or rollout > 1e6
  RECIPE_REDUCE_OK    — ratio_red = mean(B2) / mean(B) <= 1.05:
      decision = back-propagation candidate trimmed to two axes
      (depth+warmup); AMM-028 gate 1 satisfied by direct 3-seed
      comparison; trimmed candidate vs default confirmation rides on
      the already-recorded RECIPE_SYNERGIC/HORIZON chain (B2 contains
      the two load-bearing axes; its ratio vs A is reported for the
      record)
  RECIPE_REDUCE_WEAK  — 1.05 < ratio_red <= 1.15: neutral axes carry
      something jointly but under the weak-evidence bar; decision =
      five-axis candidate unchanged, reduction closed as not
      gate-passing
  RECIPE_REDUCE_NO    — ratio_red > 1.15: neutral axes jointly
      load-bearing (interaction); decision = five-axis candidate
      unchanged, LOO NEUTRAL readings explained by interaction

Anchors (deterministic CPU, same machine):
  arm A seed 0 = 3.5582 bit-for-bit (house default sentinel);
  arm B 3 seeds = {3.3910, 2.3385, 2.2052} bit-for-bit (round 228
  reproduction sentinel).

Verdict lines carry per-seed values, direction-consistency counts and
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
OK_GATE = 1.05        # preregistered: reduced composite matches five-axis
WEAK_GATE = 1.15      # preregistered: weak band upper bound
SEEDS = (0, 1, 2)     # preregistered: AMM-028 gate-3 3-seed minimum

# preregistered arms (round 227 composite, round 434 LOO, round 440 reduce)
ARM_A = {"depth": 2, "lr_decay": 1.0, "weight_decay": 0.0,
         "warmup_steps": 0, "k_train": 8}
ARM_B = {"depth": 4, "lr_decay": 0.999, "weight_decay": 1e-4,
         "warmup_steps": 200, "k_train": 4}
ARM_B2 = {"depth": 4, "lr_decay": 1.0, "weight_decay": 0.0,
          "warmup_steps": 200, "k_train": 8}


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


def classify_reduce(mses_a, mses_b, mses_b2,
                    ok_gate: float = OK_GATE, weak_gate: float = WEAK_GATE,
                    cap: float = NORM_CAP):
    """Preregistered round-440 verdict (pure, test-pinned)."""
    for tag, vals in (("A", mses_a), ("B", mses_b), ("B2", mses_b2)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "RECIPE_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} {state} "
                              f"(mse={m:.3e}): arm unusable, "
                              f"recorded as such"}
    mean_a = sum(mses_a) / len(mses_a)
    mean_b = sum(mses_b) / len(mses_b)
    mean_b2 = sum(mses_b2) / len(mses_b2)
    ratio_red = mean_b2 / max(mean_b, 1e-30)
    ratio_b2_a = mean_b2 / max(mean_a, 1e-30)
    cons_red = sum(1 for b, r in zip(mses_b, mses_b2) if r > b)
    cons_b2_a = sum(1 for a, r in zip(mses_a, mses_b2) if r < a)
    stats = {"mean_A": mean_a, "mean_B": mean_b, "mean_B2": mean_b2,
             "ratio_red": ratio_red, "ratio_B2_vs_A": ratio_b2_a,
             "mses_A": mses_a, "mses_B": mses_b, "mses_B2": mses_b2,
             "direction_consistency_red": f"{cons_red}/{len(mses_b)} "
                                          f"(B2>B)",
             "direction_consistency_B2_A": f"{cons_b2_a}/{len(mses_a)} "
                                           f"(B2<A)",
             "seed_spread_B2": max(mses_b2) / max(min(mses_b2), 1e-30)}
    if ratio_red <= ok_gate:
        verdict = "RECIPE_REDUCE_OK"
        stats["decision"] = ("reduced two-axis composite matches "
                             "five-axis: back-propagation candidate "
                             "trimmed to depth+warmup (AMM-028 g1 "
                             "gate-passing direct 3-seed evidence)")
    elif ratio_red <= weak_gate:
        verdict = "RECIPE_REDUCE_WEAK"
        stats["decision"] = ("neutral axes carry something jointly but "
                             "under the weak bar: five-axis candidate "
                             "unchanged, reduction closed as not "
                             "gate-passing")
    else:
        verdict = "RECIPE_REDUCE_NO"
        stats["decision"] = ("neutral axes jointly load-bearing "
                             "(interaction): five-axis candidate "
                             "unchanged, LOO NEUTRAL readings "
                             "explained by interaction")
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
                    default="benchmarks/physics_out_v02/recipe_reduce")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"RECIPE-REDUCE | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} "
          f"steps={args.train_steps} B={ARM_B} B2={ARM_B2} "
          f"(seeds {seeds}, AMM-028 g3 3-seed)", flush=True)

    arm_specs = (("A", ARM_A), ("B", ARM_B), ("B2", ARM_B2))
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

    verdict, detail = classify_reduce(mses["A"], mses["B"], mses["B2"])
    results = {
        "arms": {tag: {"recipe": recipe,
                       "mses": dict(zip(seeds, mses[tag]))}
                 for tag, recipe in arm_specs},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_diverged": verdict == "RECIPE_ARM_DIVERGED",
            "c_reduce_ok": verdict == "RECIPE_REDUCE_OK",
            "c_reduce_weak": verdict == "RECIPE_REDUCE_WEAK",
            "c_reduce_no": verdict == "RECIPE_REDUCE_NO"},
        "gates": {"ok_gate": OK_GATE, "weak_gate": WEAK_GATE,
                  "norm_cap": NORM_CAP},
        "anchor": ("arm A seed 0 expected 3.5582 (house default, "
                   "rounds 175/191/223/226 sentinel); arm B 3 seeds "
                   "expected {3.3910, 2.3385, 2.2052} bit-for-bit "
                   "(round 228 reproduction sentinel)")
    }
    print(f"\nRECIPE-REDUCE verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "recipe_reduce.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "recipe_reduce_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
