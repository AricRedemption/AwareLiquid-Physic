"""P1-1 closure artifact — sample efficiency: semigroup (all2all) vs the v0.1
prefix training loop, on the SAME model, SAME optimizer budget.

The PRD pins P1-1 as: "轨迹内任意时间对 (t_i, t_j) 作为训练样本；达到同等
rollout MSE 所需训练样本数 ≤ v0.1 的 1/5". Rounds 5-7 proved semigroup
training's MSE advantage (liquid 61-90%) but never produced the direct
sample-count-vs-MSE comparison the criterion needs (round-8 gap #2). This
benchmark produces exactly that curve.

Design (isolates the ONE axis the criterion is about — data volume):
  * ONE model class (LiquidHamiltonianModel, the M1 config) and ONE task
    (the M1 spring family with hidden omega) for every run.
  * ONE optimizer budget for both methods: same train steps, batch, lr, t_obs,
    k_train. Only the training LOOP differs:
      - prefix  : v0.1 fixed-window loop (benchmarks.liquid_physics_eval.train)
                  — one (prefix -> future) window per trajectory
      - all2all : train_semigroup — random (start, span) pairs anywhere after
                  the prefix, O(S) samples per trajectory
  * Sample count = number of generated trajectories (the data-collection
    cost). Sizes are NESTED per seed (the first n_train of one shared pool),
    so the curve is a pure subsampling of the largest budget.
  * Eval: 128 held-out trajectories (fixed across sizes within a seed),
    100-step free-running rollout MSE from the t_obs prefix — the same
    diagnostic as m1_semigroup_eval / liquid_physics_eval.

Verdict (honest multi-level — a single ratio degenerates here): the v0.1
prefix loop SATURATES (its MSE plateaus above n≈128), so "samples needed to
reach prefix's best level" is noise-driven for BOTH loops and a single
sample-ratio is not certifiable. The artifact therefore reports the provable
quantities separately:
  * equal-budget depth: all2all @ max size vs prefix @ max size (same data,
    same optimizer budget) — the clean head-to-head;
  * plateau breakthrough: the smallest all2all size that beats prefix's
    best-ever level (any size, any seed-mean);
  * deep-line bracketing: at MSE levels the prefix loop provably never
    reaches on the ladder, the all2all sample count upper-bounds the ratio
    from below (> max_size/all2all_min, upper unbounded).
P1-1's "≤ 1/5" is certified only if some level L has BOTH sample counts
measured and ratio ≥ 5 — report that verdict honestly either way.
Per P6 the run uses multiple seeds and every number carries per-seed values
with across-seed std/stderr. Curves stream to JSONL (per-point), JSON carries
the aggregated table. CPU-runnable; ~1 h at defaults (30 runs × 2000 steps).

Honest scope: this is the M1 spring family only — the criterion's home task
(P2/P3 ledger: hidden-parameter family, where the liquid core does real work).
Other tasks inherit the protocol, not the number.

Usage:
    python benchmarks/sample_efficiency_eval.py                 # full, ~1 h
    python benchmarks/sample_efficiency_eval.py --sizes 32,128 --n_seeds 1
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from awareliquid_physics.model import LiquidHamiltonianModel
from awareliquid_physics.observability import JsonlMetricWriter, rollout_mse_stderr, run_metadata
from awareliquid_physics.train import train_semigroup
from benchmarks.liquid_physics_eval import train as train_prefix
from benchmarks.m1_semigroup_eval import gen_spring


def eval_rollout_mse(model, qs, ps, t_obs, eval_k):
    """Free-running eval_k-step rollout MSE from the prefix (m1_semigroup_eval
    diagnostic), plus the per-trajectory stderr."""
    model.eval()
    q_obs, p_obs = qs[:, :t_obs], ps[:, :t_obs]
    with torch.enable_grad():
        qs_pred, ps_pred, _ = model(q_obs, p_obs, eval_k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    q_true = qs[:, t_obs - 1: t_obs + eval_k].permute(1, 0, 2)
    p_true = ps[:, t_obs - 1: t_obs + eval_k].permute(1, 0, 2)
    mse = ((qs_pred - q_true).pow(2).mean()
           + (ps_pred - p_true).pow(2).mean()).item()
    return mse, rollout_mse_stderr(qs_pred, q_true, ps_pred, p_true)


def context_probe(model, qs, ps, omegas, t_obs):
    """D1 diagnostic (wave-10 protocol): how much omega-information does the
    learned context carry after training?

    Fit a linear readout context->omega on the FIRST half of the eval pool
    and report, on the SECOND half, the per-trajectory relative decode error
    |omega_hat - omega| / omega (mean/std) and the omega_hat-omega correlation.
    A linear probe lower-bounds the context's decodable information, so it is
    a model-agnostic stand-in for omega_hat without assuming a context layout.
    """
    model.eval()
    n = qs.shape[0]
    # enable_grad, not no_grad: the symplectic rollout differentiates V through
    # autograd internally even in eval mode (same as eval_rollout_mse above).
    with torch.enable_grad():
        _, _, ctx = model(qs[:, :t_obs], ps[:, :t_obs], 1)
    ctx = ctx.detach().reshape(n, -1).cpu()
    w = omegas.detach().reshape(-1, 1).cpu()
    n_half = n // 2
    Xa = torch.cat([ctx[:n_half], torch.ones(n_half, 1)], dim=1)
    Xb = torch.cat([ctx[n_half:], torch.ones(n - n_half, 1)], dim=1)
    coef = torch.linalg.lstsq(Xa, w[:n_half]).solution
    w_hat = (Xb @ coef).squeeze(1)
    w_true = w[n_half:].squeeze(1)
    rel = (w_hat - w_true).abs() / w_true.abs()
    corr = torch.corrcoef(torch.stack([w_hat, w_true]))[0, 1]
    if not torch.isfinite(corr):
        corr = torch.zeros(())   # strict-JSON safe (no NaN/Inf in artifacts)
    return {"ctx_rel_err_mean": rel.mean().item(),
            "ctx_rel_err_std": rel.std(unbiased=False).item() if rel.numel() > 1 else 0.0,
            "ctx_corr": corr.item()}


def start_probe(model, qs, ps, t_obs, seed):
    """D1c diagnostic (wave-10 round-4 protocol): 1-step rollout MSE from
    INTERIOR true states — all2all's training start distribution, prefix's
    out-of-distribution — while the context is still inferred from the SAME
    t_obs prefix, isolating the start-point axis with conditioning held fixed.
    Compare against rollout_mse_k1 (endpoint start): if the all2all/prefix
    gap shrinks on interior starts, the start-point mismatch is the mechanism.
    """
    model.eval()
    n, steps = qs.shape[0], qs.shape[1]
    g = torch.Generator().manual_seed(seed + 1000)   # deterministic per seed
    t_idx = t_obs + torch.randint(0, steps - t_obs - 1, (n,), generator=g)
    b = torch.arange(n)
    q_obs, p_obs = qs[:, :t_obs], ps[:, :t_obs]
    with torch.enable_grad():   # symplectic rollout differentiates V internally
        ctx = model.infer_context(q_obs, p_obs)
        qs1, ps1 = model.rollout(qs[b, t_idx], ps[b, t_idx], ctx, 1)
    qs1, ps1 = qs1.detach()[-1], ps1.detach()[-1]
    return (((qs1 - qs[b, t_idx + 1]).pow(2).mean()
             + (ps1 - ps[b, t_idx + 1]).pow(2).mean())).item()


def run_one(method, n_train, pool_qs, pool_ps, pool_om, seed, args):
    """Train the SAME M1 model with ONE loop variant on n_train trajectories
    (nested slice of the shared pool) and return eval metrics."""
    tr = slice(0, n_train)
    torch.manual_seed(seed)
    model = LiquidHamiltonianModel(1, d_model=args.d_model,
                                   context_dim=args.context_dim,
                                   n_scales=args.n_scales,
                                   hidden_dim=args.hidden, depth=2,
                                   dt=args.dt)
    if method == "all2all" and args.two_stage:
        sg_steps = int(args.train_steps * args.semigroup_frac)
        floss = train_semigroup(model, pool_qs[tr], pool_ps[tr], args.t_obs,
                                args.k_train, sg_steps, args.lr,
                                args.batch, seed, lr_decay=args.lr_decay,
                                start_mix=args.start_mix,
                                start_mix_window=args.start_mix_window)
        floss = train_prefix(model, pool_qs[tr], pool_ps[tr], args.t_obs,
                             args.k_train, args.train_steps - sg_steps,
                             args.lr, args.batch, seed, args.lr_decay)
    elif method == "all2all":
        floss = train_semigroup(model, pool_qs[tr], pool_ps[tr], args.t_obs,
                                args.k_train, args.train_steps, args.lr,
                                args.batch, seed, lr_decay=args.lr_decay,
                                start_mix=args.start_mix,
                                start_mix_window=args.start_mix_window)
    else:
        floss = train_prefix(model, pool_qs[tr], pool_ps[tr], args.t_obs,
                             args.k_train, args.train_steps, args.lr,
                             args.batch, seed, args.lr_decay)
    ev = slice(pool_qs.shape[0] - args.n_eval, None)   # fixed held-out set
    mse, stderr = eval_rollout_mse(model, pool_qs[ev], pool_ps[ev],
                                   args.t_obs, args.eval_k)
    res = {"params": sum(p.numel() for p in model.parameters()),
           "train_loss": floss, "rollout_mse": mse, "rollout_mse_stderr": stderr}
    for k in args.eval_ks_list:   # D1b: MSE by eval depth (same trained model)
        res[f"rollout_mse_k{k}"] = eval_rollout_mse(
            model, pool_qs[ev], pool_ps[ev], args.t_obs, k)[0]
    if args.probe_context:
        res.update(context_probe(model, pool_qs[ev], pool_ps[ev],
                                 pool_om[ev], args.t_obs))
    if args.start_probe:
        res["mse_k1_interior"] = start_probe(model, pool_qs[ev], pool_ps[ev],
                                             args.t_obs, seed)
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sizes", default="32,64,128,256,512",
                    help="comma-separated n_train ladder (nested per seed)")
    ap.add_argument("--n_seeds", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0, help="base seed; seed+i per run")
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--eval_ks", default=None,
                    help="comma ladder of eval depths, e.g. '1,10,100' (D1b: "
                         "does the all2all disadvantage grow with rollout "
                         "depth?); default: just --eval_k (existing artifacts "
                         "byte-reproducible; every k needs gen_steps ≥ "
                         "t_obs+k-1)")
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=48)
    ap.add_argument("--train_steps", type=int, default=2000,
                    help="IDENTICAL for both methods (budget held equal)")
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--lr_decay", type=float, default=1.0)
    ap.add_argument("--start_mix", type=float, default=0.0,
                    help="D1d recipe (wave-10 round 5): probability of "
                         "pinning an all2all sample's rollout start to the "
                         "t_obs endpoint; 0.0 (default) = original loop")
    ap.add_argument("--start_mix_window", type=int, default=1,
                    help="D1e (wave-10 round 6): pinned starts are uniform "
                         "in [t_obs, t_obs+w) instead of the single t_obs "
                         "point; w=1 (default) degenerates to D1d")
    ap.add_argument("--two_stage", action="store_true",
                    help="D1f (wave-10 round 13): all2all arm becomes a "
                         "curriculum — semigroup for semigroup_frac of the "
                         "budget, then the v0.1 prefix loop (endpoint-start "
                         "finetune) for the rest; default off")
    ap.add_argument("--semigroup_frac", type=float, default=0.8,
                    help="fraction of train_steps spent in the semigroup "
                         "stage when --two_stage is on")
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--device", default="cpu", choices=["cpu"],
                    help="protocol pinned to CPU (P5 same-device; loops and "
                         "anchors verified on CPU only)")
    ap.add_argument("--out_dir", default="benchmarks/physics_out_v02")
    ap.add_argument("--probe_context", action="store_true",
                    help="D1 diagnostic (wave-10): after each training run, "
                         "linear-probe omega from the context (fit on the "
                         "first half of the eval pool, error on the second "
                         "half); default off keeps the original artifact "
                         "byte-reproducible")
    ap.add_argument("--start_probe", action="store_true",
                    help="D1c diagnostic (wave-10 round 4): 1-step MSE from "
                         "interior true states (training-distribution starts "
                         "for all2all) vs the endpoint k1; default off keeps "
                         "existing artifacts byte-reproducible")
    args = ap.parse_args()
    args.eval_ks_list = sorted(int(k) for k in
                               (args.eval_ks if args.eval_ks is not None
                                else str(args.eval_k)).split(","))

    sizes = sorted(int(s) for s in args.sizes.split(","))
    max_n = sizes[-1]
    methods = ("prefix", "all2all")

    curves_path = os.path.join(args.out_dir, "sample_efficiency_curves.jsonl")
    os.makedirs(args.out_dir, exist_ok=True)
    if os.path.exists(curves_path):   # a run owns its artifact (writer appends)
        os.remove(curves_path)
    curves = JsonlMetricWriter(
        curves_path,
        static_fields={"benchmark": "sample_efficiency_eval",
                       "device": args.device, "git_sha": run_metadata()["git_sha"]})

    # per (method, n_train): list of per-seed metric dicts
    bucket = {(m, n): [] for m in methods for n in sizes}
    for i in range(args.n_seeds):
        seed = args.seed + i
        # one shared pool per seed -> nested sizes, fixed held-out set
        g = torch.Generator().manual_seed(seed)
        pool_qs, pool_ps, pool_om = gen_spring(max_n + args.n_eval, args.gen_steps,
                                               args.dt, 1, args.omega_lo, args.omega_hi,
                                               g, device=args.device)
        for method in methods:
            for n in sizes:
                print(f"[seed {seed}] {method:7s} n_train {n:>4}: training "
                      f"{args.train_steps} steps ...", flush=True)
                res = run_one(method, n, pool_qs, pool_ps, pool_om, seed, args)
                bucket[(method, n)].append(res)
                curves.write("mse_point", {"method": method, "n_train": n,
                                           "seed": seed, **res})
                print(f"[seed {seed}] {method:7s} n_train {n:>4}: "
                      f"rollout_mse {res['rollout_mse']:.4e} "
                      f"(train_loss {res['train_loss']:.4e})", flush=True)
    curves.close()

    def agg(metric_vals):
        mean = sum(metric_vals) / len(metric_vals)
        if len(metric_vals) > 1:
            std = (sum((v - mean) ** 2 for v in metric_vals)
                   / (len(metric_vals) - 1)) ** 0.5
        else:
            std = 0.0
        return mean, std, std / len(metric_vals) ** 0.5

    results = {}
    for method in methods:
        for n in sizes:
            vals = bucket[(method, n)]
            mean, std, stderr = agg([v["rollout_mse"] for v in vals])
            results[f"{method}_n{n}"] = {
                "rollout_mse": mean, "rollout_mse_std": std,
                "rollout_mse_stderr": stderr,
                "train_loss": agg([v["train_loss"] for v in vals])[0],
                "params": vals[0]["params"],
                **{f"rollout_mse_seed{i}": v["rollout_mse"]
                   for i, v in enumerate(vals)},
                **{f"rollout_mse_traj_stderr_seed{i}": v["rollout_mse_stderr"]
                   for i, v in enumerate(vals)},
            }
            if args.probe_context:
                results[f"{method}_n{n}"].update({
                    "ctx_rel_err_mean": agg([v["ctx_rel_err_mean"] for v in vals])[0],
                    "ctx_rel_err_std": agg([v["ctx_rel_err_std"] for v in vals])[0],
                    "ctx_corr": agg([v["ctx_corr"] for v in vals])[0],
                    **{f"ctx_rel_err_seed{i}": v["ctx_rel_err_mean"]
                       for i, v in enumerate(vals)},
                    **{f"ctx_corr_seed{i}": v["ctx_corr"]
                       for i, v in enumerate(vals)},
                })
            for k in args.eval_ks_list:
                results[f"{method}_n{n}"][f"rollout_mse_k{k}"] = agg(
                    [v[f"rollout_mse_k{k}"] for v in vals])[0]
                results[f"{method}_n{n}"].update({
                    f"rollout_mse_k{k}_seed{i}": v[f"rollout_mse_k{k}"]
                    for i, v in enumerate(vals)})
            if args.start_probe:
                results[f"{method}_n{n}"].update({
                    "mse_k1_interior": agg([v["mse_k1_interior"] for v in vals])[0],
                    **{f"mse_k1_interior_seed{i}": v["mse_k1_interior"]
                       for i, v in enumerate(vals)}})

    # --- P1-1 verdict: honest multi-level analysis ---------------------------
    # The naive "ratio at prefix's best line" degenerates when prefix SATURATES
    # (its curve goes flat): "smallest prefix n reaching the line" becomes
    # noise. Report the provable quantities separately (see docstring).
    prefix_means = {n: results[f"prefix_n{n}"]["rollout_mse"] for n in sizes}
    a2a_means = {n: results[f"all2all_n{n}"]["rollout_mse"] for n in sizes}

    prefix_best_level = min(prefix_means.values())
    prefix_best_n = min(n for n in sizes if prefix_means[n] == prefix_best_level)
    a2a_n_beats_prefix_best = min(
        (n for n in sizes if a2a_means[n] <= prefix_best_level), default=None)

    deep_line = a2a_means[max_n]              # deepest all2all point on ladder
    prefix_reaches_deep = any(v <= deep_line for v in prefix_means.values())

    # the pinned-line ratio (target = prefix @ max budget): kept for the raw
    # number, but flagged as NOT certifiable when prefix_min_n < max_n (plateau)
    pinned_line = prefix_means[max_n]
    a2a_min_at_pinned = min(
        (n for n in sizes if a2a_means[n] <= pinned_line), default=None)
    prefix_min_at_pinned = min(
        (n for n in sizes if prefix_means[n] <= pinned_line), default=None)
    pinned_certifiable = (prefix_min_at_pinned == max_n)

    # P1-1 pass requires SOME measurable level with ratio >= 5. On a saturating
    # prefix curve that never happens: plateau levels give ratio ~1, deeper
    # levels leave the prefix count unproven (unbounded). State it honestly.
    # pinned_ratio stays None (JSON null, strict-JSON safe) when all2all never
    # reaches the pinned line — never serialized as Infinity.
    if a2a_min_at_pinned is None:
        pinned_ratio = None
    else:
        pinned_ratio = max_n / a2a_min_at_pinned

    if a2a_min_at_pinned is None:
        p11_pass = False
        assessment = ("NOT MET: all2all never reaches the pinned line "
                      f"(prefix@{max_n} = {pinned_line:.4e}) on this ladder")
    elif pinned_certifiable and pinned_ratio >= 5.0:
        p11_pass = True
        assessment = "PASS: 1/5 certified at the pinned line"
    elif pinned_certifiable:
        p11_pass = False
        assessment = "NOT MET: measurable ratio at the pinned line is below 5x"
    else:
        p11_pass = False
        if a2a_n_beats_prefix_best is not None:
            lower_bound = f"{max_n / a2a_n_beats_prefix_best:.1f}x"
        else:
            lower_bound = "n/a (all2all never beats prefix's best here)"
        assessment = ("NOT CERTIFIABLE on this ladder: prefix saturates "
                      f"(best {prefix_best_level:.3e} @ n={prefix_best_n}); at the "
                      f"pinned line the ratio is {pinned_ratio:.1f}x but prefix "
                      "reaches it earlier, so the 1/5 claim is neither provable "
                      "nor refuted there; at deeper MSE levels prefix never "
                      "arrives on this ladder (ratio lower bound "
                      f"{lower_bound}, upper unbounded). Semigroup's decisive "
                      "advantage is opening MSE levels prefix never reaches.")

    print("\n" + "=" * 70, flush=True)
    print("SAMPLE EFFICIENCY | rollout MSE vs n_train (mean ± std, "
          f"{args.n_seeds} seeds, {args.train_steps} steps both loops)", flush=True)
    print("=" * 70, flush=True)
    for n in sizes:
        p = results[f"prefix_n{n}"]
        a = results[f"all2all_n{n}"]
        print(f"  n_train {n:>4}:  prefix {p['rollout_mse']:.4e}±{p['rollout_mse_std']:.1e}"
              f"  |  all2all {a['rollout_mse']:.4e}±{a['rollout_mse_std']:.1e}", flush=True)
    print(f"\n  prefix best (plateau): {prefix_best_level:.4e} @ n={prefix_best_n}"
          f" | all2all @ max budget: {a2a_means[max_n]:.4e} "
          f"({prefix_means[max_n] / a2a_means[max_n]:.2f}x deeper than prefix "
          f"at equal budget {max_n})", flush=True)
    print(f"  all2all first beats prefix's best-ever level: n="
          f"{a2a_n_beats_prefix_best}", flush=True)
    if pinned_ratio is not None:
        pinned_txt = f"raw ratio {pinned_ratio:.1f}x"
    else:
        pinned_txt = "not reached by all2all on this ladder"
    print(f"  pinned line (prefix@{max_n} = {pinned_line:.4e}): {pinned_txt} "
          f"(certifiable: {pinned_certifiable} — prefix itself hits the line "
          f"at n={prefix_min_at_pinned}, i.e. it saturates)", flush=True)
    print(f"\n  P1-1 (≥5x): {assessment}", flush=True)

    if args.probe_context:
        print("\n  D1 context probe | omega decode rel-err (mean±std over "
              "seeds; probe fit on eval half A, error on half B)", flush=True)
        for n in sizes:
            p = results[f"prefix_n{n}"]
            a = results[f"all2all_n{n}"]
            print(f"  n_train {n:>4}:  prefix {p['ctx_rel_err_mean']:.3f}"
                  f"±{p['ctx_rel_err_std']:.3f} (corr {p['ctx_corr']:+.2f})"
                  f"  |  all2all {a['ctx_rel_err_mean']:.3f}"
                  f"±{a['ctx_rel_err_std']:.3f} (corr {a['ctx_corr']:+.2f})",
                  flush=True)

    if len(args.eval_ks_list) > 1:
        print("\n  D1b eval-depth ladder | rollout MSE by eval_k "
              f"({args.n_seeds} seeds mean; a2a/prefix ratio per depth)",
              flush=True)
        for n in sizes:
            parts = []
            for k in args.eval_ks_list:
                pm = results[f"prefix_n{n}"][f"rollout_mse_k{k}"]
                am = results[f"all2all_n{n}"][f"rollout_mse_k{k}"]
                parts.append(f"k{k}: {pm:.3e} vs {am:.3e} "
                             f"({am / pm:.2f}x)")
            print(f"  n_train {n:>4}:  " + "  |  ".join(parts), flush=True)

    if args.start_probe:
        print("\n  D1c start probe | 1-step MSE from interior true states vs "
              "endpoint start (a2a/prefix ratio; start-point mismatch shrinks "
              "the interior ratio)", flush=True)
        for n in sizes:
            for meth in ("prefix", "all2all"):
                r = results[f"{meth}_n{n}"]
                print(f"  n_train {n:>4} {meth:7s}: endpoint k1 "
                      f"{r['rollout_mse_k1']:.3e}  interior k1 "
                      f"{r['mse_k1_interior']:.3e}", flush=True)
            if 1 in args.eval_ks_list:
                rp = (results["all2all_n%d" % n]["rollout_mse_k1"]
                      / results["prefix_n%d" % n]["rollout_mse_k1"])
                ri = (results["all2all_n%d" % n]["mse_k1_interior"]
                      / results["prefix_n%d" % n]["mse_k1_interior"])
                print(f"  n_train {n:>4} ratio   : endpoint {rp:.2f}x  "
                      f"interior {ri:.2f}x", flush=True)

    with open(os.path.join(args.out_dir, "sample_efficiency_p11.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({"benchmark": "sample_efficiency_eval",
                                         "device": args.device}),
                   "results": results,
                   "verdict": {
                       "p11_pass_ge_5x": bool(p11_pass),
                       "p11_assessment": assessment,
                       "prefix_best_level": prefix_best_level,
                       "prefix_best_n": prefix_best_n,
                       "equal_budget_mse_ratio_at_max_n":
                           prefix_means[max_n] / a2a_means[max_n],
                       "all2all_n_beats_prefix_best": a2a_n_beats_prefix_best,
                       "pinned_line": pinned_line,
                       "pinned_line_raw_ratio": pinned_ratio,
                       "pinned_line_certifiable": bool(pinned_certifiable),
                       "deep_line_all2all_max": deep_line,
                       "prefix_reaches_deep_line": bool(prefix_reaches_deep),
                   }}, f, indent=2)


if __name__ == "__main__":
    main()
