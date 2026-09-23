"""
benchmarks/sign_flip_probe.py — SIGN-FLIP-PROBE (round 126): locating the
recorded semigroup sign-reversal anomaly.

Preregistered in PRD §19 round 126 BEFORE execution. Round 113 (M1-CAP-AXIS)
recorded the open problem: 1/3 of seeds show a prefix-advantage SIGN REVERSAL
(r = mse_all2all/mse_prefix < 1), constant across the full capacity sweep
(seed 1 at every d_model). Scan §30.3 (Lubana et al., ICML 2023) supplies the
mechanism frame: tanh nets have SIGN SYMMETRY, so different seeds can land in
mechanistically distinct, sign-flipped basins. This probe decides between:

  BASIN_STABLE   anomaly reproduces, flips persist at 2x budget, flipped-seed
                 training losses comparable (<=2x) — equivalent solutions in
                 sign-flipped basins (screening-tier mechanism support).
  TRANSIENT      a flipped seed heals under 2x budget — training noise.
  MISFIT         flipped seeds train much worse (loss ratio > 2) — genuine
                 underfitting, not equivalent basins.
  NOT_REPRODUCED seed 1 does not flip at d48/2000 and no other seed flips —
                 downgrade to a one-off historical record.

Protocol mirrors d1b/cap-axis pool geometry exactly (run_one reuse — the d1b
lineage), d_model=48 fixed, seeds 0..7, 2000-step budget; reproduction anchor:
cap-axis d48 per-seed ratios [3.8938, 0.7019, 2.2884] (seed 0..2) must match
bitwise (run_one seeds the torch RNG internally). Diagnostic tier: multi-seed
FINALS stay PARKED per AMM-024.

Results JSON follows the audit schema: top-level "results" key required.
meta carries exec_tier passthrough from probe_run (PROBE_TIER env).
"""

import argparse
import json
import os
import sys
from argparse import Namespace

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.observability import run_metadata  # noqa: E402
from benchmarks.m1_semigroup_eval import gen_spring  # noqa: E402
from benchmarks.sample_efficiency_eval import run_one  # noqa: E402

# cap-axis d48 per-seed ratios (PRD §19 round 113; bitwise anchors)
ANCHORS_D48 = [3.893828710272355, 0.7019011657583599, 2.288356329861092]
LOSS_RATIO_GATE = 2.0


def base_args(d_model: int = 48, steps: int = 2000,
              eval_k: int = 100) -> Namespace:
    return Namespace(
        d_model=d_model, context_dim=8, n_scales=4, hidden=48, depth=2,
        dt=0.1, omega_lo=0.7, omega_hi=1.8, t_obs=24, k_train=8, eval_k=eval_k,
        eval_ks_list=[], train_steps=steps, lr=3e-3, lr_decay=1.0,
        batch=64, n_eval=128, gen_steps=160, device="cpu",
        two_stage=False, semigroup_frac=0.8, start_mix=0.0,
        start_mix_window=1, adaptive_sampling=False,
        probe_context=True, start_probe=False)


def run_pair(n_train, pool_qs, pool_ps, pool_om, seed, args):
    res_p = run_one("prefix", n_train, pool_qs, pool_ps, pool_om, seed, args)
    res_a = run_one("all2all", n_train, pool_qs, pool_ps, pool_om, seed, args)
    r = res_a["rollout_mse"] / res_p["rollout_mse"]
    return {"r": r, "flip": bool(r < 1.0),
            "mse_prefix": res_p["rollout_mse"],
            "mse_all2all": res_a["rollout_mse"],
            "train_loss_prefix": res_p["train_loss"],
            "train_loss_all2all": res_a["train_loss"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=32)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--seeds", default="0,1,2,3,4,5,6,7")
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--ext_steps", type=int, default=4000,
                    help="2x budget stability arm for flipped seeds")
    ap.add_argument("--max_stability", type=int, default=4,
                    help="preregistered cap: stability arm runs at most the "
                         "first N flipped seeds (worst-case T1 time bound; "
                         "flip FREQUENCY is still measured on all seeds)")
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--loss_ratio_gate", type=float, default=LOSS_RATIO_GATE,
                    help="preregistered c3 threshold (equivalent-solution "
                         "signature vs genuine misfit)")
    ap.add_argument("--device", default="cpu", help="cpu | cuda")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/sign_flip_probe")
    args_cli = ap.parse_args()

    seeds = [int(s) for s in args_cli.seeds.split(",")]
    print(f"SIGN-FLIP-PROBE | d_model {args_cli.d_model} x 2 loops x "
          f"seeds {seeds} (n_train {args_cli.n_train}, 2000-step budget, "
          f"diagnostic tier)", flush=True)

    per_seed = {}
    pool_cache = {}
    for seed in seeds:
        g = torch.Generator().manual_seed(seed)
        pool_qs, pool_ps, pool_om = gen_spring(
            max(64, args_cli.n_train) + args_cli.n_eval,
            args_cli.gen_steps, 0.1, 1, 0.7, 1.8, g)
        pool_cache[seed] = (pool_qs, pool_ps, pool_om)
        a = base_args(args_cli.d_model, steps=args_cli.train_steps,
                      eval_k=args_cli.eval_k)
        a.n_eval = args_cli.n_eval
        a.gen_steps = args_cli.gen_steps
        per_seed[seed] = run_pair(args_cli.n_train, pool_qs, pool_ps,
                                  pool_om, seed, a)
        print(f"  [seed {seed}] r={per_seed[seed]['r']:.4f} "
              f"{'FLIP' if per_seed[seed]['flip'] else 'ok'} "
              f"(mse_prefix {per_seed[seed]['mse_prefix']:.4e})", flush=True)

    # reproduction anchors (seeds 0..2, d48, 2000 steps): bitwise vs cap-axis
    anchor_diffs = [abs(per_seed[s]["r"] - ANCHORS_D48[i])
                    for i, s in enumerate(seeds[:3])
                    if s in (0, 1, 2)]
    bitwise = bool(anchor_diffs) and all(d == 0.0 for d in anchor_diffs)
    print(f"  reproduction anchor diffs: {anchor_diffs} | bitwise={bitwise}",
          flush=True)

    # stability arm: flipped seeds rerun at 2x budget (capped: first
    # max_stability flipped seeds — preregistered worst-case time bound)
    stability = {}
    for seed in [s for s in seeds if per_seed[s]["flip"]][:args_cli.max_stability]:
        a2 = base_args(args_cli.d_model, steps=args_cli.ext_steps,
                       eval_k=args_cli.eval_k)
        a2.n_eval = args_cli.n_eval
        a2.gen_steps = args_cli.gen_steps
        pool_qs, pool_ps, pool_om = pool_cache[seed]
        ext = run_pair(args_cli.n_train, pool_qs, pool_ps, pool_om, seed, a2)
        stability[seed] = ext
        print(f"  [seed {seed} @{args_cli.ext_steps}] r={ext['r']:.4f} "
              f"{'FLIP persists' if ext['flip'] else 'healed'}", flush=True)

    flips = [s for s in seeds if per_seed[s]["flip"]]
    seed1_flips = per_seed[seeds[0]]["flip"] if seeds[0] == 1 else \
        per_seed[1]["flip"] if 1 in per_seed else False
    others_flip = [s for s in flips if s != 1]
    loss_ratios = {s: per_seed[s]["train_loss_all2all"]
                   / max(per_seed[s]["train_loss_prefix"], 1e-12)
                   for s in flips}
    healed = [s for s, e in stability.items() if not e["flip"]]

    # Preregistered criteria (PRD §19 round 126) — mechanical.
    criteria = {
        "c1_not_reproduced": (not seed1_flips) and len(others_flip) == 0,
        "c2_transient": len(flips) > 0 and len(healed) > 0,
        "c3_misfit_confound": any(v > args_cli.loss_ratio_gate
                                  for v in loss_ratios.values()),
    }
    if criteria["c1_not_reproduced"]:
        verdict = "NOT_REPRODUCED"
    elif criteria["c2_transient"]:
        verdict = "TRANSIENT"
    elif criteria["c3_misfit_confound"]:
        verdict = "MISFIT"
    else:
        verdict = "BASIN_STABLE"
    results = {
        "per_seed": {str(s): per_seed[s] for s in seeds},
        "stability_arm_2x": {str(s): e for s, e in stability.items()},
        "flipped_seeds": flips,
        "flip_frequency": f"{len(flips)}/{len(seeds)}",
        "seed1_flips": seed1_flips,
        "anchor_diffs": anchor_diffs,
        "anchor_bitwise_match": bitwise,
        "loss_ratios_flipped": loss_ratios,
        "healed_seeds_2x": healed,
        "criteria": criteria,
        "gates": {"loss_ratio_gate": args_cli.loss_ratio_gate},
        "verdict_semantics": "BASIN_STABLE=reproduced+persistent+comparable "
                             "losses (sign-symmetry basins, screening-tier); "
                             "TRANSIENT=flip heals at 2x; MISFIT=flipped-seed "
                             "loss ratio above gate (genuine underfit); "
                             "NOT_REPRODUCED=no flip anywhere",
    }
    print(f"\nSIGN-FLIP-PROBE verdict {verdict} | flips {len(flips)}/"
          f"{len(seeds)} | criteria {criteria}", flush=True)

    os.makedirs(args_cli.out_dir, exist_ok=True)
    with open(os.path.join(args_cli.out_dir, "sign_flip_probe.json"),
              "w") as f:
        json.dump({"args": vars(args_cli),
                   "meta": run_metadata({
                       "benchmark": "sign_flip_probe",
                       "device": args_cli.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN", "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
