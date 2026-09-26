"""
benchmarks/hom_drift_probe.py — HOM-DRIFT (round 273): long-horizon
rollout and energy-drift behavior of the homogeneous-head candidate vs
the house default head, 3 seeds, M1 spring family (E1 caliber). Scan
family 60 (long-horizon conservation family, round-273 distillation;
slot 1 = SympNets Jin et al. Neural Networks 2020 structure-preserving
⇒ bounded long-term energy error, slot 2 = Manek & Kolter NeurIPS 2019
stability-certified learning, slot 3 = Cranmer et al. 2020 Lagrangian
Neural Networks).

Why: AMM-033 (default-head swap proposal) plans an anchor reset, but
the candidate's readings stop at k=100 in-dist / k=200 extrapolation
(rounds 268/269). Long-horizon behavior is the missing dimension of
the anchor-set plan: structure-preserving literature predicts bounded
energy error for constrained/symplectic-like models vs secular drift
for generic ones. Single variable = the head (arm A = house default,
NO head swap; arm B = analytic T + direction-free homogeneous V =
HomVStabHead, the AMM-033 candidate). Both evaluated at horizons
k ∈ {100, 400, 1000} (dt=0.1 ⇒ 10s/40s/100s; 1000 = 6.25× the 16s
training window) with rollout MSE + house energy drift.

Mechanical verdict (preregistered, 3-seed; parity band ±5% = house
round-260 gates):
  HOM_ARM_DIVERGED (negative) — any reading non-finite or > 1e6
  ratio_k  = mean MSE_B(k) / mean MSE_A(k)
  dratio_k = mean drift_B(k) / mean drift_A(k)
  HOM_DRIFT_ROBUST   — ratio_k < 1.05 AND dratio_k <= 1.05 at ALL
      horizons ⇒ candidate long-horizon robust; decision = AMM-033
      anchor-reset plan adopts the long-horizon anchors (k400/k1000
      readings) with a candidate-favorable note
  HOM_DRIFT_MSE_ONLY — MSE robust at all horizons but drift ratio
      > 1.05 somewhere ⇒ conservative note in the anchor plan
  HOM_DRIFT_DEGRADES — ratio_k >= 1.05 at any horizon ⇒ long-horizon
      caveat; anchor plan keeps default-head readings for the long
      end until further evidence

Decision coupling (AMM-028 gate-1): each outcome changes the AMM-033
anchor-set plan differently (adopt-with-note / conservative note /
caveat), EIG qualified. Sentinels: arm A seed 0 = 3.5581917762756348
bitwise (house default anchor); arm B k=100 = the round-268 STAB
readings bitwise (cross-script anchor). Family boundary: scan family
60 round 1. Results JSON follows the audit schema; meta carries
exec_tier.
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

NORM_CAP = 1e6      # preregistered: divergence threshold (house caliber)
PARITY = 1.05       # preregistered: house parity band (round-260 gate)
HORIZONS = (100, 400, 1000)
SEEDS = (0, 1, 2)
B_EXPECTED_K100 = [2.0023648738861084, 1.6420986652374268,
                   2.2025928497314453]  # round-268 STAB arm, bitwise


def classify_hom_drift(mses_a, mses_b, dratios_a, dratios_b,
                       horizons=HORIZONS, parity: float = PARITY,
                       norm_cap: float = NORM_CAP):
    """Preregistered round-273 verdict (pure, test-pinned). The gates
    are PER-HORIZON: rows are [horizon][seed]; means are across seeds
    within each horizon (round-273b axis fix — the first implementation
    transposed and aggregated across horizons per seed, contradicting
    the preregistered per-horizon wording)."""
    for tag, per_arm in (("A", mses_a), ("B", mses_b)):
        for h, vals in zip(horizons, per_arm):
            for s, m in zip(SEEDS, vals):
                if not math.isfinite(m) or m > norm_cap:
                    state = ("non-finite" if not math.isfinite(m)
                             else "diverged")
                    return "HOM_ARM_DIVERGED", {
                        "reason": f"arm {tag} seed {s} k={h} {state} "
                                  f"(mse={m:.3e})"}
    mean_k = lambda rows: [sum(v) / len(v) for v in rows]
    mean_a, mean_b = mean_k(mses_a), mean_k(mses_b)
    ratios = [b / max(a, 1e-30) for a, b in zip(mean_a, mean_b)]
    mean_da, mean_db = mean_k(dratios_a), mean_k(dratios_b)
    dratios = [b / max(a, 1e-30) for a, b in zip(mean_da, mean_db)]
    stats = {"parity": parity, "horizons": list(horizons),
             "mses_A": mses_a, "mses_B": mses_b,
             "drift_A": dratios_a, "drift_B": dratios_b,
             "mean_mse_A_per_k": mean_a, "mean_mse_B_per_k": mean_b,
             "mean_drift_A_per_k": mean_da, "mean_drift_B_per_k": mean_db,
             "mse_ratio_per_k": ratios, "drift_ratio_per_k": dratios,
             "consistent_mse_B_per_seed":
                 [sum(1 for a, b in zip(ka, kb) if b < a)
                  for ka, kb in zip(zip(*mses_a), zip(*mses_b))]}
    mse_ok = all(r < parity for r in ratios)
    drift_ok = all(r <= parity for r in dratios)
    if mse_ok and drift_ok:
        verdict = "HOM_DRIFT_ROBUST"
        stats["decision"] = ("candidate long-horizon robust: AMM-033 "
                             "anchor-reset plan adopts the long-horizon "
                             "anchors (k400/k1000) with a candidate-"
                             "favorable note")
    elif mse_ok:
        verdict = "HOM_DRIFT_MSE_ONLY"
        stats["decision"] = ("MSE robust at all horizons but drift "
                             "degrades somewhere: conservative note in "
                             "the anchor plan")
    else:
        verdict = "HOM_DRIFT_DEGRADES"
        stats["decision"] = ("candidate degrades at long horizons: "
                             "anchor plan keeps default-head readings "
                             "for the long end until further evidence")
    return verdict, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=1100,
                    help="pool length; must exceed t_obs-1+max(eval_ks) "
                         "(k1000 needs >=1024; round-273 first-run fix)")
    ap.add_argument("--eval_ks", default="100,400,1000")
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
                    default="benchmarks/physics_out_v02/hom_drift")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]
    eval_ks = [int(x) for x in args.eval_ks.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"HOM-DRIFT | M1 spring omega[{args.omega_lo},{args.omega_hi}]"
          f" horizons={eval_ks}: A=house default head vs B=analyticT+"
          f"direction-free-homV (seeds {seeds}; round-273 prereg, "
          f"scan family 60)", flush=True)

    mses = {"A": {k: [] for k in eval_ks}, "B": {k: [] for k in eval_ks}}
    drifts = {"A": {k: [] for k in eval_ks}, "B": {k: [] for k in eval_ks}}
    for seed in seeds:
        for tag in ("A", "B"):
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            # arm A = default construction (NO head swap); arm B = head
            # swap AFTER the model draw (round-249/268 order); single
            # variable = the head
            if tag == "B":
                model.ham = HomVStabHead(1, hidden_dim=args.hidden,
                                         depth=2,
                                         context_dim=args.context_dim)
            train_prefix(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                         args.train_steps, args.lr, args.batch, seed)
            for k in eval_ks:
                res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                               k, args.dt)
                mses[tag][k].append(res["rollout_mse"])
                drifts[tag][k].append(res["energy_drift_final"])
                print(f"  [arm {tag} seed {seed} k={k}] MSE "
                      f"{res['rollout_mse']:.4e} | drift "
                      f"{res['energy_drift_final']:.4f}", flush=True)

    verdict, detail = classify_hom_drift(
        [mses["A"][k] for k in eval_ks], [mses["B"][k] for k in eval_ks],
        [drifts["A"][k] for k in eval_ks],
        [drifts["B"][k] for k in eval_ks], horizons=eval_ks)
    bitwise_a = mses["A"][eval_ks[0]][0] == SENTINEL
    bitwise_b = mses["B"][eval_ks[0]] == B_EXPECTED_K100
    sentinels = {
        "A_seed0_house_default_k100": {
            "expected": SENTINEL, "actual": mses["A"][eval_ks[0]][0],
            "bitwise_match": bitwise_a},
        "B_round268_STAB_k100": {
            "expected": B_EXPECTED_K100,
            "actual": mses["B"][eval_ks[0]],
            "bitwise_match": bitwise_b,
            "note": "cross-script anchor (round-268 STAB arm)"},
    }
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinels": sentinels,
        "criteria": {"c_diverged": verdict == "HOM_ARM_DIVERGED",
                     "c_robust": verdict == "HOM_DRIFT_ROBUST",
                     "c_mse_only": verdict == "HOM_DRIFT_MSE_ONLY",
                     "c_degrades": verdict == "HOM_DRIFT_DEGRADES"},
        "gates": {"parity": PARITY, "norm_cap": NORM_CAP,
                  "seeds": list(SEEDS), "eval_ks": eval_ks},
        "anchor": "single variable = the head; horizon axis k∈"
                  f"{eval_ks}; house evaluate() caliber",
    }
    print(f"\nHOM-DRIFT verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"sentinels A={bitwise_a} B={bitwise_b}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "hom_drift.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "hom_drift_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
