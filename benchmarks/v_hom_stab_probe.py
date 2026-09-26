"""
benchmarks/v_hom_stab_probe.py — V-HOM-STAB (round 268): magnitude-
direction decoupling of the homogeneous-V head (direction channel
removed), 3 seeds, M1 spring family (E1 caliber). Scan family 54
in-segment round 3 (new marathon segment; round-65 conditional entry
triggered, family quota reset; entry = round-261 verdict row + scan
§57).

Round-261 context: homogeneous V = ‖q‖²·s_θ(q̂, ctx) showed a strong
mechanism signal (seed 1 rel_comp 1.443 near-perfect scale-equivariant
recovery) blocked by training catastrophe on seeds 0/2 (MSE 2456.6 /
701.8 vs healthy ~2.4-2.8). Preregistered mechanism refinement (this
round, BEFORE execution): in dim=1, q̂ = q/‖q‖ = sign(q) is BINARY and
its end-to-end autograd Jacobian is exactly 0 away from q=0 (numerator
|q| − q·sign(q) vanishes bit-exactly), so a gradient-level detach
decoupling would be a NO-OP (arms bitwise identical). The pathology is
the discontinuous FEATURE: q̂ flips ±1 at every zero crossing, so the
represented V is discontinuous at q=0 unless s(+1, ctx) = s(−1, ctx)
— nothing enforces that, asymmetric sides give a V-kick at q=0 and the
rollout loss explodes (matches the round-261 bimodal pattern). In 1-D,
a CONTINUOUS degree-2-homogeneous V is direction-free by necessity.

Single variable (preregistered round 268): full decoupling of the
direction channel (the 1-D executable form of the scan §57.1
magnitude-direction decoupling) —
  arm REF  = round-261 arm-B construction, V = ‖q‖²·s_θ(q̂, ctx)
             (direction input, discontinuous; unstable reference);
  arm STAB = V = ‖q‖²·s_θ(0, ctx) (direction channel pinned to zero:
             exactly degree-2 homogeneous — V(λq) = λ²V(q), even in q,
             hence continuous at q=0 by construction; contains the true
             ½ω²q² with s = const-per-ctx; inner input width unchanged
             so parameter draws match the round-261 arm B).
Hypothesis under test: the round-261 seed-1 extrapolation benefit is
carried by homogeneity ALONE (direction-free suffices), not by the
direction pathway that also carries the instability.

Readings: in-dist rollout MSE (k=100, house evaluate) + amplitude
extrapolation rel_comp (round-216 caliber, scale pools {1,2,4}).

Mechanical verdict (preregistered, 3-seed):
  STAB_ARM_DIVERGED (negative) — any reading non-finite or > 1e6
  per-seed catastrophe gate: MSE > 100 (inside the round-261 bimodal
      gap: healthy ≤ 2.84, catastrophic ≥ 701.8; conservative side)
  STAB_REPAIRS      — STAB 0/3 catastrophic AND median rel_comp_STAB
      < 3.0: decoupling repairs stability AND keeps the extrapolation
      benefit; decision = direction-free homogeneous head candidate
      upgrade (head-construction independent line)
  STAB_STABLE_ONLY  — STAB 0/3 catastrophic AND median >= 3.0:
      stability restored but benefit not retained — the benefit needed
      the direction pathway; honest downgrade
  STAB_PARTIAL      — STAB 1-2/3 catastrophic: mitigated, not removed
  STAB_NULL         — STAB 3/3 catastrophic: prescription fails, T2
      parking confirmed

Reference reproduction (annotation, not a gate): REF arm expected to
reproduce the round-261 stored arm-B readings bit-for-bit
[2456.613037109375, 2.3841938972473145, 701.840576171875] (identical
construction and seed draw order, deterministic CPU); a 0/3-
catastrophic REF is recorded honestly as a reproduction failure and
the verdict is still computed mechanically.

Decision coupling (AMM-028 gate-1): the outcomes route the homogeneous
head-construction candidate differently (upgrade / downgrade /
parking-confirmed), EIG qualified. Family boundary: scan family 54
round 3 of the new segment. Results JSON follows the audit schema
(top-level "results" key); meta carries exec_tier from probe_run.
"""

import argparse
import json
import math
import os
import sys

import torch
import torch.nn as nn

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from awareliquid_physics.model import LiquidHamiltonianModel  # noqa: E402
from awareliquid_physics.observability import run_metadata  # noqa: E402
from benchmarks.equiv_head_probe import (  # noqa: E402
    AnalyticTHead, gen_spring_scaled, median, rel_mse_scaled)
from benchmarks.liquid_physics_eval import (  # noqa: E402
    evaluate, train as train_prefix)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402
from benchmarks.v_hom_probe import HomVHead  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NORM_CAP = 1e6    # preregistered: divergence threshold (house caliber)
CAT_GATE = 100.0  # preregistered: per-seed catastrophe gate (round-261
                  # bimodal gap: healthy <= 2.84, catastrophic >= 701.8)
REL_GATE = 3.0    # preregistered: round-216 repair gate
SEEDS = (0, 1, 2)
REF_EXPECTED_MSE = [2456.613037109375, 2.3841938972473145,
                    701.840576171875]  # round-261 stored arm B, bitwise
REF_EXPECTED_COMP = [7.826242458211071, 1.4428559373081256,
                     18.62075516374382]


class QuadraticDirectionFree(nn.Module):
    """V(q, ctx) = ‖q‖² · s(0, ctx): degree-2 homogeneous with the
    direction channel fully decoupled (round-268 arm STAB) — the
    direction block of the inner net's input is pinned to zero, so the
    represented V is even in q and continuous at q=0 by construction:
    the 1-D executable form of the scan §57.1 decoupling prescription
    (a gradient-only detach would be a no-op: the 1-D sign Jacobian
    vanishes bit-exactly away from zero). The inner net keeps its
    original input width (zeroed block instead of a shrunk layer), so
    parameter shapes and the torch RNG draw order match HomVHead
    exactly — REF reproduction anchor."""

    def __init__(self, inner: nn.Module, dim: int):
        super().__init__()
        self.inner = inner
        self.dim = dim

    def forward(self, v_in: torch.Tensor) -> torch.Tensor:
        q = v_in[..., :self.dim]
        nq = q.norm(dim=-1, keepdim=True).clamp_min(1e-12)
        zeros = torch.zeros_like(q)
        feats = torch.cat([zeros, v_in[..., self.dim:]], dim=-1)
        return (nq ** 2) * self.inner(feats)


class HomVStabHead(AnalyticTHead):
    """Analytic T + direction-free degree-2 homogeneous V (round-268
    arm STAB). Same parameter draw order as HomVHead (the wrapper adds
    no parameters), so torch RNG sequences match the round-261 arm-B
    construction exactly — REF reproduction anchor."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.V = QuadraticDirectionFree(self.V, self.dim)


def classify_stab(mses_ref, mses_stab, comps_stab,
                  cat_gate: float = CAT_GATE, rel_gate: float = REL_GATE,
                  norm_cap: float = NORM_CAP):
    """Preregistered round-268 verdict (pure, test-pinned)."""
    for tag, vals in (("REF", mses_ref), ("STAB", mses_stab)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > norm_cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "STAB_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} {state} (mse={m:.3e})"}
    cat_ref = [m > cat_gate for m in mses_ref]
    cat_stab = [m > cat_gate for m in mses_stab]
    n_stab = sum(cat_stab)
    med_cs = median(comps_stab)
    stats = {"cat_gate": cat_gate, "rel_gate": rel_gate,
             "mses_REF": mses_ref, "mses_STAB": mses_stab,
             "comps_STAB": comps_stab,
             "catastrophic_REF": cat_ref, "catastrophic_STAB": cat_stab,
             "n_catastrophic_REF": sum(cat_ref),
             "n_catastrophic_STAB": n_stab,
             "rel_comp_median_STAB": med_cs}
    if n_stab == 0:
        if med_cs < rel_gate:
            verdict = "STAB_REPAIRS"
            stats["decision"] = ("decoupling repairs stability AND keeps "
                                 "the extrapolation benefit: direction-"
                                 "free homogeneous head candidate upgrade "
                                 "(head-construction independent line)")
        else:
            verdict = "STAB_STABLE_ONLY"
            stats["decision"] = ("stability restored but the extrapolation "
                                 "benefit is not retained: the benefit "
                                 "needed the direction pathway; honest "
                                 "downgrade")
    elif n_stab < len(SEEDS):
        verdict = "STAB_PARTIAL"
        stats["decision"] = ("catastrophe mitigated, not removed "
                             f"({n_stab}/3 seeds above the gate)")
    else:
        verdict = "STAB_NULL"
        stats["decision"] = ("decoupling prescription fails: T2 parking "
                             "confirmed")
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
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--scales", default="1,2,4")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/v_hom_stab")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]
    scales = [float(x) for x in args.scales.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    scale_pools = {}
    for s in scales:
        gs = torch.Generator().manual_seed(0)
        qs_s, ps_s, _ = gen_spring_scaled(args.n_eval, args.gen_steps,
                                          args.dt, args.omega_lo,
                                          args.omega_hi, gs, scale=s,
                                          device=args.device)
        scale_pools[s] = (qs_s, ps_s)
    print(f"V-HOM-STAB | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} steps={args.train_steps} both-analyticT:"
          f" REF=V ‖q‖²·s(q̂,ctx) vs STAB=V ‖q‖²·s(ctx) direction-free "
          f"(seeds {seeds}; round-268 preregistration, round-65 "
          f"conditional entry)", flush=True)

    arms = {"REF": {"mses": [], "comps": []},
            "STAB": {"mses": [], "comps": []}}
    for seed in seeds:
        for tag, cls in (("REF", HomVHead), ("STAB", HomVStabHead)):
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            # head swap AFTER the model draw, round-249/261 construction
            # order (RNG sequence identical to the round-261 arm B =>
            # REF bitwise reproduction anchor); single variable = the
            # direction channel of the homogeneous V
            model.ham = cls(1, hidden_dim=args.hidden, depth=2,
                            context_dim=args.context_dim)
            train_prefix(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                         args.train_steps, args.lr, args.batch, seed)
            res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                           args.eval_k, args.dt)
            rels = {}
            for s in scales:
                qs_s, ps_s = scale_pools[s]
                r = rel_mse_scaled(model, qs_s, ps_s, args.t_obs,
                                   args.eval_k, args.dt)
                rels[s] = r["rel_mse"]
            comp = rels[scales[-1]] / max(rels[1.0], 1e-30)
            arms[tag]["mses"].append(res["rollout_mse"])
            arms[tag]["comps"].append(comp)
            print(f"  [arm {tag} seed {seed}] MSE "
                  f"{res['rollout_mse']:.4e} | rel_comp {comp:.3f}",
                  flush=True)

    verdict, detail = classify_stab(arms["REF"]["mses"],
                                    arms["STAB"]["mses"],
                                    arms["STAB"]["comps"])
    bitwise = (arms["REF"]["mses"] == REF_EXPECTED_MSE)
    sentinels = {"REF_seedS_round261B": {
        "expected_mse": REF_EXPECTED_MSE,
        "actual_mse": arms["REF"]["mses"],
        "expected_comp": REF_EXPECTED_COMP,
        "actual_comp": arms["REF"]["comps"],
        "bitwise_match": bitwise,
        "note": "annotation not a gate; 0/3-catastrophic REF = honest "
                "reproduction failure, verdict still mechanical"}}
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinels": sentinels,
        "criteria": {"c_diverged": verdict == "STAB_ARM_DIVERGED",
                     "c_repairs": verdict == "STAB_REPAIRS",
                     "c_stable_only": verdict == "STAB_STABLE_ONLY",
                     "c_partial": verdict == "STAB_PARTIAL",
                     "c_null": verdict == "STAB_NULL"},
        "gates": {"cat_gate": CAT_GATE, "rel_gate": REL_GATE,
                  "norm_cap": NORM_CAP, "seeds": list(SEEDS),
                  "scales": scales},
        "anchor": "REF = round-261 arm-B configuration (direction "
                  "input); STAB = direction channel removed; both "
                  "exactly degree-2 homogeneous, same RNG draw order",
    }
    print(f"\nV-HOM-STAB verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"REF bitwise reproduction={bitwise}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "v_hom_stab.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "v_hom_stab_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
