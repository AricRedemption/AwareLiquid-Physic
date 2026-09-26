"""
benchmarks/v_hom_probe.py — V-HOM (round 261): homogeneous-potential
injection (V side), 3 seeds, on the M1 spring family (E1 calibre).

Preregistered in PRD §19 round 260 BEFORE execution (AMM-027 distill
routing, scan family 54 round 2). Round 249 (EQUIV-HEAD) showed:
injecting the analytic T = ½Σp² improves in-distribution rollout
(−14%, 3/3 seeds) but amplitude extrapolation gets WORSE (rel_comp
median 9.07 vs 3.33) — the equivariance gap redirects to V and the
context channel. This probe tests the V side under a single variable:
BOTH arms carry the analytic T (the better round-249 baseline);
arm A = V free MLP, arm B = V(q|ctx) = ‖q‖² · s_θ(q̂, ctx) with q̂ = q/‖q‖ — exactly
degree-2 homogeneous in q (true ½ω²q² representable; autograd
differentiates the product). Refinement vs the round-260 wording
(q²·s_θ(q): not homogeneous for arbitrary s — homogeneity unit test
caught it before execution; recorded in the round-261 record).

Readings: in-dist rollout MSE (k=100, house evaluate) + amplitude
extrapolation rel_comp (round-216 caliber, scale pools {1,2,4}).

Mechanical verdict (preregistered, 3-seed):
  VHOM_ARM_DIVERGED (negative) — any reading non-finite or > 1e6
  VHOM_REPAIRS  — in-dist ratio ∈ [0.95, 1.05] AND median rel_comp_B
      < 3: V homogeneity repairs the extrapolation share; decision =
      full homogeneous-head construction candidate upgrade
  VHOM_PARTIAL  — in-dist ratio in band AND 3 <= rel_comp_B <
      0.7 x rel_comp_A: partial repair; residual = context channel
      (round-244 reading)
  VHOM_NULL     — in-dist ratio in band but rel_comp_B not reduced:
      V homogeneity is not the extrapolation carrier; attribution
      redirects to ctx/integrator

Decision coupling (AMM-028 gate-1): the three outcomes route the head
parameterization candidate differently. Sentinel: arm A = the
round-249 arm B configuration (analytic T + free V); seed 0 expected
2.7786638736724854 bit-for-bit (cross-script anchor). Family boundary:
scan family 54 in-segment round 2 of 2 — family closes after this.
Results JSON follows the audit schema (top-level "results" key); meta
carries exec_tier from probe_run.
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
    SENTINEL, AnalyticTHead, gen_spring_scaled, median,
    rel_mse_scaled)
from benchmarks.liquid_physics_eval import (  # noqa: E402
    evaluate, train as train_prefix)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NORM_CAP = 1e6   # preregistered: divergence threshold
LO_GATE = 0.95   # preregistered: in-dist parity band
HI_GATE = 1.05
REL_GATE = 3.0   # preregistered: round-216 repair gate
SEEDS = (0, 1, 2)
SENTINEL_A = 2.7786638736724854  # round-249 arm B (analytic T + free V)


class ScaledQuadratic(nn.Module):
    """Wrap a scalar net s into V(q, ctx) = ‖q‖² · s(q̂, ctx) where
    q̂ = q/‖q‖: exactly degree-2 homogeneous in q for ANY s (the
    direction is scale-invariant, so V(s·q) = s²·V(q) identically).
    The naive q²·s(q) form is NOT homogeneous (s sees the raw q) —
    caught by the homogeneity unit test before execution."""

    def __init__(self, inner: nn.Module, dim: int):
        super().__init__()
        self.inner = inner
        self.dim = dim

    def forward(self, v_in: torch.Tensor) -> torch.Tensor:
        q = v_in[..., :self.dim]
        nq = q.norm(dim=-1, keepdim=True).clamp_min(1e-12)
        qhat = q / nq
        feats = torch.cat([qhat, v_in[..., self.dim:]], dim=-1)
        return (nq ** 2) * self.inner(feats)


class HomVHead(AnalyticTHead):
    """Analytic T + degree-2 homogeneous V (round-260 arm B)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.V = ScaledQuadratic(self.V, self.dim)


def classify_vhom(mses_a, mses_b, comps_a, comps_b,
                  lo_gate: float = LO_GATE, hi_gate: float = HI_GATE,
                  rel_gate: float = REL_GATE):
    """Preregistered round-260 verdict (pure, test-pinned)."""
    for tag, vals in (("A", mses_a), ("B", mses_b)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > NORM_CAP:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "VHOM_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} {state} (mse={m:.3e})"}
    mean_a = sum(mses_a) / len(mses_a)
    mean_b = sum(mses_b) / len(mses_b)
    ratio = mean_b / max(mean_a, 1e-30)
    med_ca = median(comps_a)
    med_cb = median(comps_b)
    stats = {"ratio": ratio, "mean_A": mean_a, "mean_B": mean_b,
             "mses_A": mses_a, "mses_B": mses_b,
             "rel_comp_A": comps_a, "rel_comp_B": comps_b,
             "rel_comp_median_A": med_ca, "rel_comp_median_B": med_cb,
             "consistent": sum(1 for a, b in zip(mses_a, mses_b) if b < a)}
    in_band = lo_gate <= ratio <= hi_gate
    if in_band and med_cb < rel_gate:
        verdict = "VHOM_REPAIRS"
        stats["decision"] = ("V homogeneity repairs the extrapolation "
                             "share: full homogeneous-head construction "
                             "candidate upgrade")
    elif in_band and med_cb < 0.7 * med_ca:
        verdict = "VHOM_PARTIAL"
        stats["decision"] = ("partial repair: residual attributed to the "
                             "context channel (round-244 reading)")
    else:
        verdict = "VHOM_NULL"
        stats["decision"] = ("V homogeneity is not the extrapolation "
                             "carrier: attribution redirects to ctx/"
                             "integrator")
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
                    default="benchmarks/physics_out_v02/v_hom")
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
    print(f"V-HOM | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} steps={args.train_steps} "
          f"both-analyticT: A=V-free vs B=V-hom(q²·s) (seeds {seeds}; "
          f"round-260 preregistration)", flush=True)

    arms = {"A": {"mses": [], "comps": []},
            "B": {"mses": [], "comps": []}}
    for seed in seeds:
        for tag, hom in (("A", False), ("B", True)):
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            # head swap AFTER the model draw, matching the round-249
            # construction order (sentinel clause); BOTH arms carry the
            # analytic T (round-249 arm B baseline), single variable =
            # the V form
            head_cls = HomVHead if hom else AnalyticTHead
            model.ham = head_cls(1, hidden_dim=args.hidden, depth=2,
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

    verdict, detail = classify_vhom(arms["A"]["mses"], arms["B"]["mses"],
                                    arms["A"]["comps"],
                                    arms["B"]["comps"])
    sentinels = {"A_seed0_round249B": {
        "expected": SENTINEL_A, "actual": arms["A"]["mses"][0],
        "bitwise_match": arms["A"]["mses"][0] == SENTINEL_A}}
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinels": sentinels,
        "criteria": {"c_diverged": verdict == "VHOM_ARM_DIVERGED",
                     "c_repairs": verdict == "VHOM_REPAIRS",
                     "c_partial": verdict == "VHOM_PARTIAL",
                     "c_null": verdict == "VHOM_NULL"},
        "gates": {"lo_gate": LO_GATE, "hi_gate": HI_GATE,
                  "rel_gate": REL_GATE, "norm_cap": NORM_CAP,
                  "seeds": list(SEEDS), "scales": scales},
        "anchor": "A = round-249 arm B configuration; seed 0 expected "
                  "2.7787 (cross-script anchor)"},
    print(f"\nV-HOM verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"sentinel={sentinels['A_seed0_round249B']['bitwise_match']}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "v_hom.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "v_hom_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
