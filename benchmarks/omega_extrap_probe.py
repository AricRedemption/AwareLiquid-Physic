"""
benchmarks/omega_extrap_probe.py — OMEGA-EXTRAP (round 115, dir/omega-extrap).

Preregistered in PRD §19 round 115 BEFORE execution: quantify how the M1
arms degrade OUTSIDE the training omega band [0.7, 1.8], and whether the
hard-constraint structure mitigates that degradation.

  train (equal budget, seed 0):  liquid (ctx dim 8) + static (no ctx)
  eval pools (128 traj each):    in-band [0.7,1.8] anchor, low [0.3,0.6],
                                 high [1.9,2.2]
  primary metric:                D(arm, band) = MSE_band / MSE_inband
                                 (k=100 rollout MSE, q+p)
  ctx readout:                   closed-form least-squares omega decoder,
                                 fit on the in-band eval pool, applied
                                 per band (rel err + Pearson corr)

Negative criteria ①-③ are RELATIVE by design (round-74 rule: thresholds
from house anchors/contrast arms, not absolute magic numbers — no
out-of-band house precedent exists). Results JSON follows the audit
schema; meta carries exec_tier passthrough from probe_run.
"""

import argparse
import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.hamiltonian import HamiltonianHead
from awareliquid_physics.model import LiquidHamiltonianModel
from awareliquid_physics.observability import rollout_mse_stderr, run_metadata
from awareliquid_physics.train import train_semigroup
from benchmarks.m1_semigroup_eval import StaticHamWrapper, gen_spring


def make_pool(lo, hi, n, seed, gen_steps=160, dt=0.1):
    g = torch.Generator().manual_seed(seed)
    return gen_spring(n, gen_steps, dt, 1, lo, hi, g)


def rollout_mse(model, pool_qs, pool_ps, t_obs=24, eval_k=100):
    """k-step rollout MSE (q+p) from the t_obs prefix — house convention
    (m1_semigroup_eval / eval_rollout_mse)."""
    model.eval()
    q_obs, p_obs = pool_qs[:, :t_obs], pool_ps[:, :t_obs]
    with torch.enable_grad():
        qs_pred, ps_pred, _ = model(q_obs, p_obs, eval_k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    q_true = pool_qs[:, t_obs - 1: t_obs + eval_k].permute(1, 0, 2)
    p_true = pool_ps[:, t_obs - 1: t_obs + eval_k].permute(1, 0, 2)
    mse = ((qs_pred - q_true).pow(2).mean()
           + (ps_pred - p_true).pow(2).mean()).item()
    return mse, rollout_mse_stderr(qs_pred, q_true, ps_pred, p_true)


def ctx_decode(model, pool_qs, pool_ps, omegas, fit_ctx, fit_omega):
    """Closed-form least-squares omega decoder (fit on in-band ctx), applied
    to a pool. Returns mean relative decode error and Pearson corr."""
    model.eval()
    with torch.no_grad():
        ctx = model.infer_context(pool_qs[:, :24], pool_ps[:, :24])
        ctx = ctx.detach()
    w = torch.linalg.lstsq(fit_ctx, fit_omega.unsqueeze(-1))
    pred = (ctx @ w.solution).squeeze(-1)
    rel = ((pred - omegas).abs() / omegas.clamp_min(1e-6)).mean().item()
    corr = torch.corrcoef(torch.stack([pred, omegas]))[0, 1].item()
    return {"rel_err": rel, "corr": corr}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--hidden", type=int, default=48)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/omega_extrap")
    args = ap.parse_args()

    # training pool: house band, seed 0
    qs, ps, omega = make_pool(0.7, 1.8, args.n_train, args.seed,
                              args.gen_steps, args.dt)
    print(f"OMEGA-EXTRAP | train w~U[0.7,1.8] n={args.n_train} "
          f"steps={args.train_steps} seed={args.seed}; "
          f"eval bands in[0.7,1.8] low[0.3,0.6] high[1.9,2.2]", flush=True)

    arms = {}
    torch.manual_seed(args.seed)
    liquid = LiquidHamiltonianModel(1, d_model=args.d_model,
                                    context_dim=args.context_dim,
                                    n_scales=4, hidden_dim=args.hidden,
                                    depth=2, dt=args.dt)
    torch.manual_seed(args.seed)
    static = StaticHamWrapper(HamiltonianHead(1, hidden_dim=args.hidden,
                                              depth=2, context_dim=0),
                              args.dt)
    for name, model in (("liquid", liquid), ("static", static)):
        floss = train_semigroup(model, qs, ps, args.t_obs, args.k_train,
                                args.train_steps, args.lr, args.batch,
                                args.seed)
        arms[name] = model
        print(f"  [{name}] trained, loss {floss:.4e}", flush=True)

    # eval pools: in-band anchor + two out-of-band pools
    pools = {"in": make_pool(0.7, 1.8, args.n_eval, args.seed + 100,
                             args.gen_steps, args.dt),
             "low": make_pool(0.3, 0.6, args.n_eval, args.seed + 101,
                              args.gen_steps, args.dt),
             "high": make_pool(1.9, 2.2, args.n_eval, args.seed + 102,
                               args.gen_steps, args.dt)}

    results = {"mse_by_band": {}, "degradation_ratio": {}, "ctx_decode": {}}
    for name, model in arms.items():
        for band, (bqs, bps, _) in pools.items():
            mse, se = rollout_mse(model, bqs, bps, args.t_obs, args.eval_k)
            results["mse_by_band"].setdefault(name, {})[band] = mse
            results["mse_by_band"][name][f"{band}_stderr"] = se
        inb = results["mse_by_band"][name]["in"]
        for band in ("low", "high"):
            results["degradation_ratio"].setdefault(name, {})[band] = \
                results["mse_by_band"][name][band] / inb
        print(f"  [{name}] MSE in {results['mse_by_band'][name]['in']:.3e} "
              f"| low {results['mse_by_band'][name]['low']:.3e} "
              f"| high {results['mse_by_band'][name]['high']:.3e} "
              f"| D(low) {results['degradation_ratio'][name]['low']:.1f} "
              f"D(high) {results['degradation_ratio'][name]['high']:.1f}",
              flush=True)

    # ctx omega decoder: fit on in-band pool (liquid only has ctx)
    iq, ip, io = pools["in"]
    with torch.no_grad():
        fit_ctx = liquid.infer_context(iq[:, :24], ip[:, :24]).detach()
    results["ctx_decode"]["in"] = ctx_decode(liquid, iq, ip, io,
                                             fit_ctx, io)
    for band in ("low", "high"):
        bq, bp, bo = pools[band]
        results["ctx_decode"][band] = ctx_decode(liquid, bq, bp, bo,
                                                 fit_ctx, bo)
        print(f"  [ctx] decode {band}: rel_err "
              f"{results['ctx_decode'][band]['rel_err']:.3f} corr "
              f"{results['ctx_decode'][band]['corr']:.3f}", flush=True)

    dl, ds = results["degradation_ratio"]["liquid"], \
        results["degradation_ratio"]["static"]
    # Preregistered criteria ①-③ (PRD §19 round 115) — mechanical.
    results["criteria"] = {
        "c1_pipeline_failed": bool(
            any(v != v or v > 1e3 for v in
                results["mse_by_band"]["liquid"].values())
            or results["mse_by_band"]["liquid"]["in"]
            > 5 * results["mse_by_band"]["static"]["in"]),
        "c2_structure_amplifies_ood_risk": bool(
            dl["low"] >= 2 * ds["low"] and dl["high"] >= 2 * ds["high"]),
        "c3_near_band_collapse": bool(
            dl["low"] >= 100 or dl["high"] >= 100),
    }
    mitigates = bool(dl["low"] < ds["low"] and dl["high"] < ds["high"]
                     and results["ctx_decode"]["low"]["corr"] >= 0.8
                     and results["ctx_decode"]["high"]["corr"] >= 0.8)
    results["structure_mitigates_ood"] = mitigates
    verdict = "PASS" if not any(results["criteria"].values()) else "NEGATIVE"
    print(f"\nOMEGA-EXTRAP verdict {verdict} | criteria "
          f"{results['criteria']} | mitigates {mitigates}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "omega_extrap.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "omega_extrap_probe", "device": "cpu",
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN", "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
