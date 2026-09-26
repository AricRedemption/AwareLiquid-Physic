"""
benchmarks/pool_bits_probe.py — POOL-BITS (round 275): training-basin
stability under bit-level pool perturbations, default head vs the
AMM-033 candidate head, 3 seeds, M1 spring family (E1 caliber). Scan
family 61 (training-basin stability family, round-275 distillation;
slot 1 = Entezari et al. ICLR 2022 linear mode connectivity, slot 2 =
Frankle & Carbin ICLR 2019 lottery ticket, slot 3 = Dinh et al. ICML
2017 sharp minima can generalize).

Why: round 273 accidentally demonstrated that changing ONLY the pool
tensor length (gen_steps 160 -> 1100; same seed, same omega/q0/p0
draws, same systems — the differences are low-order bits from
size-dependent elementwise transcendental kernels) swung the DEFAULT
head's seed-0 MSE by 25% while the candidate head moved ~0.05%. This
probe measures that texture properly: 4 pool variants (gen_steps in
{160, 300, 600, 1100} — identical distribution, bit-perturbed
trajectories) x 2 heads x 3 seeds, k=100 in-dist rollout MSE.

Arms: A = house default head (NO head swap; variant-160 seed 0 is the
house anchor 3.5582, bitwise); B = analytic T + direction-free
homogeneous V (HomVStabHead; variant-160 seed 0 = round-268 STAB
2.0024, bitwise). Per (head, seed) the reading is the across-variant
spread = max/min of the 4 variant MSEs.

Mechanical verdict (preregistered, 3-seed):
  HOM_ARM_DIVERGED (negative) — any reading non-finite or > 1e6
  med_def / med_cand = median across-seed spread per head
  ANCHOR_CANDIDATE_STABLE — med_cand < med_def AND med_cand < 1.10:
      candidate anchors are basin-stable ⇒ AMM-033 anchor plan may
      use fewer pool variants (single-variant anchors viable)
  ANCHOR_BOTH_FRAGILE — med_def >= 1.10 AND med_cand >= 1.10:
      both heads fragile ⇒ anchor plan requires a multi-variant
      protocol (spread reported per anchor)
  ANCHOR_NO_DIFFERENCE — otherwise ⇒ no stability difference
      measurable; anchor plan neutral

Decision coupling (AMM-028 gate-1): each outcome changes the AMM-033
anchor-set variant protocol differently, EIG qualified. Sentinels:
variant-160 column must reproduce the historical anchors bitwise
(same construction calls as rounds 269/268). Family boundary: scan
family 61 round 1. Results JSON follows the audit schema.
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
    SENTINEL, median)
from benchmarks.liquid_physics_eval import (  # noqa: E402
    evaluate, train as train_prefix)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402
from benchmarks.v_hom_stab_probe import HomVStabHead  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NORM_CAP = 1e6     # preregistered: divergence threshold (house caliber)
STABLE_GATE = 1.10  # preregistered: absolute basin-stability gate
VARIANTS = (160, 300, 600, 1100)
SEEDS = (0, 1, 2)
A_ANCHOR_160 = SENTINEL                    # 3.5581917762756348
B_ANCHOR_160 = 2.0023648738861084          # round-268 STAB seed 0


def classify_pool_bits(spreads_def, spreads_cand,
                       stable_gate: float = STABLE_GATE,
                       norm_cap: float = NORM_CAP):
    """Preregistered round-275 verdict (pure, test-pinned). Spreads are
    per-seed across-variant max/min ratios."""
    for tag, vals in (("A", spreads_def), ("B", spreads_cand)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > norm_cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "HOM_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} {state} "
                              f"(spread={m:.3e})"}
    med_def = median(spreads_def)
    med_cand = median(spreads_cand)
    stats = {"stable_gate": stable_gate,
             "spreads_default": spreads_def,
             "spreads_candidate": spreads_cand,
             "median_spread_default": med_def,
             "median_spread_candidate": med_cand}
    if med_cand < med_def and med_cand < stable_gate:
        verdict = "ANCHOR_CANDIDATE_STABLE"
        stats["decision"] = ("candidate anchors are basin-stable: AMM-033 "
                             "anchor plan may use fewer pool variants "
                             "(single-variant anchors viable)")
    elif med_def >= stable_gate and med_cand >= stable_gate:
        verdict = "ANCHOR_BOTH_FRAGILE"
        stats["decision"] = ("both heads basin-fragile: anchor plan "
                             "requires a multi-variant protocol (spread "
                             "reported per anchor)")
    else:
        verdict = "ANCHOR_NO_DIFFERENCE"
        stats["decision"] = ("no stability difference measurable: anchor "
                             "plan neutral")
    return verdict, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--variants", default="160,300,600,1100")
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
                    default="benchmarks/physics_out_v02/pool_bits")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]
    variants = [int(x) for x in args.variants.split(",")]

    pools = {}
    for v in variants:
        g = torch.Generator().manual_seed(0)
        qs, ps, om = gen_spring(args.n_train + args.n_eval, v, args.dt, 1,
                                args.omega_lo, args.omega_hi, g,
                                device=args.device)
        pools[v] = (qs, ps, om)
    ev = slice(args.n_train, None)
    print(f"POOL-BITS | M1 spring pool-bit variants {variants} (same "
          f"seed=0 draws, low-bit transcendental differences only) "
          f"heads: A=house default vs B=candidate HomVStabHead (seeds "
          f"{seeds}; round-275 preregistration, scan family 61)",
          flush=True)

    mses = {h: {v: [] for v in variants} for h in ("A", "B")}
    for seed in seeds:
        for tag in ("A", "B"):
            for v in variants:
                qs, ps, om = pools[v]
                torch.manual_seed(seed)
                model = LiquidHamiltonianModel(
                    1, d_model=args.d_model, context_dim=args.context_dim,
                    n_scales=args.n_scales, hidden_dim=args.hidden,
                    depth=2, dt=args.dt)
                # arm A = default construction (NO head swap); arm B =
                # head swap AFTER the model draw; single variable = the
                # head (pool variant is the perturbation axis)
                if tag == "B":
                    model.ham = HomVStabHead(
                        1, hidden_dim=args.hidden, depth=2,
                        context_dim=args.context_dim)
                train_prefix(model, qs[:args.n_train], ps[:args.n_train],
                             args.t_obs, args.k_train, args.train_steps,
                             args.lr, args.batch, seed)
                res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                               args.eval_k, args.dt)
                mses[tag][v].append(res["rollout_mse"])
                print(f"  [arm {tag} seed {seed} steps={v}] MSE "
                      f"{res['rollout_mse']:.4e}", flush=True)

    spreads_def = []
    spreads_cand = []
    for h, acc in (("A", spreads_def), ("B", spreads_cand)):
        for i in range(len(seeds)):
            vals = [mses[h][v][i] for v in variants]
            acc.append(max(vals) / min(vals))
    verdict, detail = classify_pool_bits(spreads_def, spreads_cand)
    bitwise_a = mses["A"][variants[0]][0] == A_ANCHOR_160
    bitwise_b = mses["B"][variants[0]][0] == B_ANCHOR_160
    sentinels = {
        "A_seed0_variant160_house_default": {
            "expected": A_ANCHOR_160,
            "actual": mses["A"][variants[0]][0],
            "bitwise_match": bitwise_a},
        "B_seed0_variant160_round268": {
            "expected": B_ANCHOR_160,
            "actual": mses["B"][variants[0]][0],
            "bitwise_match": bitwise_b,
            "note": "variant-160 pools are constructed identically to "
                    "the historical calls, so bitwise anchors apply "
                    "here (round-273 lesson: only same-parameter pool "
                    "calls carry bitwise anchors)"},
    }
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinels": sentinels,
        "mses_by_head_variant": {h: {str(v): mses[h][v]
                                     for v in variants}
                                 for h in ("A", "B")},
        "criteria": {"c_diverged": verdict == "HOM_ARM_DIVERGED",
                     "c_candidate_stable":
                         verdict == "ANCHOR_CANDIDATE_STABLE",
                     "c_both_fragile": verdict == "ANCHOR_BOTH_FRAGILE",
                     "c_no_difference":
                         verdict == "ANCHOR_NO_DIFFERENCE"},
        "gates": {"stable_gate": STABLE_GATE, "norm_cap": NORM_CAP,
                  "seeds": list(SEEDS), "variants": list(variants)},
        "anchor": "perturbation axis = pool tensor length only (same "
                  "draws, low-bit differences); single variable = the "
                  "head",
    }
    print(f"\nPOOL-BITS verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"sentinels A160={bitwise_a} B160={bitwise_b}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "pool_bits.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "pool_bits_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
