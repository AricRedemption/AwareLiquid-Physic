"""
benchmarks/tosa_decouple_probe.py — TOSA-CTX-DECOUPLE (round 241):
training-window × evaluation-prefix 2x2 decouple, 3 seeds, on the M1
spring family (E1 calibre).

Preregistered in PRD §19 round 240 BEFORE execution (AMM-027 pool
routing: the round-223 TOSA-LADDER verdict line flagged "窗长效应与
ctx 推断质量解耦未测" and the round-227 RECIPE entry held t_obs out
of the composite for "评估口径歧义"). Round 223 judged t_obs=8 best
by 4.5% — but each ladder arm was evaluated from its OWN window
(evaluate with t_obs = train t_obs), so that gain mixes a training-
window effect with an evaluation-prefix effect. This probe separates
the two: train arms t_obs_train ∈ {8, 24} x 3 seeds (house
train_prefix, verbatim), each trained model evaluated twice on the
same held-out trajectories — once from its own window (replicating
round 223) and once from the fixed default window 24 (the decoupled
readout).

Mechanical verdict (preregistered, 3-seed mean ratio
r = mean_MSE(t8-train, eval@24) / mean_MSE(t24-train, eval@24) —
training-window effect at FIXED evaluation):
  DEC_ARM_DIVERGED (negative) — any arm/seed/eval non-finite or > 1e6
  DEC_TRAIN_BENEFICIAL — r < 0.95: t8 training-side effect survives
      decoupling; t_obs=8 flagged as recipe-candidate annotation
  DEC_TRAIN_NULL — 0.95 <= r <= 1.05: round-223 t8 gain was an
      evaluation-prefix artifact; t_obs stays 24, round-223 reading
      downgraded (presentation-layer revision at merge time)
  DEC_TRAIN_HARMFUL — r > 1.05: shorter training window harmful,
      recorded as such

Report-only secondary gate: evaluation-prefix sensitivity of the
t8-trained arm — mean_MSE(t8-train, eval@24) / mean_MSE(t8-train,
eval@8) — quantifies how much extending the inference prefix from 8
to 24 costs a short-window-trained model (caliber material for the
round-223 t16/t48 sawtooth texture).

The verdict line carries per-seed values, direction-consistency count
(# seeds with t8 < t24 at fixed eval) and per-arm seed spread
(AMM-028 gate-3). Cross-validation anchors: (t24-train, eval@24)
seed 0 = 3.5581917762756348 (house default sentinel) and (t8-train,
eval@8) seed 0 = 3.4044134616851807 (round-223 t8 arm), both
bit-for-bit. Family boundary: TOSA family in-segment round 2 of 2 —
family closes after this. Results JSON follows the audit schema
(top-level "results" key); meta carries exec_tier from probe_run.
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

NORM_CAP = 1e6          # preregistered: divergence threshold
BENEFICIAL_GATE = 0.95  # preregistered: r < gate => train-side effect
HARM_GATE = 1.05        # preregistered: r > gate => shorter harmful
SEEDS = (0, 1, 2)       # preregistered: AMM-028 gate-3 3-seed minimum
SENTINEL_T24 = 3.5581917762756348   # house default (t24, eval@24) s0
SENTINEL_T8 = 3.4044134616851807    # round-223 t8 arm (t8, eval@8) s0


def mean(vals):
    return sum(vals) / len(vals)


def classify_decouple(mses_t8_fixed, mses_t24_fixed,
                      beneficial_gate: float = BENEFICIAL_GATE,
                      harm_gate: float = HARM_GATE,
                      cap: float = NORM_CAP):
    """Preregistered round-240 verdict (pure, test-pinned).

    mses_* are rollout MSEs at FIXED eval@24, 3-seed lists:
    mses_t8_fixed = t8-trained arm, mses_t24_fixed = t24-trained arm.
    """
    for tag, vals in (("t8", mses_t8_fixed), ("t24", mses_t24_fixed)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "DEC_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} {state} "
                              f"(mse={m:.3e}): arm unusable, "
                              f"recorded as such"}
    mean_t8 = mean(mses_t8_fixed)
    mean_t24 = mean(mses_t24_fixed)
    ratio = mean_t8 / max(mean_t24, 1e-30)
    consistent = sum(1 for a, b in zip(mses_t8_fixed, mses_t24_fixed)
                     if a < b)
    spread_t8 = max(mses_t8_fixed) / max(min(mses_t8_fixed), 1e-30)
    spread_t24 = max(mses_t24_fixed) / max(min(mses_t24_fixed), 1e-30)
    stats = {"ratio": ratio, "mean_t8": mean_t8, "mean_t24": mean_t24,
             "mses_t8": mses_t8_fixed, "mses_t24": mses_t24_fixed,
             "direction_consistency": f"{consistent}/{len(mses_t8_fixed)}",
             "seed_spread_t8": spread_t8, "seed_spread_t24": spread_t24}
    if ratio < beneficial_gate:
        verdict = "DEC_TRAIN_BENEFICIAL"
        stats["decision"] = ("t8 training-side effect survives decoupling: "
                             "t_obs=8 flagged as recipe-candidate "
                             "annotation")
    elif ratio <= harm_gate:
        verdict = "DEC_TRAIN_NULL"
        stats["decision"] = ("round-223 t8 gain was an evaluation-prefix "
                             "artifact: t_obs stays 24, round-223 reading "
                             "downgraded (presentation-layer revision at "
                             "merge time)")
    else:
        verdict = "DEC_TRAIN_HARMFUL"
        stats["decision"] = ("shorter training window harmful at 3-seed "
                             "fixed eval: recorded as such")
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
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--fixed_eval_tobs", type=int, default=24)
    ap.add_argument("--train_tobs", default="8,24")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/tosa_decouple")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]
    t_trains = sorted(int(x) for x in args.train_tobs.split(","))

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"TOSA-CTX-DECOUPLE | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} "
          f"steps={args.train_steps} train_tobs={t_trains} "
          f"eval=own+fixed{args.fixed_eval_tobs} (seeds {seeds}, "
          f"AMM-028 g3; round-240 preregistration)", flush=True)

    mses = {}   # mses[t_train]["own"/"fixed"][seed_index]
    for t_train in t_trains:
        mses[t_train] = {"own": [], "fixed": []}
        for seed in seeds:
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            train_prefix(model, qs[tr], ps[tr], t_train, args.k_train,
                         args.train_steps, args.lr, args.batch, seed)
            r_own = evaluate(model, qs[ev], ps[ev], om[ev], t_train,
                             args.eval_k, args.dt)
            r_fix = evaluate(model, qs[ev], ps[ev], om[ev],
                             args.fixed_eval_tobs, args.eval_k, args.dt)
            mses[t_train]["own"].append(r_own["rollout_mse"])
            mses[t_train]["fixed"].append(r_fix["rollout_mse"])
            print(f"  [t_obs {t_train:>2} seed {seed}] eval@{t_train} "
                  f"{r_own['rollout_mse']:.4e} | eval@"
                  f"{args.fixed_eval_tobs} {r_fix['rollout_mse']:.4e}",
                  flush=True)

    verdict, detail = classify_decouple(
        mses[8]["fixed"] if 8 in mses else [],
        mses[24]["fixed"] if 24 in mses else [])
    prefix_sensitivity = (mean(mses[8]["fixed"])
                          / max(mean(mses[8]["own"]), 1e-30)) \
        if 8 in mses else None
    sentinels = {
        "t24_train_eval24_seed0": {
            "expected": SENTINEL_T24,
            "actual": mses[24]["fixed"][0] if 24 in mses else None,
            "bitwise_match": (24 in mses
                              and mses[24]["fixed"][0] == SENTINEL_T24)},
        "t8_train_eval_own_seed0": {
            "expected": SENTINEL_T8,
            "actual": mses[8]["own"][0] if 8 in mses else None,
            "bitwise_match": (8 in mses
                              and mses[8]["own"][0] == SENTINEL_T8)}}
    results = {
        "arms": {f"t{t}_own": mses[t]["own"] for t in t_trains}
                | {f"t{t}_fixed": mses[t]["fixed"] for t in t_trains},
        "verdict": verdict,
        "verdict_detail": detail,
        "prefix_sensitivity_t8": {"ratio": prefix_sensitivity,
                                  "caliber": "mean(t8,eval@24)/"
                                             "mean(t8,eval@8), "
                                             "report-only"},
        "sentinels": sentinels,
        "criteria": {
            "c_diverged": verdict == "DEC_ARM_DIVERGED",
            "c_beneficial": verdict == "DEC_TRAIN_BENEFICIAL",
            "c_null": verdict == "DEC_TRAIN_NULL",
            "c_harmful": verdict == "DEC_TRAIN_HARMFUL"},
        "gates": {"beneficial_gate": BENEFICIAL_GATE,
                  "harm_gate": HARM_GATE, "norm_cap": NORM_CAP,
                  "seeds": list(SEEDS), "train_tobs": t_trains,
                  "fixed_eval_tobs": args.fixed_eval_tobs},
        "anchor": "t24/eval24 seed0 = 3.5582 (house default sentinel) + "
                  "t8/eval-own seed0 = 3.4044 (round-223 t8 arm)"},
    print(f"\nTOSA-CTX-DECOUPLE verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"sentinels t24={sentinels['t24_train_eval24_seed0']['bitwise_match']} "  # noqa: E501
          f"t8={sentinels['t8_train_eval_own_seed0']['bitwise_match']} | "
          f"prefix_sensitivity={prefix_sensitivity if prefix_sensitivity is None else round(prefix_sensitivity, 3)}",  # noqa: E501
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "tosa_decouple.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "tosa_decouple_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
