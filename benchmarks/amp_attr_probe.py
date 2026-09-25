"""
benchmarks/amp_attr_probe.py — AMP-ATTR (round 244): linearity-
equivariance attribution on the M1 spring family (E1 calibre).

Preregistered in PRD §19 round 242 BEFORE execution (AMM-027 pool
routing: round 216/217 flagged "线性不变性未被继承深层读数=可检测
机制线索" as the AMPLITUDE-family follow-up). Round 216 measured the
SYMPTOM (AMPEX_DEGRADES: rel_comp=4.08 — the model does not inherit
the exact scaling equivariance of the linear oscillator, where scaling
initial conditions by s scales the exact solution by s and leaves
omega unchanged). This probe attributes the nonlinearity to a LAYER:

  ① ctx invariance   — infer_context(s·prefix) vs infer_context(prefix),
    relative diff, s ∈ {2, 4}. Ideal 0: the physical latent (omega) is
    amplitude-invariant, so a faithful inference head returns the same
    context. Violation => inference-layer nonlinearity.
  ② head equivariance — with the SAME forced context (the scale-1
    inferred ctx), rollout(s·s0, ctx) vs s·rollout(s0, ctx), relative
    error, s ∈ {2, 4}. Ideal 0 for an equivariant head. Violation =>
    dynamics-head nonlinearity.
  ③ attribution      — relative magnitude of ② vs ① decides the primary
    carrier (head / ctx / mixed).

Report-only verdict (RESIDUAL-SPEC precedent — no pass/fail gate):
  AMPATTR_OK — all diagnostics finite (report delivered)
  AMPATTR_UNRESOLVABLE (negative, preregistered round-242 判负) — any
      diagnostic non-finite or computation anomalous

Calibers: relative errors are RMS(s·R1 − Rs) / RMS(s·R1) over the full
rollout tensor, median across the 128 held-out trajectories; ctx diff
is ‖ctx_s − ctx_1‖₂ / ‖ctx_1‖₂ per trajectory, median across
trajectories. Decision coupling (AMM-028 gate-1): head-attributed =>
head-equivariance candidate annotation (architecture-line parking);
ctx-attributed => converges with round-239 (ctx does not carry omega)
+ round-241 (prefix-length brittleness) into the system-level
"inference head is the primary bias carrier" mechanism sentence;
mixed => both noted. Family boundary: AMPLITUDE family in-segment
round 2 of 2 — family closes after this. Sentinel: the training arm is
the house default — seed 0 standard eval must match 3.5581917762756348
bit-for-bit. Results JSON follows the audit schema (top-level
"results" key); meta carries exec_tier from probe_run.
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

SENTINEL = 3.5581917762756348  # house default seed 0 (round-181 clause)
SCALES = (2, 4)                # preregistered: round-216 scale grid


def rms(t):
    return torch.sqrt((t ** 2).mean()).item()


def median(vals):
    s = sorted(vals)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def ctx_invariance(model, qs, ps, t_obs, scale):
    """① relative ctx diff between scaled and raw prefix, per
    trajectory -> median. Ideal 0 (omega is amplitude-invariant)."""
    with torch.enable_grad():
        c1 = model.infer_context(qs[:, :t_obs], ps[:, :t_obs]).detach()
        cs = model.infer_context(scale * qs[:, :t_obs],
                                 scale * ps[:, :t_obs]).detach()
    d = torch.norm(cs - c1, dim=1) / torch.norm(c1, dim=1).clamp_min(1e-30)
    vals = [v for v in d.tolist()]
    if not all(math.isfinite(v) for v in vals):
        return {"median": float("nan"), "per_traj": vals}
    return {"median": median(vals), "per_traj": vals}


def head_equivariance(model, qs, ps, t_obs, k, scale):
    """② forced-ctx rollout equivariance error, per trajectory ->
    median. Ideal 0 for a linear-equivariant head."""
    with torch.enable_grad():
        ctx = model.infer_context(qs[:, :t_obs], ps[:, :t_obs]).detach()
        q0 = qs[:, t_obs - 1]
        p0 = ps[:, t_obs - 1]
        r1_q, r1_p = model.rollout(q0, p0, ctx, k)
        rs_q, rs_p = model.rollout(scale * q0, scale * p0, ctx, k)
    num_q = rms(scale * r1_q - rs_q)
    den_q = rms(scale * r1_q) + 1e-30
    num_p = rms(scale * r1_p - rs_p)
    den_p = rms(scale * r1_p) + 1e-30
    err = (num_q / den_q + num_p / den_p) / 2
    return {"value": err, "finite": math.isfinite(err)}


def classify_ampattr(ctx_res, head_res):
    """Preregistered round-242 verdict (pure, test-pinned)."""
    for tag, d in (("ctx", ctx_res), ("head", head_res)):
        for s in d:
            v = d[s].get("median", d[s].get("value"))
            if not math.isfinite(v):
                return "AMPATTR_UNRESOLVABLE", {
                    "reason": f"{tag} s={s} diagnostic non-finite "
                              f"({v}): preregistered negative branch"}
    return "AMPATTR_OK", {
        "attribution_rule": "primary carrier = larger of head-equivariance "
                            "error vs ctx-invariance diff (relative "
                            "magnitudes, per preregistered round-242 "
                            "decomposition)"}


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
    ap.add_argument("--k_train", type=int, default=8)
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
                    default="benchmarks/physics_out_v02/amp_attr")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"AMP-ATTR | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} steps={args.train_steps} "
          f"scales={list(SCALES)} (seeds {seeds}; round-242 "
          f"preregistration, report-only attribution)", flush=True)

    per_seed = []
    for seed in seeds:
        torch.manual_seed(seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
            dt=args.dt)
        train_prefix(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                     args.train_steps, args.lr, args.batch, seed)
        res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                       args.eval_k, args.dt)
        ctx_res = {s: ctx_invariance(model, qs[ev], ps[ev], args.t_obs, s)
                   for s in SCALES}
        head_res = {s: head_equivariance(model, qs[ev], ps[ev],
                                         args.t_obs, args.eval_k, s)
                    for s in SCALES}
        per_seed.append({"seed": seed,
                         "rollout_mse": res["rollout_mse"],
                         "ctx_invariance": ctx_res,
                         "head_equivariance": head_res})
        c2 = ctx_res[2]["median"]; c4 = ctx_res[4]["median"]
        h2 = head_res[2]["value"]; h4 = head_res[4]["value"]
        print(f"  [seed {seed}] MSE {res['rollout_mse']:.4e} | "
              f"ctx-diff s2 {c2:.3f} s4 {c4:.3f} | head-err s2 {h2:.3f} "
              f"s4 {h4:.3f}", flush=True)

    ctx_agg = {s: median([p["ctx_invariance"][s]["median"]
                          for p in per_seed]) for s in SCALES}
    head_agg = {s: median([p["head_equivariance"][s]["value"]
                           for p in per_seed]) for s in SCALES}
    verdict, detail = classify_ampattr(
        {s: {"median": ctx_agg[s]} for s in SCALES},
        {s: {"value": head_agg[s]} for s in SCALES})
    sentinels = {"arm_seed0": {
        "expected": SENTINEL, "actual": per_seed[0]["rollout_mse"],
        "bitwise_match": per_seed[0]["rollout_mse"] == SENTINEL}}
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "attribution": {
            "ctx_invariance_median_by_scale": ctx_agg,
            "head_equivariance_median_by_scale": head_agg,
            "primary_carrier": ("head" if head_agg[2] > ctx_agg[2]
                                else "ctx"),
            "caliber": "medians across seeds of per-seed medians across "
                       "trajectories; relative RMS calibers, report-only"},
        "per_seed": per_seed,
        "sentinels": sentinels,
        "criteria": {"c_ok": verdict == "AMPATTR_OK",
                     "c_unresolvable": verdict == "AMPATTR_UNRESOLVABLE"},
        "anchor": "training arm = house default; seed 0 eval expected "
                  "3.5582 (rounds 175/191/223/226 sentinel)"}
    print(f"\nAMP-ATTR verdict {verdict} | primary="
          f"{results['attribution']['primary_carrier']} | "
          f"sentinel={sentinels['arm_seed0']['bitwise_match']}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "amp_attr.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "amp_attr_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
