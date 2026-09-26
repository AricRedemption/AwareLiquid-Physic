"""
benchmarks/hom_default_probe.py — HOM-DEFAULT (round 269): the full
homogeneous-head construction vs the house default head, 3 seeds, M1
spring family (E1 caliber). Scan family 54, new-segment round 2 of 2
(family closes for the segment after this). Explicit follow-up of the
round-268 verdict row (STAB_REPAIRS: "齐次头完整构造入 house 默认 M1
的实现确认探针").

Lineage: house default = free-form H and V (sentinel seed 0 = 3.5582);
round 249 injected the analytic T (in-dist −14% but extrapolation
worse); round 268 added the direction-free homogeneous V on top of the
analytic T (stability repaired + extrapolation benefit 3/3). The
complete candidate = analytic T + direction-free homogeneous V
(HomVStabHead). This probe asks the DECISION question directly: the
complete construction vs the house DEFAULT head, single variable =
the head itself (arm A = default construction, NO head swap; arm B =
head swap to HomVStabHead after the model draw).

Readings: in-dist rollout MSE (k=100, house evaluate) + amplitude
extrapolation rel_comp (round-216 caliber, scale pools {1,2,4}).
Expected anchors: arm A seed 0 = 3.5581917762756348 (house default
sentinel, bitwise); arm B = the round-268 STAB readings bitwise
[2.0023648738861084, 1.6420986652374268, 2.2025928497314453]
(cross-script anchor — same construction and seed draw order).

Mechanical verdict (preregistered, 3-seed):
  HOM_ARM_DIVERGED (negative) — any reading non-finite or > 1e6
  ratio = mean MSE_B / mean MSE_A; med = median rel_comp
  HOM_DEFAULT_DOMINATES — ratio < 0.95 AND med_B < med_A: complete
      construction better in-dist AND extrapolation ⇒ default-M1
      replacement candidate (head-construction independent line)
  HOM_DEFAULT_INDIST_ONLY — ratio < 0.95 AND med_B >= med_A
  HOM_DEFAULT_EXTRAP_ONLY — ratio in [0.95, 1.05] AND med_B <
      0.7 x med_A (round-216-style material-extrapolation gate)
  HOM_DEFAULT_PARITY — ratio in band AND med_B >= 0.7 x med_A: no net
      gain over the default (the round-268 gains were vs the
      analytic-T baseline, not vs the default) ⇒ honest downgrade
  HOM_DEFAULT_WORSE — ratio > 1.05 ⇒ candidate downgrade

Decision coupling (AMM-028 gate-1): each outcome changes the default-M1
head candidate state (replacement candidate / scoped gain / parity
downgrade / downgrade), EIG qualified. NOTE: this is an architecture
axis, not a training-recipe axis — the AMM-028 gate-2 combination
reflux (RECIPE-SYNTHESIS) is orthogonal and unaffected. Family
boundary: scan family 54 new-segment round 2 of 2 — closes after this.
Results JSON follows the audit schema; meta carries exec_tier.
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
from benchmarks.equiv_head_probe import (  # noqa: E402
    SENTINEL, gen_spring_scaled, median, rel_mse_scaled)
from benchmarks.liquid_physics_eval import (  # noqa: E402
    evaluate, train as train_prefix)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402
from benchmarks.v_hom_stab_probe import HomVStabHead  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NORM_CAP = 1e6    # preregistered: divergence threshold (house caliber)
LO_GATE = 0.95    # preregistered: in-dist material band
HI_GATE = 1.05
EXTRAP_GATE = 0.7  # preregistered: material extrapolation improvement
SEEDS = (0, 1, 2)
SENTINEL_A = SENTINEL  # house default arm A seed 0 = 3.5581917762756348
B_EXPECTED_MSE = [2.0023648738861084, 1.6420986652374268,
                  2.2025928497314453]  # round-268 STAB arm, bitwise
B_EXPECTED_COMP = [2.2357698178622973, 1.7046374779630944,
                   1.378721458484866]


def classify_hom_default(mses_a, mses_b, comps_a, comps_b,
                         lo: float = LO_GATE, hi: float = HI_GATE,
                         ex_gate: float = EXTRAP_GATE,
                         norm_cap: float = NORM_CAP):
    """Preregistered round-269 verdict (pure, test-pinned)."""
    for tag, vals in (("A", mses_a), ("B", mses_b)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > norm_cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "HOM_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} {state} (mse={m:.3e})"}
    mean_a = sum(mses_a) / len(mses_a)
    mean_b = sum(mses_b) / len(mses_b)
    ratio = mean_b / max(mean_a, 1e-30)
    med_ca = median(comps_a)
    med_cb = median(comps_b)
    stats = {"ratio": ratio, "mean_A": mean_a, "mean_B": mean_b,
             "mses_A": mses_a, "mses_B": mses_b,
             "rel_comp_A": comps_a, "rel_comp_B": comps_b,
             "rel_comp_median_A": med_ca, "rel_comp_median_B": med_cb}
    in_band = lo <= ratio <= hi
    if ratio < lo and med_cb < med_ca:
        verdict = "HOM_DEFAULT_DOMINATES"
        stats["decision"] = ("complete construction better in-dist AND "
                             "extrapolation: default-M1 replacement "
                             "candidate (head-construction independent "
                             "line)")
    elif ratio < lo:
        verdict = "HOM_DEFAULT_INDIST_ONLY"
        stats["decision"] = ("in-dist gain only: scoped candidate, "
                             "extrapolation parity or worse vs default")
    elif in_band and med_cb < ex_gate * med_ca:
        verdict = "HOM_DEFAULT_EXTRAP_ONLY"
        stats["decision"] = ("extrapolation gain only: scoped candidate, "
                             "in-dist parity vs default")
    elif in_band:
        verdict = "HOM_DEFAULT_PARITY"
        stats["decision"] = ("no net gain over the default (round-268 "
                             "gains were vs the analytic-T baseline): "
                             "honest downgrade")
    else:
        verdict = "HOM_DEFAULT_WORSE"
        stats["decision"] = ("complete construction worse than the "
                             "default in-dist: candidate downgrade")
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
                    default="benchmarks/physics_out_v02/hom_default")
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
    print(f"HOM-DEFAULT | M1 spring omega[{args.omega_lo},{args.omega_hi}]"
          f" hidden={args.hidden} steps={args.train_steps}: A=house "
          f"default head vs B=analyticT+direction-free-homV (seeds "
          f"{seeds}; round-269 preregistration)", flush=True)

    arms = {"A": {"mses": [], "comps": []},
            "B": {"mses": [], "comps": []}}
    for seed in seeds:
        for tag in ("A", "B"):
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            # arm A = default construction (NO head swap — house default
            # draw); arm B = head swap AFTER the model draw (round-249/
            # 268 construction order); single variable = the head
            if tag == "B":
                model.ham = HomVStabHead(1, hidden_dim=args.hidden,
                                         depth=2,
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

    verdict, detail = classify_hom_default(arms["A"]["mses"],
                                           arms["B"]["mses"],
                                           arms["A"]["comps"],
                                           arms["B"]["comps"])
    bitwise_a = arms["A"]["mses"][0] == SENTINEL_A
    bitwise_b = arms["B"]["mses"] == B_EXPECTED_MSE
    sentinels = {
        "A_seed0_house_default": {
            "expected": SENTINEL_A, "actual": arms["A"]["mses"][0],
            "bitwise_match": bitwise_a},
        "B_round268_STAB": {
            "expected_mse": B_EXPECTED_MSE,
            "actual_mse": arms["B"]["mses"],
            "expected_comp": B_EXPECTED_COMP,
            "actual_comp": arms["B"]["comps"],
            "bitwise_match": bitwise_b,
            "note": "cross-script anchor: same construction and seed "
                    "draw order as the round-268 STAB arm"},
    }
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinels": sentinels,
        "criteria": {"c_diverged": verdict == "HOM_ARM_DIVERGED",
                     "c_dominates": verdict == "HOM_DEFAULT_DOMINATES",
                     "c_indist_only": verdict == "HOM_DEFAULT_INDIST_ONLY",
                     "c_extrap_only": verdict == "HOM_DEFAULT_EXTRAP_ONLY",
                     "c_parity": verdict == "HOM_DEFAULT_PARITY",
                     "c_worse": verdict == "HOM_DEFAULT_WORSE"},
        "gates": {"lo_gate": LO_GATE, "hi_gate": HI_GATE,
                  "extrap_gate": EXTRAP_GATE, "norm_cap": NORM_CAP,
                  "seeds": list(SEEDS), "scales": scales},
        "anchor": "A = house default head (sentinel 3.5582, bitwise); "
                  "B = HomVStabHead (round-268 STAB arm, bitwise)",
    }
    print(f"\nHOM-DEFAULT verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"sentinels A={bitwise_a} B={bitwise_b}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "hom_default.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "hom_default_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
