"""
benchmarks/genlen_probe.py — GENLEN-PROBE (round 255): training
trajectory length (t0-coverage) ladder, 3 seeds, on the M1 spring
family (E1 calibre).

Preregistered in PRD §19 round 254 BEFORE execution (AMM-027 distill
routing, self-generated scan family 56). Hook: the round-252
root-cause revision surfaced an accidental measurement — the DEFAULT
configuration trained on a longer trajectory pool (gen-301, residual
caliber) reached rollout MSE 2.9031 vs 3.5582 on the canonical pool,
same configuration same seed. The mechanism is NOT the data values
(round-252: first-161 steps bitwise identical across gen_steps) but
the training t0 sampling range: t0 ∈ [0, S - t_obs - k_train), so a
longer trajectory covers more start positions (D1g start-coverage
direction). This probe tests that signal directly.

Arms: training pools gen_steps ∈ {160, 301, 450} x 3 seeds (house
prefix train, canonical slices). ALL evaluation on the SAME canonical
held-out (gen-160, k=100) — only the training t0 range varies.
Sentinels: the 160-arm is the historical default path (seed 0 =
3.5581917762756348 bitwise); the 301-arm seed 0 must match
2.9031009674072266 (the residual_spec2 default arm, r246) — a free
cross-script replication anchor.

Mechanical verdict (preregistered, spread = max/min of 3-seed means):
  GENLEN_ARM_DIVERGED (negative) — any arm/seed non-finite or rollout
      > 1e6
  GENLEN_UNRESOLVABLE — spread < 1.05: start coverage saturated at the
      canonical length (the r246-era single reading attributed to
      single-seed noise, recorded as such)
  GENLEN_RESOLVED — spread >= 1.05: report the best training length
      and direction + D1g cross-reference; decision = house training
      trajectory length becomes a free configuration improvement
      (recipe 7th-axis candidate, back-propagation PR annotation
      upgrade)

Decision coupling (AMM-028 gate-1): the two outcomes change the house
training-length configuration decision (candidate upgrade / saturation
record). Family boundary: scan family 56 round 1 — distinct from the
D1 line (start redistribution WITHIN a fixed trajectory), LEN-EXTRAP
(evaluation extrapolation), KSPAN (rollout span). Results JSON follows
the audit schema (top-level "results" key); meta carries exec_tier
from probe_run.
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

NORM_CAP = 1e6   # preregistered: divergence threshold
SPREAD_GATE = 1.05  # preregistered: spread >= gate => resolved
SEEDS = (0, 1, 2)
SENTINEL_160 = 3.5581917762756348   # house default path arm seed 0
SENTINEL_301 = 2.9031009674072266   # residual_spec2 default arm s0 (r246)


def median(vals):
    s = sorted(vals)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def classify_genlen(mean_by_len, spread_gate: float = SPREAD_GATE,
                    cap: float = NORM_CAP):
    """Preregistered round-254 verdict (pure, test-pinned)."""
    for L, m in mean_by_len.items():
        if not math.isfinite(m) or m > cap:
            return "GENLEN_ARM_DIVERGED", {
                "reason": f"arm gen{L} mean non-finite/diverged ({m:.3e})"}
    lens = sorted(mean_by_len)
    spread = max(mean_by_len.values()) / max(min(mean_by_len.values()), 1e-30)
    best = min(mean_by_len, key=mean_by_len.get)
    stats = {"means": dict(mean_by_len), "spread": spread,
             "best_gen_steps": best}
    if spread < spread_gate:
        verdict = "GENLEN_UNRESOLVABLE"
        stats["decision"] = ("start coverage saturated at the canonical "
                             "length: the r246-era single reading "
                             "attributed to single-seed noise, recorded "
                             "as such")
    else:
        verdict = "GENLEN_RESOLVED"
        stats["decision"] = ("training trajectory length is a live "
                             "configuration variable: house training "
                             "length = free improvement candidate "
                             "(recipe 7th-axis candidate)")
    return verdict, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps_list", default="160,301,450")
    ap.add_argument("--eval_gen_steps", type=int, default=160)
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
                    default="benchmarks/physics_out_v02/genlen_probe")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]
    lens = sorted(int(x) for x in args.gen_steps_list.split(","))

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval,
                            args.eval_gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"GENLEN-PROBE | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} "
          f"steps={args.train_steps} train_len ladder={lens} "
          f"(seeds {seeds}; eval all on canonical held-out; round-254 "
          f"preregistration)", flush=True)

    mses = {L: [] for L in lens}
    for L in lens:
        gL = torch.Generator().manual_seed(0)
        qs_L, ps_L, _ = gen_spring(args.n_train + args.n_eval, L,
                                   args.dt, 1, args.omega_lo,
                                   args.omega_hi, gL, device=args.device)
        for seed in seeds:
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            train_prefix(model, qs_L[tr], ps_L[tr], args.t_obs,
                         args.k_train, args.train_steps, args.lr,
                         args.batch, seed)
            res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                           args.eval_k, args.dt)
            mses[L].append(res["rollout_mse"])
            print(f"  [gen {L:>3} seed {seed}] rollout MSE "
                  f"{res['rollout_mse']:.4e}", flush=True)

    mean_by_len = {L: sum(mses[L]) / len(seeds) for L in lens}
    verdict, detail = classify_genlen(mean_by_len)
    sentinels = {
        "arm160_seed0": {"expected": SENTINEL_160,
                         "actual": mses[160][0] if 160 in mses else None,
                         "bitwise_match": 160 in mses
                         and mses[160][0] == SENTINEL_160},
        "arm301_seed0_r246": {"expected": SENTINEL_301,
                              "actual": mses[301][0] if 301 in mses
                              else None,
                              "bitwise_match": 301 in mses
                              and mses[301][0] == SENTINEL_301}}
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "per_seed": {f"gen{L}": mses[L] for L in lens},
        "sentinels": sentinels,
        "criteria": {"c_diverged": verdict == "GENLEN_ARM_DIVERGED",
                     "c_unresolvable": verdict == "GENLEN_UNRESOLVABLE",
                     "c_resolved": verdict == "GENLEN_RESOLVED"},
        "gates": {"spread_gate": SPREAD_GATE, "norm_cap": NORM_CAP,
                  "seeds": list(seeds), "gen_steps_list": lens},
        "anchor": "arm160 s0 = 3.5582 (house default sentinel) + "
                  "arm301 s0 = 2.9031 (residual_spec2 r246 replication)"},
    print(f"\nGENLEN-PROBE verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"means={ {L: round(m, 4) for L, m in mean_by_len.items()} } | "
          f"sentinels={sentinels['arm160_seed0']['bitwise_match']}/"
          f"{sentinels['arm301_seed0_r246']['bitwise_match']}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "genlen_probe.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "genlen_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
