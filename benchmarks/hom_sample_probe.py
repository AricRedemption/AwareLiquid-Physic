"""
benchmarks/hom_sample_probe.py — HOM-SAMPLE (round 277): sample
efficiency of the AMM-033 candidate head vs the house default head,
3 training sizes x 3 seeds, M1 spring family (E1 caliber). Scan family
62 (inductive bias x sample efficiency family; slot 1 = Mialon
arXiv:2302.10692 data-constrained inductive biases, slot 2 = Elesedy &
Zaidi ICML 2021 provably strict equivariance benefit, slot 3 = Lyle
et al. arXiv:2005.00178 benefits of invariance).

Classical prediction: a constrained (structure-matched) model pays
less for scarce data than a free-form model — its advantage should
GROW as training trajectories shrink. The candidate head already wins
at the house size (n_train=256, ratio 0.66 in round 269); this probe
measures the size axis: n_train in {64, 128, 256}, single variable =
the head (A = house default, NO head swap, seed-0/256 = house anchor
3.5582; B = analytic T + direction-free homogeneous V, seed-0/256 =
round-269 B arm bitwise).

Mechanical verdict (preregistered, 3-seed; ratios are per-size means
B/A):
  HOM_ARM_DIVERGED (negative) — any reading non-finite or > 1e6
  HOM_SAMPLE_CAND_WORSE — ratio_256 > 1.0: candidate behind at the
      house size here (contradicts round 269; honest annotation)
  HOM_SAMPLE_SMALLDATA_ADV — ratio_64 < 0.97 x ratio_256: the
      advantage grows toward scarce data ⇒ AMM-033 annotation
      upgraded (inductive-bias value strongest where data is scarce)
  HOM_SAMPLE_FLAT — |ratio_64 - ratio_256| small (ratio_64 <= 1.03 x
      ratio_256): advantage size-independent
  HOM_SAMPLE_REVERSED — otherwise: advantage vanishes when data is
      scarce (the constraint net needs data to fit s_theta) ⇒
      conservative annotation

Decision coupling (AMM-028 gate-1): each outcome changes the AMM-033
benefit-scope/anchor annotation differently, EIG qualified. Family
boundary: scan family 62 round 1. Results JSON follows the audit
schema.
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
    SENTINEL, gen_spring_scaled)
from benchmarks.liquid_physics_eval import (  # noqa: E402
    evaluate, train as train_prefix)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402
from benchmarks.v_hom_stab_probe import HomVStabHead  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NORM_CAP = 1e6   # preregistered: divergence threshold (house caliber)
GROW_GATE = 0.97  # preregistered: advantage-growth gate
FLAT_GATE = 1.03  # preregistered: flatness band (ratio_64/ratio_256)
SIZES = (64, 128, 256)
SEEDS = (0, 1, 2)


def classify_hom_sample(ratios, sizes=SIZES, grow_gate: float = GROW_GATE,
                        flat_gate: float = FLAT_GATE,
                        norm_cap: float = NORM_CAP, mses=None):
    """Preregistered round-277 verdict (pure, test-pinned). `ratios` =
    per-size mean MSE_B/mean MSE_A, ordered as `sizes`."""
    if mses is not None:
        for tag, per in (("A", mses["A"]), ("B", mses["B"])):
            for n, vals in zip(sizes, per):
                for s, m in zip(SEEDS, vals):
                    if not math.isfinite(m) or m > norm_cap:
                        state = ("non-finite" if not math.isfinite(m)
                                 else "diverged")
                        return "HOM_ARM_DIVERGED", {
                            "reason": f"arm {tag} seed {s} n={n} {state} "
                                      f"(mse={m:.3e})"}
    r64, r256 = ratios[0], ratios[-1]
    stats = {"grow_gate": grow_gate, "flat_gate": flat_gate,
             "sizes": list(sizes), "ratio_per_size": ratios}
    if r256 > 1.0:
        verdict = "HOM_SAMPLE_CAND_WORSE"
        stats["decision"] = ("candidate behind the default at the house "
                             "size in this run: honest annotation, "
                             "contradicts round 269")
    elif r64 < grow_gate * r256:
        verdict = "HOM_SAMPLE_SMALLDATA_ADV"
        stats["decision"] = ("advantage grows toward scarce data: AMM-033 "
                             "annotation upgraded — inductive-bias value "
                             "strongest where data is scarce")
    elif r64 <= flat_gate * r256:
        verdict = "HOM_SAMPLE_FLAT"
        stats["decision"] = ("advantage size-independent across the "
                             "measured ladder")
    else:
        verdict = "HOM_SAMPLE_REVERSED"
        stats["decision"] = ("advantage vanishes when data is scarce: "
                             "the constrained net needs data to fit "
                             "s_theta; conservative annotation")
    return verdict, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--sizes", default="64,128,256")
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--gen_steps", type=int, default=160)
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
                    default="benchmarks/physics_out_v02/hom_sample")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]
    sizes = [int(x) for x in args.sizes.split(",")]

    n_max = 256 + args.n_eval
    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(n_max, args.gen_steps, args.dt, 1,
                            args.omega_lo, args.omega_hi, g,
                            device=args.device)
    ev = slice(256, None)
    print(f"HOM-SAMPLE | M1 spring sizes={sizes}: A=house default head "
          f"vs B=analyticT+direction-free-homV (seeds {seeds}; round-277 "
          f"preregistration, scan family 62)", flush=True)

    mses = {h: {n: [] for n in sizes} for h in ("A", "B")}
    for seed in seeds:
        for tag in ("A", "B"):
            for n in sizes:
                tr = slice(0, n)
                torch.manual_seed(seed)
                model = LiquidHamiltonianModel(
                    1, d_model=args.d_model, context_dim=args.context_dim,
                    n_scales=args.n_scales, hidden_dim=args.hidden,
                    depth=2, dt=args.dt)
                # arm A = default construction (NO head swap); arm B =
                # head swap AFTER the model draw; single variable = the
                # head (size is the measured axis)
                if tag == "B":
                    model.ham = HomVStabHead(
                        1, hidden_dim=args.hidden, depth=2,
                        context_dim=args.context_dim)
                train_prefix(model, qs[tr], ps[tr], args.t_obs,
                             args.k_train, args.train_steps, args.lr,
                             args.batch, seed)
                res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                               args.eval_k, args.dt)
                mses[tag][n].append(res["rollout_mse"])
                print(f"  [arm {tag} seed {seed} n={n}] MSE "
                      f"{res['rollout_mse']:.4e}", flush=True)

    mean = lambda rows: [sum(v) / len(v) for v in rows]
    mean_a = mean([mses["A"][n] for n in sizes])
    mean_b = mean([mses["B"][n] for n in sizes])
    ratios = [b / max(a, 1e-30) for a, b in zip(mean_a, mean_b)]
    verdict, detail = classify_hom_sample(
        ratios, sizes=sizes,
        mses={"A": [mses["A"][n] for n in sizes],
              "B": [mses["B"][n] for n in sizes]})
    bitwise_a = mses["A"][256][0] == SENTINEL
    sentinels = {"A_seed0_size256_house_default": {
        "expected": SENTINEL, "actual": mses["A"][256][0],
        "bitwise_match": bitwise_a}}
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinels": sentinels,
        "mses_by_head_size": {h: {str(n): mses[h][n] for n in sizes}
                              for h in ("A", "B")},
        "criteria": {"c_diverged": verdict == "HOM_ARM_DIVERGED",
                     "c_cand_worse": verdict == "HOM_SAMPLE_CAND_WORSE",
                     "c_smalldata": verdict == "HOM_SAMPLE_SMALLDATA_ADV",
                     "c_flat": verdict == "HOM_SAMPLE_FLAT",
                     "c_reversed": verdict == "HOM_SAMPLE_REVERSED"},
        "gates": {"grow_gate": GROW_GATE, "flat_gate": FLAT_GATE,
                  "norm_cap": NORM_CAP, "seeds": list(SEEDS),
                  "sizes": sizes},
        "anchor": "single variable = the head; size ladder is the "
                  "measured axis; eval pool fixed (n_eval=128, same "
                  "seed-0 draws)",
    }
    print(f"\nHOM-SAMPLE verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"sentinel A={bitwise_a}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "hom_sample.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "hom_sample_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
