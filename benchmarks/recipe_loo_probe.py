"""
benchmarks/recipe_loo_probe.py — RECIPE-LOO (round 434):
leave-one-out ablation of the five-axis composite recipe (arm B of
RECIPE-SYNTHESIS, round 227/228), 3 seeds each, on the M1 spring
family.

Preregistered in PRD §19 round 434 BEFORE execution. RECIPE-SYNTHESIS
judged RECIPE_SYNERGIC (ratio=0.893, 10.7% composite gain, 3/3
direction-consistent) but round 228 explicitly registered the family
follow-up: "single-axis contributions are inseparable inside the
composite (attribution = family follow-up candidate, needs 3-seed
single-axis ablation)" — this probe is that registered follow-up.
AMM-038 clause 7 backlog item 5 unlocked combination experiments.

Arms: A (house default, anchor), B (five-axis composite), and five
LOO arms B-minus-axis (axis x reverted to its default value, the other four
kept at arm-B optima).

Mechanical verdict (preregistered), per-axis first:
  for axis x: loo_ratio_x = mean(B\\x) / mean(B)
    loo_ratio_x > 1.05  => axis x LOAD_BEARING (removal degrades >=5%)
    loo_ratio_x < 0.95  => axis x HARMFUL_IN_COMPOSITE (removal
                           improves >=5%: demotion candidate)
    otherwise           => NEUTRAL (simplification candidate, weaker
                           evidence)
Aggregate:
  RECIPE_ARM_DIVERGED    — any arm/seed non-finite or rollout > 1e6
  RECIPE_LOO_HARMFUL     — >=1 axis harmful: decision = back-propagation
                           candidate trimmed to B minus harmful axes;
                           trimmed-composite re-verification queued as
                           family follow-up
  RECIPE_LOO_ALL_LOAD    — all five axes load-bearing: decision =
                           five-axis candidate unchanged, single-axis
                           attribution closed (gain is synergy, not
                           single-axis), WARMUP contra-expectation
                           attribution closed with it
  RECIPE_LOO_PARTIAL     — otherwise: decision = five-axis candidate
                           unchanged; load-bearing axes recorded;
                           neutral axes flagged as simplification
                           candidates (3-seed, weaker evidence)

Anchors (deterministic CPU, same machine as round 228):
  arm A seed 0 = 3.5582 bit-for-bit (house default sentinel, rounds
  175/191/223/226); arm B 3 seeds = {3.3910, 2.3385, 2.2052}
  bit-for-bit (round 228 reproduction sentinel).

Verdict lines carry per-seed values, direction-consistency counts and
seed spreads per axis (AMM-028 gate 3). ctx_dim stays excluded
(inference-semantic recalibration, separate family follow-up); t_obs
stays excluded (evaluation-window ambiguity).
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
LOAD_GATE = 1.05      # preregistered: loo_ratio above => load-bearing
HARM_GATE = 0.95      # preregistered: loo_ratio below => harmful
SEEDS = (0, 1, 2)     # preregistered: AMM-028 gate-3 3-seed minimum

# preregistered arms (round 227 composite, round 434 LOO reverts)
ARM_A = {"depth": 2, "lr_decay": 1.0, "weight_decay": 0.0,
         "warmup_steps": 0, "k_train": 8}
ARM_B = {"depth": 4, "lr_decay": 0.999, "weight_decay": 1e-4,
         "warmup_steps": 200, "k_train": 4}
LOO_AXES = ("depth", "lr_decay", "weight_decay", "warmup_steps",
            "k_train")


def loo_arm(axis: str):
    """Arm B with one axis reverted to its arm-A (default) value."""
    arm = dict(ARM_B)
    arm[axis] = ARM_A[axis]
    return arm


def train_recipe(model, qs, ps, t_obs, k_train, steps, lr, batch, seed,
                 lr_decay: float = 1.0, weight_decay: float = 0.0,
                 warmup_steps: int = 0):
    """House prefix loop with the three recipe knobs composed.

    Identical rng consumption to benchmarks.liquid_physics_eval.train:
    with lr_decay=1.0, weight_decay=0.0, warmup_steps=0 the lr schedule
    is constant 1.0 — bit-for-bit the house default arm (sentinel
    clause r181). Copied verbatim from
    benchmarks/recipe_synthesis_probe.py (round 227).
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


def classify_loo(mses: dict, load_gate: float = LOAD_GATE,
                 harm_gate: float = HARM_GATE, cap: float = NORM_CAP):
    """Preregistered round-434 verdict (pure, test-pinned).

    mses maps arm tag -> list of per-seed rollout MSEs, arm tags being
    "A", "B" and "B\\<axis>" for each axis in LOO_AXES.
    """
    for tag in sorted(mses):
        for s, m in zip(SEEDS, mses[tag]):
            if not math.isfinite(m) or m > cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "RECIPE_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} {state} "
                              f"(mse={m:.3e}): arm unusable, "
                              f"recorded as such"}
    mean_b = sum(mses["B"]) / len(mses["B"])
    axes = {}
    for axis in LOO_AXES:
        vals = mses[f"B\\{axis}"]
        mean_loo = sum(vals) / len(vals)
        ratio = mean_loo / max(mean_b, 1e-30)
        consistent = sum(1 for b, l in zip(mses["B"], vals) if l > b)
        spread = max(vals) / max(min(vals), 1e-30)
        if ratio > load_gate:
            cls = "LOAD_BEARING"
        elif ratio < harm_gate:
            cls = "HARMFUL_IN_COMPOSITE"
        else:
            cls = "NEUTRAL"
        axes[axis] = {"loo_ratio": ratio, "mean_loo": mean_loo,
                      "mses_loo": vals, "direction_consistency":
                      f"{consistent}/{len(vals)} (loo>B)",
                      "seed_spread_loo": spread, "class": cls}
    harmful = [a for a in LOO_AXES
               if axes[a]["class"] == "HARMFUL_IN_COMPOSITE"]
    load = [a for a in LOO_AXES if axes[a]["class"] == "LOAD_BEARING"]
    stats = {"mean_B": mean_b, "mses_B": mses["B"],
             "axes": axes,
             "harmful_axes": harmful, "load_bearing_axes": load}
    if harmful:
        verdict = "RECIPE_LOO_HARMFUL"
        stats["decision"] = (f"axes {harmful} harmful inside the "
                             "composite: trim back-propagation "
                             "candidate to B minus harmful axes; "
                             "trimmed-composite re-verification "
                             "queued as family follow-up")
    elif len(load) == len(LOO_AXES):
        verdict = "RECIPE_LOO_ALL_LOAD"
        stats["decision"] = ("all five axes load-bearing: five-axis "
                             "back-propagation candidate unchanged; "
                             "single-axis attribution closed (gain is "
                             "synergy); WARMUP contra-expectation "
                             "attribution closed with it")
    else:
        verdict = "RECIPE_LOO_PARTIAL"
        stats["decision"] = ("five-axis back-propagation candidate "
                             "unchanged; load-bearing axes recorded; "
                             "neutral axes flagged as simplification "
                             "candidates (3-seed, weaker evidence)")
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
                    default="benchmarks/physics_out_v02/recipe_loo")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"RECIPE-LOO | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} steps={args.train_steps} "
          f"B={ARM_B} LOO axes={LOO_AXES} (seeds {seeds}, "
          f"AMM-028 g3 3-seed)", flush=True)

    arm_specs = [("A", ARM_A), ("B", ARM_B)]
    arm_specs += [(f"B\\{axis}", loo_arm(axis)) for axis in LOO_AXES]
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

    verdict, detail = classify_loo(mses)
    results = {
        "arms": {tag: {"recipe": recipe,
                       "mses": dict(zip(seeds, mses[tag]))}
                 for tag, recipe in arm_specs},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_diverged": verdict == "RECIPE_ARM_DIVERGED",
            "c_harmful": verdict == "RECIPE_LOO_HARMFUL",
            "c_all_load": verdict == "RECIPE_LOO_ALL_LOAD",
            "c_partial": verdict == "RECIPE_LOO_PARTIAL"},
        "gates": {"load_gate": LOAD_GATE, "harm_gate": HARM_GATE,
                  "norm_cap": NORM_CAP},
        "anchor": ("arm A seed 0 expected 3.5582 (house default, "
                   "rounds 175/191/223/226 sentinel); arm B 3 seeds "
                   "expected {3.3910, 2.3385, 2.2052} bit-for-bit "
                   "(round 228 reproduction sentinel)")
    }
    print(f"\nRECIPE-LOO verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "recipe_loo.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "recipe_loo_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
