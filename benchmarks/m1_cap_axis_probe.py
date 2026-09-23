"""
benchmarks/m1_cap_axis_probe.py — M1-CAP-AXIS (round 113, dir/m1-cap-axis).

Preregistered in PRD §19 round 113 BEFORE execution: does the prefix-vs-
all2all training gap on the n32 spring pool PERSIST across model capacity
(d_model), or is it a low-capacity artifact?

  r(dm) = mean_seeds MSE_all2all / mean_seeds MSE_prefix   (k=100 rollout)

Mirrors the d1b protocol CODE PATH exactly by reusing run_one from
sample_efficiency_eval (same pools-per-seed, same eval tail, same
probe_context diagnostic) — the strongest possible bridge to the d1b
anchor (r(48)=2.314, prefix_n32 mean=5.006, 3 seeds). Negative criteria
①-③ are preregistered in PRD §19. The d1b seed-level spread on all2all
([16.9, 2.9, 14.9]; 1/3 sign reversals — the recorded "sign stability"
open problem) is why 3 seeds are mandatory here: single-seed trends are
meaningless on this axis.

Results JSON follows the audit schema (top-level "results" key); meta
carries exec_tier passthrough from probe_run (PROBE_TIER env).
"""

import argparse
import json
import os
import sys
from argparse import Namespace

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from awareliquid_physics.observability import run_metadata
from benchmarks.m1_semigroup_eval import gen_spring
from benchmarks.sample_efficiency_eval import run_one

# d1b anchors (benchmarks/physics_out_v02/d1b_eval_depth, 3 seeds, seed 0-2)
D1B_R48 = 2.314
D1B_PREFIX48_MEAN = 5.006


def base_args(d_model: int, steps: int = 2000,
              eval_k: int = 100) -> Namespace:
    """d1b args (sample_efficiency_p11.json) with d_model varied.
    steps/eval_k overridable for smoke runs only (preregistered protocol
    values are the defaults)."""
    return Namespace(
        d_model=d_model, context_dim=8, n_scales=4, hidden=48, depth=2,
        dt=0.1, omega_lo=0.7, omega_hi=1.8, t_obs=24, k_train=8, eval_k=eval_k,
        eval_ks_list=[], train_steps=steps, lr=3e-3, lr_decay=1.0,
        batch=64, n_eval=128, gen_steps=160, device="cpu",
        two_stage=False, semigroup_frac=0.8, start_mix=0.0,
        start_mix_window=1, adaptive_sampling=False,
        probe_context=True, start_probe=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=32)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--d_models", default="24,48,96")
    ap.add_argument("--train_steps", type=int, default=2000,
                    help="preregistered budget is the 2000 default; smoke "
                         "runs may shrink it (round-84: smoke products are "
                         "schema/shape evidence only)")
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/m1_cap_axis")
    args_cli = ap.parse_args()

    seeds = [int(s) for s in args_cli.seeds.split(",")]
    d_models = [int(d) for d in args_cli.d_models.split(",")]
    print(f"M1-CAP-AXIS | d_model {d_models} x 2 loops x seeds {seeds} "
          f"(n_train {args_cli.n_train}, equal budget 2000 steps)", flush=True)

    # d1b pool geometry: 64+128 trajectories per seed -> training on the
    # first n_train=32 and evaluating on the fixed tail 128 means the
    # d_model=48/seed0 configs are EXACT replicas of d1b's same config
    # (strongest bridge; gate ① is near-bitwise for that point).
    pool_train = max(64, args_cli.n_train)
    grid = {}
    for seed in seeds:
        g = torch.Generator().manual_seed(seed)
        pool_qs, pool_ps, pool_om = gen_spring(
            pool_train + args_cli.n_eval, args_cli.gen_steps, 0.1, 1,
            0.7, 1.8, g)
        for dm in d_models:
            a = base_args(dm, steps=args_cli.train_steps,
                          eval_k=args_cli.eval_k)
            a.n_eval = args_cli.n_eval
            a.gen_steps = args_cli.gen_steps
            for method in ("prefix", "all2all"):
                res = run_one(method, args_cli.n_train, pool_qs, pool_ps,
                              pool_om, seed, a)
                grid.setdefault((dm, method), []).append(res)
                print(f"  [seed {seed}] d_model {dm:>3} {method:>7}: "
                      f"rollout_mse {res['rollout_mse']:.4e} "
                      f"(train_loss {res['train_loss']:.4e})", flush=True)

    def mean(dm, method, key="rollout_mse"):
        vals = [r[key] for r in grid[(dm, method)]]
        return sum(vals) / len(vals)

    results = {"by_config": {f"d{dm}_{m}": grid[(dm, m)]
                             for dm in d_models for m in ("prefix", "all2all")},
               "r_by_dmodel": {}}
    flip_counts = {}
    for dm in d_models:
        m_pre, m_all = mean(dm, "prefix"), mean(dm, "all2all")
        per_seed_r = [ra["rollout_mse"] / rp["rollout_mse"]
                      for ra, rp in zip(grid[(dm, "all2all")],
                                        grid[(dm, "prefix")])]
        flips = sum(1 for r in per_seed_r if r < 1.0)
        results["r_by_dmodel"][str(dm)] = {
            "mse_prefix_mean": m_pre, "mse_all2all_mean": m_all,
            "ratio": m_all / m_pre,
            "per_seed_ratio": per_seed_r, "sign_reversals": flips}
        flip_counts[str(dm)] = flips
        print(f"  d_model {dm:>3}: prefix {m_pre:.3e} | all2all {m_all:.3e} "
              f"| r = {m_all / m_pre:.2f} | reversals {flips}/{len(seeds)}",
              flush=True)

    r48 = results["r_by_dmodel"]["48"]["ratio"] if 48 in d_models else None
    p48 = (results["r_by_dmodel"]["48"]["mse_prefix_mean"]
           if 48 in d_models else None)
    r96 = results["r_by_dmodel"].get("96", {}).get("ratio")
    pre96 = results["r_by_dmodel"].get("96", {}).get("mse_prefix_mean")
    results["criteria"] = {
        # ① bridge to d1b anchors (×[0.5,2] and ×[0.67,1.5])
        "c1_bridge_broken": bool(
            r48 is not None and not (1.16 <= r48 <= 4.63)) or bool(
            p48 is not None and not (3.35 <= p48 <= 7.51)),
        # ② advantage vanishes at the top of the capacity axis
        "c2_low_capacity_artifact": bool(r96 is not None and r96 < 1.5),
        # ③ a run failed to train (non-finite loss / diverged prefix arm)
        "c3_training_failed": any(
            r["train_loss"] != r["train_loss"] or r["train_loss"] > 1e3
            for rs in grid.values() for r in rs) or bool(
            pre96 is not None and pre96 > 50),
    }
    results["gates"] = {"r48_bridge": [1.16, 4.63],
                        "prefix48_bridge": [3.35, 7.51],
                        "r96_gate": 1.5}
    results["sign_reversals_by_dmodel"] = flip_counts
    verdict = "PASS" if not any(results["criteria"].values()) else "NEGATIVE"
    print(f"\nM1-CAP-AXIS verdict {verdict} | criteria "
          f"{results['criteria']}", flush=True)

    os.makedirs(args_cli.out_dir, exist_ok=True)
    with open(os.path.join(args_cli.out_dir, "m1_cap_axis.json"), "w") as f:
        json.dump({"args": {"n_train": args_cli.n_train,
                            "n_eval": args_cli.n_eval,
                            "gen_steps": args_cli.gen_steps,
                            "seeds": seeds, "d_models": d_models,
                            "train_steps": args_cli.train_steps,
                            "eval_k": args_cli.eval_k, "device": "cpu",
                            "protocol": "run_one (d1b code path)"},
                   "meta": run_metadata({
                       "benchmark": "m1_cap_axis_probe", "device": "cpu",
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN", "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
