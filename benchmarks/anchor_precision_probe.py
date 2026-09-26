"""
benchmarks/anchor_precision_probe.py — ANCHOR-PRECISION (round 406):
numerical-precision robustness of anchor readouts, fp32 (house
caliber) vs fp64 recomputation of the SAME weights on the SAME pools.
Scan family 65 (evaluation-variance / numerical-nondeterminism anchor
robustness family, round-405 distillation; slot 1 = Bouthillier et al.
MLSys 2021 variance accounting, slot 2 = Yuan et al. NeurIPS 2025
numerical nondeterminism, slot 3 = Nagarajan et al. 2018 RL
reproducibility).

Why: POOL-BITS (round 275) showed bit-level pool-composition
perturbations swing single-readout anchors beyond the 1.10 gate for
BOTH heads, so AMM-033's anchor plan condition 5 requires per-anchor
multi-variant spread annotations. Yuan et al. (2025) independently
show evaluation readouts swing under precision/hardware changes
(float non-associativity). Open decision: does the precision axis
also belong in the anchor protocol, or is the pool-composition axis
sufficient?

Arms (each arm's weights trained ONCE at the house caliber, seed 0;
single weight set per anchor family — no seed axis, deterministic
inference):
  A = house default head, variant-160 pool (k100) + variant-1100 pool
      (k400, anchor-plan long-horizon caliber, round-273)
  B = AMM-033 candidate head (HomVStabHead), same two pools
Readouts per (arm, pool): rollout_mse, energy_drift_final,
energy_drift_max — fp32 baseline vs fp64 recomputation
(model.double() + pool.double()).

Mechanical verdict (preregistered round 405, PRD section 19):
  per readout r: precision_spread = |r_fp32 - r_fp64| / |r_fp64|
  max_spread = max over all (arm, pool, readout) — 12 values
  PRECISION_ANCHOR_ROBUST  — max_spread <= 0.10: pool-composition
      axis is sufficient, AMM-033 anchor plan condition 5 keeps its
      current text (literature stays [coordinate]-level corroboration)
  PRECISION_ANCHOR_FRAGILE — max_spread > 0.10: anchor plan
      condition 5 gains a precision-variant axis (each anchor carries
      fp32/fp64 dual-readout spread annotation)
  Gate 0.10 = POOL-BITS 1.10 gate caliber (round 275 precedent).

Sentinels: fp32 k100 variant-160 rollout MSE must reproduce the
historical anchors bitwise (A = house 3.5582, B = round-268 STAB
2.0024; same construction calls as rounds 269/268/275 — only
same-parameter pool calls carry bitwise anchors). exec_tier=T1,
conclusion grade = protocol-design input only (T1 routing caliber),
not a terminal claim; the AMM-033 implementation-time anchor final
run (hidden-set discipline) remains the terminal caliber.
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

PRECISION_GATE = 0.10  # preregistered round 405 (= POOL-BITS 1.10 caliber)
READOUTS = ("rollout_mse", "energy_drift_final", "energy_drift_max")
A_ANCHOR_160 = SENTINEL            # 3.5581917762756348 (house, k100/v160)
B_ANCHOR_160 = 2.0023648738861084  # round-268 STAB seed 0 (k100/v160)


def classify_anchor_precision(spreads, gate: float = PRECISION_GATE):
    """Preregistered round-405 verdict (pure, test-pinned). `spreads`
    maps (arm, eval_k) -> {readout: spread}. Non-finite any spread
    counts as fragile (a non-reproducible anchor cannot anchor)."""
    flat = {}
    for key, per_readout in spreads.items():
        for name, s in per_readout.items():
            if not math.isfinite(s) or s > gate:
                flat[key] = {"readout": name, "spread": s,
                             "finite": math.isfinite(s)}
    max_spread = max(v["spread"] for v in flat.values()) if flat else max(
        s for per in spreads.values() for s in per.values())
    if flat:
        worst = max(flat.values(), key=lambda v: v["spread"])
        verdict = "PRECISION_ANCHOR_FRAGILE"
        decision = ("precision axis swings anchor readouts beyond the "
                    "gate: AMM-033 anchor plan condition 5 gains a "
                    "precision-variant axis (fp32/fp64 dual readout per "
                    f"anchor); worst={worst['readout']} "
                    f"spread={worst['spread']:.3e}")
    else:
        verdict = "PRECISION_ANCHOR_ROBUST"
        decision = ("precision axis is within the gate everywhere: "
                    "pool-composition axis is sufficient, AMM-033 "
                    "anchor plan condition 5 keeps its current text")
    stats = {"gate": gate, "violations": flat,
             "max_spread": max_spread, "decision": decision}
    return verdict, stats


def _eval_both_precisions(model, qs, ps, om, t_obs, eval_k, dt, ev):
    """Evaluate the same weights at fp32 (house caliber) and fp64
    (deepcopy(model).double() + pool.double()); returns
    {readout: (r32, r64)}. deepcopy keeps any head swap (arm B)."""
    import copy

    out = {}
    r32 = evaluate(model, qs[ev], ps[ev], om[ev], t_obs, eval_k, dt)
    m64 = copy.deepcopy(model).double()
    r64 = evaluate(m64, qs[ev].double(), ps[ev].double(),
                   om[ev].double(), t_obs, eval_k, dt)
    for name in READOUTS:
        out[name] = (r32[name], r64[name])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/anchor_precision")
    args = ap.parse_args()

    # (arm tag, pool gen_steps, eval_k) — k100 on the house anchor pool
    # (variant-160), k400 on the long-horizon pool (variant-1100,
    # anchor-plan round-273 caliber; 1100 >= t_obs+400 steps).
    plan = (("A", 160, 100), ("A", 1100, 400),
            ("B", 160, 100), ("B", 1100, 400))
    pools = {}
    for _, steps, _ in plan:
        if steps not in pools:
            g = torch.Generator().manual_seed(0)
            pools[steps] = gen_spring(args.n_train + args.n_eval, steps,
                                      args.dt, 1, args.omega_lo,
                                      args.omega_hi, g,
                                      device=args.device)
    ev = slice(args.n_train, None)
    print(f"ANCHOR-PRECISION | fp32 vs fp64 anchor readouts, arms "
          f"A=house default B=candidate HomVStabHead, seed 0 each, "
          f"plan={plan} (round-406 preregistration, scan family 65)",
          flush=True)

    read32 = {}
    read64 = {}
    for tag, steps, eval_k in plan:
        qs, ps, om = pools[steps]
        torch.manual_seed(0)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=args.n_scales, hidden_dim=args.hidden,
            depth=args.depth, dt=args.dt)
        if tag == "B":
            model.ham = HomVStabHead(
                1, hidden_dim=args.hidden, depth=args.depth,
                context_dim=args.context_dim)
        train_prefix(model, qs[:args.n_train], ps[:args.n_train],
                     args.t_obs, args.k_train, args.train_steps,
                     args.lr, args.batch, 0)
        pair = _eval_both_precisions(model, qs, ps, om, args.t_obs,
                                     eval_k, args.dt, ev)
        for name, (r32, r64) in pair.items():
            read32[(tag, steps, eval_k, name)] = r32
            read64[(tag, steps, eval_k, name)] = r64
        print(f"  [arm {tag} pool={steps} k={eval_k}] " +
              " ".join(f"{n} {r32:.6e}/{r64:.6e}"
                       for n, (r32, r64) in pair.items()), flush=True)

    spreads = {}
    for tag, steps, eval_k in plan:
        key = f"{tag}_pool{steps}_k{eval_k}"
        spreads[key] = {
            name: abs(read32[(tag, steps, eval_k, name)]
                      - read64[(tag, steps, eval_k, name)])
            / abs(read64[(tag, steps, eval_k, name)])
            for name in READOUTS}
    verdict, detail = classify_anchor_precision(spreads)

    bitwise_a = read32[("A", 160, 100, "rollout_mse")] == A_ANCHOR_160
    bitwise_b = read32[("B", 160, 100, "rollout_mse")] == B_ANCHOR_160
    sentinels = {
        "A_seed0_v160_k100_house_default": {
            "expected": A_ANCHOR_160,
            "actual": read32[("A", 160, 100, "rollout_mse")],
            "bitwise_match": bitwise_a},
        "B_seed0_v160_k100_round268": {
            "expected": B_ANCHOR_160,
            "actual": read32[("B", 160, 100, "rollout_mse")],
            "bitwise_match": bitwise_b,
            "note": "variant-160 pools are constructed identically to "
                    "the historical calls, so bitwise anchors apply "
                    "(round-273 lesson: only same-parameter pool calls "
                    "carry bitwise anchors)"},
    }
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinels": sentinels,
        "readouts_fp32": {f"{t}_{s}_k{k}_{n}": v
                          for (t, s, k, n), v in read32.items()},
        "readouts_fp64": {f"{t}_{s}_k{k}_{n}": v
                          for (t, s, k, n), v in read64.items()},
        "precision_spreads": spreads,
        "criteria": {"c_robust": verdict == "PRECISION_ANCHOR_ROBUST",
                     "c_fragile": verdict == "PRECISION_ANCHOR_FRAGILE"},
        "gates": {"precision_gate": PRECISION_GATE,
                  "readouts": list(READOUTS), "seed": 0},
        "anchor": "perturbation axis = eval precision only (same "
                  "weights, same pool); fp64 = model.double() + "
                  "pool.double() recomputation",
    }
    print(f"\nANCHOR-PRECISION verdict {verdict} | "
          f"{detail['decision']} | sentinels A={bitwise_a} "
          f"B={bitwise_b}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "anchor_precision.json"),
              "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "anchor_precision_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
