"""D1g (wave-10 round 18): one-step error as a FUNCTION of start time.

Preregistered in PRD §19 round 17 / paper-sketch §7 (coverage-density
argument). Retrains the D1c arms (prefix vs all2all, n ∈ {32,64},
3 seeds, identical budget), then sweeps the 1-step rollout start t0
across the whole trajectory (context still inferred from the fixed
t_obs prefix) and reports the error profile binned by t0.

Predictions under the coverage-density claim (P1):
  * prefix  : error notched low near the training window [0, t_obs+k),
              rising with arc distance;
  * all2all : flat for t0 >= t_obs (orbit-covered), behaviour unknown
              before t_obs (never a start for either loop).

Models are saved under --save_dir (default /tmp) and are NOT committed
(never-list: no .pt in git).

Usage:
    python benchmarks/start_time_sweep.py                 # 12 arms, ~9 min
    python benchmarks/start_time_sweep.py --sizes 32 --n_seeds 1  # smoke
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from awareliquid_physics.model import LiquidHamiltonianModel
from awareliquid_physics.observability import run_metadata
from awareliquid_physics.train import train_semigroup
from benchmarks.liquid_physics_eval import train as train_prefix
from benchmarks.m1_semigroup_eval import gen_spring


def time_bins(n_steps: int, n_bins: int):
    """Bin edges [t, t+1) over [0, n_steps): returns (edges, bin_of_t)."""
    edges = [round(i * n_steps / n_bins) for i in range(n_bins + 1)]
    edges[-1] = n_steps
    bin_of = [min(int(t * n_bins / n_steps), n_bins - 1) for t in range(n_steps)]
    return edges, bin_of


def sweep_profile(model, qs, ps, t_obs, edges, bin_of):
    """1-step rollout MSE binned by start time t0 (context from the fixed
    prefix). Returns per-bin mean error over all (trajectory, t) pairs."""
    model.eval()
    n = qs.shape[0]
    S = qs.shape[1]
    with torch.enable_grad():
        ctx = model.infer_context(qs[:, :t_obs], ps[:, :t_obs])
    errs = torch.zeros(S - 1)
    cnt = torch.zeros(S - 1)
    B = torch.arange(n)
    for t0 in range(S - 1):
        with torch.enable_grad():
            qs1, ps1 = model.rollout(qs[B, t0], ps[B, t0], ctx, 1)
        e = ((qs1.detach()[-1] - qs[B, t0 + 1]).pow(2).mean(dim=1)
             + (ps1.detach()[-1] - ps[B, t0 + 1]).pow(2).mean(dim=1))
        errs[t0] = e.mean()
        cnt[t0] = 1
    n_bins = len(edges) - 1
    prof = []
    for b in range(n_bins):
        lo, hi = edges[b], edges[b + 1]
        seg = errs[lo:max(hi, lo + 1)]
        prof.append(seg.mean().item() if seg.numel() else float("nan"))
    return prof


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sizes", default="32,64")
    ap.add_argument("--n_seeds", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=48)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--lr_decay", type=float, default=1.0)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--device", default="cpu", choices=["cpu"])
    ap.add_argument("--n_bins", type=int, default=16)
    ap.add_argument("--save_dir", default="/tmp/d1g_models")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/d1g_sweep")
    args = ap.parse_args()
    sizes = sorted(int(s) for s in args.sizes.split(","))

    os.makedirs(args.save_dir, exist_ok=True)
    os.makedirs(args.out_dir, exist_ok=True)
    results = {}
    for i in range(args.n_seeds):
        seed = args.seed + i
        g = torch.Generator().manual_seed(seed)
        pool_qs, pool_ps, _ = gen_spring(max(sizes) + args.n_eval,
                                         args.gen_steps, args.dt, 1,
                                         args.omega_lo, args.omega_hi, g,
                                         device=args.device)
        ev = slice(pool_qs.shape[0] - args.n_eval, None)
        edges, bin_of = time_bins(args.gen_steps, args.n_bins)
        for method in ("prefix", "all2all"):
            for n in sizes:
                torch.manual_seed(seed)
                model = LiquidHamiltonianModel(
                    1, d_model=args.d_model, context_dim=args.context_dim,
                    n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
                    dt=args.dt)
                tr = slice(0, n)
                if method == "all2all":
                    train_semigroup(model, pool_qs[tr], pool_ps[tr],
                                    args.t_obs, args.k_train,
                                    args.train_steps, args.lr, args.batch,
                                    seed, lr_decay=args.lr_decay)
                else:
                    train_prefix(model, pool_qs[tr], pool_ps[tr],
                                 args.t_obs, args.k_train,
                                 args.train_steps, args.lr, args.batch,
                                 seed, args.lr_decay)
                torch.save(model.state_dict(),
                           os.path.join(args.save_dir,
                                        f"{method}_n{n}_s{seed}.pt"))
                prof = sweep_profile(model, pool_qs[ev], pool_ps[ev],
                                     args.t_obs, edges, bin_of)
                results.setdefault(f"{method}_n{n}", {}) \
                       .setdefault(f"seed{seed}", {})["profile"] = prof
                print(f"[seed {seed}] {method:7s} n={n:>3}: profile "
                      f"{['%.1e' % p for p in prof]}", flush=True)

    # aggregate: mean profile across seeds per (method, n)
    agg = {}
    for key, seeds in results.items():
        profs = [v["profile"] for v in seeds.values()]
        agg[key] = {"bin_edges_t": edges,
                    "profile_mean": [sum(p[j] for p in profs) / len(profs)
                                     for j in range(len(profs[0]))],
                    **{f"profile_seed{i}": p
                       for i, p in enumerate(profs)}}
    with open(os.path.join(args.out_dir, "start_time_sweep.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({"benchmark": "start_time_sweep",
                                         "device": args.device}),
                   "results": agg}, f, indent=2)
    print(f"-> {os.path.join(args.out_dir, 'start_time_sweep.json')}",
          flush=True)


if __name__ == "__main__":
    main()
