"""
benchmarks/residual_spec3_probe.py — SPEC3 (round 283): re-measurement
of the k_train={4,8} residual-spectrum comparison under the CORRECTED
spectral cutoff (AMM-031 as fixed in round 267), 3 seeds, M1 spring
family. Closes the round-267 pending item ("residual_spec2 的 low_band
绝对值待重算").

Background: round-246 (RESIDUAL-SPEC-2) compared k4/k8 arms with a
hand-rolled hf ratio whose cutoff was 2*omega_max*dt/(2pi) = 0.0573 Hz
— dt in the numerator, 100x too low (round-267 correction). Both arms
shared the wrong cutoff, so the r246 ordering was *internally*
consistent, but its absolute values were flagged pending recompute.
Since round 267, the house `evaluate()` carries the corrected
`residual_low_band_ratio` key (band top = omega_max/(2*pi*dt) =
2.865 Hz). This probe reruns the SAME arms/pool/construction and reads
the corrected key directly — no copied wrong code anywhere.

Construction mirrors r246 exactly: E1 pool with gen_steps=301 (same
seed-0 draws -> same pool bits -> scalar-MSE cross-script anchors),
k_train arms {4, 8} x seeds {0, 1, 2}, house evaluate at k=100.
Expected scalar anchors (bitwise): k4 arm
[2.526942491531372, 3.024425745010376, 2.004868745803833], k8 arm
[2.9031009674072266, 2.423386812210083, 3.1820216178894043].

Mechanical verdict (preregistered, 3-seed; gate on the across-seed
median difference of the corrected low_band ratio):
  SPEC3_UNRESOLVABLE (negative) — any reading non-finite or > 1e6
  SPEC3_ORDER_REPRODUCES — med(low_k4) - med(low_k8) >= +0.01: the
      r246 ordering survives the cutoff correction ⇒ AMM-031 secondary
      criterion keeps its standing with corrected house values
  SPEC3_ORDER_TIED — |med(low_k4) - med(low_k8)| < 0.01 (1% of
      energy): composition parity under the corrected cutoff ⇒ the
      r246 spectral increment was a cutoff artifact; criterion
      downgraded to reference-only
  SPEC3_ORDER_FLIPS — med(low_k4) - med(low_k8) <= -0.01: ordering
      reverses ⇒ r246 ordering was a cutoff artifact, criterion
      downgraded with reversed sign

Decision coupling (AMM-028 gate-1): each outcome changes the AMM-031
house secondary-criterion annotation differently (keep-with-corrected-
values / reference-only downgrade / sign-reversed downgrade), and
closes the round-267 pending item either way. Family bookkeeping:
RESIDUAL family caliber-correction closure (round-267 registered
non-pool item, unparked by the round-283 parking-lot three-question
audit: T1-local, reversible, no user resources). Results JSON follows
the audit schema; meta carries exec_tier.
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NORM_CAP = 1e6   # preregistered: divergence threshold (house caliber)
TIED_GATE = 0.01  # preregistered: 1%-of-energy composition parity band
SEEDS = (0, 1, 2)
A4_EXPECTED_MSE = [2.526942491531372, 3.024425745010376, 2.004868745803833]
B8_EXPECTED_MSE = [2.9031009674072266, 2.423386812210083, 3.1820216178894043]
R246_WRONGCUT_LOW = {"k4": [0.0748731360822491, 0.14118544077191986,
                            0.06589602541110051],
                     "k8": [0.0675448416715716, 0.06431859056834177,
                            0.12447865522979018]}


def classify_spec3(lows_k4, lows_k8,
                   tied_gate: float = TIED_GATE,
                   norm_cap: float = NORM_CAP):
    """Preregistered round-283 verdict (pure, test-pinned)."""
    for tag, vals in (("k4", lows_k4), ("k8", lows_k8)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > norm_cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "SPEC3_UNRESOLVABLE", {
                    "reason": f"arm k{tag} seed {s} {state} "
                              f"(low_band={m:.3e})"}
    med = lambda v: sorted(v)[len(v) // 2]
    med_k4, med_k8 = med(lows_k4), med(lows_k8)
    diff = med_k4 - med_k8
    stats = {"tied_gate": tied_gate, "low_band_k4": lows_k4,
             "low_band_k8": lows_k8, "median_low_k4": med_k4,
             "median_low_k8": med_k8, "median_diff": diff,
             "r246_wrongcut_low": R246_WRONGCUT_LOW}
    if abs(diff) < tied_gate:
        verdict = "SPEC3_ORDER_TIED"
        stats["decision"] = ("composition parity under the corrected "
                             "cutoff: the r246 spectral increment was a "
                             "cutoff artifact; AMM-031 secondary "
                             "criterion downgraded to reference-only")
    elif diff > 0:
        verdict = "SPEC3_ORDER_REPRODUCES"
        stats["decision"] = ("r246 ordering survives the cutoff "
                             "correction: AMM-031 secondary criterion "
                             "keeps its standing with corrected house "
                             "values")
    else:
        verdict = "SPEC3_ORDER_FLIPS"
        stats["decision"] = ("ordering reverses under the corrected "
                             "cutoff: the r246 ordering was a cutoff "
                             "artifact; criterion downgraded with "
                             "reversed sign")
    return verdict, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=301)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--ktrain_arms", default="4,8")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/residual_spec_3")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]
    k_arms = [int(x) for x in args.ktrain_arms.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"SPEC3 | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"gen_steps={args.gen_steps} ktrain_arms={k_arms} corrected "
          f"house residual_low_band_ratio (seeds {seeds}; round-283 "
          f"preregistration, round-267 pending-item closure)", flush=True)

    mses = {k: [] for k in k_arms}
    lows = {k: [] for k in k_arms}
    for k_train in k_arms:
        for seed in seeds:
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            train_prefix(model, qs[tr], ps[tr], args.t_obs, k_train,
                         args.train_steps, args.lr, args.batch, seed)
            res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                           args.eval_k, args.dt)
            mses[k_train].append(res["rollout_mse"])
            lows[k_train].append(res["residual_low_band_ratio"])
            print(f"  [k_train {k_train:>2} seed {seed}] MSE "
                  f"{res['rollout_mse']:.4e} | low_band "
                  f"{res['residual_low_band_ratio']:.6f}", flush=True)

    verdict, detail = classify_spec3(lows[k_arms[0]], lows[k_arms[1]])
    bitwise = (mses[k_arms[0]] == A4_EXPECTED_MSE
               and mses[k_arms[1]] == B8_EXPECTED_MSE)
    sentinels = {
        "scalar_cross_script_anchors": {
            "expected_k4": A4_EXPECTED_MSE, "actual_k4": mses[k_arms[0]],
            "expected_k8": B8_EXPECTED_MSE, "actual_k8": mses[k_arms[1]],
            "bitwise_match": bitwise,
            "note": "same pool bits and construction as r246; the MSE "
                    "path is untouched by the AMM-031 spectral key, so "
                    "the scalar readings are bitwise anchors"},
    }
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinels": sentinels,
        "criteria": {"c_unresolvable": verdict == "SPEC3_UNRESOLVABLE",
                     "c_reproduces": verdict == "SPEC3_ORDER_REPRODUCES",
                     "c_tied": verdict == "SPEC3_ORDER_TIED",
                     "c_flips": verdict == "SPEC3_ORDER_FLIPS"},
        "gates": {"tied_gate": TIED_GATE, "norm_cap": NORM_CAP,
                  "seeds": list(SEEDS), "ktrain_arms": k_arms},
        "anchor": "corrected house caliber (AMM-031 as fixed r267): "
                  "band top omega_max/(2*pi*dt); r246 wrong-cutoff "
                  "values recorded for contrast only",
    }
    print(f"\nSPEC3 verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"scalar anchors bitwise={bitwise}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "residual_spec_3.json"),
              "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "residual_spec3_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
